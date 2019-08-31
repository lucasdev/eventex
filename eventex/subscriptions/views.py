from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionsForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionsForm(request.POST)
        if form.is_valid():
            body = render_to_string('subscription_mail.txt', form.cleaned_data)
            mail.send_mail('Confirmação de Inscrição',
                           body,
                           'contato@eventex.com.br',
                           ['contato@eventex.com.br', form.cleaned_data['email']])

            messages.success(request, 'Inscrição realizada com sucesso')
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscription_form.html', {'form': form})

    else:
        form = {'form': SubscriptionsForm()}
        return render(request, 'subscription_form.html', form)
