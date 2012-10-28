from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns("",
    url('^user/([A-Za-z0-9@]+)', views.user, name='user'),
    url("^blog/articles/", views.custom_article_list, name="custom_article_list"),
    url(r'^post/(?P<post_id>\d+)/(?P<slug>.+)$', views.post, name='post'),
    url(r'^post/(?P<post_id>\d+)/?$', views.post, name='post'),
    url(r'^rss.xml', 'mezzanine.blog.views.blog_post_feed', {'format': 'rss'}, name='old_rss')
)

# EOF

