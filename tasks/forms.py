from django import forms
from .models import Project, Currency, ActiveProject

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'location', 'currency')

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ('eur_sar', 'usd_sar', 'eur_usd')

class ActiveProjectForm(forms.ModelForm):
    class Meta:
        model:ActiveProject
        fields = ('user', 'project')
