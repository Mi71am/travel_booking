from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination


class Booking(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
	start_date = models.DateField(default="2025-01-01")
	end_date = models.DateField(default="2025-01-02")
	number_of_people = models.PositiveIntegerField()
	total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.destination.name} ({self.start_date} to {self.end_date})"
