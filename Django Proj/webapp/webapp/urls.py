from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import webapp.regbackend as regbackend
import experiment.views as views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),

    # urls experiment
    url(r'^experiments/checkForm$',views.checkForm , name='checkForm'),
    url(r'^experiments/$', views.experiments, name='exp'),
    url(r'^experiments/downloadInputFile', views.downloadInputFile, name='downloadInputFile'),
    url(r'^experiments/downloadOutputFile$', views.downloadOutputFile, name='downloadOutputFile'),
    url(r'^experiment/sample/(?P<path>[a-zA-Z0-9\u00C0-\u00FF]+)$', views.downloadSample,name='sampleDownload'),
    url(r'^experiments/result$', views.result, name='result'),

    # django admin
    url(r'^Django_admin/', include(admin.site.urls)),

    # urls register
    url(r'^accounts/register/', regbackend.MyRegistrationView.as_view(),
        name='register_custom'),
    url(r'^complete/', views.register_sucess, name='complete'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # user profile
    url(r'^profile/(?P<username>[a-zA-Z0-9\u00C0-\u00FF]+)$', views.getUserProfile, name="userProfile"),
    url(r'^profile/(?P<uname>[a-zA-Z0-9\u00C0-\u00FF]+)/save', views.saveProfile, name="saveProfile"),

    # ADMIN
    url(r'^admin/remove/(?P<model>[a-zA-Z0-9\u00C0-\u00FF]+)$', views.removeList, name="removeList"), #DELETE

    # ADMIN algorithm 
    url(r'^admin/algorithms/$', views.listAlg, name="listAlgorithm"), #READ
    url(r'^admin/algorithms/(?P<alg>[a-zA-Z0-9\u00C0-\u00FF]+)$', views.seeAlg, name="seeAlgorithm"), #READ
    url(r'^admin/algorithms/(?P<idAlg>[a-zA-Z0-9\u00C0-\u00FF]+)/update$',views.updateAlg, name="updateAlgorithm"), #UPDATE
    url(r'^admin/algorithms/addAlgorithm/$', views.addAlg, name="addAlgorithm"), #CREATE
    url(r'^admin/algorithms/addAlgorithm/save',views.saveAlg, name="saveAlgorithm"), #CREATE
    url(r'^admin/algorithms/statistics/$', views.appStatistics, name='appStatistics'),

    # ADMIN users
    url(r'^admin/users/$', views.listUsers, name="listUsers"), #READ
    url(r'^admin/users/(?P<appUser>[a-zA-Z0-9\u00C0-\u00FF]+)_(?P<authUser>[a-zA-Z0-9\u00C0-\u00FF]+)$', views.seeUser, name="seeUser"), #READ
    url(r'^admin/users/addUser/$', views.addUser, name="addUser"), #CREATE    
    url(r'^admin/users/addUser/save',views.saveUser, name="saveUser"), #CREATE
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
