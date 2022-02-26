from django.contrib import admin

# Register your models here.
from .models import *

class contactAdmin(admin.ModelAdmin):
    list_display=("name","contact","email","message")
admin.site.register(contact,contactAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display=('id',"cname","cpic","cdate",)
admin.site.register(category,categoryAdmin)

class profileAdmin(admin.ModelAdmin):
    list_display=("name","mobile","email","passwd","address","myfile")
admin.site.register(profile,profileAdmin)

class productAdmin(admin.ModelAdmin):
    list_display=('id',"name","ppic","color","tprice","disprice","pdes","category","pdate")
admin.site.register(product,productAdmin)

class offerAdmin(admin.ModelAdmin):
    list_display=('id',"name","ppic","pdate")
admin.site.register(offer,offerAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display=('id',"pid","userid","remarks","status","odate")
admin.site.register(order,orderAdmin)

class addtocartAdmin(admin.ModelAdmin):
    list_display=('id',"pid","userid","status","cdate")
admin.site.register(addtocart,addtocartAdmin)

class feedAdmin(admin.ModelAdmin):
    list_display=("name","contact","email","message")
admin.site.register(feed,feedAdmin)