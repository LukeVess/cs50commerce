from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, Category, Items, Comment, Watchlist, Bid
from django import forms
from django.forms import ModelForm
from django.contrib import messages

class Create_List(ModelForm):
    class Meta:
        model = Items
        fields = ["name", "img", "start_price", "description", "category"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "custom_item_create_name",
                "placeholder": "Add a name...",
                   }),
            "start_price": forms.NumberInput(attrs={
                "class": "custom_item_create_price",
                "placeholder": "Add a price",
            }),
            "description": forms.Textarea(attrs={
                "class":  "custom_item_description",
                "placeholder": "Add a description",
            }),

            "category": forms.Select(attrs={
                "class": "custom_item_category",
                "placeholder": "Select a Category",
            })
            
        }

class Create_Comment(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={
            "class": "custom-comment-input", 
            "placeholder": "Add a comment...", 
            })
        }
        labels = {"comment": ""}

class M_Category(ModelForm):
    class Meta:
        model = Items
        fields = ["category"]  # Only "category" field
        widgets = {
            "category": forms.Select(attrs={
                "class": "custom_category_dropdown",  # Apply custom class here
            })
        }
        labels = {
            "category": ""  # Set empty label for "category"
        }

class Biding(ModelForm):
    class Meta:
        model = Bid
        fields = ["value"]
        widgets = {
            "value": forms.NumberInput(attrs={
                "class": "custom-bid-input", 
                "placeholder": "Bid Amount", 
                "inputmode": "numeric"  # Ensures numeric keyboard on mobile devices
            })
        }
        labels = {"value": ""}

class Close(ModelForm):
    class Meta:
        model = Items
        fields=  ["sold"]

def index(request):

    return render(request, "auctions/index.html", {
        "items": Items.objects.filter(sold=False).order_by('-created_at')
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
@login_required
def create_list(request):
    form = Create_List()
    if request.method == "POST":
        form = Create_List(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.actual_price = item.start_price
            item.save()
            return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create_list.html", {
        "form": form
    })
@login_required
def watchlist(request):
    if request.method == "POST":
        id_item = int(request.POST.get("item"))
        item = get_object_or_404(Items, id=id_item)
        user = request.user
        if not Watchlist.objects.filter(user=user, item=item).exists():
            # If not, create and save the Watchlist entry
            Watchlist.objects.create(user=user, item=item)
        
        return HttpResponseRedirect(reverse("index"))
    else:

        user_watchlist = Watchlist.objects.filter(user=request.user)
        
        return render(request, "auctions/watchlist.html", {
            "items": user_watchlist
        })

def item_list(request, item_id):

    if request.method == "GET":
        form = Create_Comment()
        bid = Biding()
        close = Close()
        iten = get_object_or_404(Items, id=item_id)
        comments = Comment.objects.filter(item__id=item_id)
        user = request.user
        if iten.user == user:
            return render(request, "auctions/item_list.html", {
                "item": iten,
                "comment": form,
                "comments": comments,
                "bid": bid,
                "close": close
            })
        else: 
            return render(request, "auctions/item_list.html", {
            "item": iten,
            "comment": form,
            "comments": comments,
            "bid": bid
            })
        
@login_required
def create_comment(request, item_id):
    if request.method == "POST":
        form = Create_Comment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.item = get_object_or_404(Items, id=item_id)
            comment.save()
            return HttpResponseRedirect(reverse("item_list", args=[item_id]))
    return HttpResponseRedirect(reverse("item_list", args=[item_id]))

@login_required
def category(request):
    if request.method == "GET":
        category = M_Category()
        return render(request, "auctions/category.html", {
            "category": category
        })
    if request.method == "POST":
        form = M_Category()
        category_a = M_Category(request.POST)
        if category_a.is_valid():
            category_item = Items.objects.filter(category = category_a.cleaned_data['category'])
            return render(request, "auctions/category.html", {
                "items":category_item,
                "category": form
            })
@login_required
def bid(request, item_id):
    if request.method == "POST":
        bid = Biding(request.POST)
        if bid.is_valid():
            item = get_object_or_404(Items, id=item_id)
            bid_value = bid.save(commit=False)
            if bid_value.value > item.actual_price:
                bidded = bid.save(commit=False)
                bidded.user = request.user
                bidded.item = item
                item.actual_price = bidded.value
                bidded.save()
                item.save()
                return HttpResponseRedirect(reverse("item_list", kwargs={"item_id": item_id}))  
            else:
                return HttpResponseRedirect(reverse("item_list", kwargs={"item_id": item_id}))  
@login_required
def close(request, item_id):
    if request.method == "POST":
        closing = Close(request.POST)
        if closing.is_valid():
            close = closing.save(commit=False)
            item = get_object_or_404(Items, id=item_id)
            #owner = owner.objects.order_by("-created_at").first()
            owner = Bid.objects.filter(item=item.id).order_by("-created_at").first()
            if owner is None:
                messages.error(request,'Your item dont have bids on it! ')
                return HttpResponseRedirect(reverse("item_list", kwargs={"item_id": item_id})) 
            item.sold = True
            item.owner = owner.user
            item.save()
            return HttpResponseRedirect(reverse("index"))
        
