from django import forms

class CategoryForm(forms.Form):
    CATEGORY_CHOICES = (
    ("student", "I’m a Student"),
    ("teacher", "I’m a Teacher"),
    )
    category = forms.ChoiceField(
    choices=CATEGORY_CHOICES,
    widget=forms.RadioSelect,
    label="Select who you are"
    )