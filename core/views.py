from django.shortcuts import render
from . import models as core_models
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, View
from .models import Order, OrderItem, Address
from .forms import CheckoutForm, CouponForm
from . import forms as core_forms
from django.shortcuts import render
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
import os
import mimetypes




# For mails
from django.conf import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
SENDER_EMAIL = settings.EMAIL_HOST_USER
# For mails

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

# Create your views here.
def home(request):
    category = request.GET.get('category')
    if category:
        all_items = core_models.Item.objects.filter(category=category)
    else:
        all_items = core_models.Item.objects.all()
    all_items_p = Paginator(all_items, 20)
    page = request.GET.get('page')
    all_items = all_items_p.get_page(page)
    context = {
        'all_items': all_items,
        'all_recipes': core_models.Recipes.objects.all(),
        'all_blogs': core_models.Blog.objects.all(),
        'all_categories': core_models.Category.objects.all(),
        'all_carausels': core_models.Carausel.objects.all(),
        'all_testimonials': core_models.Testimonial.objects.all(),
    }
    return render(request, 'store/home.html', context)

def product_detail(request, slug):
    item = core_models.Item.objects.get(slug=slug)
    key_ingredients = item.key_ingredients
    if key_ingredients:
        ingredients = key_ingredients.split(',')
    else:
        ingredients = ['No Ingredients']
    context = {
        'title': "Product detail",
        'object': item,
        'ingredients': ingredients,
        'images': range(item.number_of_images)
    }
    return render(request, 'store/product-detail.html', context)



def profile(request):
    return render(request, 'store/index.html')

def terms_and_conditions(request):
    return render(request, 'store/terms_and_conditions.html')

def about_us(request):
    return render(request, 'store/about_us.html')

def privacy(request):
    return render(request, 'store/privacy.html')

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = core_models.Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'title': "Order Summary"
            }
            return render(self.request, 'store/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required(login_url='/accounts/login/')
def add_to_cart(request, slug):
    item = get_object_or_404(core_models.Item, slug=slug)
    order_item, created = core_models.OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = core_models.Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated in your cart.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("product-detail", slug=slug)
    else:
        order = core_models.Order.objects.create(
            user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("product-detail", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(core_models.Item, slug=slug)
    order_qs = core_models.Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = core_models.OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("product-detail", slug=slug)
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("product-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product-detail", slug=slug)
    

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(core_models.Item, slug=slug)
    order_qs = core_models.Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = core_models.OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product-detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product-detail", slug=slug)

def get_coupon(request, code):
    try:
        coupon = core_models.Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            if self.request.GET.get('q'):
                search = self.request.GET.get('q')
                return redirect('/search-result/' + search)
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
                'title': 'Checkout',
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "store/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(form.errors)
            if form.is_valid():

                order.email = form.cleaned_data.get('email')
                order.firstname = form.cleaned_data.get('firstname')
                order.lastname = form.cleaned_data.get('lastname')
                order.phone_number = form.cleaned_data.get('phone_number')
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    scity = form.cleaned_data.get(
                        'scity')
                    sdistrict = form.cleaned_data.get(
                        'sdistrict')
                    sstate = form.cleaned_data.get(
                        'sstate')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            city = scity,
                            district = sdistrict,
                            state = sstate,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    bcity = form.cleaned_data.get(
                        'bcity')
                    bdistrict = form.cleaned_data.get(
                        'bdistrict')
                    bstate = form.cleaned_data.get(
                        'bstate')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            city = bcity,
                            district = bdistrict,
                            state = bstate,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = 'R'

                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                elif payment_option == 'R':
                    return redirect('/payment')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout')
            else:
                messages.warning(self.request, "Invalid Form!")
                return redirect("checkout")
            messages.warning(self.request, "some error occured")
            return redirect("checkout")
        except:
            messages.warning(self.request, "You do not haverstjhrh an active order")
            return redirect("order-summary")


def subscribe_newsletter(request):
    new_subscriber = core_models.Newsletter()
    new_subscriber.email = request.POST.get('subscriber_email')
    new_subscriber.save()
    messages.info(request, "You have successfully subscribed to our newsletter!")
    return redirect("home")

def send_mail_contact_message(message):
    context = {
        "message": message
    }
    html_content = render_to_string("mails/contact_mail.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "New Message",
        text_content,
        SENDER_EMAIL,
        ['priyanshusingh1998@gmail.com', 'sales@foodsense.store']
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def contact_us(request):
    new_message = core_models.ContactMessage()
    new_message.name = request.POST.get('name')
    new_message.email = request.POST.get('email')
    new_message.subject = request.POST.get('subject')
    new_message.message = request.POST.get('message')
    new_message.save()
    send_mail_contact_message(new_message)
    messages.info(request, "We have recieved your message. Thanks for reaching out to us!")
    return redirect("home")

def send_mail_for_distribution_request(dist_form):
    context = {
        "object": dist_form
    }
    html_content = render_to_string("mails/distribution_form_mail.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "New Destribution Request",
        text_content,
        SENDER_EMAIL,
        ['priyanshusingh1998@gmail.com', 'sales@foodsense.store']
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def distribution_form(request):
    new_destribution_form = core_models.DestributionForm()
    new_destribution_form.name = request.POST.get('name')
    new_destribution_form.email = request.POST.get('email')
    new_destribution_form.contact_number = request.POST.get('contact_number')
    new_destribution_form.description = request.POST.get('description')
    new_destribution_form.save()
    send_mail_for_distribution_request(new_destribution_form)
    messages.info(request, "We have recieved your request. Thanks for reaching out to us!")
    return redirect("home")

def blog_detail(request, slug):
    if request.method=='GET':
        curr_blog = core_models.Blog.objects.get(slug=slug)
        context = {
            'object': curr_blog,
            'title': curr_blog.title,
            'EditBlogForm': core_forms.AddBlogForm(instance=curr_blog)
        }
        return render(request, 'store/blog-detail.html', context)
    
    if request.method=='POST':
        curr_blog = core_models.Blog.objects.get(slug=slug)
        edit_blog_form = core_forms.AddBlogForm(request.POST, request.FILES, instance=curr_blog)
        if edit_blog_form.is_valid():
            the_blog = edit_blog_form.save(commit=False)
            print(the_blog.slug, the_blog.content)
            the_blog.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('blog-detail', slug=slug)

def recipe_detail(request, slug):
    if request.method=='GET':
        curr_recipe = core_models.Recipes.objects.get(slug=slug)
        context = {
            'object': curr_recipe,
            'title': curr_recipe.title,
            'EditRecipeForm': core_forms.AddRecipeForm(instance=curr_recipe)
        }
        return render(request, 'store/recipe-detail.html', context)
    
    if request.method=='POST':
        curr_recipe = core_models.Recipes.objects.get(slug=slug)
        edit_recipe_form = core_forms.AddRecipeForm(request.POST, request.FILES, instance=curr_recipe)
        if edit_recipe_form.is_valid():
            edit_recipe_form.save()
            messages.success(request, 'Recipe Updated successfully')
            return redirect('recipe-detail', slug=slug)

def download_brochure(request):
    filename = os.path.join(settings.BASE_DIR, 'static/foodsense_brochure.pdf')
    path = open(filename, 'rb')
    mime_type, _ = mimetypes.guess_type(filename)
    # content = FileWrapper(open(filename))
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Foodsense-Brochure.pdf'
    return response


