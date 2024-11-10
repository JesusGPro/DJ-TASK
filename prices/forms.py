from django import forms
from .models import Price, Task,  TaskComponent
from django.contrib.auth.models import User
from django.db import models



class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ('code', 'denomination', 'price', 'currency', 'unit', 'tag', 'reference', 'user', 'project')

    def __init__(self, *args, project=None, user=None, **kwargs):
        self.user = user
        self.project = project
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['user'].initial = self.user


class TaskForm(forms.ModelForm):
    components = forms.ModelMultipleChoiceField(queryset=Price.objects.all(), required=False)
    
    class Meta:
        model = Task
        fields = ('code', 'name', 'project', 'unit', 'price', 'currency', 'components')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['currency'].widget = forms.HiddenInput()  # make the currency field hidden

class ComponentForm(forms.ModelForm):
    code = forms.ModelChoiceField(queryset=Price.objects.all())

    class Meta:
        model = TaskComponent
        fields = ('task', 'code', 'quantity')

    def clean_code(self):
        code_value = self.cleaned_data['code']
        print(code_value)
        try:
            price_instance = Price.objects.get(code=code_value)
            return price_instance
        except Price.DoesNotExist:
            raise forms.ValidationError("Invalid code")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].to_python = lambda value: value
    