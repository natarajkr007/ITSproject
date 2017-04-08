from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response, redirect
from EMS.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from .models import UserProfile,Energy
from .forms import NameForm
import urllib2
import json
import datetime
import urllib
import cookielib
from getpass import getpass
from django.contrib.auth.models import User
from django.core import serializers

# Use the login_required() decorator to ensure only those logged in can access the view.

def index(request):
    if request.user.is_authenticated:
        return redirect('EMS:profile')
    user_count = UserProfile.objects.count()
    context = {
        'user_count' : user_count,
    }
    return render(request, 'EMS/index1.html', context)


def register(request):
    # Like before, get the request's context.
    # context = RequestContext(request)
    if request.user.is_authenticated:
        return redirect('EMS:profile')

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

            messages.success(request, 'Registration complete. Please, LogIn')
            return redirect('EMS:index')

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
                return redirect('EMS:profile')
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
    messages.success(request, 'Logged out successfuly')
    # Take the user back to the homepage.
    return redirect('EMS:index')

@login_required
def user_profile(request):
    serviceno = request.user.username
    user_id = User.objects.get(username=serviceno).id
    role = UserProfile.objects.get(user=user_id).role
    energy = Energy.objects.filter(serviceno=serviceno)
    sum = 0

    for energy in energy:
        sum += float(energy.consumption)

    context_user = {
        'sum' : sum,
    }
    if request.user.is_authenticated and role == 'C':
        return render(request, 'EMS/user_profile.html', context_user)
    elif request.user.is_authenticated and role == 'O':
        user = UserProfile.objects.all()
        energy = Energy.objects.all()
        day = []
        for i in user:
            sum = 0.0
            for j in energy:
                timestamp = j.timestamp
                dayMonth = timestamp.split()
                if str(i.user) == str(j.serviceno) and str(dayMonth[0]) == str(datetime.datetime.now().strftime('%Y-%m-%d')):
                    sum = sum + float(j.consumption)
            day.append(sum)
        month=[]
        for i in user:
            sum = 0.0
            for j in energy:
                if str(i.user) == str(j.serviceno) and str(j.month) == str(datetime.datetime.now().strftime('%m')) and str(j.year)==str(datetime.datetime.now().strftime('%Y')):
                    sum = sum + float(j.consumption)
            month.append(sum)

        total=zip(user,day,month)
        context_admin = {
            'total':total,
        }

        return render(request, 'EMS/admin_profile.html', context_admin)
    # else:
    #     return HttpResponse('he is not customer')

@login_required
def monitor (request):
    username="default"
    if request.user.is_authenticated() and request.user.is_superuser:
        username = request.user.username
    # url = ('https://energymonitoring.000webhostapp.com/getenergy.php/?serviceno='+str(username))
    # f = urllib2.urlopen(url)  # send a GET request
    # x = str(f.read())
    # r = unicode(x, "utf-8")  # convert it into string using utf-8 encoding
    # r = json.loads(r)  # python lib to load a json string as dictionary
    # t = r['result']
    # #k=t['consumption']
    serviceno = request.user.username
    user_id = User.objects.get(username=serviceno).id
    role = UserProfile.objects.get(user=user_id).role
    user = UserProfile.objects.all()
    energy = Energy.objects.all()
    k=[]
    for i in user:
        sum=0.0
        for j in energy:
            timestamp=j.timestamp
            dayMonth=timestamp.split()
            if str(i.user)==str(j.serviceno) and str(dayMonth[0])==str(datetime.datetime.now().strftime('%Y-%m-%d')):
                sum=sum+float(j.consumption)
        k.append(sum)


    context = {
        'consumption': username,
        'role': role,
        'user':user,
        'energy':k,
    }
    return render(request, 'EMS/monitor.html', context)

@login_required
def show(request):

    today_day = str(datetime.datetime.now().date()).split("-")[2]  # gets today's date to make a query
    today_month = str(datetime.datetime.now().date()).split("-")[1]
    today_year = str(datetime.datetime.now().date()).split("-")[0]

    if request.user.is_authenticated():
        username = request.user.username
        energy1 = Energy.objects.filter(serviceno = username, year = today_year, month = today_month, day = today_day)
        time = []
        consumption = []
        for i in energy1:
            time.append(str(i.hour))
            consumption.append(float(i.consumption))

        context = {
            'energy': energy1,
            'time': time,
            'consumption': consumption,
        }
        return render(request, 'EMS/show.html', context)

@login_required
def dashboard(request):
    username = request.user.id
    role = UserProfile.objects.get(user = username).role
    if role == 'C':
        return redirect('EMS:user_dashboard')
    else:
        return redirect('EMS:official_dashboard')

@login_required
def user_dashboard(request):

    today_day = str(datetime.datetime.now().date()).split("-")[2]  # gets today's date to make a query
    today_month = str(datetime.datetime.now().date()).split("-")[1]
    today_year = str(datetime.datetime.now().date()).split("-")[0]

    username = request.user.username
    energy = Energy.objects.filter(serviceno = username, year = today_year, month = today_month, day = today_day)

    # to calculate today's total energy till time
    sum = 0
    consumedValues = []
    for energy in energy:
        consumedValues.append(float(energy.consumption))
        sum += float(energy.consumption)

    # to calculate peak power consumed hour
    peakPower = max(consumedValues)
    peakHour = consumedValues.index(peakPower)
    minPower = min(consumedValues)
    minHour = consumedValues.index(minPower)

    context = {
        'sum' : sum,
        'values' : consumedValues,
        'peakPower' : peakPower,
        'peakHour' : peakHour,
        'minPower' : minPower,
        'minHour' : minHour
    }

    return render(request, 'EMS/user_dashboard.html', context)

@login_required
def official_dashboard(request):
    return render(request, 'EMS/official_dashboard.html')

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



def insert(request):
    if request.method == 'GET':
        serviceno = request.GET.get('sno', '')
        consumption = request.GET.get('consumption','')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        split_timestamp = timestamp.split()

        date = split_timestamp[0]
        split_date = date.split("-")
        year = split_date[0]
        month = split_date[1]
        day = split_date[2]

        time = split_timestamp[1]
        split_time = time.split(":")
        hour = split_time[0]

        p = Energy(serviceno=serviceno, consumption=consumption, timestamp=timestamp, hour=hour, year=year, month=month, day=day)
        p.save()
        context = {

            'comp': 'true',
        }
        return render(request, 'EMS/insert.html', context)


def message(request):
    username = '8332895680'
    passwd = 'yuvayuva'
    serviceno = request.GET.get('number', '')
    user_id = User.objects.get(username=serviceno).id
    number=str(UserProfile.objects.get(user=user_id).phone_no)
    # number = '7702300077'
    message = "Please be consious on your power usage!!!! From EMS"

    # Logging into the SMS Site
    url = 'http://site24.way2sms.com/Login1.action?'
    data = 'username=' + username + '&password=' + passwd + '&Submit=Sign+in'

    # For Cookies:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Adding Header detail:
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]

    try:
        usock = opener.open(url, data)
    except IOError:
        return

    jession_id = str(cj).split('~')[1].split(' ')[0]
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    send_sms_data = 'ssaction=ss&Token=' + jession_id + '&mobile=' + number + '&message=' + message + '&msgLen=136'
    opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token=' + jession_id)]

    try:
        sms_sent_page = opener.open(send_sms_url, send_sms_data)
    except IOError:
        return
    return render(request, 'EMS/message.html', {'phone_no':number})
