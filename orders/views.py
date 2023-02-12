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

