"""mission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from quickstart import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as authview
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('mes-missionlist/<int:id>/', views.MesMissionList.as_view()),
    path('mes-missionlist/', views.MesMissionList.as_view()),
    path('mes-missionlist/traitement/<int:id>/', views.MesMissionTraitement.as_view()),
    path('mes-missiondetail/<int:pk>/', views.MesMissionDetail.as_view()),
    path('Envoyelist/', views.EnvoyeList.as_view()),
    path('Envoyedetail/<int:pk>/', views.EnvoyeDetail.as_view()),
    path('processlist/', views.ProcessList.as_view()),
    path('processg/', views.ProcessG.as_view()),
    path('processDetail/<int:pk>/', views.ProcessDetail.as_view()),
    path('Stepprocess/', views.StepprocessList.as_view()),
    path('Stepprocess/<int:pk>/', views.StepprocessDetail.as_view()),
    path('userlist/', views.userList.as_view()),
    path('userdetail/<int:pk>/', views.userDetail.as_view()),
    path('Employelist/', views.employeList.as_view()),
    path('Employedetail/', views.employeDetail.as_view()),
    path('polelist/', views.poleList.as_view()),
    path('poledetail/<int:pk>/', views.poleDetail.as_view()),
    path('entitelist/', views.entiteList.as_view()),
    path('entitedetail/<int:pk>/', views.entiteDetail.as_view()),
    path('projetlist/', views.projetList.as_view()),
    path('projetdetail/', views.projetDetail.as_view()),
    path('typeprojetlist/', views.typeprojetList.as_view()),
    path('typrojetdetail/<int:pk>/', views.typeprojetDetail.as_view()),
    path('CountryList/', views.CountryList.as_view()),
    path('CountryDetail/', views.CountryDetail.as_view()),
    path('WorldcitiesList/', views.WorldcitiesList.as_view()),
    path('WorldcitiesDetail/<int:pk>/', views.WorldcitiesDetail.as_view()),
    path('RegimeList/', views.RegimeList.as_view()),
    path('RegimeDetail/<int:pk>/', views.RegimeDetail.as_view()),
    path('GroupList/', views.GroupList.as_view()),
    path('GroupDetail/<int:pk>', views.GroupDetail.as_view()),
    path('TypestepsList/', views.TypestepsList.as_view()),
    path('TypestepsDetail/<int:pk>', views.TypestepsDetail.as_view()),
    path('CategorieList/', views.CategorieList.as_view()),
    path('CategorieDetail/<int:pk>/', views.CategorieDetail.as_view()),
    path('ZoneList/', views.ZoneList.as_view()),
    path('ZoneDetail/<int:pk>/', views.ZoneDetail.as_view()),
    path('BaremeList/', views.BaremeList.as_view()),
    path('BaremeDetail/<int:pk>/', views.BaremeDetail.as_view()),
    path('Montant_zoneList/', views.Montant_zoneList.as_view()),
    path('Montant_zoneDetail/<int:pk>/', views.Montant_zoneDetail.as_view()),
    path('ServiceList/', views.ServiceList.as_view()),
    path('ServiceDetail/<int:pk>/', views.ServiceDetail.as_view()),
    path('BankList/', views.BankList.as_view()),
    path('BankDetail/<int:pk>/', views.BankDetail.as_view()),
    path('Bareme_detailList/', views.Bareme_detailList.as_view()),
    path('Bareme_detailDetail/<int:pk>/', views.Bareme_detailDetail.as_view()),
    path('delais_bareme/', views.delais_bareme.as_view()),
    path('Validations/', views.Validations.as_view()),
    path('Billets/', views.Billets.as_view()),
    
    path('Numero/', views.NumeroDetail.as_view()),
    path('PaysList/', views. PaysList.as_view()),
    path('PaysDetail/', views. PaysDetail.as_view()),
    path('paiement/', views.paiement.as_view()),
    path('Finalisation/', views.Finalisation.as_view()),
    path('reception_paiement/', views.reception_paiement.as_view()),
    path('justification/', views.justificationList.as_view()),
    path('justificationList/<int:envoye>/', views.justificationList.as_view()),
    path('justificationDetail/<int:pk>/', views.justificationDetail.as_view()),
    path('authentification', views.StepprocessDetail.as_view()),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


