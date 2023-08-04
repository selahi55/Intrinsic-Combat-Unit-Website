from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('insights/', views.admin_insights, name='insights'),

    # TRAINERS Model
    path('trainers/', views.trainers, name="trainers"),
    path('trainers/email-all/', views.send_mail_to_all_trainers, name="email_all_trainers"),
    path('trainers/<uuid:trainer_id>/', views.edit_trainer, name="edit_trainer"),
    path('trainers/<uuid:trainer_id>/email/', views.send_mail_to_trainer, name="email_trainer"),
    path('trainers/<uuid:trainer_id>/delete/', views.delete_trainer, name="delete_trainer"),

    # CLIENT Model
    path('clients/', views.clients, name="clients"),

    # CONTACT Model
    path('potential-clients/', views.potential_clients, name="potential_clients"),
    path('potential-clients/email-all/', views.send_mail_to_all, name="email_all_potential_clients"),
    path('potential-clients/<int:id>/', views.edit_potential_client, name="edit_potential_client"),
    path('potential-clients/<int:id>/email/', views.send_mail_to_client, name="email_potential_client"),
    path('potential-clients/<int:id>/delete/', views.delete_potential_client, name="delete_potential_client"),
]