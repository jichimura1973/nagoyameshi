from django import forms
from .models import Reservation, Review
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator

class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        # fields = ('date', 'time', 'number_of_people',)
        fields = ('reservation_date', 'reservation_time', 'number_of_people')
        # widgets = {'reservation_date': forms.DateInput(), 'reservation_time': forms.TimeInput}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reservation_date'].widget.attrs['class'] = 'form-control'
        self.fields['reservation_date'].widget.attrs['id'] = 'reservation_date'
        self.fields['reservation_date'].widget.attrs['name'] = 'reservation_date'
        # self.fields['reservation_date'].widget.attrs['help_text'] = "予約日を選択してください。"
        self.fields['reservation_time'].widget.attrs['class'] = 'form-control'
        self.fields['reservation_time'].widget.attrs['id'] = 'reservation_time'
        self.fields['reservation_time'].widget.attrs['name'] = 'reservation_time'
        
        # self.fields['reservation_date'] = forms.DateField(
        #     input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        #     required=True,
        #     label="予約日",
        #     initial=datetime.now,
        #     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        #     help_text="予約日を選択してください。",
        #     validators=[MaxValueValidator(datetime.now())],
        #     disabled=False,
        #     localize=True
        # )
        # self.fields['reservation_time'].widget.attrs['class'] = 'form-control'
        # self.fields['reservation_time'].widget.attrs['id'] = 'reservation_time'
        # self.fields['reservation_time'].widget.attrs['name'] = 'reservation_time'
        # self.fields['time'] = forms.TimeField(label='時刻',
        #                                 widget=forms.TimeInput(attrs={"class": "form-control", "name:": 'reservation_time', "type": "datetime-local", "value": timezone.datetime.now().strftime('%HH:%MM')}),
        #                                 # input_formats=['%Y-%m-%dT%H:%M']
        #                                 input_formats=['%HH:%MM']
        #                                 )
        # print('⭐️')
        # print(timezone.datetime.now().strftime('%Y-%m-%d'))
        self.fields['number_of_people'].widget.attrs['class'] = 'form-control'
        
class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'rate', 'visited_at')
        widgets = {'rate': forms.RadioSelect(), 'visited_at': forms.SelectDateWidget }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['cols'] = '30'
        self.fields['comment'].widget.attrs['rows'] = '5'
        self.fields['rate'].widget.attrs['class'] = 'form-check-input'
        self.fields['visited_at'].widget.attrs['class'] = 'form-control'
        # self.fields['visited_at'].widget.attrs['id'] = 'visited_at'
        # self.fields['visited_at'].widget.attrs['name'] = 'visited_at'    
    