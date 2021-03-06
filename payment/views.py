from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
#from zeep import Client
from orders.models import Order
from .tasks import payment_coplated

MERCHANT = ''
client = '' # Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = ''  # Optional
mobile = ''  # Optional
CallbackURL = 'http://127.0.0.1:8000/payment/verify/' # Important: need to edit for realy server.

def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        request.session.modified = True
    # result = client.service.PaymentRequest(MERCHANT, order.final_price, description, order.email, order.phone, CallbackURL)
    # if result.Status == 100:
    #     return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    # else:
    #     return HttpResponse('Error code: ' + str(result.Status))
    return HttpResponse('Error code')

def verify(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            message = 'Transaction success.\nRefID: ' + str(result.RefID)
        elif result.Status == 101:
            message = 'Transaction submitted : ' + str(result.Status)
        else:
            message = 'Transaction failed.\nStatus: ' + str(result.Status)
    else:
        message = 'Transaction failed or canceled by user'
        """ order.paid = True
        order.transaction_id = ""
        order.save(update_fields=['paid', 'transaction_id']) """
        # lounch asynchronous task
        payment_coplated.delay(order.id)
    return render(request, 'payment/verify.html', {"message":message})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')