from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime
from django.contrib import messages

from .models import User, Auctions, Bids, Comments, Categories

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.CookieStorage'


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auctions.objects.all().filter(closed=False)
    })


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


def create_view(request):
    if request.method == 'POST':
        data = request.POST
    
        title = data.get("title")
        description = data.get("description")
        starting_bid = data.get("starting_bid")
        image = data.get("image")
        category = Categories.objects.get(name=data.get("category"))
        creator = User.objects.get(id=request.user.id)

        auction = Auctions(title=title, description=description, starting_bid=starting_bid, image=image, category=category, time=datetime.now(), creator=creator)
            

        auction.save()
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "categories": Categories.objects.all()
        })

def listings(request, id):
    onWatchlist = False
    auction = Auctions.objects.get(id=id)
    bids = auction.bids.all().order_by('-bid')
    total_bids = len(bids)
    print(auction.comments.all())

    try:
        current_bid = bids[0]
    except:
        current_bid = auction
        current_bid.bid = auction.starting_bid

    try:
        if request.user.watchlist.get(id=auction.id):
            onWatchlist = True
    except:
        pass


    return render(request, "auctions/listings.html", {
        "auction": auction,
        "onWatchlist": onWatchlist,
        "bids": bids,
        "current_bid": current_bid,
        "total_bids": total_bids
    })

def watchlist(request):
    if request.method == "POST":
        auction = Auctions.objects.get(id=request.POST.get("id"))
        request.user.watchlist.add(auction)
        
        print(request.user.watchlist)

        return HttpResponseRedirect(reverse("watchlist"))

    else:
        watchlist = request.user.watchlist.all()
        print(watchlist)
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })

def remove_watchlist(request):
    if request.method == "POST":
        auction = Auctions.objects.get(id=request.POST.get("id"))
       
        request.user.watchlist.remove(auction)

        return HttpResponseRedirect(reverse("watchlist"))

def bid(request):
    if request.method == "POST":
        auction = Auctions.objects.get(id=request.POST.get("id"))
        bid = int(request.POST.get("bid"))
        user = User.objects.get(id=request.user.id)
        time = datetime.now()

        try:
            current_bid = auction.bids.order_by('-bid').first().bid
        except AttributeError:
            current_bid = auction.starting_bid

        if current_bid < bid:
            newBid = Bids(auction=auction, bid=bid, user=user, time=time)
            newBid.save()
            print("Se guardó")
        else:
            messages.add_message(request, messages.WARNING, 'Your bid must be greater than the current bid!')
            return HttpResponseRedirect(reverse("listings", kwargs={'id': request.POST.get("id")}))

        return HttpResponseRedirect(reverse("listings", kwargs={'id': request.POST.get("id")}))

def close_view(request):
    if request.method == "POST":
        auction = Auctions.objects.get(id=request.POST.get("id"))
        bids = auction.bids.all().order_by('-bid')

        winnerBid = bids[0]
        winner = winnerBid.user

        auction.closed = True
        auction.winner = winner
        
        auction.save()

        return HttpResponseRedirect(reverse("index"))

def comment(request):
    if request.method == "POST":
        auction = Auctions.objects.get(id=request.POST.get("id"))
        user = User.objects.get(id=request.user.id)
        comment = request.POST.get("comment")
        time = datetime.now()

        newComment = Comments(auction=auction, user=user, comment=comment, time=time)
        newComment.save()
        print("Se guardó")

        return HttpResponseRedirect(reverse("listings", kwargs={"id": auction.id}))


def categories(request):
    return render(request, 'auctions/categories.html', {
        "categories": Categories.objects.all()
    })

def category(request, category):
    filter = Categories.objects.get(name=category)
    auctions = Auctions.objects.all().filter(category=filter, closed=False)

    return render(request, 'auctions/category.html', {
        "category": filter,
        "auctions": auctions
    })