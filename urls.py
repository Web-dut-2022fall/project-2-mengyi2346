from django.urls import path,re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activeListings", views.activeListing, name="activeListing"),
    path("createListings", views.createListings, name="createListings"),
    path("categories", views.categories, name="categories"),
    path("createListingView", views.createListingView, name="createListingView"),
    re_path(r'^category/(.+)/$', views.listcategory, name="listcategory"),
    re_path(r'^specific/(.+)/$', views.specificPage, name="specificPage"),
    path("newBid", views.newBid, name="newBids"),
    path("add",views.add,name="add"),
    path("remove",views.remove,name="remove"),
    path("close",views.close,name="close"),
    path("watchlist",views.watchListPage,name="watchlist"),
    path("content",views.newComment,name="newComment")
]
