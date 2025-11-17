from django.contrib.auth.decorators import login_required
@login_required
def start_payment(request):
	booking_id = request.GET.get('booking_id')
	booking = None
	if booking_id:
		try:
			booking = Booking.objects.get(id=booking_id, user=request.user)
		except Booking.DoesNotExist:
			booking = None
	payments = Payment.objects.filter(user=request.user).order_by('-date')
	form = PaymentForm(request.POST or None)
	receipt = None
	if booking:
		receipt = {
			'destination': booking.destination.name,
			'start_date': booking.start_date,
			'end_date': booking.end_date,
			'number_of_people': booking.number_of_people,
			'total_cost': booking.total_cost,
			'notes': booking.notes,
		}
	if request.method == "POST" and form.is_valid():
		payment = form.save(commit=False)
		payment.user = request.user
		payment.status = 'pending'
		if booking:
			payment.notes = f"Booking ID: {booking.id} | {payment.notes}"
		payment.save()
		return redirect('payments_index')
	return render(request, 'payments/payment_base.html', {
		'form': form,
		'receipt': receipt,
		'booking': booking,
		'payments': payments,
	})

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from .forms import PaymentForm
from bookings.models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	booking_id = request.GET.get('booking_id')
	booking = None
	if booking_id:
		try:
			booking = Booking.objects.get(id=booking_id, user=request.user)
		except Booking.DoesNotExist:
			booking = None
	payments = Payment.objects.filter(user=request.user).order_by('-date')
	form = PaymentForm(request.POST or None)
	receipt = None
	if booking:
		receipt = {
			'destination': booking.destination.name,
			'start_date': booking.start_date,
			'end_date': booking.end_date,
			'number_of_people': booking.number_of_people,
			'total_cost': booking.total_cost,
			'notes': booking.notes,
		}
	if request.method == "POST" and form.is_valid():
		payment = form.save(commit=False)
		payment.user = request.user
		payment.status = 'pending'
		if booking:
			payment.notes = f"Booking ID: {booking.id} | {payment.notes}"
		payment.save()
		return redirect('payments_index')
	return render(request, 'payments/payment_base.html', {"payments": payments, "form": form, "receipt": receipt})
