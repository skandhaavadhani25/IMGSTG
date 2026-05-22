from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('application',views.application,name='application'),
    path('overview',views.overview,name='overview'),     
    path('key',views.key,name='key'),
    path('login',views.login,name='login'),
    path('encryption/', views.encryption_view, name='encryption'),
    path('decryption/', views.decryption_view, name='decryption'),
    path('register',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('contacts',views.contacts,name='contacts'),
    path('AES',views.AES,name='AES'),
    path('option',views.option,name='option'),
    path('option2',views.option2,name='option2'),
    path('vencryption/',views.vencryption_view, name='vencryption'),
    path('vdecryption/',views.vdecryption_view, name='vdecryption'),
    path('aencryption/',views.aencryption_view, name='aencryption'),
    path('adecryption/',views.adecryption_view, name='adecryption'),
]