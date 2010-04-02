"""
    limited.pages.models
    ~~~~~~~~~~~~~~~~~~~~
    Database models of the `limited.pages` app.
"""
# coding: utf-8
import os.path
from django.utils.translation import ugettext as _
from django.db import models
from django.db.models.signals import class_prepared
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as urlresolve
from django.conf import settings
from limited.utils import thumbnail
from limited import markup

def apply_filter_method(**kwargs):
    model = kwargs.pop('sender')
    def filter(*args, **kwargs):
        kwargs.pop('public', None)
        return model.objects.filter(public=True, *args, **kwargs)
    model.filter = staticmethod(filter)
class_prepared.connect(apply_filter_method)
# very, very, very ugly.

class Page(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)

    # static page or blog entry?
    title = models.CharField(_('Title'), max_length=200, unique=True)
    text = models.TextField(_('Text'))
    url = models.SlugField(_('Slug'), unique=True)

    tags = models.ManyToManyField(_('Tag'), blank=True)
    language = models.CharField(_('Language'), max_length=2,
        default=settings.LANGUAGE_CODE[:2], blank=True)
    other_languages = models.CharField(_('Other languages'), max_length=100,
        help_text=_('(comma separated post ids)'), blank=True)

    isblog = models.BooleanField(_('Is a blog entry'), default=True)

    edit_time = models.DateTimeField('Last edited', blank=True, null=True)
    creation_time = models.DateTimeField('Creation date', auto_now_add=True)
    # timestamps
    popular = models.BooleanField(_('Is a popular entry'))
    public = models.BooleanField(_('Is public (published)'), default=True)
    in_navigation = models.BooleanField(_('Showed in top navigation'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-edit_time']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    @property
    def parsed(self):
        return markup.parse(self.text)

    @property
    def absolute_url(self):
        return urlresolve('single_post' if self.isblog else 'single_page',
                          kwargs={'single' : self.url})

    @property
    def time(self):
        return self.edit_time or self.creation_time

class Comment(models.Model):
    page = models.ForeignKey('Page')
    # parent page that owns this child
    name = models.CharField(_('Name'), max_length=50)
    text = models.TextField(_('Comment'))
    public = models.BooleanField(_('Is public (published)'), default=True)
    creation_time = models.DateTimeField(_('Creation time'), auto_now_add=True)

    class Meta:
        ordering = ['-creation_time']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __unicode__(self):
        return _("Comment %s by \"%s\")") % (self.id, self.name)

    @property
    def parsed(self):
        return markup.parse_comment(self.text)

class Tag(models.Model):
    name = models.CharField(_('Tag'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)

    class Meta:
        ordering = ['-name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return self.name

    def page_count(self):
        return self.page_set.count()

class Image(models.Model):
    file = models.ImageField(_('Picture'),
            upload_to=settings.UPLOAD_DIRS['images'])

    @property
    def thumbnail(self):
        return thumbnail.thumbnailize(self.file.name)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-file']
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')

class File(models.Model):
    file = models.FileField(_('File'), upload_to=settings.UPLOAD_DIRS['files'])

    class Meta:
        ordering = ['-file']
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __unicode__(self):
        return self.name
