from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings

from .models import Contact, Client, Trainer
from .forms import ContactForm, ContactModelForm, EmailForm, TrainerEditForm

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def shop(request):
    return render(request, 'shop.html', {})

def pricing(request):
    return render(request, 'pricing.html', {})

# CONTACT -------------------------------------------------------------------------------------------------------->
def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            contact_objects = Contact.objects.filter(date=cd['date']).count()
            if contact_objects > 8:
                messages.error(request, 'There is no availibility for that date.')
            else:
                first_name  = cd['first_name']
                last_name   = cd['last_name']
                email       = cd['email']
                message     = cd['message']
                date        = cd['date']
                discipline  = cd['discipline']
                new_contact = Contact(first_name=first_name, last_name=last_name, 
                                      email=email, message=message, date=date, 
                                      discipline=discipline)
                new_contact.save()
                messages.success(request, 'You have submitted a request for appointment. You will recieve an email soon.')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

