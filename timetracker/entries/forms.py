from django import forms
from django.utils import timezone

from .models import Project, Client, Entry


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'client')

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('start', 'stop', 'project', 'description')
        help_texts = {
        'start': 'Format: 2006-10-25 14:30',
        'stop': 'Format: 2006-10-25 14:30'
        }

    def save(self, commit=True):
        entry = super(EntryForm, self).save(commit=False)

        if commit:
            entry.save()

        return entry

    def clean_start(self):
        """
        Validation for start field
        """
        start = self.cleaned_data['start']
        if start >= timezone.now():
            raise forms.ValidationError('Start time must be in the past')

        # Must return the value, regardless of whether we changed it or not
        return start

    def clean(self):
        """
        This method handles the validation of the form overall and is useful for
        handling scenarios like when a field relies on another field
        """
        # Call parent's clean method to ensure any validation logic in parent class
        # is preserved
        cleaned_data = super(EntryForm, self).clean()

        # Get the start and stop values from the cleaned_data dictionary, or None
        # if the dictionary keys are missing
        start = cleaned_data.get('start', None)
        stop = cleaned_data.get('stop', None)
        if 'create_endnow' in self.data:
            stop = timezone.now()
            cleaned_data['stop'] = stop

        if stop and start and (stop < start):
            raise forms.ValidationError('End time must come after start time')

        return cleaned_data
