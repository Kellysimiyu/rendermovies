from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=120,
                        widget=forms.TextInput(attrs={"placeholder": "Search movies…"}))
