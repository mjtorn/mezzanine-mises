from django.contrib.auth import models as auth_models

from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext

from mezzanine.blog import models

import datetime

def user(request, username):
    """View user
    """

    viewed_user = get_object_or_404(auth_models.User, username=username)

    context = {
        'viewed_user': viewed_user,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('user/view.html', req_ctx)

def custom_article_list(request):
    """Deal with article listing
    """

    now = datetime.datetime.now()

    posts = models.BlogPost.objects.filter(publish_date__lte=now).order_by('-publish_date')

    context = {
        'posts': posts,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('blog/custom_article_list.html', req_ctx)

# EOF

