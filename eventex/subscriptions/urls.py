from django.urls import path

from eventex.subscriptions.views import subscribe, detail

app_name = 'subscriptions'

urlpatterns = [
    path('', subscribe, name='new'),
    path('<str:pk>/', detail, name='detail'),
]
