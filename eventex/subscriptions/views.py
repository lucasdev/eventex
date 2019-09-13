from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionsForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionsForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscription_form.html', {'form': form})

    _send_mail('Confirmação de Inscrição',
               settings.DEFAULT_FROM_EMAIL,
               form.cleaned_data['email'],
               'subscription_mail.txt',
               form.cleaned_data)

    Subscription.objects.create(**form.cleaned_data)

    messages.success(request, 'Inscrição realizada com sucesso')
    return HttpResponseRedirect('/inscricao/')


def new(request):
    form = {'form': SubscriptionsForm()}
    return render(request, 'subscription_form.html', form)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
