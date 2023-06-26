from django.urls import path
from . import views

urlpatterns = [
     path('add_product/', views.add_product, name='add_product'),
     path('edit_product/<int:product_id>/', views.edit_product,
          name='edit_product'),
     path('delete_product/<int:product_id>/', views.delete_product,
          name='delete_product'),
     path('add_comment/<int:product_id>/', views.add_comment,
          name='add_comment'),
     path('view_comments/', views.view_comments, name='view_comments'),
     path('approve_comment/<int:comment_id>/', views.approve_comment,
          name='approve_comment'),
     path('delete_comment/<int:comment_id>/', views.delete_comment,
          name='delete_comment'),
     path('contact_us/', views.contact_us, name='contact_us'),
     path('store_inbox/', views.store_inbox, name='store_inbox'),
     path('delete_message/<int:message_id>/', views.delete_message,
          name='delete_message'),
     path('newsletter/', views.newsletter, name='newsletter'),
     path('view_newsletter/', views.view_newsletter, name='view_newsletter'),
     path('delete_subscriber/<int:email_id>/', views.delete_subscriber,
          name='delete_subscriber'),
]
