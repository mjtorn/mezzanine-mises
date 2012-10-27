from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns("",
    url('^user/([A-Za-z0-9@]+)', views.user, name='user'),
    url("^blog/articles/", views.custom_article_list, name="custom_article_list"),
)

# EOF

