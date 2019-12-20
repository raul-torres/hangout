from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q
import dateutil.parser

# Create your views here.
def index(request):
    return redirect('/main')

def main(request):
    return render(request, 'main.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        hashed_pw= bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        new_user = User.objects.create(name = request.POST['name'],user_name = request.POST['user_name'], password = hashed_pw)
        request.session['loggedInUser'] = new_user.id
    return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        logged_in_user = User.objects.get(user_name = request.POST['user_name'])
        request.session['loggedInUser'] = logged_in_user.id
        return redirect('/travels')

def travels(request):
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    your_trips = Trip.objects.filter(planned_by = logged_in_user, status = "pending") |Trip.objects.filter(users_joining = logged_in_user, status = 'pending')

    others_trips = Trip.objects.exclude(Q(planned_by = logged_in_user) | Q(users_joining = logged_in_user) |Q(status = 'success')| Q(status = 'cancelled'))
    context = {
        'LIU' : logged_in_user,
        'YT' : your_trips,
        'OT' : others_trips,
    }
    return render(request, 'travels.html', context)

def add(request):
    return render(request, 'add.html')

def trip_creator(request):
    errors = User.objects.trip_validator(request.POST)
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add')
    else:
        new_trip = Trip.objects.create(destination = request.POST['destination'], desc = request.POST['desc'], travel_date_to = request.POST['travel_date_to'], travel_date_from = request.POST['travel_date_from'], planned_by = logged_in_user, address = request.POST['address'])
        print(new_trip)
        return redirect('/travels')

def destination(request, TID):
    this_trip = Trip.objects.get(id = TID)
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    trip_messages = Message.objects.filter(trip = this_trip)
    context = {
        'TT' : this_trip,
        'LIU' : logged_in_user,
        'TM' : trip_messages
    }
    return render(request, 'destination.html', context)

def join(request, TID):
    this_trip = Trip.objects.get(id = TID)
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    this_trip.users_joining.add(logged_in_user)
    return redirect('/travels')

def edit(request, TID):
    this_trip = Trip.objects.get(id = TID)
    context = {
        'TT' : this_trip
    }
    return render(request, 'edit.html', context)

def save(request, TID):
    trip_to_update = Trip.objects.get(id = TID)
    TDT_converted = dateutil.parser.parse(request.POST['travel_date_to'])
    TDF_converted = dateutil.parser.parse(request.POST['travel_date_from'])
    trip_to_update.destination = request.POST['destination']
    trip_to_update.address = request.POST['address']
    trip_to_update.desc = request.POST['desc']
    trip_to_update.travel_date_to = TDT_converted
    trip_to_update.travel_date_from = TDF_converted
    trip_to_update.save()
    return redirect('/destination/'+TID)

def message_create(request, TID):
    current_trip = Trip.objects.get(id = TID)
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    new_message = Message.objects.create(content = request.POST['new_message'], user = logged_in_user, trip = current_trip)
    print(new_message)
    return redirect('/destination/' + TID)

def success(request, TID):
    current_trip = Trip.objects.get(id = TID)
    current_trip.status = 'success'
    current_trip.save()
    return redirect('/travels')

def cancelled(request, TID):
    current_trip = Trip.objects.get(id = TID)
    current_trip.status = 'cancelled'
    current_trip.save()
    return redirect('/travels')

def past_hangouts(request):
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    your_success_trips = Trip.objects.filter(planned_by = logged_in_user, status = 'success') | Trip.objects.filter(users_joining = logged_in_user, status = 'success')

    your_cancelled_trips = Trip.objects.filter(planned_by = logged_in_user, status = 'cancelled') | Trip.objects.filter(users_joining = logged_in_user, status = 'cancelled')

    others_trips = Trip.objects.exclude(Q(planned_by = logged_in_user)|Q(users_joining = logged_in_user)|Q(status = 'pending'))
    context = {
        'LIU' :logged_in_user,
        'YST' :your_success_trips,
        'YCT' : your_cancelled_trips,
        'OT' : others_trips,
    }

    return render(request, 'past_hangouts.html', context)

def past_destination(request, TID):
    this_trip = Trip.objects.get(id = TID)
    logged_in_user = User.objects.get(id = request.session['loggedInUser'])
    trip_messages = Message.objects.filter(trip = this_trip)
    context = {
        'TT' : this_trip,
        'LIU' : logged_in_user,
        'TM' : trip_messages
    }
    return render(request, "past_destination.html", context)



def logout(request):
    request.session.clear()
    return redirect('/')