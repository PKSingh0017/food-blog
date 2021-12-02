from django import forms
from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm, ResetPasswordForm
from django.db.models import fields

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from . import models as core_models

class MyCustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['remember'].widget.attrs.update({
            'class': 'row align-items-center remember'
        })

class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class MyCustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomChangePasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class MyCustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    bstate = forms.CharField(required=False)
    bcity = forms.CharField(required=False)
    bdistrict = forms.CharField(required=False)
    sstate = forms.CharField(required=False)
    scity = forms.CharField(required=False)
    sdistrict = forms.CharField(required=False)
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.IntegerField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

class AddBlogForm(forms.ModelForm):
    class Meta:
        model = core_models.Blog
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AddBlogForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = core_models.Recipes
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AddRecipeForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })