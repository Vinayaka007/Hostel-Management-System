from django import forms
from .models import Register
from .models import HostelApp
from django import forms
from .models import HostelApp


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your father's name"}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your institution name'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your course name'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your registration number'}),
            'ac_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your academic year'}),
            'course_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your course year'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        }



class LoginForm(forms.Form):
    reg_no = forms.CharField(label='Registration Number', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)





class HostelApplicationForm(forms.ModelForm):
    class Meta:
        model = HostelApp
        fields = ['photo', 'number_of_sharing', 'mother_name', 'occupation', 'landline_num', 'emergency_contact', 'father_email']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'number_of_sharing': forms.NumberInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'landline_num': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'father_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }




from django import forms
from .models import ComplaintBox

class ComplaintBoxForm(forms.ModelForm):
    class Meta:
        model = ComplaintBox
        fields = ['name', 'email', 'phone', 'register_number', 'subject', 'complaint']


from django import forms

class RoomAllotForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    usn = forms.CharField(max_length=20, required=True)



from django import forms

class AdminLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)



from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
