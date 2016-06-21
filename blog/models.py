from django.db import models
from django.conf import settings
from datetime import datetime
from django.db.models.signals import post_save
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mass_mail, send_mail
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Entry(models.Model):
    """
    A blog Entry
    """
    title = models.CharField('Titre', max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publication_date')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(default=datetime.now())
    modification_date = models.DateTimeField(auto_now=True)
    body = RichTextUploadingField('Contenu')
    def __str__(self):
        return self.title
    def count_com(self):
        return self.comments.count()
    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-publication_date']

    @models.permalink
    def get_absolute_url(self):
        return ('blog:blog_entry', (), {
            'year': self.publication_date.year,
            'month': self.publication_date.month,
            'day': self.publication_date.day,
            'slug': self.slug,
        })

class Comment(models.Model):
    entry = models.ForeignKey(Entry, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['creation_date']

def send_entry_mail(sender, instance, **kwargs):
    text = get_template('blog/mail/newentry.txt')
    d = Context({ 'entry': instance, 'url' : settings.URL })
    text_content = text.render(d)
    users = User.objects.filter(is_active=True, profile__family__leave_date__isnull=True).exclude(email='')
    tuple = ()
    for user in users:
        tuple = tuple + ((
            '[AMAP a la noix] ' + instance.title,
            text_content,
            instance.author.email,
            [user.email, ]),)
    send_mass_mail(tuple)

def send_comment_mail(sender, instance, **kwargs):
    text = get_template('blog/mail/newcomment.txt')
    d = Context({ 'comment': instance, 'url' : settings.URL })
    text_content = text.render(d)
    send_mail(
        '[AMAP a la noix] COMMENTAIRE ' + instance.entry.title,
        text_content,
        'no-reply@alanoix.fr',
        [instance.entry.author.email],
        fail_silently=True)

post_save.connect(send_entry_mail, sender=Entry)
post_save.connect(send_comment_mail, sender=Comment)
