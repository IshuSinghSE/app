from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.functional import cached_property
import datetime
from django.template.defaultfilters import slugify
#from django.utils.encoding import python_2_unicode_compatible
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
#from  embed_video.fields  import  EmbedVideoField

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


link ={
    'fb':'https://www.facebook.com/',
    'ig':'https://www.instagram.com/',
    'tw':'https://www.twitter.com/',
    'gp':'https://www.googleplus.com/',
    'yt':'https://www.youtube.com/',
    'pt':'https://www.pinterest.com/',
    'tg':'https://www.telegram.com/',
}
# POSTS #

class post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    POST_CHOICES = (
        ('article', 'Article'),
        ('video', 'Video'),
        ) 

    title    = models.CharField(max_length=200,default='this is my blog', blank=True, null=True)
    author   = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=200,default="coding",blank=True,null=True)
    body     = RichTextField(blank=True,null=True)
    image    = models.ImageField(upload_to="Images_post/",blank=True,null=True)
    snippet  = models.CharField(max_length=300,default='Vivamus non condimentum orci. Pellentesque venenatis nibh sit amet est vehicula lobortis. Cras eget aliquet eros. Nunc lectus elit, suscipit at nunc sed, finibus imperdiet ipsum.')
    publish  = models.DateTimeField(default=timezone.now)
    created  = models.DateField(auto_now_add=True)
    updated  = models.DateField(auto_now=True)
    status   = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') 
    #video = EmbedVideoField()

    content_type   = models.CharField(max_length=10, choices=POST_CHOICES, default='article') 
    likes    = models.ManyToManyField(User, related_name="blog_post_likes", blank=True)
    slug     = models.SlugField(max_length=200, null=False, unique=True)
    hit_count_generic =  GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    tags = TaggableManager() 
    approved = models.BooleanField(default=False)
    feed = models.BooleanField(default=False)


    class Meta:
        ordering = ('-publish',)

    def total_likes(self):
        return self.likes.count()
    
        

    @cached_property
    def is_published(self):
        return self.publish <= timezone.now()

    def publisheds(self):
        self.publish = timezone.now()

    def __str__(self):
        return self.title + ' | ' + str(self.author) + ' | ' + str(self.publish) + ' | ' + str(self.approved)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    def get_absolute_url(self):
     #   return reverse('article_detail', args=str([self.slug]) )
         return reverse('article_detail', kwargs={ "slug":  self.slug })

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            queryset = post.objects.all().filter(slug__iexact=original_slug).count()
            count = 1
            slug = original_slug
            while(queryset):
                slug = original_slug + '-' + str(count)
                count += 1
                queryset = post.objects.all().filter(slug__iexact=slug).count()

            self.slug = slug

        if self.feed:
            try:
                temp = post.objects.get(feed=True)
                if self != temp:
                    temp.feed = False
                    temp.save()
            except post.DoesNotExist:
                pass

            
        # if self.status == 'published':
            # self.created = timezone.now()
        # else:
            # self.publish = None
        # super(post, self).save(*args, **kwargs)
        return super(post, self).save(*args, **kwargs)

   
# CATEGORIES #    
class category(models.Model):
    name     = models.CharField(max_length=200)
    image    = models.ImageField(upload_to="Category/",blank=True,null=True)
    about    = models.CharField(max_length=200,default='Vivamus non condimentum orci. Pellentesque venenatis nibh sit amet est vehicula lobortis.', blank=True, null=True)
    created  = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
     #   return reverse('article_detail', args=(str(self.id)) )
         return reverse('index')


#profile
class profile(models.Model):
     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
     profile_pic = models.ImageField(blank=True,null=True,upload_to="Images/profile")
     bio = models.TextField()
     facebook_url   = models.URLField(max_length=200,blank=True, null=True )
     instagram_url  = models.URLField(max_length=200,blank=True, null=True )
     twitter_url    = models.URLField(max_length=200,blank=True, null=True )
     pinterest_url  = models.URLField(max_length=200,blank=True, null=True )
     youtube_url    = models.URLField(max_length=200,blank=True, null=True )
     website_url    = models.URLField(max_length=200,blank=True, null=True )
     
     def __str__(self):
       return str(self.user)

     def get_absolute_url(self):
        return reverse('index')
'''      
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
    instance.profile.save()        
'''
class SubscribedUsers(models.Model):
    email = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
       return '%s - %s' % (self.name, self.email)

class Comment(models.Model):
    CommentPost = models.ForeignKey(post, related_name="comments", on_delete=models.CASCADE)
    #name = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField(get_user_model())
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return str(self.author) + ' | ' + str(self.body) 

    @property 
    def get_comments(self):
        return Comment.objects.filter(parent=self).reverse()# .filter(active=True)

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

'''
class  Video(models.Model):
    Title = models.CharField(max_length=200)
    Body = models.TextField()
    video = EmbedVideoField()
'''