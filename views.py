from ast import Is
from multiprocessing import reduction
from re import I, S
from turtle import tiltangle, title
from urllib.parse import uses_relative
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,auctions,bids, comments, wathclist
import time
import random
defaultimage  ="https://bkimg.cdn.bcebos.com/pic/d6ca7bcb0a46f21f73ed0799fd246b600d33ae1b?x-bce-process=image/resize,m_lfit,w_536,limit_1/format,f_jpg"

def index(request):
    return render(request, "auctions/layout.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
#active listing 
#view all of the currently active auction listings
def activeListing(request):
    return render(request, "auctions/index.html",{
        "auctions":auctions.objects.all()
    })
#create listing 
#view the create listings page
@login_required
def createListings(request):
    return render(request, "auctions/create.html")

def createListingView(request):
    title=request.POST["title"]
    description=request.POST["description"]
    startingBid=request.POST["startingBid"]
    image=request.POST["image"]
    username = request.user.get_username
    if image=="":
        image = defaultimage
    Category=request.POST["Category"]
    createTime = time.asctime( time.localtime(time.time()) )
    createTime = str(createTime)
    auction =auctions(title=title,description=description,startbid=startingBid,image=image,category=Category,createTime=createTime,createby=username,status = "open")
    bid = bids(title=title,nowbid=startingBid,createby=username)
    auction.save()
    bid.save()
    return render(request, "auctions/index.html")

#Categories page
#return all the categories
def categories(request):
    return render(request, "auctions/categroies.html",{
        "auctions":auctions.objects.all()
    })
#Categories page
#specific categories
def listcategory(request,param):
    return render(request,"auctions/categroy.html",{
        "auctions":auctions.objects.filter(category=param),
        "categroy":param
    })

#watchList
@login_required
def watchListPage(request):
    username = request.user.get_username
    return render(request,"auctions/watch.html",{
        "auctions":wathclist.objects.filter(user=username)
    })

#specific Page
def specificPage(request,param):
    t = param
    isLogin =request.user.is_authenticated
    if isLogin == False:
        username = "Anonymous"
    else:
        username = request.user.get_username
    auction = auctions.objects.filter(title=t)
    #if owner
    if username == auction[0].createby:
        sameOwner =True
    else:
        sameOwner =True
    #now biding price
    bid = bids.objects.filter(title=t)
    nowPrice = bid[0].nowbid
    #if buyer
    if username == bid[0].createby:
        sameBuyer = True
    else:
        sameBuyer = False
    # if in watchList
    wl = wathclist.objects.filter(user=username,title=t)
    if len(wl)==0:
        isInWatchList =False
    else:
        isInWatchList = True
    return render(request,"auctions/Specification.html",{
        "isLogin":isLogin,
        "sameOwner":sameOwner,
        "sameBuyer":sameBuyer,
        "isInWatchList":isInWatchList,
        "nowPrice":nowPrice,
        "auction":auction[0],
        "comments":comments.objects.filter(title=t),
        "status":auction[0].status
    })
#add item
def add(request):
    title = request.POST["title"]
    description = request.POST["description"]
    startbid = request.POST["startbid"]
    category = request.POST["category"]
    image = request.POST["image"]
    createTime = request.POST["createTime"]
    username = request.user.get_username
    wl = wathclist(user=username,title=title,description=description,startbid =startbid,category=category,image=image, createTime =createTime)
    wl.save()
    return render(request,"auctions/blank.html",{
        "msg":"add success"
    })

#remove item
def remove(request):
    title = request.POST["title"]
    wathclist.objects.filter(title=title).delete()
    return render(request,"auctions/blank.html",{
        "msg":"remove success"
    })

#close item
def close(request):
    title = request.POST["title"]
    nowUser = bids.objects.filter(title=title)[0].createby
    auctions.objects.filter(title=title).update(createby=nowUser,status="close")
    wathclist.objects.filter(title=title).update(user=nowUser)
    return render(request,"auctions/blank.html",{
        "msg":"close success"
    })

#make a new bid
def newBid(request):
    title = request.POST["title"]
    newBid = request.POST["newBid"]
    bid =  bids.objects.filter(title=title)
    if bid[0].nowbid >=newBid:
        msg = "Error You new Bid shall be higher"
    else:
        bids.objects.filter(title=title).update(nowbid=newBid)
        msg ="Bid success"
    return render(request,"auctions/blank.html",{
        "msg":msg
    })

#add new Comment
def newComment(request):
    title = request.POST["title"]
    comment = request.POST["comments"]
    username = request.user.username
    ncomments = comments(title=title,content =comment,name=username)
    ncomments.save()
    return render(request,"auctions/blank.html",{
        "msg":"comment success"
    })