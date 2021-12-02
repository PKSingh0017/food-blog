from django.urls import path
from . import views as front_views

urlpatterns = [
    path('edit_hero/', front_views.edit_hero, name='edit_hero'),
    path('edit_SocialMedia/', front_views.edit_SocialMedia, name='edit_SocialMedia'),
    path('edit_Contact/', front_views.edit_Contact, name='edit_Contact'),
    path('edit_Newsletter/', front_views.edit_Newsletter, name='edit_Newsletter'),
    path('docs/<doc_name>/', front_views.docs, name='docs'),
    path('edit_docs/<doc_name>/', front_views.edit_docs, name='edit_docs'),
]