from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.anasayfa, name="main"),
	path('sepet/', views.sepet, name="cart"),
	path('cikis/', views.cikis, name="checkout"),
	path('magaza/', views.magaza, name="store"),
	path('update_item/', views.updateItem, name="update_item"),
	path('proccess_order/', views.proccessOrder, name="proccess_order"),

]