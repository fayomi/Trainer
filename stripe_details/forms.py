from django import forms
from .models import Individual, Company, ExternalAccount


class IndividualForm(forms.ModelForm):

    class Meta:
        model = Individual
        fields = ('legal_entity_dob_day','legal_entity_dob_month','legal_entity_dob_year','legal_entity_first_name',
                    'legal_entity_last_name','legal_entity_address_line1','legal_entity_address_city','legal_entity_address_postal_code')
