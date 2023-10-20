from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.translation import gettext as _
from .forms import ContactUsFrom
from django.contrib import messages


class HomePageView(TemplateView):
    template_name = 'home.html'


def contact_us_view(request):
    if request.method == 'POST':
        contact_us_form = ContactUsFrom(request.POST)

        if contact_us_form.is_valid():
            contact_us_form.save()
            messages.success(request, _('Message Saved.'))

    return render(request, 'pages/contact.html')
