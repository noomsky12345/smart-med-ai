from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.predict_risk, name='predict_risk'), # หน้าแรกแดชบอร์ด
    path('patients/', views.patients_mock, name='patients'),
    path('history/', views.history, name='history'),
    path('settings/', views.settings_page, name='settings'),
    path('login/', auth_views.LoginView.as_view(template_name='prediction/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.predict_risk, name='predict_risk'),
]