from django.contrib.auth import models as auth_models

from django.db import models

from mezzanine.blog import models as blog_models

import hashlib

import random

import time

class UserProfile(models.Model):
    """Profile model
    """

    user = models.OneToOneField(auth_models.User)

    verification_code = models.CharField(max_length=40, null=True, blank=True, default=None)
    is_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s\'s profile' % self.user.username

    def gen_verification_code(self):
        """Generate code if it does not exist
        """

        if self.verification_code:
            return self.verification_code
        else:
            # Secure enough ;)
            timebase = str(time.time() / 10000000000).split('.')[1]
            randbase = str(random.random()).split('.')[1]
            base = '%s%s%s' % (timebase, self.user.email, randbase)

            self.verification_code = hashlib.sha1(base).hexdigest()

            self.save()

            return self.verification_code


def userprofile_creator(sender, instance, created, **kwargs):
    """Create a profile if none exists
    """

    if created:
        UserProfile.objects.create(user_id=instance.id)

models.signals.post_save.connect(userprofile_creator, sender=auth_models.User, dispatch_uid='userprofile_creation')


class Slogan(models.Model):
    """Different small slogans to change on page loads
    """

    slogan = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%s' % self.slogan


class BlogPostExtra(models.Model):
    """Take the query overhead instead of dealing with south kludges
    """

    blog_post = models.OneToOneField(blog_models.BlogPost)

    co_author = models.ForeignKey(auth_models.User, null=True, blank=True, default=None, verbose_name='Co-Author', related_name='coauthor')
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)


def blogpostextra_creator(sender, instance, created, **kwargs):
    """Create extra data for blog post
    """

    if created:
        BlogPostExtra.objects.create(blog_post_id=instance.id)

models.signals.post_save.connect(blogpostextra_creator, sender=blog_models.BlogPost, dispatch_uid='blogpostextra_creation')

# EOF

