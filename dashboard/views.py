from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from accounts.forms import ContactForm, ContactModelForm, EmailForm, TrainerEditForm
from accounts.models import Contact, Client, Trainer

# Admin Views---------------------------------------------->
@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html', {})

@staff_member_required
def admin_login(request):
    return render(request, 'admin/admin_login.html', {})

@staff_member_required
def admin_insights(request):
    return render(request, 'admin/admin_insights.html', {})

# TRAINERS ---------------------------------------------------------------->
@staff_member_required
def trainers(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainers.html', {'trainers': trainers})

@staff_member_required
def send_mail_to_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, trainer_id=trainer_id)

    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            cd   = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                settings.DEFAULT_FROM_MAIL,
                [trainer.email],
                fail_silently=False,
            )
            messages.success(request,'Email sent successfully.')
            return redirect('trainers')
    else:
        form = EmailForm()  
    return render(request, 'trainers/email_trainer.html', {'form': form,
                                                          'trainer': trainer})

@staff_member_required
def send_mail_to_all_trainers(request):
    trainers = Trainer.objects.all()
    trainer_emails  = [obj.email for obj in trainers]

    if request.method == 'POST':
        form = EmailForm()
        if form.is_valid():
            cd   = form.cleaned_data
            send_mass_mail(
                cd['subject'],
                cd['message'],
                settings.DEFAULT_FROM_MAIL,
                trainer_emails,
                fail_silently=False,
            )
    else:
        form = EmailForm()
    return render(request, 'trainers/email_all_trainers.html', {'form': form})

@staff_member_required
def edit_trainer(request, trainer_id):
    instance = get_object_or_404(Trainer, trainer_id=trainer_id)
    trainer_class = instance.courses
    print(trainer_class)

    if request.method == 'POST':
        form = TrainerEditForm(data=request.POST, instance=instance)
        if form.is_valid():
            instance.percent = form.cleaned_data['percent']
            instance.save()
            # SEND EMAIL TO CLIENT THAT APPOINTMENT INFORMATION HAS BEEN CHANGED
            messages.success(request, 'Entry has been saved.')
            return redirect('trainers')
    else:
        form = TrainerEditForm(instance=instance)
    return render(request, 'trainers/edit_trainer.html', {'form': form,
                                                          'trainer': instance})

@staff_member_required
def delete_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, trainer_id=trainer_id)

    if request.method == 'POST':
        trainer.delete()
        messages.success(request, 'Entry has been deleted.')
        return redirect('potential_clients')
    else:
        return render(request, 'trainers/delete_trainer.html', {'trainer': trainer})

# CLIENTS ----------------------------------------------------------------->
@staff_member_required
def clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/clients.html', {'clients': clients})

# Add staff member required decorator to all these
# @staff_member_required
@staff_member_required
def potential_clients(request):
    potential_clients = Contact.objects.all()
    return render(request, 'contact/potential_clients.html', {'potential_clients': potential_clients})

@staff_member_required
def send_mail_to_client(request, id):
    potential_client = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            cd   = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                settings.DEFAULT_FROM_MAIL,
                [potential_client.email],
                fail_silently=False,
            )
            messages.success(request,'Email sent successfully.')
            return redirect('potential_clients')
    else:
        form = EmailForm()  
    return render(request, 'contact/email_potential_client.html', {'form': form,
                                                                   'potential_client': potential_client})

@staff_member_required
def send_mail_to_all(request):
    potential_clients = Contact.objects.all()
    recipient_emails  = [obj.email for obj in potential_clients]

    if request.method == 'POST':
        form = EmailForm()
        if form.is_valid():
            cd   = form.cleaned_data
            send_mass_mail(
                cd['subject'],
                cd['message'],
                settings.DEFAULT_FROM_MAIL,
                recipient_emails,
                fail_silently=False,
            )
    else:
        form = EmailForm()
    return render(request, 'contact/email_all_potential_clients.html', {'form': form})

@staff_member_required
def edit_potential_client(request, id):
    instance = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        form = ContactModelForm(data=request.POST, instance=instance)
        if form.is_valid():
            instance.date       = form.cleaned_data['date']
            instance.discipline = form.cleaned_data['discipline']
            instance.save()
            # SEND EMAIL TO CLIENT THAT APPOINTMENT INFORMATION HAS BEEN CHANGED
            messages.success(request, 'Entry has been saved.')
            return redirect('potential_clients')
    else:
        form = ContactModelForm(instance=instance)
    return render(request, 'contact/edit_potential_client.html', {'form': form,
                                                                  'potential_client': instance})

@staff_member_required
def delete_potential_client(request, id):
    potential_client = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        potential_client.delete()
        messages.success(request, 'Entry has been deleted.')
        return redirect('potential_clients')
    else:
        return render(request, 'contact/delete_potential_client.html', {'potential_client': potential_client})