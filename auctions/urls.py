from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item_list/<int:item_id>", views.item_list, name="item_list"),
    path("comment/<int:item_id>", views.create_comment, name="comment"),
    path("category", views.category, name="category"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("close/<int:item_id>", views.close, name="close")
]
