import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Posts,Follow,Like
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.core.serializers import serialize

def index(request):
    list_for_like=[]
    all_post=Posts.objects.all()
    all_post = all_post.order_by("-timestamp").all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_post, 10)
    try:
        users = paginator.page(page)
        time.sleep(1)
    except PageNotAnInteger:
        users = paginator.page(0.5)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        x=request.user
        try:
            new=Like.objects.get(liker=x)
        except Like.DoesNotExist:
            new=Like.objects.create(liker=x)
            new.save()
        fonka=new.liked.iterator()
        for f in fonka:
            list_for_like.append(f)
        return render(request, "network/index.html",{"Posts":users,"user":x,"list":list_for_like})
    return render(request, "network/index.html",{"Posts":users,})
@login_required
def create(request):
    if request.method == "POST":
        new_post=Posts.objects.create(owner=request.user,text=request.POST["value"])
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
@csrf_exempt
def profile(request,namee):
    if request.method == 'GET': 
        list_for_like=[]
        a=User.objects.get(username= namee)
        b=a.id
        x=request.user
        current_post=Posts.objects.filter(owner = b)
        current_post = current_post.order_by("-timestamp").all()
        page = request.GET.get('page', 1)
        paginator = Paginator(current_post, 10)
        try:
            users = paginator.page(page)
            time.sleep(1)
        except PageNotAnInteger:
            users = paginator.page(0.5)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        # For current user follower and following numbers
        list_for_followers=[]
        list_for_following=[]
        try:
            want=Follow.objects.get(name = a)
        except Follow.DoesNotExist:
            want = Follow.objects.create(name= a)    
            want.save()     
        f_r=want.followers.iterator()
        f_ing=want.following.iterator()
        for c in f_r:
            list_for_followers.append(c)
        for y in f_ing:
            list_for_following.append(y)
        unfollow=''    
        if x in list_for_followers:
            unfollow='active'
        #like button list
        try:
            new=Like.objects.get(liker=request.user)
        except Like.DoesNotExist:
            new=Like.objects.create(liker=request.user)
            new.save()
        fonka=new.liked.iterator()
        for f in fonka:
            list_for_like.append(f)
        return render(request, "network/profile_page.html",{"list":list_for_like,"unfollow":unfollow,"name":namee,"curr_post":users,"username":request.user, "following":len(list_for_following),"followers":len(list_for_followers)})
def following(request):
    list_for_like=[]
    x=request.user
    all_names=[]
    try:
        want=Follow.objects.get(name = x)
    except Follow.DoesNotExist:
        want = Follow.objects.create(name= x)    
        want.save()     
    f_ing=want.following.iterator()
    list_for_curr_post=[]
    new_list=[]
    for y in f_ing:
        all_names.append(y)
        list_for_curr_post.append(Posts.objects.filter(owner = y))
    for a in list_for_curr_post:
        a=a.order_by("-timestamp").all()
        for b in a:
            new_list.append(b)
    page = request.GET.get('page', 1)
    paginator = Paginator(new_list , 10)
    try:
        users = paginator.page(page)
        time.sleep(1)
    except PageNotAnInteger:
        users = paginator.page(0.5)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    try:
        new=Like.objects.get(liker=request.user)
    except Like.DoesNotExist:
        new=Like.objects.create(liker=request.user)
        new.save()
    fonka=new.liked.iterator()
    for f in fonka:
        list_for_like.append(f)
    return render(request, "network/following.html",{"list":list_for_like,"names":all_names,"curr_post":users})
@csrf_exempt
def edit(request,x):
    if request.method =='PUT':
        a=Posts.objects.get(pk=x)
        data = json.loads(request.body)
        x=data["text"]
        a.text=x
        a.save()
        return HttpResponse(status=204)
@csrf_exempt
def like(request,y):
    if request.method =='PUT':
        a=Posts.objects.get(pk=y)
        x=request.user
        try:
            new=Like.objects.get(liker=x)
            new.liked.add(a)
            new.save()
        except Like.DoesNotExist:
            new1=Like.objects.create(liker=x)
            new1.liked.add(a)
            new1.save()     
        a.like+=1
        a.save()
        return HttpResponse(status=204)

@csrf_exempt
def unlike(request,y):
    if request.method =='PUT':
        a=Posts.objects.get(pk=y)
        x=request.user
        new=Like.objects.get(liker=x)
        new.liked.remove(a)
        new.save()
        a.like-=1
        a.save()
        return HttpResponse(status=204)
@csrf_exempt
def follow(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        name=data["curr_name"]
        a=User.objects.get(username = name)
        b=a.id
        c=User.objects.get(username= request.user)
        d=c.id
        try:
            followie=Follow.objects.get(name = b)
        except Follow.DoesNotExist:
            followie = Follow.objects.create(name= b)    
            followie.save()     
        try:
            follower=Follow.objects.get(name= d)
        except Follow.DoesNotExist:
            follower = Follow.objects.create(name= d)    
            follower.save()
    
        followie.followers.add(request.user)
        follower.following.add(a)
        followie.save()
        follower.save()
        return HttpResponse(status=204)
@csrf_exempt
def unfollow(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        name=data["curr_name"]
        a=User.objects.get(username = name)
        b=a.id
        c=User.objects.get(username= request.user)
        d=c.id
        followie=Follow.objects.get(name = b)
        follower=Follow.objects.get(name= d)    
        followie.followers.remove(request.user)
        follower.following.remove(a)
        followie.save()
        follower.save()
        return HttpResponse(status=204)
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
