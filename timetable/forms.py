from django import forms

class CourseForm(forms.Form):
	course_code = forms.CharField(max_length=8)