from django import forms
from .models import WorkLevel, WorkPackage, Work, Measurement
from django.forms import ModelForm
from django.forms import formset_factory
from django.core.exceptions import ValidationError


class WorkLevelForm(ModelForm):
    class Meta:
        model = WorkLevel
        fields = ('project','level_number',)

class WorkPackageForm(forms.ModelForm):
    class Meta:
        model = WorkPackage
        fields = ('name', 'description', 'parent')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = WorkPackage.objects.all()
    
class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('task', 'work_package', 'quantity')

class WPIdForm(forms.Form):
    work_package_id = forms.CharField(max_length=50)


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('description', 'nr', 'width', 'length', 'height', 'comment')


