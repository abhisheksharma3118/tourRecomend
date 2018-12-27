from django.conf.urls  import url
from .import views
app_name = "reviews"
urlpatterns = [
    url(r'^$',views.review_list,name='review_list'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    url(r'^tour$', views.tour_list, name='tour_list'),
    url(r'^tour/(?P<tour_id>[0-9]+)/$', views.tour_detail, name='tour_detail'),
    url(r'^tour/(?P<tour_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$',views.user_review_list,name='user_review_list'),
    url(r'^review/user/$',views.user_review_list,name='user_review_list'),
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list')
]
