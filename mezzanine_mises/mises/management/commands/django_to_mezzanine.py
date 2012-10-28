from django.core.management.base import BaseCommand

from django.contrib.auth import models as auth_models

from django.core.exceptions import ImproperlyConfigured

from django.conf import settings

from django.db import transaction

from mezzanine.blog import models as blog_models

from ... import models

import re

class Command(BaseCommand):
    """Deal with data migration
    """

    def _tx(self, from_model, to_model, from_db='django_mises', to_db='default', fmap=None, extras=None, cb=None):
        """Transfer data from one place to the other, fmap can be a field map dictionary
        """

        to_model.objects.using(to_db).all().delete()

        if fmap is None:
            fmap = {}

        if extras is None:
            extras = {}

        field_names = [f.name for f in from_model._meta.fields]

        print 'Transferring "%s" -> "%s"' % (from_model, to_model)
        from_obs = from_model.objects.using(from_db).all().order_by('id')
        for fob in from_obs:
            kwargs = dict(
                [(fmap.get(field_name, field_name), getattr(fob, field_name)) for field_name in field_names]
            )

            deferred = {}
            rel = None
            for k, v in kwargs.items():
                if '.' in k:
                    v_ = kwargs.pop(k)
                    if v_:
                        rel, k_ = k.split('.', 1)
                        deferred[k_] = v_

            kwargs.update(extras)

            tob = to_model.objects.using(to_db).create(**kwargs)

            if cb is not None:
                cb(tob)

            ## TO WAR
            # Mezzanine forces a publish_date so hack it
            if kwargs.has_key('publish_date') and kwargs['publish_date'] is None:
                tob.status = 1
                tob.save()

            if deferred:
                rel_ob = getattr(tob, rel)
                for k, v in deferred.items():
                    try:
                        setattr(rel_ob, k, v)
                    except ValueError:
                        ## Assume foreign key on wrong db
                        v = v.__class__.objects.using(to_db).get(id=v.id)
                        setattr(rel_ob, k, v)
                rel_ob.save()

        print to_model.objects.using(to_db).all().count()

    @transaction.commit_on_success
    def handle(self, *args, **options):
        """JFDI method
        """

        if not settings.DATABASES.has_key('django_mises'):
            raise ImproperlyConfigured('Need django_mises db conf')

        from django_mises.users import models as dmu_models
        from django_mises.main import models as dmm_models
        from django_mises.blog import models as dmb_models

        self._tx(dmm_models.Slogan, models.Slogan)
        self._tx(auth_models.User, auth_models.User)
        self._tx(auth_models.Group, auth_models.Group)
        self._tx(dmu_models.UserProfile, models.UserProfile)

        # CREATE TABLE "blog_blogpost" ("status" integer NOT NULL, "_meta_title" varchar(500) NULL, "allow_comments" bool NOT NULL DEFAULT 1, "user_id" integer NOT NULL, "description" text NOT NULL, "title" varchar(500) NOT NULL, "short_url" varchar(200), "site_id" integer NOT NULL DEFAULT 1, "keywords_string" varchar(500) NOT NULL DEFAULT '', "content" text NOT NULL, "rating_count" integer NOT NULL DEFAULT 0, "publish_date" datetime, "gen_description" bool NOT NULL DEFAULT 1, "featured_image" varchar(255), "rating_average" real NOT NULL DEFAULT 0, "id" integer PRIMARY KEY, "comments_count" integer NOT NULL DEFAULT 0, "slug" varchar(2000), "expiry_date" datetime);
        blogmap = {
            'author': 'user',
            'co_author': 'blogpostextra.co_author',
            'preview': 'description',
            'preview_img': 'featured_image',
            'publish_at': 'publish_date',
            'updated_at': 'blogpostextra.updated_at',
        }

        blogextras = {
            'site_id': 1,
        }

        def fix_post(post):
            """Callback to fix post paths and publication
            """

            ## Paths
            # Always save, see if that creates thumbnails
            if post.featured_image is not None:
                upload_idx = post.featured_image.path.find('upload')
                # These exist already elsewhere
                if post.featured_image.path.startswith('http'):
                    post.featured_image.path = 'uploads/%s' % post.featured_image.filename

                elif upload_idx > -1:
                    post.featured_image.path = post.featured_image.path[upload_idx:]

                m = re.search('<img.*/>', post.content)
                tag = m.group()
                post.content = post.content.replace(tag, '')

                post.save()

                assert post.featured_image.exists(), 'Not found: %s' % post.featured_image.path

            ## Publication status
            if not post.publish_date:
                post.status = 1

        self._tx(dmb_models.Post, blog_models.BlogPost, fmap=blogmap, extras=blogextras, cb=fix_post)

# EOF

