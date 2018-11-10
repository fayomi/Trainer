from django.db import models
from gym.models import User

# Create your models here.
class StripeDetail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100,null=True)
    stripe_id = models.CharField(max_length=200,null=True)
    stripe_pub_key = models.CharField(max_length=200,null=True)
    stripe_secret_key = models.CharField(max_length=200,null=True)
    legal_entity_type = models.CharField(max_length=100,null=True)

    class Meta:
        db_table = 'StripeDetail'

class Individual(models.Model):
    stripe_detail = models.ForeignKey(StripeDetail,on_delete=models.CASCADE, null=True)
    legal_entity_address_city = models.CharField(max_length=100,blank=False)
    legal_entity_address_line1 = models.CharField(max_length=100,blank=False)
    legal_entity_address_postal_code = models.CharField(max_length=100,blank=False)
    legal_entity_dob_day = models.PositiveIntegerField(blank=False)
    legal_entity_dob_month = models.PositiveIntegerField(blank=False)
    legal_entity_dob_year = models.PositiveIntegerField(blank=False)
    legal_entity_first_name = models.CharField(max_length=100,blank=False)
    legal_entity_last_name = models.CharField(max_length=100,blank=False)
    tos_acceptance_date = models.DateTimeField(auto_now_add=True)
    tos_acceptance_ip = models.CharField(max_length=100,blank=False)

    class Meta:
        db_table = 'StripeIndividual'


class Company(models.Model):
    stripe_detail = models.ForeignKey(StripeDetail,on_delete=models.CASCADE, null=True)
    legal_entity_address_city = models.CharField(max_length=100,blank=False)
    legal_entity_address_line1 = models.CharField(max_length=100,blank=False)
    legal_entity_address_postal_code = models.CharField(max_length=100,blank=False)
    legal_entity_business_name = models.CharField(max_length=200,blank=False)
    legal_entity_typebusiness_tax_id = models.CharField(max_length=200,blank=False)
    companies_house_registration_number_CRN = models.CharField(max_length=200,blank=False)
    legal_entity_personal_address_city = models.CharField(max_length=100,blank=False)
    legal_entity_personal_address_line1 = models.CharField(max_length=100,blank=False)
    legal_entity_personal_address_postal_code = models.CharField(max_length=100,blank=False)
    tos_acceptance_date = models.DateTimeField(auto_now_add=True)
    tos_acceptance_ip = models.CharField(max_length=100,blank=False)

    class Meta:
        db_table = 'StripeCompany'


class ExternalAccount(models.Model):
    stripe_detail = models.ForeignKey(StripeDetail,on_delete=models.CASCADE, null=True)
    external_account_new_id = models.CharField(max_length=200)
    name = models.CharField(max_length=100,null=True)
    object = models.CharField(max_length=100,blank=False) #Should be bank_account.
    country = models.CharField(max_length=100,blank=False) #Should be GB
    currency = models.CharField(max_length=100,blank=False) #Should be gbp
    account_holder_name = models.CharField(max_length=100,blank=False)
    account_holder_type = models.CharField(max_length=100,blank=False) #The type of entity that holds the account.
    routing_number = models.CharField(max_length=100,blank=False) #SORT CODE
    account_number = models.CharField(max_length=100,blank=False) #ACCOUNT NUMBER

    class Meta:
        db_table = 'StripeExternalAccount'




#test







# "external_account",
