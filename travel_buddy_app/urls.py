from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('main', views.main),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('travels', views.travels),
    path('add', views.add),
    path('trip_creator', views.trip_creator),
    path('destination/<TID>', views.destination),
    path('join/<TID>', views.join),
    path('edit/<TID>', views.edit),
    path('save/<TID>', views.save),
    path('message_create/<TID>', views.message_create),
    path('success/<TID>', views.success),
    path('cancelled/<TID>', views.cancelled),
    path('past_hangouts', views.past_hangouts),
    path('past_destination/<TID>', views.past_destination),
]