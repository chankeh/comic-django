from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries import countries

from userena.forms import SignupForm


class SignupFormExtra(SignupForm):
    first_name = forms.CharField(label=_(u'First Name'),
                                 max_length=30,
                                 required=True)
    last_name = forms.CharField(label=_(u'Last Name'),
                                max_length=30,
                                required=True)
    institution = forms.CharField(label=_(u'Institution'),
                                  max_length=100,
                                  required=True,
                                  help_text=_(u'Institution you are affiliated to.'))
    department = forms.CharField(label=_(u'Department'),
                                 max_length=100,
                                 required=True,
                                 help_text=_(u'Department you represent.'))
    country = forms.ChoiceField(label=_(u'Country'),
                                choices=tuple([('00', _('-' * 9))] + list(countries)),
                                required=True)
    website = forms.CharField(label=_(u'Website'),
                              max_length=150,
                              required=False,
                              help_text=_(u'A website which describes you or your department'))


    def __init__(self, *args, **kw):
        super(SignupFormExtra, self).__init__(*args, **kw)

    def clean_country(self):
        """ Make sure the user changed the country field.
        """
        country = self.cleaned_data['country']
        if country == '00':
            raise forms.ValidationError("Please choose a valid country.")
        return country

    def save(self):
        user = super(SignupFormExtra, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        user_profile = user.user_profile
        user_profile.institution = self.cleaned_data['institution']
        user_profile.department = self.cleaned_data['department']
        user_profile.country = self.cleaned_data['country']
        user_profile.save()

        return user
