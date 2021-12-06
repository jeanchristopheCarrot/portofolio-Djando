from django import forms

class LogInForm(forms.Form):
    username = forms.CharField(label='id_username', max_length=100)
    password = forms.CharField(label='id_password', max_length=100)
    
class UpdateForm(forms.Form):
    word = forms.CharField(label='id_word', max_length=100)
    letter = forms.CharField(label='id_letter', max_length=1)
    score = forms.IntegerField(label='id_score')