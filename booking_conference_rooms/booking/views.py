from django.shortcuts import render
from booking.models import Room, RoomBooking
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from datetime import date


# Create your views here.

def main(request):
    today = date.today()
    all_rooms = Room.objects.all().order_by('id')
    reserved_rooms_id = []

    'Today booked rooms list'
    reservations = RoomBooking.objects.filter(booking_date = str(date.today()))
    for reservation in reservations:
        reserved_rooms_id.append(reservation.room_id.id)

    return render(request,
                  'main.html',
                  context=({'rooms': all_rooms,
                           'reserved_rooms_id': reserved_rooms_id,
                            'today': today}))



@csrf_protect
def add_new_room(request):
    if request.method == "GET":
        return render(request,
                      'add_new_room.html', )

    elif request.method == "POST":
        all_rooms = Room.objects.all()
        room_name = request.POST.get('room_name')
        seats_number = request.POST.get('seats_number')
        projector = request.POST.get('projector')

        if projector == 'on':
            projector = True
        else:
            projector = False

        if room_name == "" or seats_number == "":
            results = "Room name or seats number filed is empty. Fill the gaps!"
            return render(request,
                          'add_new_room.html',
                          context=({'results': results}))

        for room_id in all_rooms:
            if room_id.room_name == room_name:
                results = "Room already exist. Change name"
                return render(request,
                              'add_new_room.html',
                              context=({'results': results}))

        new_room = Room.objects.create(room_name=room_name, seats_number=seats_number, projector=projector)
        return HttpResponseRedirect('/room')


def delete(request, id):
    room = Room.objects.get(pk=id)
    room.delete()
    return HttpResponseRedirect('/room')


def modify(request, id):
    room = Room.objects.get(pk=id)
    ctx = {'room_name': room.room_name,
           'seats_number': room.seats_number,
           'projector': room.projector}

    if request.method == "GET":
        return render(request,
                      'modify.html',
                      context=(ctx))

    elif request.method == "POST":
        all_rooms = Room.objects.exclude(pk=id)
        room_name = request.POST.get('room_name')
        seats_number = request.POST.get('seats_number')
        projector = request.POST.get('projector')

        if projector == 'on':
            projector = True
        else:
            projector = False

        if room_name == "" or seats_number == "":
            ctx['results'] = "Room name or seats number filed is empty. Fill the gaps!"
            return render(request,
                          'modify.html',
                          context=(ctx))

        for room_id in all_rooms:
            if room_id.room_name == room_name:
                ctx['results'] = "Room already exist. Change name"
                return render(request,
                              'modify.html',
                              context=(ctx))
            else:
                room_edit = Room.objects.get(pk=id)
                room_edit.room_name = room_name
                room_edit.seats_number = seats_number
                room_edit.projector = projector
                room_edit.save()

        return HttpResponseRedirect('/room')


def reserve(request, id):
    room = Room.objects.get(pk=id)
    ctx = {'min_date': str(date.today()),
           'room_name': room.room_name, }
    if request.method == "GET":
        return render(request,
                      'reserve.html',
                      context=(ctx))

    if request.method == "POST":
        date_to_reserve = str(request.POST.get('reserve_date'))
        comments = request.POST.get('comments')
        room_reservations = RoomBooking.objects.filter(room_id=id)

        for room in room_reservations:
            if str(room.booking_date) == date_to_reserve:
                ctx['results'] = f'Room already reserved at {date_to_reserve}.'
                return render(request,
                              'reserve.html',
                              context=(ctx))

        RoomBooking.objects.create(booking_date=date_to_reserve, room_id=Room.objects.get(pk=id), comments=comments)
        return HttpResponseRedirect('/room')


def room_details(request, id):
    room = Room.objects.get(pk=id)
    reservations = RoomBooking.objects.filter(room_id=id).order_by('booking_date')
    ctx = {'room_name': room.room_name,
           'seats_number': room.seats_number,
           'projector': room.projector,
           'reservations': reservations,
           'id': id}
    return render(request,
                  'room_details.html',
                  context=(ctx))
