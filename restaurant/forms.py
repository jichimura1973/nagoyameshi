from django import forms
from .models import Reservation, Review, Restaurant, Category
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

class RestaurantUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name',
                  'description',
                  'postal_code', 
                  'tel_number', 
                  'address', 
                  'price_max', 
                  'price_min', 
                  'seats_number',
                  'close_day_of_week',
                  'category',
                  'photo'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'NAGOYAMESHI店名'})
        self.fields['description'].widget = forms.Textarea(attrs={'class':'form-control', 'placeholder': '店舗の説明'})
        self.fields['postal_code'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-4567'})
        self.fields['tel_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0123-45-6789'})
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '東京都千代田区神田棟堀町300番地'})
        self.fields['price_max'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['price_min'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['seats_number'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['close_day_of_week'].widget = forms.TextInput(attrs={'class': 'form-control','placeholder': '日曜日'})
        forms.ModelChoiceField(label="カテゴリ", queryset=Category.objects.all())
        photo = forms.ImageField(label='店舗画像', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

class RestaurantCreateForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name',
                  'description',
                  'postal_code', 
                  'address', 
                  'tel_number', 
                  'price_max', 
                  'price_min', 
                  'close_day_of_week',
                  'seats_number',
                  'category'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'NAGOYAMESHI店名'})
        self.fields['description'].widget = forms.Textarea(attrs={'class':'form-control', 'placeholder': '店舗の説明'})
        self.fields['postal_code'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-4567'})
        self.fields['tel_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0123-45-6789'})
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '東京都千代田区神田棟堀町300番地'})
        self.fields['price_max'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['price_min'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['seats_number'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['close_day_of_week'].widget = forms.TextInput(attrs={'class': 'form-control','placeholder': '日曜日'})
        forms.ModelChoiceField(label="カテゴリ", queryset=Category.objects.all())

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'photo',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'ひつまぶし'})
        photo = forms.ImageField(label='店舗画像', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
