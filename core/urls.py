from django.urls import path
from . import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),
    path('profile/', core_views.profile, name='profile'),
    path('product-detail/<slug>/', core_views.product_detail, name='product-detail'),
    path('recipe-detail/<slug>/', core_views.recipe_detail, name='recipe-detail'),
    path('blog-detail/<slug>/', core_views.blog_detail, name='blog-detail'),

    path('add-to-cart/<slug>/', core_views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', core_views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', core_views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('order-summary/', core_views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', core_views.CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', core_views.AddCouponView.as_view(), name='add-coupon'),
    path('subscribe_newsletter/', core_views.subscribe_newsletter, name='subscribe_newsletter'),
    path('contact_us/', core_views.contact_us, name='contact_us'),
    path('distribution_form/', core_views.distribution_form, name='distribution_form'),
    path('download-brochure', core_views.download_brochure, name='download-brochure')
]