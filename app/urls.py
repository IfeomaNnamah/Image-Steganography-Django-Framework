# from django.conf.paths import urls
from django.urls import path
from . import views
# app_name = 'app'

urlpatterns = [
	path('home/', views.index, name='index'),
	path('pencode/', views.p_encode, name='p_encode'),
	path('mails/', views.mail_view, name='mails'),
	# path('savekey/', views.savekey, name='savekey'),
	path('<int:id>/download/', views.download, name='download'),
	path('sharestegoimage/', views.sharestegoimage, name='sharestegoimage'),
	path('pdecode/', views.p_decode, name='p_decode'),
	path('', views.login_page, name='login'),
	path('register/', views.register, name='register'),
	path('logoutpage/', views.logout_page, name='logout'),
	path('encode/', views.encode, name='encode'),
	path('decode/', views.decode, name='decode'),
path('checkecondefile/', views.checkecondefile, name='checkecondefile'),
]