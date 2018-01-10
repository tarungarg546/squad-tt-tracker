from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compare_teams/$', views.compare_teams, name='compare_teams'),
    url(r'^compare_users/$', views.compare_users, name='compare_users')
]
