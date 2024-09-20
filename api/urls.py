from django.urls import path
from .views import WaitlistView

app_name='api'
urlpatterns = [
    path('waitlist/', WaitlistView.as_view(), name='waitlist'),
]
