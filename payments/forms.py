from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
	class Meta:
		model = Payment
		fields = ['amount', 'method', 'notes']
		widgets = {
			'amount': forms.NumberInput(attrs={'min': 1, 'step': '0.01', 'placeholder': 'Amount (USD)'}),
			'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any notes or instructions...'}),
		}
