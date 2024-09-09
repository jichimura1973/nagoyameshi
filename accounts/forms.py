from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import CustomUser, Job

class MySignupForm(SignupForm):
    user_name_kanji = forms.CharField(max_length=255, label='氏名')
    user_name_kana = forms.CharField(max_length=255, label='フリガナ')
    # zip_code = forms.CharField(max_length=255, label='郵便番号')
    # address = forms.CharField(max_length=255, label='住所')
    # phone_number = forms.CharField(max_length=255, label='電話番号')
    birthday = forms.CharField(max_length=255, label='誕生日')
    gender = forms.CharField(max_length=50, label="性別")
    # job = forms.CharField(max_length=255, label='職業')
    job = forms.ModelChoiceField(label="職業", queryset=Job.objects.all())
    is_subscribed = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields['user_name_kanji'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '侍 太郎'})
        self.fields['user_name_kana'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'サムライ タロ'})
        # self.fields['zip_code'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '1010022'})
        # self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '東京都千代田区神田棟堀町300番地'})
        # self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09012345678'})
        self.fields['birthday'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '19950401'})
        self.fields['gender'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '男性/女性'})
        # self.fields['job'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'エンジニア'})
        forms.ModelChoiceField(label="職業", queryset=Job.objects.all())
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder':'taro.samurai@example.com'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})
    
    def signup(self, request, user):
        user.user_name_kanji = self.cleaned_data['user_name_kanji']
        user.user_name_kana = self.cleaned_data['user_name_kana']
        # user.zip_code = self.cleaned_data['zip_code']
        # user.address = self.cleaned_data['address']
        # user.phone_number = self.cleaned_data['phone_number']
        user.birthday = self.cleaned_data['birthday']
        user.gender = self.cleaned_data['gender']
        # user.job = self.cleaned_data['job']
        user.job = Job.objects.get(id=self.cleaned_data['job'])
        user.save()
        return user
      
class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'メールアドレス'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード'})

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('user_name_kanji', 'user_name_kana', 'birthday', 'gender', 'job', 'email',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name_kanji'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '侍 太郎'})
        self.fields['user_name_kana'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'サムライ タロ'})
        # self.fields['zip_code'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '1010022'})
        # self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '東京都千代田区神田棟堀町300番地'})
        # self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09012345678'})
        self.fields['birthday'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '19950401'})
        self.fields['gender'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': '男性/女性'})
        # self.fields['job'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder': 'エンジニア'})
        forms.ModelChoiceField(label="職業", queryset=Job.objects.all())
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder':'taro.samurai@example.com'})