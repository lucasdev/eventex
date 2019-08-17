from django.shortcuts import render

# Create your views here.
from eventex.subscriptions.forms import SubscriptionsForm


def subscribe(request):
    form = {'form': SubscriptionsForm()}
    return render(request, 'subscription_form.html', form)
