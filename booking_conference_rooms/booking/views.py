from django.shortcuts import render
from booking.models import Room, RoomBooking
from django.http import HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from datetime import date


class main(View):
    def get(self, request):
        today = date.today()
        all_rooms = Room.objects.all().order_by('id')
        reserved_rooms_id = []

        'Today booked rooms list'
        reservations = RoomBooking.objects.filter(booking_date=str(date.today()))
        for reservation in reservations:
            reserved_rooms_id.append(reservation.room_id.id)

        return render(request,
                      'main.html',
                      context=({'rooms': all_rooms,
                                'reserved_rooms_id': reserved_rooms_id,
                                'today': today}))


class add_new_room(View):
    def get(self, request):
        return render(request,
                      'add_new_room.html', )

    def post(self, request):
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


class delete(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        room.delete()
        return HttpResponseRedirect('/room')


class modify(View):

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        ctx = {'room_name': room.room_name,
               'seats_number': room.seats_number,
               'projector': room.projector}

        return render(request,
                      'modify.html',
                      context=(ctx))

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        ctx = {'room_name': room.room_name,
               'seats_number': room.seats_number,
               'projector': room.projector}
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


class reserve(View):

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        ctx = {'min_date': str(date.today()),
               'room_name': room.room_name, }

        return render(request,
                      'reserve.html',
                      context=(ctx))

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        ctx = {'min_date': str(date.today()),
               'room_name': room.room_name, }

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


class room_details(View):
    def get(self, request, id):
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
