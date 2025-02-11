from django.contrib import admin
from .models import User, Category, Items, Comment, Watchlist, Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)