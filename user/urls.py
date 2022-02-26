from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home/',views.home),
    path('about/',views.about),
    path('contactus/',views.contactus),
    path('services/',views.services),
    path('myorders/',views.myorders),
    path('myprofile/',views.myprofile),
    path('products/',views.prod),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('viewdetails/',views.viewdetails),
    path('process/',views.process),
    path('logout/',views.logout),
    path('cart/',views.cart),
    path('feedback/',views.feedback),
    path('update/',views.update),
]