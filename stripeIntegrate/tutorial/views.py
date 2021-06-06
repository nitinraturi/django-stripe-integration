import stripe
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

#home view
def home(request):
    return render(request,'checkout.html')

#success view
def success(request):
    return render(request,'success.html')
    
#cancel view
def cancel(request):
    return render(request,'cancel.html')

@csrf_exempt
def create_checkout_session(request):
    order=Order(email=" ",paid="False",amount=0,description=" ")
    order.save()
    session = stripe.checkout.Session.create(
    client_reference_id=request.user.id if request.user.is_authenticated else None,
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'inr',
        'product_data': {
          'name': 'Intro to Django Course',
        },
        'unit_amount': 10000,
      },
      'quantity': 1,
    }],
    metadata={
        "order_id":order.id
    },
    mode='payment',
    success_url=YOUR_DOMAIN + '/success.html',
    cancel_url=YOUR_DOMAIN + '/cancel.html',
    )
    print(session)
    #ID=order.id
    #order= Order.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)
    #order.save()
    return JsonResponse({'id': session.id})

@csrf_exempt
def webhook(request):
    print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
         #creating order
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] /100
        sessionID = session["id"]
        ID=session["metadata"]["order_id"]
        Order.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)

    return HttpResponse(status=200)
