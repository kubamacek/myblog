from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    '''Custom models manager for published posts'''
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    '''Definition of Post object'''
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    objects = models.Manager()
    objects_published = PublishedManager()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])


class Comment(models.Model):
    '''Definition of Comment object'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment was added by {} under {}'.format(self.name, self.post)
