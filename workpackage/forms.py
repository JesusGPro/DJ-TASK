from django import forms
from .models import WorkLevel, WorkPackage, Work, Measurement
from prices.models import Task
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
        fields = ('name', 'description', 'parent', 'project')

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


class CopyWorkPackageForm(forms.Form):
    source_workpackage = forms.ChoiceField()
    destination_workpackage = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(CopyWorkPackageForm, self).__init__(*args, **kwargs)
        self.fields['source_workpackage'].choices = [(wp.id, wp.name) for wp in WorkPackage.objects.all()]
        self.fields['destination_workpackage'].choices = [(wp.id, wp.name) for wp in WorkPackage.objects.all()]


class CopyWorkForm(forms.Form):
    works_to_copy = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, source_workpackage_id, *args, **kwargs):
        super(CopyWorkForm, self).__init__(*args, **kwargs)
        works = Work.objects.filter(work_package_id=source_workpackage_id)
        self.fields['works_to_copy'].choices = [(w.id, f"{w.task.name} x {w.quantity}") for w in works]