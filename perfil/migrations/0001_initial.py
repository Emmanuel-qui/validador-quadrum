# Generated by Django 4.1.2 on 2022-12-11 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('rfc', models.CharField(max_length=20)),
                ('telephone', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('regime_fiscal', models.CharField(choices=[('601', 'General de Ley Personas Morales'), ('603', 'Personas Morales con Fines no Lucrativos'), ('605', 'Sueldos y Salarios e Ingresos Asimilados a Salarios'), ('606', 'Arrendamiento'), ('607', 'Régimen de Enajenación o Adquisición de Bienes'), ('608', 'Demás ingresos'), ('610', 'Residentes en el Extranjero sin Establecimiento Permanente en México'), ('611', 'Ingresos por Dividendos (socios y accionistas)'), ('612', 'Personas Físicas con Actividades Empresariales y Profesionales'), ('614', 'Ingresos por intereses')], max_length=10)),
                ('person_type', models.CharField(choices=[('M', 'Persona Moral'), ('F', 'Persona Fisica')], max_length=1)),
                ('image_profile', models.ImageField(blank=True, default='/media/image/img-quadrum.jpeg', null=True, upload_to='image/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
