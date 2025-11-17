from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking

class Payment(models.Model):
	booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	method = models.CharField(max_length=20, choices=[
		('card', 'Credit/Debit Card'),
		('paypal', 'PayPal'),
		('bank', 'Bank Transfer'),
	])
	date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('completed', 'Completed'),
		('failed', 'Failed'),
	], default='pending')
	notes = models.TextField(blank=True)

	def __str__(self):
		return f"{self.user.username} - {self.amount} ({self.status})"
