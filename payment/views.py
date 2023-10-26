import json
import requests
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.conf import settings
from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    response = requests.post(
        'https://api.zarinpal.com/pg/v4/payment/request.json',
        headers=request_header,
        data=json.dumps(request_data),
    )

    data = response.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == "OK":
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority
        }

        response = requests.post(
            'https://api.zarinpal.com/pg/v4/payment/verify.json',
            headers=request_header,
            data=json.dumps(request_data),
        )

        if 'data' in response.json():
            data = response.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_text = data
                order.save()
                return HttpResponse('پرداخت با موفقیت انجام شد.')

            elif payment_code == 101:
                return HttpResponse('این تراکنش قبلا ثبت شده است.')

            else:
                error_code = response.json()['data']['errors']['code']
                error_message = response.json()['data']['errors']['message']
                return HttpResponse(f' پرداخت ناموفق بود.{error_code} {error_message}')

    else:
        return HttpResponse(f' پرداخت ناموفق بود')
