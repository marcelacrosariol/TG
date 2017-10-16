from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import webapp.regbackend as regbackend
import experiment.views as views

urlpatterns = [
    # urls experiment
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^experiments/checkForm$',
        views.checkForm , name='checkForm'),
    url(r'^experiments/$', views.experiments, name='exp'),
    url(r'^experiments/remove$', views.experimentsRemove, name='expRemove'),
    url(r'^experiments/downloadInputFile', views.downloadInputFile,
        name='downloadInputFile'),
    url(r'^experiments/downloadOutputFile', views.downloadOutputFile,
        name='downloadOutputFile'),
    url(r'^experiment/sample/(?P<path>[a-zA-Z0-9]+)', views.downloadSample,
        name='sampleDownload'),

    #django admin
    url(r'^experiments/result$', views.result, name='result'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^statistics', views.appStatistics, name='appStatistics'),

    # urls register
    url(r'^accounts/register/', regbackend.MyRegistrationView.as_view(),
        name='register_custom'),
    url(r'^complete/', views.register_sucess, name='complete'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # user profile
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', views.getUserProfile, name="userProfile"),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/save', views.saveProfile, name="saveProfile"),

    # add algorithm 
    url(r'^addAlgorithm/$', views.addAlg, name="addAlgorithm"),
    url(r'^addAlgorithm/save',views.saveAlg, name="saveAlgorithm"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
