from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_risk, name='predict_risk'), # หน้าแรกแดชบอร์ด
    path('patients/', views.patients_mock, name='patients'),
    path('history/', views.history, name='history'),
    path('settings/', views.settings_page, name='settings'),
]