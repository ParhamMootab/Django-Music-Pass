from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketingAPI.as_view()),
    path('<int:seat_number>', views.SingleTicketAPI.as_view())
]
