from django.shortcuts import render, redirect
# from gym.models import User,TrainerProfile
from .models import StripeDetail, Individual
from .forms import IndividualForm
from django.contrib.auth.decorators import login_required

import requests
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



# @login_required
# def stripe_register(request):
#     # get stripe id public and secret key
#     if (request.GET.get('stripe_register')):
#         user_id = request.user.id
#         import time
#         def createStripeAcct():
#             acct = stripe.Account.create(
#                 country="GB",
#                 type="custom"
#                 )
#             # print(acct.items)
#             # acct_id = acct.id
#             # print(acct.id)
#             # acct.legal_entity.dob.day = 8
#             # acct.legal_entity.dob.month = 7
#             # acct.legal_entity.dob.year = 1992
#             acct_keys = acct.items
#             # print(acct.items())
#             for x, y in acct_keys():
#                 print(x,y)
#             #     if x == 'keys':
#             #         pub = y['publishable']
#             #         sec = y['secret']
#             return
#
#     createStripeAcct()
#     # acct = stripe.Account.retrieve('acct_1DUJvLAO3xaCPEYY')
#     # print(acct)





@login_required
def stripe_register(request):
    # get stripe id public and secret key
    if (request.GET.get('stripe_register')):
        user_id = request.user.id

        def createStripeAcct():
            acct = stripe.Account.create(
                country="GB",
                type="custom"
                )
            acct_id = acct.id
            acct_keys = acct.items
            for x, y in acct_keys():
                if x == 'keys':
                    pub = y['publishable']
                    sec = y['secret']
            return acct_id, pub, sec


        stripe_deets = createStripeAcct()
        # print(stripe_deets)


        try:
            stripe_details = StripeDetail.objects.create(
                user = request.user,
                name = request.user.trainerprofile.name,
                stripe_id = stripe_deets[0],
                stripe_pub_key = stripe_deets[1],
                stripe_secret_key = stripe_deets[2],
            )
            stripe_details.save()
            return redirect('stripe:stripe_individual')

        except IOError as e:
                return e



        # statusChange()
        # # createAvailabeSession()
        # return redirect('gym:client_profile',pk=user_id) #move to pending page
    else: # probably change status to complete

        print('nothing to see here')
        pass


    return render(request, 'stripe_details/stripe_register.html')



@login_required
def stripe_individual(request):
    user_id = request.user.id

    # make this a global variable
    stripe_detail = StripeDetail.objects.get(user=user_id)

    # to get the users stripe account id
    stripe_account = stripe_detail.stripe_id

    # function to send verification data to stripe
    def send_to_stripe(stripe_detail):
        individual = Individual.objects.get(stripe_detail=stripe_detail)

        import time
        acct = stripe.Account.retrieve(stripe_account)

        acct.legal_entity.address.city = individual.legal_entity_address_city
        acct.legal_entity.address.line1 = individual.legal_entity_address_line1
        acct.legal_entity.address.postal_code = individual.legal_entity_address_postal_code
        acct.legal_entity.dob.day = individual.legal_entity_dob_day
        acct.legal_entity.dob.month = individual.legal_entity_dob_month
        acct.legal_entity.dob.year = individual.legal_entity_dob_year
        acct.legal_entity.first_name = individual.legal_entity_first_name
        acct.legal_entity.last_name = individual.legal_entity_last_name
        acct.legal_entity.type = 'individual'

        acct.tos_acceptance.date = int(time.time())
        acct.tos_acceptance.ip = '8.8.8.8' #TO BE REWORKED
        acct.save()
        print(acct)



# legal_entity_address_city = models.CharField(max_length=100,blank=False)
# legal_entity_address_line1 = models.CharField(max_length=100,blank=False)
# legal_entity_address_postal_code = models.CharField(max_length=100,blank=False)
# legal_entity_dob_day = models.PositiveIntegerField(blank=False)
# legal_entity_dob_month = models.PositiveIntegerField(blank=False)
# legal_entity_dob_year = models.PositiveIntegerField(blank=False)
# legal_entity_first_name = models.CharField(max_length=100,blank=False)
# legal_entity_last_name = models.CharField(max_length=100,blank=False)
# tos_acceptance_date = models.DateTimeField(auto_now_add=True)
# tos_acceptance_ip = models.CharField(max_length=100,blank=False)




    if request.method == 'POST':
        form = IndividualForm(request.POST)

        if form.is_valid():
            individual = form.save()
            individual.stripe_detail = stripe_detail
            individual.save()

            send_to_stripe(stripe_detail)

            return redirect('/')
    else:
        form = IndividualForm()

    context = {'form': form}
    return render(request,'stripe_details/stripe_individual.html', context)
