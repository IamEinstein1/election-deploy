import socket

from django.shortcuts import render, redirect
from .models import ASPL, SPL, User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate
global current_user


def ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        current_ip = x_forwarded_for.split(',')[0]
        print(f"IP: {current_ip}")
        try:
            socket.inet_aton(current_ip)
            ip_valid = True
        except socket.error:
            ip_valid = False
    else:
        current_ip = request.META.get('REMOTE_ADDR')
        print(f"IP: (2nd method) {current_ip}")
        try:
            socket.inet_aton(current_ip)
            ip_valid = True
            try:
                global current_user
                current_user = User.objects.get(ip=current_ip)
                current_user.save()
            except User.DoesNotExist:
                # global current_user
                current_user = User.objects.create(ip=current_ip)
                current_user.save()
        except socket.error:
            ip_valid = False
    print(f"IS valid: {ip_valid}, \n Addres:  {current_ip}")
    return redirect("voting:logic")


def index(request):
    global current_user
    current_user.spl_done = False
    current_user.aspl_done = 
    current_user.save()
    candidates = SPL.objects.all()
    return render(request, 'vote/index.html', context={"candidates": candidates})


def spl(request):
    if request.method == "GET":
        return render(request, "vote/error.html", context={"text": "Invalid method", "type": "primary"})
    else:
        try:
            selected_candidate = SPL.objects.get(pk=request.POST['SPL'])
        except(KeyError, SPL.DoesNotExist):
            candidates = SPL.objects.all()
            error = "You have not selected a candidate."
            return render(request, 'vote/index.html', {'candidates': candidates, 'error_message': error})
        else:
            global current_user
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
        global current_user
        if current_user.spl_done == False:
            return render(request, "vote/index.html", context={"candidates": SPL.objects.all()})
        elif current_user.aspl_done == False:
            return render(request, "vote/voted.html", context={"candidates": ASPL.objects.all()})
        elif current_user.spl_done == True and current_user.aspl_done == True:
            return render(request, "vote/thanks.html")
        else:
            return HttpResponse("<h1>Some Server Error</h1>")
    except(ValueError, NameError):
        return render(request, "vote/error.html", context={"text": "Invalid method", "type": "info"})
    # candidates = ASPL.objects.all()
    # return render(request, 'vote/voted.html', context={"candidates": candidates})


def thanks(request):
    global current_user
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


# logic for :
#       quitting in between
num = 1


def logic(request):
    # global num
    # if num == 1:
    # num += 1
    # print(num)
    # return redirect("voting:ip")
    # else:
    global current_user
    if current_user.spl_done == False:
        return render(request, "vote/index.html", context={"candidates": SPL.objects.all()})
    elif current_user.aspl_done == False:
        return render(request, "vote/voted.html", context={"candidates": ASPL.objects.all()})
    elif current_user.spl_done == True and current_user.aspl_done == True:
        current_user.spl_done = False
        current_user.aspl_done = False
        current_user.save()
        return render(request, "vote/thanks.html")
    else:
        return HttpResponse("<h1>Some Server Error</h1>")


# import socket
# from django.shortcuts import render, redirect
# from .models import ASPL, SPL, User
# from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
# from django.contrib.auth import authenticate


# def index(request):
#     global spl_done
#     global aspl_done
#     spl_done = False
#     aspl_done = False
#     candidates = SPL.objects.all()
#     return render(request, 'vote/index.html', context={"candidates": candidates})


# def spl(request):
#     if request.method == "GET":
#         return render(request, "vote/error.html", context={"text": "Invalid method", "type": "primary"})
#     else:
#         global spl_done
#         global aspl_done
#         try:
#             selected_candidate = SPL.objects.get(pk=request.POST['SPL'])
#         except(KeyError, SPL.DoesNotExist):
#             candidates = SPL.objects.all()
#             error = "You have not selected a candidate."
#             return render(request, 'vote/index.html', {'candidates': candidates, 'error_message': error})
#         else:
#             selected_candidate.votes += 1
#             selected_candidate.save()
#             spl_done = True
#             return HttpResponseRedirect(reverse('voting:voted'))


# def aspl(request):
#     if request.method == "GET":
#         return render(request, "vote/error.html", context={"text": "Invalid method", "type": "info"})
#     else:
#         global aspl_done
#         try:
#             selected_candidate = ASPL.objects.get(pk=request.POST['ASPL'])
#         except(KeyError, ASPL.DoesNotExist):
#             candidates = ASPL.objects.all()
#             error = "You have not selected a candidate"
#             return render(request, 'vote/voted.html', {'candidates': candidates, 'error_message': error})
#         else:
#             selected_candidate.votes += 1
#             selected_candidate.save()
#             aspl_done = True

#             return HttpResponseRedirect(reverse('voting:thanks'))


# def voted(request):
#     global spl_done
#     global aspl_done
#     try:
#         if spl_done == False:
#             return render(request, "vote/index.html", context={"candidates": SPL.objects.all()})
#         elif aspl_done == False:
#             return render(request, "vote/voted.html", context={"candidates": ASPL.objects.all()})
#         elif spl_done == True and aspl_done == True:
#             return render(request, "vote/thanks.html")
#         else:
#             return HttpResponse("<h1>Some Server Error</h1>")
#     except(ValueError, NameError):
#         return render(request, "vote/error.html", context={"text": "Invalid method", "type": "info"})

#     # candidates = ASPL.objects.all()
#     # return render(request, 'vote/voted.html', context={"candidates": candidates})


# def thanks(request):
#     global spl_done
#     global aspl_done
#     spl_done = False
#     aspl_done = False
#     return render(request, 'vote/thanks.html')


# def result(request):
#     if request.method == "GET":
#         return render(request, "vote/error.html", context={"type": "danger", "text": "You are not authorized to see the results"})
#     elif request.method == "POST":

#         aspl_can = ASPL.objects.order_by('-votes')[:]
#         spl_can = SPL.objects.order_by('-votes')[:]
#         password = request.POST['password']
#         username = request.POST['username']
#         user = authenticate(username=username, password=password)
#         if user != None:
#             return render(request, "vote/result.html", context={"spl_can": spl_can, "aspl_can": aspl_can})
#         else:
#             return render(request, "vote/error.html", context={"type": "danger", "text": "You are not authorized to see the results"})


# def login(request):
#     return render(request, "vote/login.html")


# # logic for :
# #       quitting in between
# num = 1


# def logic(request):
#     global num
#     if num == 1:
#         num += 1
#         print(num)
#         return redirect("voting:ip")
#     else:
#         global spl_done
#         global aspl_done
#         if spl_done == False:
#             return render(request, "vote/index.html", context={"candidates": SPL.objects.all()})
#         elif aspl_done == False:
#             return render(request, "vote/voted.html", context={"candidates": ASPL.objects.all()})
#         elif spl_done == True and aspl_done == True:
#             spl_done = False
#             aspl_done = False
#             return render(request, "vote/thanks.html")
#         else:
#             return HttpResponse("<h1>Some Server Error</h1>")
