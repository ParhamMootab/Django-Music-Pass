from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketingAPI.as_view()),
    path('<int:ticket_id>', views.SingleTicketAPI.as_view())
]
