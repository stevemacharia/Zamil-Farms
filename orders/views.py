import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django_renderpdf.views import PDFView
import datetime
from django.shortcuts import render, redirect
from user.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserMobileUpdateForm
from orders.forms import PaymentForm
from .models import Order, OrderDetail
from weasyprint import HTML, CSS
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.shortcuts import render
from user.models import UserProfile
from product.models import Product
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

@login_required
def checkout(request):
    cart = request.session['cart'].items()
    student = User.objects.get(id=request.user.id)
    if UserProfile.objects.filter(user=student):
        if cart:
            if request.method == 'POST':
                u_form = UserUpdateForm(request.POST, instance=request.user)
                su_form = UserMobileUpdateForm(request.POST, instance=request.user.userprofile)
                p_form = PaymentForm()
                if su_form.is_valid() & u_form.is_valid():
                    su_form.save()
                    u_form.save()
                    messages.success(request, f'Your account has been updated!')
                return redirect('checkout')

            else:
                su_form = UserMobileUpdateForm(instance=request.user.userprofile)
                u_form = UserUpdateForm(instance=request.user)
                p_form = PaymentForm()
            student = User.objects.get(id=request.user.id)
            context = {
                'student': student,
                'su_form': su_form,
                'u_form': u_form,
                'p_form': p_form,
            }
            return render(request, 'orders/checkout.html', context)
        else:
            return redirect('checkout')
    else:
        messages.warning(request, f'Kindly create a student account to enroll to a course.!')
        return redirect('profile')


@login_required
def order_add(request):
    payment_options = 'Cash On Delivery'
    global shortcode
    shortcode = str(uuid.uuid4())[:5]
    current_user = request.user
    global userinfo
    userinfo = User.objects.get(username=current_user)
    total_bill = 0.0
    for key, value in request.session['cart'].items():
        total_bill = total_bill + (float(value['price']) * value['quantity'])
    cart_total_amount_b = ("{:.2f}".format(total_bill))

    if not request.session['cart']:
        messages.warning(request, f'Your Shopping cart is empty! Start Shopping.')
        return redirect('checkout')
    else:
        T1 = Order(
            order_name_id=shortcode,
            payment_method=payment_options,
            order_amount=cart_total_amount_b,
            customer_id=current_user,
        )
        T1.save()
        for key, value in request.session['cart'].items():
            Product.objects.filter(id=value['product_id']).exists()
            # new_product_quantity = Product.objects.get(id=value['product_id'])
            # new_product_quantity.product_quantity = F('product_quantity') - value['quantity']
            # new_product_quantity.save()
            T2 = OrderDetail(
                order_name_id=shortcode,
                product_id=value['product_id'],
                product_name=value['name'],
                product_quantity=value['quantity'],
                product_price=value['price'],
            )
            T2.save()


        # cart = Cart(request)
        # cart.clear()
        return redirect('cash_invoice', order_id=shortcode)


def cash_invoice(request, order_id, *args, **kwargs):
    shortcode = order_id
    template_name = get_template('orders/cash_invoice.html')
    OrderModel = Order.objects.get(order_name_id=shortcode)
    user = request.user
    if Order.objects.filter(order_name_id=shortcode).exists():
        context = {
            'customerorder': Order.objects.filter(order_name_id=shortcode),
            'customerorderdetail': OrderDetail.objects.filter(order_name_id=shortcode),
            'user': user,
        }
        rendered_html = template_name.render(context)
        pdf_file = HTML(string=rendered_html).write_pdf()
        ########## Update Orders Model ##############
        OrderModel.invoice_doc = SimpleUploadedFile('MasomoPortal Invoice-' + OrderModel.order_name_id + '.pdf',
                                                    pdf_file,
                                                    content_type='application/pdf')
        OrderModel.save()
        ############################################
        ######################## mail system ####################################
        htmly = get_template('user/email_invoice.html')
        base_dir = settings.MEDIA_ROOT
        d = {
            'username': user,
            'invoice_no': shortcode,
        }
        subject, from_email, to, bcc = 'ZAMIL FARM INVOICE', settings.EMAIL_HOST_USER, user.email, 'info@arieshelby.com'
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to], [bcc])
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file(OrderModel.invoice_doc.path)
        msg.send()
        # ##################################################################
        # return HttpResponse(rendered_html)
        # return render(request, 'orders/cash_invoice.html', context)
        return render(request, 'payments/payment_messages.html', context)



class LabelsView(LoginRequiredMixin, PDFView):
    """Generate labels for some Shipments.

    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'orders/pdf_invoice.html'

    download_name = 'Masomo Portal Invoices' + \
                    str(datetime.datetime.now()) + '.pdf'
    prompt_download = True

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        template_name = 'orders/pdf_invoice.html'
        OrderModel = Order.objects.filter(order_name_id=shortcode)
        context = super().get_context_data(*args, **kwargs)
        context['user'] = userinfo
        context['customerorderdetails'] = OrderDetail.objects.filter(order_name_id=shortcode)
        context['customerorders'] = Order.objects.filter(order_name_id=shortcode)
        rendered_html = template_name.render(context)
        pdf_file = HTML(string=rendered_html).write_pdf(
            stylesheets=[CSS(settings.STATIC_ROOT + 'style.css')])
        OrderModel.invoice_doc = SimpleUploadedFile(pdf_file, content_type='application/pdf')
        OrderModel.save()

        return context





