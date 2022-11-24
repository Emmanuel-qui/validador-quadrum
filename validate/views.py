from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views import View
# importando libreria para responder en formato json.
from django.http import JsonResponse
# importando formulario para documentos
from .forms import FileForm
# importamos la clase Validate
from .utils import Validate
# Importamos el modelo
from .models import ValidateResultModel


from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.conf import settings

#from perfil.models import AccountModel
from django.contrib.auth.models import User

from validate.generate_pdf import PDF

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Mostrando de seccion de carga de CFDI (carga template).

class IndexView(LoginRequiredMixin,View):
	login_url = '/accounts/login/'
	redirect_field_name = 'redirect_to'
	def get(self, request):

		#Obtenemos el formulario creado y lo mandamos a la vista.
		form = FileForm()
		return render(request, 'validate/index.html', {'form':form})

	def post(self, request):
		# Obtenemos el documento enviado
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			m = form.save()
			# Obtenemos el file del request y lo amacenamos
			xml_file = m.file
			# mandamos el xml como parametro a la clase Validate para hacer el proceso de validacion.
			validate = Validate(xml_file)
			data = {'response':validate.response, 'success':True}
			return JsonResponse(data)
       


# Mostrando la vista de historico de validaciones (carga template).

class ResultValidate(LoginRequiredMixin,View):
	login_url = '/accounts/login/'
	template_name = "validate/result.html"
	def get(self, request):
		return render(request, self.template_name)


# Vista para la implementacion de datatables 
class ValidateResult(View):

	def post(self, request):
		lista_result = []
		start = int(request.POST.get("start"))
		length = int(request.POST.get("length"))
		rfc_emisor = request.POST.get("rfc_emisor")
		rfc_receptor = request.POST.get("rfc_receptor")
		fecha_validate = request.POST.get("fecha_validacion")

		lista_objetos = ValidateResultModel.objects.all()
		if rfc_emisor:
			lista_objetos = lista_objetos.filter(rfc_business__icontains=rfc_emisor)
		elif rfc_receptor:
			lista_objetos = lista_objetos.filter(rfc_receiver__icontains=rfc_receptor)
		elif fecha_validate:
			lista_objetos = lista_objetos.filter(validate_date__icontains=fecha_validate)

			
		total_records = lista_objetos.count()
		lista_objetos = lista_objetos[start:start+length]

		for item in lista_objetos:
			lista_result.append({
				'id': item.id,
				'rfc_emisor': item.rfc_business,
				'rfc_receptor': item.rfc_receiver,
				'version': item.version,
				'fecha': item.date,
				'fecha_validacion':item.validate_date,
				'sello':item.stamp,

			})
		
		
		response = {
			"aaData": lista_result,
			"iTotalRecords": total_records,
			"iTotalDisplayRecords": total_records,
		}
		return JsonResponse(response)




# Funcion para mostrar 
# el detalle del resultado de una validacion.
@login_required
def ValidateResultDetail(request, pk):

		validate_invoice = ValidateResultModel.objects.get(id=pk)
		tipo = ""
		if validate_invoice.voucher_type == "I":
			tipo = "Ingreso"
		elif validate_invoice.voucher_type == "E":
			tipo = "Egreso"
		else:
			tipo = "Pago"

		sello_sat = ""

		if validate_invoice.stamp_sat:
			sello_sat = "Encontrado"
		else: 
			sello_sat = "No encontrado"
		
		sello = "Incorrecto"

		if validate_invoice.stamp:
			sello = "Correcto"

		response = {
			'id': validate_invoice.id,
			'Resultado': validate_invoice.results,
			'Version': validate_invoice.version,
			'Receptor': validate_invoice.rfc_receiver,
			'Metodo_pago': validate_invoice.metodo_pago,
			'Emisor': validate_invoice.rfc_business,
			'Fecha': validate_invoice.date,
			'Fecha_validacion': validate_invoice.validate_date,
			'Lugar_ex': validate_invoice.place_of_expedition,
			'Tipo': tipo,
			'Total': validate_invoice.total,
			'Estructura': validate_invoice.estruc,
			'Sello': sello,
			'Sello_sat': sello_sat,
			'Error_msj': validate_invoice.error_ws

		}

		return render(request, 'validate/detail.html', context=response)

	

# Vista que sirve para la generacion de PDF.
class GeneratePdf(View):

	def get(self, request, pk):
		pdf_obj = PDF(pk)
		pdf_result =  pdf_obj.generate()
		response = HttpResponse(pdf_result, content_type='application/pdf')
		return response




# Vista que sirve para el 
# envio de pdf por email
class UserEmail(View):

	def get(self,request,pk):

		user_obj = request.user
		pdf_obj = PDF(1)
		pdf_result =  pdf_obj.generate()

		msj = EmailMessage(subject="Reporte comprobante",
            body="Estimado usuario, le compartimos el reporte del resultado de la validación con Validador Quadrum.",
            from_email=settings.EMAIL_HOST_USER,
			to=[user_obj.email],
			)
		msj.attach('reporte.pdf',pdf_result,'application/pdf')

		msj.send()

		response = {'msj': 'Correo enviado'}

		return JsonResponse(response)