import uuid

from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
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

    cleaned_data = form.cleaned_data
    cleaned_data['uuid'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, cleaned_data['cpf']))
    subscription = Subscription.objects.create(**cleaned_data)

    _send_mail('Confirmação de Inscrição',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email,
               'subscription_mail.txt',
               {'subscription': subscription})

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.uuid))


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(uuid=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscription_detail.html', {'subscription': subscription})


def new(request):
    form = {'form': SubscriptionsForm()}
    return render(request, 'subscription_form.html', form)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
