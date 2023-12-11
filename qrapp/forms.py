from django import forms

class QRCodeForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea, label="QR Code Data")
    size = forms.IntegerField(min_value=1, initial=10, label="Size")
    border = forms.IntegerField(min_value=0, initial=4, label="Border")
    fill_color = forms.CharField(max_length=7, initial="#000000", label="Fill Color")
    back_color = forms.CharField(max_length=7, initial="#FFFFFF", label="Background Color")
    transparent_background = forms.BooleanField(required=False, label="Transparent Background")
    is_google_drive_link = forms.BooleanField(required=False, label="Is this a Google Drive link?")