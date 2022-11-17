
from django.shortcuts import render

from django.urls import path

from . import views

# Create your urls here.

app_name = 'validate'

urlpatterns = [

    path('', views.IndexView.as_view(), name="index"),

    path('result/', views.ResultValidate.as_view(), name="result"),

    path('validateresult/', views.ValidateResult.as_view(), name="validateresult"),

    path('detail/<int:pk>', views.ValidateResultDetail, name="detail"),

    path('pdf/<int:pk>', views.GeneratePdf.as_view(), name="generate-pdf"),

    path('send/<int:pk>', views.UserEmail.as_view(), name="email"),
]
