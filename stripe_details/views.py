from django.shortcuts import render
# from gym.models import User,TrainerProfile
from .models import StripeDetail
from django.contrib.auth.decorators import login_required

import requests
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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

        except IOError as e:
                return e



        # statusChange()
        # # createAvailabeSession()
        # return redirect('gym:client_profile',pk=user_id) #move to pending page
    else: # probably change status to complete
        print('nothing to see here')
        pass

    return render(request, 'stripe_details/stripe_register.html')
