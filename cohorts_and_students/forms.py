from django import forms
from .models import Cohort, Student

class CohortForm(forms.ModelForm):
    class Meta:
        model = Cohort
        fields = ('cohort_name', 'start_date', 'end_date')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('cohort', 'first_name', 'last_name')