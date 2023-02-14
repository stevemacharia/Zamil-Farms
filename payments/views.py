import json
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from product.models import Product
from django.contrib import messages
from django_pesapal.views import PaymentRequestMixin
from django.views.generic import TemplateView
from orders.models import CustomerOrder, CustomerOrderDetails
from django_pesapal.models import Transaction
from django.db.models import F
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from cart.cart import Cart


class PaymentView(TemplateView, PaymentRequestMixin):
    template_name = "payments/pesapal.html"
    def get_context_data(self,  **kwargs):
        global shortcode
        shortcode = str(uuid.uuid4())[:5]
        current_user = self.request.user
        global userinfo
        userinfo = User.objects.get(username=current_user)
        total_bill = 0.0
        payment_options = "UNDEFINED"
        for key, value in self.request.session['cart'].items():
            total_bill = total_bill + (float(value['price']) * value['quantity'])
        cart_total_amount_b = ("{:.2f}".format(total_bill))

        if StudentProfile.objects.filter(user=current_user).exists():
            UserDetail = UserProfile.objects.get(user=current_user)
            if not self.request.session['cart']:
                messages.warning(self.request, f'Your Shopping cart is empty! Start Shopping.')
                return redirect('checkout')
            else:
                T1 = Order(
                    order_name_id=shortcode,
                    payment_method=payment_options,
                    order_amount=cart_total_amount_b,
                    customer_id=current_user,
                )
                T1.save()
                for key, value in self.request.session['cart'].items():
                    if Product.objects.filter(id=value['product_id']).exists():
                        EnrolledCourse = Product.objects.get(id=value['product_id'])
                        if Course.objects.get(product=EnrolledCourse):
                            NewCourse = Course.objects.get(product=EnrolledCourse)
                            NewCourse.students.add(User.objects.get(id=self.request.user.id))
                        else:
                            messages.warning(self.request, f'Failed to Enroll to course')
                            return redirect('checkout')
                        T2 = OrderDetail(
                            order_name_id=shortcode,
                            product_id=value['product_id'],
                            product_name=value['name'],
                            product_price=value['price'],
                        )
                        T2.save()
                    else:
                        T2 = OrderDetail(
                            order_name_id=shortcode,
                            product_id=value['product_id'],
                            product_name=value['name'],
                            product_price=value['price'],
                        )
                        T2.save()
                # cart = Cart(request)
                # cart.clear()
        cart_total_amount_b = 1
        ctx = super(PaymentView, self).get_context_data(**kwargs)
        order_info = {
            "id": shortcode,
            "amount": cart_total_amount_b,
            "description": "Payment for X",
            "reference": shortcode,
            "phone_number": "0711253491",
            "email_address": userinfo.email,
        }

        ctx["pesapal_url"] = self.get_payment_url(**order_info)
        return ctx


def payment_option(request):
    return render(request, 'payments/payment_option.html')


def payment_confirmation(request):
    order_id = request.GET.get('pesapal_merchant_reference')
    merchant_info = request.GET.get('pesapal_merchant_reference')
    payment_status_completed = 1
    payment_status_pending = 0
    # if Transaction.objects.filter(merchant_reference=order_id):
    if Transaction.objects.filter(merchant_reference=order_id, payment_status=payment_status_completed):
        shortcode = order_id
        template_name = get_template('orders/paid_invoice.html')
        OrderModel = CustomerOrder.objects.get(order_name_id=shortcode)
        user = request.user
        ###########Update payment method on orders model########
        current_transaction = Transaction.objects.get(merchant_reference=order_id,
                                                      payment_status=payment_status_completed)
        pesapal_payment_method = current_transaction.payment_method
        OrderModel.payment_method = pesapal_payment_method
        OrderModel.save()
        ##########################
        if CustomerOrder.objects.filter(order_name_id=shortcode).exists():
            context = {
                'customerorder': CustomerOrder.objects.filter(order_name_id=shortcode),
                'customerorderdetail': CustomerOrderDetails.objects.filter(order_name_id=shortcode),
                'user': user,
            }
            rendered_html = template_name.render(context)
            pdf_file = HTML(string=rendered_html).write_pdf()

            ########## Update Orders Model ##############
            OrderModel.invoice_doc = SimpleUploadedFile('Alexadashcams Invoice-' + OrderModel.order_name_id + '.pdf',
                                                        pdf_file,
                                                        content_type='application/pdf')
            OrderModel.save()
            # ##############################
            ######################## mail system ####################################
            htmly = get_template('users/email_invoice.html')
            base_dir = settings.MEDIA_ROOT
            d = {
                'username': user,
                'invoice_no': shortcode,
            }
            subject, from_email, to, bcc = 'ALEXADASHCAMS INVOICE', settings.EMAIL_HOST_USER, user.email, 'info@arieshelby.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to], [bcc])
            msg.attach_alternative(html_content, "text/html")
            msg.attach_file(OrderModel.invoice_doc.path)
            msg.send()
            # ##################################################################
            # return HttpResponse(rendered_html)
        context = {
            'transaction_messages': payment_status_completed,
        }
        return render(request, 'payments/payment_messages.html', context)
    elif Transaction.objects.filter(merchant_reference=order_id, payment_status=payment_status_pending):
        messages.warning(request, f'Payment transaction failed, Kindly tray again.')
        return redirect('payment_option')
        # return render(request, 'orders/checkout.html', context)
    else:
        return redirect('transaction_completed')


def payment_failed(request):
    return render(request, 'payments/payment_failed.html')
