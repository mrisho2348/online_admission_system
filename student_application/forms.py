from django import forms

from student_application.models import   SessionYearModel,EducationLevel


class DateInput(forms.DateInput):
    input_type = "date"

class AddSubjectForm(forms.Form):
    subject_name = forms.CharField(
        label='Subject Name',
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    school_level = forms.ModelChoiceField(
        label='School Level',
        queryset=EducationLevel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
 
class AddSessionYearForm(forms.Form):
    session_start = forms.DateField(label='Session start year',widget = forms.DateInput(attrs={"class":"form-control","placeholder":"Enter session start year","type":"date"}))
    session_end = forms.DateField(label='Session end year',widget = forms.DateInput(attrs={"class":"form-control","placeholder":"Enter session end year","type":"date"}))
    

  