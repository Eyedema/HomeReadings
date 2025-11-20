from django import forms

class UploadFileForma(forms.Form):
    file = forms.FileField()