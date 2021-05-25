from enum import auto
from django import forms
from datetime import datetime

class BookForm(forms.Form):
    title = forms.CharField(max_length=255)
    author = forms.CharField(max_length=255)
    description = forms.CharField(widget = forms.Textarea, max_length=255)


