from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection


# Create your views here.
def home(req):
    odata = offer.objects.all().order_by('-id')[0:6]
    cdata = category.objects.all().order_by('-id')[0:6]
    pdata = product.objects.all().order_by('-id')[0:12]
    noofitemsincart=addtocart.objects.all().count()
    print(noofitemsincart)

    return render(req, 'user/index.html', {"offers": odata,"data": cdata, "products": pdata,"noofitemsincart":noofitemsincart})


def about(req):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    return render(req, 'user/about.html',{"noofitemsincart":noofitemsincart})


def contactus(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    status = False
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Message = request.POST.get("msg", "")
        res = contact(name=Name, contact=Mobile, email=Email, message=Message)
        res.save()
        status = True
        # return HttpResponse("<script>alert('Thanks For Enquiry..');window.location.href='/user/contactus/'</script>")
    return render(request, 'user/contactus.html', {'S': status,"noofitemsincart":noofitemsincart})


def services(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    return render(request, 'user/services.html',{"noofitemsincart":noofitemsincart})


def myorders(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    userid=request.session.get('userid')
    oid=request.GET.get('oid')
    orderdata=""
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*, p.* from user_order o,user_product p where o.pid=p.id and o.userid='"+str(userid)+"'")
        orderdata=cursor.fetchall()
        if oid:
            result=order.objects.filter(id=oid,userid=userid)
            result.delete()
            return HttpResponse("<script>alert(Your order has been cancled);window.location.href='/user/orders';</script>")
    else:
        return HttpResponse("<script>alert('Yoy are not login first Login...');window.location.href='/user/signin/'</script>")

    return render(request, 'user/myorders.html',{"pendingorder":orderdata,"noofitemsincart":noofitemsincart})


def myprofile(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    if request.session.get('userid'):
        userid = request.session.get('userid')
        cursor = connection.cursor()
        cursor.execute(
        "select s.* from user_profile s")
        profile = cursor.fetchall()
        return render(request, 'user/myprofile.html',{"profile":profile,"noofitemsincart":noofitemsincart})
    else:
        return HttpResponse(
        "<script>alert('Your are not login');window.location.href='/user/signin/'</script>")


def prod(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    cdata = category.objects.all().order_by('-id')
    x = request.GET.get('abc')

    if x is not None:
        pdata = product.objects.filter(category=x)
    else:
        pdata = product.objects.all().order_by('-id')

    return render(request, 'user/products.html', {"cat": cdata, "products": pdata,"noofitemsincart":noofitemsincart})


def signup(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    status = False
    if request.method == 'POST':
        name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Password = request.POST.get("passwd", "")
        ProfilePhoto = request.FILES['myfile']
        Address = request.POST.get("address", "")
        d = profile.objects.filter(email=Email)
        if d.count() > 0:
            return HttpResponse(
                "<script>alert('You are already registered..');window.location.href='/user/signup/'</script>")
        else:
            res = profile(name=name, mobile=Mobile, email=Email, passwd=Password, myfile=ProfilePhoto,
                          address=Address)
            res.save()
            return HttpResponse(
                "<script>alert('You are registered successfully..');window.location.href='/user/signup/'</script>")
        # return HttpResponse("<script>alert('Thanks For SignUp..');window.location.href='/user/signup/';</script>")
    return render(request, 'user/signup.html',{"noofitemsincart":noofitemsincart})


def signin(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    if request.method == 'POST':

        uname = request.POST.get("uname")
        passwd = request.POST.get("passwd")
        checkuser = profile.objects.filter(email=uname, passwd=passwd)
        if (checkuser):
            request.session['userid'] = uname
            return HttpResponse("<script>alert('Logged In Successfully');window.location.href='/user/myprofile';</script>")

        else:
            return HttpResponse(
                "<script>alert('UserID or Password is Incorrect');window.location.href='/user/signin';</script>")
    return render(request, 'user/signin.html',{"noofitemsincart":noofitemsincart})


def viewdetails(request):
    a = request.GET.get('msg')
    data = product.objects.filter(id=a)
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)

    return render(request, 'user/viewdetails.html', {"d": data,"noofitemsincart":noofitemsincart})


def process(request):
    userid = request.session.get('userid')
    pid = request.GET.get('pid')
    btn = request.GET.get('bn')
    print(userid, pid, btn)
    if userid is not None:
        if btn=='cart':
            checkcartitem=addtocart.objects.filter(pid=pid,userid=userid)
            if checkcartitem.count()==0:
                addtocart(pid=pid, userid=userid, status=True, cdate=datetime.datetime.now()).save()
                return HttpResponse("<script>alert('Your items is successfuly added in cart...');window.location.href='/user/home/'</script>")
            else:
                return HttpResponse("<script>alert('This item is already in the cart...');window.location.href='/user/home/'</script>")
        elif btn=='order':
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your ordered have confirmed..');window.location.href='/user/myorders/'</script>")

        elif btn=='orderfromcart':
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your ordered have confirmed..');window.location.href='/user/myorders/'</script>")
        return render(request,'user/process.html', {"alreadylogin": True})
    else:
        return HttpResponse("<script>window.location.href='/user/signin/'</script>")


def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")


def cart(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    if request.session.get('userid'):
        userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_product p where p.id=c.pid and userid='"+str(userid)+"'")
        cartdata=cursor.fetchall()
        pid=request.GET.get('pid')
        if request.GET.get('pid'):
            res=addtocart.objects.filter(id=pid,userid=userid)
            res.delete()
            return HttpResponse("<script>alert('Your product removeed successfully');window.location.href='/user/cart/'</script>")

    return render(request,'user/cart.html',{"cart":cartdata,"noofitemsincart":noofitemsincart})

def feedback(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    data = feed.objects.all().order_by('name')[0:6]
    status = False
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Message = request.POST.get("msg", "")
        d= feed.objects.filter(email=Email)
        if d.count() > 0:
            return HttpResponse(
                "<script>alert('YOU ALREADY FEEDBACK US...');window.location.href='/user/myprofile/'</script>")
        else:
            res = feed(name=Name, contact=Mobile, email=Email, message=Message)
            res.save()
            return HttpResponse(
                "<script>alert('THANKS FOR FEEDBACK... WE HOPE YOU FEEL VERY WELL WITH US...');window.location.href='/user/myprofile/'</script>")

    return render(request, 'user/feedback.html', {"data":data,"noofitemsincart":noofitemsincart})

def update(request):
    noofitemsincart = addtocart.objects.all().count()
    print(noofitemsincart)
    user=request.session.get('userid')
    pdata=profile.objects.filter(email=user)
    if user:

        if request.method == 'POST':
            name = request.POST.get("name", "")
            Mobile = request.POST.get("mobile", "")
            Password = request.POST.get("passwd", "")
            ProfilePhoto = request.FILES['myfile']
            Address = request.POST.get("address", "")
            profile(email=user,name=name,passwd=Password,mobile=Mobile,myfile=ProfilePhoto,address=Address).save()
            return HttpResponse("<script>alert('Your profile updated succesfully..');window.location.href='/user/myprofile/'</script>")
    return render(request, 'user/update.html',{"profile":pdata,"noofitemsincart":noofitemsincart})