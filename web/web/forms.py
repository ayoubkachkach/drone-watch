from django import forms
from web.models import LabelPost


class HomeForm(forms.ModelForm):
    urls = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = LabelPost
        fields = ('urls',)

    def __init__(self, *args, **kwargs):
        super(HomeForm,
              self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['urls'].widget.attrs['cols'] = 100
        self.fields['urls'].widget.attrs['rows'] = 50
