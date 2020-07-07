from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

## for logins
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse   ## THIS is changed from  "from django.core.urlresolvers import reverse"
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "basic_app/index.html")

@login_required
def special(request):
    return HttpResponse("You are logged in ... NICE!!!")


@login_required
def user_logout(request):
    ## we use this decorator to ensure that user is logged before using any view(here to LOGOUT)
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):

    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  ## Form data is saved in database
            user.set_password(user.password)  ## Here hashing is done
            user.save()

            profile = profile_form.save(commit = False) ## We didnt commit because we wanted to manipulate this data before saving to avoid collisions
            profile.user = user  ## This creates that same one to one relation as in models.py

            if "profile_pic"  in request.FILES :
                ## U can use this same method while uploading any pdf or .csv ,,ex:resume
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

        return render(request, "basic_app/registration.html",
                      {"user_form": user_form,
                       "profile_form": profile_form,
                       "registered": registered})





def user_login(request):
    if request.method == "POST" :
        username = request.POST.get("username")  ## AS per field name used in HTML form
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                ## Active means not a dormant account
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid credentials applied!!")

    else:
        return render(request, "basic_app/login.html", {})
    ## Render means to use the context dictionary in template/html page



