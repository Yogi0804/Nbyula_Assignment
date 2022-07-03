from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', views.getRoutes, name="get_routes"),
    path('register/', views.register, name="register"),
    path('sheduleAppointment/', views.sheduleAppointment, name="shedule_appointment"),
    path('upcomingAppointment/', views.upcomingAppointment, name="upcoming_appointment"),
    path('UpdateProfile/', views.UpdateProfile, name="update_profile"),
    path('allAppointments/', views.allAppointments, name="all_appointments"),
    path('offHours/', views.offHours, name="off_hours"),
    path('deleteAppointment/<int:pk>/', views.deleteAppointment, name="delet_appointment"),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
