import re
import socket
from django.shortcuts import render, redirect
from .models import ASPL, SPL, User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate
current_user = None


def ip(request):
    global current_user
    if request.method == "GET":

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if not x_forwarded_for:
            current_ip = request.META.get('REMOTE_ADDR')
            try:
                socket.inet_aton(current_ip)
                method = "2nd Method"
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP adress is not valid"})

        else:
            current_ip = x_forwarded_for.split(',')[0]
            try:
                socket.inet_aton(current_ip)
                method = "1st method"
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP address is not valid"})
        try:
            current_user = User.objects.get(pk=current_ip)
        except (User.DoesNotExist, KeyError):
            current_user = User.objects.create(pk=current_ip)
            current_user.ip = current_ip
            current_user.method = method
            current_user.times_visited += 1
            current_user.save()
        else:
            current_user.method = method
            current_user.times_visited += 1
            current_user.save()
        if current_user.mail_real == False and current_user.times_visited > 1:
            return redirect("voting:mail")
        else:
            return redirect("voting:logic")
    elif request.method == "POST":
        mail = request.POST['mail']
        pattern = r'\w+40\d{4}@npschennai.com'
        res = re.match(pattern, mail)
        if res == None:
            return render(request, "vote/email.html", context={"error_message": "You have not entered a valid school email address"})
        else:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if not x_forwarded_for:
                current_ip = request.META.get('REMOTE_ADDR')
                try:
                    socket.inet_aton(current_ip)
                    method = "2nd method"
                except socket.error:
                    return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP adress is not valid"})
            else:
                current_ip = x_forwarded_for.split(',')[0]
            try:
                socket.inet_aton(current_ip)
                method = "1st method"
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP address is not valid"})
            try:
                current_user = User.objects.get(pk=current_ip)
            except (User.DoesNotExist, KeyError):
                current_user = User.objects.create(pk=current_ip)
                current_user.mail_real = True
                current_user.method = method
                current_user.email = mail
                current_user.ip = current_ip
                current_user.times_visited += 1
                current_user.save()
            else:
                current_user.method = method
                current_user.email = mail
                current_user.mail_real = True
                current_user.times_visited += 1
                current_user.save()
            return redirect("voting:logic")


def index(request):
    try:
        if current_user == None:
            return redirect("voting:ip")
        elif current_user.mail_real == False:
            return redirect("voting:mail")
        else:
            if current_user.spl_done == False and current_user.aspl_done == False:
                return render(request, "vote/index.html", context={"candidates": SPL.objects.all()})
            elif current_user.aspl_done == False and current_user.spl_done == True:
                return redirect("voting:voted")
            elif current_user.spl_done == True and current_user.aspl_done == True:
                return redirect("voting:thanks")
            else:
                return HttpResponse("<h1>Some Server Error</h1>")
    except(ValueError, NameError):
        return render(request, "vote/error.html", context={"text": "Invalid method", "type": "info"})


def spl(request):
    if request.method == "GET":
        return render(request, "vote/error.html", context={"text": "Invalid method", "type": "primary"})
    elif request.method == "POST":
        try:
            selected_candidate = SPL.objects.get(pk=request.POST['SPL'])
        except(KeyError, SPL.DoesNotExist):
            candidates = SPL.objects.all()
            return render(request, 'vote/index.html', {'candidates': candidates, 'error_message': "You have not selected a candidate."})
        else:
            if current_user == None:
                return redirect("voting:ip")
            elif current_user.mail_real == False:
                return redirect("voting:mail")
            else:
                selected_candidate.votes += 1
                selected_candidate.save()
                current_user.spl_done = True
            current_user.save()
            return HttpResponseRedirect(reverse('voting:voted'))


def aspl(request):
    if request.method == "GET":
        return render(request, "vote/error.html", context={"text": "Invalid method", "type": "info"})

    else:
        try:
            selected_candidate = ASPL.objects.get(pk=request.POST['ASPL'])
        except(KeyError, ASPL.DoesNotExist):
            candidates = ASPL.objects.all()
            error = "You have not selected a candidate"
            return render(request, 'vote/voted.html', {'candidates': candidates, 'error_message': error})
        else:
            if current_user == None:
                return redirect("voting:ip")
            elif current_user.mail_real == False:
                return redirect("voting:mail")
            else:
                # global current_user
                selected_candidate.votes += 1
                selected_candidate.save()
                current_user.aspl_done = True
                current_user.save()
                return HttpResponseRedirect(reverse('voting:thanks'))


def voted(request):
    try:
        if current_user == None:
            return redirect("voting:ip")
        elif current_user.mail_real == False:
            return redirect("voting:mail")
        else:
            # global current_user
            if current_user.spl_done == False and current_user.aspl_done == False:
                return redirect("voting:index")
            elif current_user.aspl_done == False and current_user.spl_done == True:
                return render(request, "vote/voted.html", context={"candidates": ASPL.objects.all()})
            elif current_user.spl_done == True and current_user.aspl_done == True:
                return redirect("voting:thanks")
            else:
                return HttpResponse("<h1>Some Server Error</h1>")
    except(ValueError, NameError):
        return render(request, "vote/error.html", context={"text": "Invalid method", "type": "info"})


def thanks(request):
    if current_user == None or current_user.email == "mail":
        return redirect("voting:ip")
    else:
        current_user.aspl_done = False
        current_user.spl_done = False
        current_user.save()
        return render(request, 'vote/thanks.html')


def result(request):
    if request.method == "GET":
        return render(request, "vote/error.html", context={"type": "danger", "text": "You are not authorized to see the results"})
    elif request.method == "POST":
        global current_user
        aspl_can = ASPL.objects.order_by('-votes')[:]
        spl_can = SPL.objects.order_by('-votes')[:]
        password = request.POST['password']
        username = request.POST['username']
        user = authenticate(username=username, password=password)
        if user != None:
            return render(request, "vote/result.html", context={"spl_can": spl_can, "aspl_can": aspl_can})
        else:
            return render(request, "vote/error.html", context={"type": "danger", "text": "You are not authorized to see the results"})


def login(request):
    return render(request, "vote/login.html")


def logic(request):
    global current_user
    if current_user == None:
        return redirect("voting:ip")
    else:
        if current_user.spl_done == False and current_user.aspl_done == False:
            return redirect("voting:index")
        elif current_user.aspl_done == False and current_user.spl_done == True:
            return redirect("voting:voted")
        elif current_user.spl_done == True and current_user.aspl_done == True:
            return redirect("voting:thanks")
        else:
            return HttpResponse("<h1>Some Server Error</h1>")


def mail(request):
    global current_user
    if current_user == None:
        return render(request, "vote/email.html")
    else:
        return redirect("voting:logic")
