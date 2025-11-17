from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def booking_summary(request):
	# Handle delete
	if request.method == 'POST' and 'delete' in request.POST:
		booking = get_object_or_404(Booking, id=request.POST['delete'], user=request.user)
		booking.delete()
		return redirect('booking_summary')
	bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
	total_amount = sum(b.total_cost for b in bookings)
	return render(request, 'bookings/booking_summary.html', {
		'bookings': bookings,
		'total_amount': total_amount,
		'show_actions': True
	})
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import datetime
from .models import Booking
from destinations.models import Destination

@login_required
def book_trip(request, destination):
	print('DEBUG book_trip called, method:', request.method)
	trip_prices = {
		'norway': {'name': 'Viking Voyage', 'price': 1800},
		'sweden': {'name': 'Frostbound Frontier', 'price': 1500},
		'denmark': {'name': 'Runestone Realms', 'price': 1400},
		'finland': {'name': 'Aurora Awakening', 'price': 1600},
		'iceland': {'name': 'Saga of Fire & Ice', 'price': 1900},
		'estonia': {'name': 'Mystic Baltic Quest', 'price': 1300},
	}
	trip_id = destination.lower()
	trip = trip_prices.get(trip_id)
	if not trip:
		messages.error(request, 'Invalid destination selected.')
		return redirect('create_booking')

	# Generate fixed date ranges (6 options, 2 weeks apart)
	base = datetime.date(2025, 7, 25)
	fixed_dates = []
	for i in range(6):
		start = base + datetime.timedelta(days=i*14)
		end = start + datetime.timedelta(days=13)
		fixed_dates.append({'start': start, 'end': end})

	booking_success = False
	if request.method == 'POST':
		try:
			print('DEBUG book_trip POST block entered')
			people = int(request.POST.get('number_of_people', 1))
			print('DEBUG people:', people)
			notes = request.POST.get('notes', '')
			print('DEBUG notes:', notes)
			selected_range = request.POST.get('date_range', '')
			print('DEBUG selected_range:', selected_range)
			from datetime import datetime as dt
			try:
				start_date, end_date = selected_range.split('|')
				print('DEBUG start_date:', start_date, 'end_date:', end_date)
				# Parse to date objects (YYYY-MM-DD)
				if isinstance(start_date, str):
					start_date = dt.strptime(str(start_date).strip(), '%Y-%m-%d').date()
				if isinstance(end_date, str):
					end_date = dt.strptime(str(end_date).strip(), '%Y-%m-%d').date()
				print('DEBUG parsed start_date:', start_date, 'parsed end_date:', end_date)
			except ValueError:
				print('DEBUG ValueError in date parsing, using base')
				start_date = base
				end_date = base + datetime.timedelta(days=13)
			price = trip['price'] / 2
			print('DEBUG price:', price)
			total_cost = people * price
			print('DEBUG total_cost:', total_cost)
			# Get destination object
			try:
				dest_obj = Destination.objects.get(name__iexact=destination)
				print('DEBUG dest_obj:', dest_obj)
			except Destination.DoesNotExist:
				print('DEBUG Destination.DoesNotExist')
				messages.error(request, 'Destination not found. Please contact support.')
				return redirect('create_booking')
			print('DEBUG before booking create')
			booking = Booking.objects.create(
				user=request.user,
				destination=dest_obj,
				start_date=start_date,
				end_date=end_date,
				number_of_people=people,
				total_cost=total_cost,
				notes=notes
			)
			print('DEBUG after booking create:', booking)
			from django.urls import reverse
			from django.http import HttpResponseRedirect
			redirect_url = reverse('booking_summary')
			print('DEBUG redirecting to booking summary:', redirect_url)
			return HttpResponseRedirect(redirect_url)
		except Exception as e:
			print('DEBUG POST error:', e)
			raise

	# GET request: render the booking form
	# ...existing code...

	# Get user_profile for navbar/profile pic
	from users.models import UserProfile
	user_profile = None
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
		pass

	return render(request, 'bookings/book_trip.html', {
		'trip': trip,
		'trip_id': trip_id,
		'fixed_dates': fixed_dates,
		'booking_success': booking_success,
		'user_profile': user_profile,
		'user': request.user
	})

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import datetime
from .models import Booking
from destinations.models import Destination

# Booking form
class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['destination', 'start_date', 'end_date', 'number_of_people', 'notes']
		widgets = {
			'start_date': forms.DateInput(attrs={'type': 'date'}),
			'end_date': forms.DateInput(attrs={'type': 'date'}),
			'notes': forms.Textarea(attrs={'rows': 2}),
		}


@login_required
def create_booking(request):
	trip_prices = {
		'norway': 1800, 'sweden': 1500, 'denmark': 1400,
		'finland': 1600, 'iceland': 1900, 'estonia': 1300
	}
	trip_name = request.GET.get('trip')
	destination = None
	if trip_name:
		try:
			destination = Destination.objects.get(name__iexact=trip_name.capitalize())
		except Destination.DoesNotExist:
			destination = None

	# Handle booking deletion
	if request.method == 'POST' and 'delete' in request.POST:
		booking = get_object_or_404(Booking, id=request.POST['delete'], user=request.user)
		booking.delete()
		messages.success(request, 'Booking deleted.')
		return redirect('create_booking')

	# Handle booking creation
	if request.method == 'POST' and 'delete' not in request.POST:
		form = BookingForm(request.POST)
		if destination:
			form.fields['destination'].queryset = Destination.objects.filter(name__iexact=trip_name.capitalize())
		if form.is_valid():
			booking = form.save(commit=False)
			booking.user = request.user
			if destination:
				booking.destination = destination
			trip_key = booking.destination.name.lower() if booking.destination else ''
			price = trip_prices.get(trip_key, 1000) / 2
			booking.total_cost = price * booking.number_of_people
			booking.save()
			return redirect('/bookings/create/?just_booked=1#mybookings')
	else:
		if destination:
			form = BookingForm(initial={'destination': destination.id})
			form.fields['destination'].queryset = Destination.objects.filter(name__iexact=trip_name.capitalize())
		else:
			form = BookingForm()

	# Get user_profile for navbar/profile pic
	from users.models import UserProfile
	user_profile = None
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
		pass

	# No bookings list on this page anymore
	return render(request, 'bookings/create_booking.html', {
		'form': form,
		'selected_destination': destination,
		'user_profile': user_profile,
		'user': request.user
	})

@login_required
def booking_list(request):
	# Handle delete
	if request.method == 'POST' and 'delete' in request.POST:
		booking = get_object_or_404(Booking, id=request.POST['delete'], user=request.user)
		booking.delete()
		return redirect('booking_list')
	latest_id = request.GET.get('latest')
	if latest_id:
		bookings = Booking.objects.filter(user=request.user, id=latest_id)
		show_only_latest = True
	else:
		bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
		show_only_latest = False
	return render(request, 'bookings/booking_list.html', {'bookings': bookings, 'show_only_latest': show_only_latest})
