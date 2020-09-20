import re
import socket
from django.shortcuts import render, redirect
from .models import ASPL, SPL, User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate

num = 1
current_user = None


def ip(request):
    if request.method == "GET":
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            current_ip = x_forwarded_for.split(',')[0]
            try:
                socket.inet_aton(current_ip)
                try:
                    global current_user
                    current_user = User.objects.get(ip=current_ip)
                    current_user.times_visited += 1
                    current_user.save()
                except (User.DoesNotExist, NameError, KeyError):
                    current_user = User.objects.create(ip=current_ip)
                    current_user.save()
                    return render(request, "vote/index.html", context={"candidates": SPL.objects.all(), "abc": "name"})
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP address is not valid"})
        else:
            current_ip = request.META.get('REMOTE_ADDR')
            try:
                socket.inet_aton(current_ip)
                try:
                    current_user = User.objects.get(ip=current_ip)
                    current_user.times_visited += 1
                    current_user.save()
                except (User.DoesNotExist, NameError, KeyError):
                    current_user = User.objects.create(ip=current_ip)
                    current_user.save()
                    return render(request, "vote/index.html", context={"candidates": SPL.objects.all(), "abc": "name"})
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP adress is not valid"})
        return redirect("voting:logic")
    elif request.method == "POST":
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            current_ip = x_forwarded_for.split(',')[0]
            try:
                socket.inet_aton(current_ip)
                try:
                    current_user = User.objects.get(ip=current_ip)
                    email = request.POST['mail']
                    if re.match(r"\w+40\d{4}@npschennai.com", email) == None:
                        return render(request, "vote/email.html", context={"error_message": "Enter a valid email\n The format should be 'name40admissionno@npschennai.com'"})
                    else:
                        current_user.email = email
                        current_user.times_visited += 1
                        current_user.save()
                except (User.DoesNotExist, NameError, KeyError):
                    current_user = User.objects.create(ip=current_ip)
                    email = request.POST['mail']
                    if re.match(r"\w+40\d{4}@npschennai.com", email) == None:
                        return render(request, "vote/email.html", context={"error_message": "Enter a valid email\n The format should be 'name40admissionno@npschennai.com'"})
                    else:
                        current_user.email = email
                        current_user.save()
                    return render(request, "vote/index.html", context={"candidates": SPL.objects.all(), "abc": "name"})
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP address is not valid"})
        else:
            current_ip = request.META.get('REMOTE_ADDR')
            try:
                socket.inet_aton(current_ip)
                try:
                    current_user = User.objects.get(ip=current_ip)
                    current_user.times_visited += 1
                    email = request.POST['mail']
                    if re.match(r"\w+40\d{4}@npschennai.com", email) == None:
                        return render(request, "vote/email.html", context={"error_message": "Enter a valid email\n The format should be 'name40admissionno@npschennai.com'"})
                    else:
                        current_user.email = email
                    current_user.save()
                except (User.DoesNotExist, NameError, KeyError):
                    current_user = User.objects.create(ip=current_ip)
                    email = request.POST['mail']
                    if re.match(r"\w+40\d{4}@npschennai.com", email) == None:
                        return render(request, "vote/email.html", context={"error_message": "Enter a valid email\n The format should be 'name40admissionno@npschennai.com'"})
                    else:
                        current_user.email = email
                    current_user.save()
                    return render(request, "vote/index.html", context={"candidates": SPL.objects.all(), "abc": "name"})
            except socket.error:
                return render(request, "vote/error.html", context={"type": "danger", "text": "Your IP adress is not valid"})
        return redirect("voting:logic")


def index(request):
    try:
        if current_user == None:
            return redirect("voting:ip")
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
            if 'name' in request.POST:
                global current_user
                selected_candidate.votes += 1
                selected_candidate.save()
                current_user.spl_done = True
                current_user.name = request.POST['name']

                current_user.save()
                return HttpResponseRedirect(reverse('voting:voted'))
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
            global current_user
            selected_candidate.votes += 1
            selected_candidate.save()
            current_user.aspl_done = True
            current_user.save()
            return HttpResponseRedirect(reverse('voting:thanks'))


def voted(request):
    try:
        if current_user == None:
            return redirect("voting:ip")
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
    if current_user == None:
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


# def templater(request):
    # global num
    # if num == 1:
        # num += 1
        # return redirect("voting:ip")
    # if current_user.email == "mail":
        # return render(request, "vote/email.html")
    # else:
        # print(current_user.mail)
        # return redirect("voting:logic")
#
#
# def email(request):
    # if request.method == "POST":
        # email = request.POST['mail']
        # if re.match(r"\w+40\d{4}@npschennai.com", email) == None:
            # return render(request, "vote/email.html", context={"error_message": "Enter a valid email\n The format should be 'name40admissionno@npschennai.com'"})
        # else:
            # return redirect("voting:ip")
#
