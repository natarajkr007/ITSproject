from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response, redirect
from EMS.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from .models import UserProfile
from .forms import NameForm
import urllib2
import json
import urllib
from django.contrib.auth.models import User
# Use the login_required() decorator to ensure only those logged in can access the view.

def index(request):
    user_count = UserProfile.objects.count()
    context = {
        'user_count' : user_count,
    }
    return render(request, 'EMS/index1.html', context)


def register(request):
    # Like before, get the request's context.
    # context = RequestContext(request)
    if request.user.is_authenticated:
        return redirect('EMS:index')

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'EMS/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    # Like before, obtain the context for the user's request.
    # context = RequestContext(request)
    if request.user.is_authenticated:
        return redirect('EMS:index')

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                # return HttpResponseRedirect('/EMS/')
                request.session['user'] = user.username
                return redirect('EMS:index')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # return render_to_response('EMS/login.html', {}, context)
        return render(request, 'EMS/login.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return redirect('EMS:index')

@login_required
def user_profile(request):
    return render(request, 'EMS/user_profile.html')

@login_required
def monitor (request):
    if request.user.is_authenticated():
        username = request.user.username
    url = ('https://energymonitoring.000webhostapp.com/getenergy.php/?serviceno='+str(username))
    f = urllib2.urlopen(url)  # send a GET request
    x = str(f.read())
    r = unicode(x, "utf-8")  # convert it into string using utf-8 encoding
    r = json.loads(r)  # python lib to load a json string as dictionary
    t = r['result']
    #k=t['consumption']
    context = {
        'consumption': t,
    }
    return render(request, 'EMS/monitor.html', context)

@login_required
def forum(request):

    if request.method == 'POST':

        if request.user.is_authenticated():
            username = request.user.username

        form = NameForm(request.POST)

        if form.is_valid():
            complaint = form.cleaned_data['complaint']
            complaint=complaint.replace(" ","+")
            url = ('https://energymonitoring.000webhostapp.com/forumenter.php/?complaint='+complaint+'&serviceno='+username)
            f = urllib2.urlopen(url)
            x = str(f.read())
            request.method='NULL'
            return forum(request)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        g=1
    url = ('https://energymonitoring.000webhostapp.com/getforum.php')
    f = urllib2.urlopen(url)  # send a GET request
    x = str(f.read())
    r = unicode(x, "utf-8")  # convert it into string using utf-8 encoding
    r = json.loads(r)  # python lib to load a json string as dictionary
    t = r['result']

    context = {

            'comp': t,
        }
    if g==1:
        context.update({'form': form})
    return render(request, 'EMS/forum.html', context)
