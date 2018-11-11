from django import forms
from .models import Individual, Company, ExternalAccount


class IndividualForm(forms.ModelForm):

    class Meta:
        model = Individual
        fields = ('legal_entity_dob_day','legal_entity_dob_month','legal_entity_dob_year','legal_entity_first_name',
                    'legal_entity_last_name','legal_entity_address_line1','legal_entity_address_city','legal_entity_address_postal_code')




class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('legal_entity_first_name','legal_entity_last_name','legal_entity_dob_day','legal_entity_dob_month','legal_entity_dob_year','legal_entity_business_name','legal_entity_address_line1','legal_entity_address_city','legal_entity_address_postal_code',
                    'legal_entity_type_business_tax_id','legal_entity_personal_address_line1','legal_entity_personal_address_city','legal_entity_personal_address_postal_code')
