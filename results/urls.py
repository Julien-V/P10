from django.urls import path

from .import views


urlpatterns = [
    path('search_results', views.search_results, name='search_results'),
    path('substitute', views.substitute, name='substitute'),
    path('product', views.product, name='product'),
    path('log_in', views.log_in, name='authentification'),
    path('log_out', views.log_out, name='deauthentification'),
    path('sign_in', views.sign_in, name="register"),
    path('account', views.account, name="account"),
    path('terms', views.terms, name="terms"),
    path('home', views.index, name='home'),
    path('', views.index, name="home")
]
