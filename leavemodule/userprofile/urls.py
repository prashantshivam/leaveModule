from django.conf.urls import url, include;
from . import views;
from leavemodule import views as leavemodule_views;
urlpatterns = [
	url(r'^home', views.user_home),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^leaveform/', leavemodule_views.getLeaveTemplate, name='leave_app'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile/(?P<username>[a-zA-Z\.0-9]{3,30})/leaveDetails', views.leaveDetails, name='leaveDetails'),
	url(r'^profile/(?P<username>[a-zA-Z\.0-9]{3,30})/Approve', views.approve, name='profile'),
	url(r'^profile/(?P<username>[a-zA-Z\.0-9]{3,30})/(?P<leave_id>\d+)/$', views.leaveShow, name='leaveShow'),
	url(r'^delete/(?P<username>[a-zA-Z\.0-9]{3,30})/(?P<leave_id>\d+)/$', views.delete, name='leaveDelete'),
	url(r'^approve/(?P<username>[a-zA-Z\.0-9]{3,30})/(?P<leave_id>\d+)/$', views.accept, name='leaveApprove'),
	url(r'^forward/(?P<username>[a-zA-Z\.0-9]{3,30})/(?P<leave_id>\d+)/$', views.forward, name='leaveApprove'),
	url(r'^test', views.test),
] 