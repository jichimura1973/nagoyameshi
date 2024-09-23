from django import forms
from .models import Reservation

class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        # fields = ('date', 'time', 'number_of_people',)
        fields = ('reservation_date','number_of_people')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reservation_date'].widget.attrs['class'] = 'form-control'
        self.fields['reservation_date'].widget.attrs['id'] = 'reservation_date'
        self.fields['reservation_date'].widget.attrs['name'] = 'reservation_date'
        self.fields['reservation_date'].widget.attrs['class'] = 'form-control'
        self.fields['number_of_people'].widget.attrs['class'] = 'form-control'