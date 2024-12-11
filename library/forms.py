from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введіть ваше ім'я"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Введіть вашу пошту"
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Напишіть ваш коментар",
                'rows': 4
            }),
        }

class EmailForm(forms.Form):
    name = forms.CharField(label="Ваше ім'я", max_length=70, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введіть вашe і'мя"}))
    email = forms.EmailField(label='Ваша пошта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть вашу пошту'}))
    to = forms.EmailField(label='Пошта друга', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть вашу пошту'}))
    comment = forms.CharField(label="Коментар",required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))