from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<str:id>", views.listings, name="listings" ),
    path("remove", views.remove_watchlist, name="remove"),
    path("bid", views.bid, name="bid"),
    path("close", views.close_view, name="close"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name='categories'),
    path('category/<str:category>', views.category, name='category')
]
