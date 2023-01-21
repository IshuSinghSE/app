from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView , CreateView, DetailView, UpdateView, DeleteView
from .models import post, category, Comment, link
from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import PostForm, EditForm, CommentForm, ContactForm
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView
from taggit.models import Tag

from django.contrib import messages
from django.http import JsonResponse
import re
from .models import SubscribedUsers
from django.core.mail import send_mail
from django.conf import settings

import datetime
from datetime import timedelta

# Create your views here.


class HomeView(ListView):
    model = post
    template_name = "index.html"
    context_object_name = "post"
    paginate_by = 3
    ordering = ['-publish']


    def get_context_data(self, *args, **kwargs):

        today = datetime.date.today() - timedelta(days=7)
        category_menu = category.objects.all()
        tags_menu     = Tag.objects.all()
       

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context.update({'posts': post.objects.filter(approved =True, publish__isnull=False, status='published').all().order_by('-publish',)})
        context.update({'draft': post.objects.filter(publish__isnull=False, status='draft').all().order_by('-publish',)})
        context.update({'feed': post.objects.filter(feed=True,approved =True,  status='published')})
        context.update({'popular_posts': post.objects.filter(approved =True, status='published').order_by('-hit_count_generic__hits')[0:10],})

        context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})

        #context["page_obj"] = page_obj
        context["category_menu"] = category_menu
        context["tags_menu"] = tags_menu
        context["link"] = link
        
        return context


class ArticleView(HitCountDetailView):
    model = post
    template_name ='article_detail.html'
    form_class = CommentForm
    ordering = ['-publish']
    #paginate_by = 1
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        
        category_menu = category.objects.all()
        tags_menu     = Tag.objects.all()
        post_tags_ids = post.tags.values_list('id', flat = True)
        #post_list = post.objects.all()
        context = super(ArticleView, self).get_context_data(*args, **kwargs)
        context.update({'popular_posts': post.objects.filter(approved =True, status='published').order_by('-hit_count_generic__hits')[:10],})
        context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'similar_post':  post.published.filter(tags__in=post_tags_ids, approved = True, status='published').annotate(same_tags=Count('tags')).order_by('-publish')[0:2],})


        connected_comments = Comment.objects.filter(CommentPost=self.get_object())
        number_of_comments = connected_comments.count()
        context['comments'] = connected_comments
        context['no_of_comments'] = number_of_comments
        context['comment_form'] = CommentForm()
        
        #stuff = get_object_or_404(post, id=self.kwargs[slug])
        #total_likes = stuff.total_likes()

        liked = False
        #if stuff.likes.filter(id=self.request.user.id).exists():
         #   liked = True

       # context["total_likes"] = total_likes
        #context["post_list"] = post_list
        context["liked"] = liked
        context["category_menu"] = category_menu
        context["tags_menu"] = tags_menu
        context["link"] = link
        return context

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                body = comment_form.cleaned_data['body']
                #email = comment_form.cleaned_data['email']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None
            
            new_comment = Comment(body=body, author=self.request.user, email=self.request.user.email, CommentPost=self.get_object(), parent=parent)#
            new_comment.save()
            messages.success(self.request, 'Your comment ' + '"' + str(body) + '"' + ' has been succesfully created ! ')
            return redirect(self.request.path_info, 'article_detail.html')
            

    def delete_post(self, id, request, *args):

            messages.success(self.request, 'Your comment ' + '"' + str(body) + '"' + ' has been succesfully created ! ')
            return redirect(self.request.path_info, 'article_detail.html', args=[str(id)])

class AddPostView(CreateView):
    model = post
    template_name = 'add_post.html'
    form_class = PostForm
   
    def get_context_data(self, *args, **kwargs):
        category_menu = category.objects.all()
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})

        context["category_menu"] = category_menu
        return context  
    
    def get_success_url(self):
        messages.success(self.request, 'Your post has been succesfully created ! ')
        return reverse_lazy('index')    


class UpdatePostView(UpdateView):
    model = post
    form_class = EditForm
    template_name ='update_post.html'
    #fields = ['title','author','category','body','image']

    def get_context_data(self, *args, **kwargs):
        category_menu = category.objects.all()
        context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
        context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})

        context["category_menu"] = category_menu
        return context
    def get_success_url(self):
        messages.success(self.request, 'Your post has been succesfully updated ! ')
        return reverse_lazy('index')
    
class DeletePostView(DeleteView):
    model = post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        category_menu = category.objects.all()
        context = super(DeletePostView, self).get_context_data(*args, **kwargs)
        context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})

        context["category_menu"] = category_menu
        return context

    def get_success_url(self):
        messages.success(self.request, 'Your post has been succesfully deleted ! ')
        return reverse_lazy('index')

def CategoryView(request, categories):
    category_posts = post.objects.filter(category=categories.replace('-',' '))
   

   # def get_context_data(self, *args, **kwargs):
    category_menu = category.objects.all()
    context={'categories':categories.replace('-',' ').title(), 'category_posts':category_posts}
    
    context.update({'popular_posts': post.objects.filter(approved =True, status='published').order_by('-hit_count_generic__hits')[:10],})
   # context = super(CategoryView, self).get_context_data(*args, **kwargs)
    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})

    context["category_menu"] = category_menu 
    return render(request, 'categories.html',context )

def CategoryList(request):
    category_list = category.objects.all()
   
    category_menu = category.objects.all()
    context={ 'category_list':category_list}
    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context["category_menu"] = category_menu
    
    return render(request, 'categories_list.html',context)


def LikeView(request, pk):
    posts = get_object_or_404(post,id=request.POST.get('like_id'))
    liked = False
    if posts.likes.filter(id=request.user.id).exists():
        posts.likes.remove(request.user)
        liked = False
    else:
        posts.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))

    

def index1(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        name = post_data.get("name", None)
        subscribedUsers = SubscribedUsers()
        subscribedUsers.email = email
        subscribedUsers.name = name
        subscribedUsers.save()
        # send a confirmation mail
        subject = 'NewsLetter Subscription'
        message = 'Hlo ' + name + ', Thanks for subscribing us. You will get notification of latest articles posted on our website. Please do not reply on this email. checkout our website --- https://ishusinghse.github.io/'
        email_from = 'ishu.111636@gmail.com'#settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, "Newsletter Sent! ")
        return redirect('index')
        
        # res = JsonResponse({'msg': 'Thanks. Subscribed Successfully!'})
        # return res
        # return render(request, 'contact.html')
    return render(request, 'index.html',{})

def validate_email(request): 
    email = request.POST.get("email", None)   
    if email is None:
        res = JsonResponse({'msg': 'Email is required.'})
    elif SubscribedUsers.objects.get(email = email):
        res = JsonResponse({'msg': 'Email Address already exists'})
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'Invalid Email Address'})
    else:
        res = JsonResponse({'msg': ''})
    return res


def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'test'
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, 'ishu.111636@gmail.com', ['ishu.111636@yahoo.com','candyking1002263@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found!')
            messages.success(request, 'your query has been sent!')
            return redirect('/')
    form = ContactForm

    context = {'form':form}
    category_menu = category.objects.all()
    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context["category_menu"] = category_menu
    
    return render(request,'contact.html',context ) 

def reviews(request):
    context = {}
    category_menu = category.objects.all()
    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context["category_menu"] = category_menu

    return render(request,'reviews.html', context) 

def videos(request):

    context = {}
    category_menu = category.objects.all()
    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context["category_menu"] = category_menu
    
    return render(request,'videos.html',context) 

def gadgets(request):
    context = {}
    category_menu = category.objects.all()
    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context["category_menu"] = category_menu

    return render(request,'gadgets.html',context) 

def author(request):
    return render(request,'author.html') 
    
def help_support(request):
    return render(request,'help_support.html') 

def about_us(request):
    return render(request,'about_us.html') 

def term_privacy(request):
    return render(request,'term_privacy.html') 

def cookies(request):
    return render(request,'cookies.html') 

def faq(request):
    return render(request,'faq.html') 
    
def single(request):
    return render(request,'single.html') 

def tag_detail(request, tag):
    posts = post.objects.filter(tags__slug=tag, publish__isnull=False, status='published').all().order_by('-publish',)
    tags_menu  = Tag.objects.all()

    context = {'posts':posts,'tag':tag, 'tags_menu':tags_menu}
    category_menu = category.objects.all()
    context.update({'popular_posts': post.objects.filter(tags__slug = tag,approved =True, status='published').order_by('-hit_count_generic__hits')[0:10],})

    context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
    context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
    context["category_menu"] = category_menu

    return render(request, 'tag_detail.html', context )


class TagListView(ListView, Tag):
    model = post
    template_name = "tag_detail.html"
    
    paginate_by = 3
    ordering = ['-publish']

    def get_queryset(self):
        return  post.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(*args, **kwargs)
        category_menu = category.objects.all()
        context.update({'science'   : post.objects.filter(category = 'science', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'technology': post.objects.filter(category = 'technology', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'social_media': post.objects.filter(category = 'social media', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
        context.update({'coding'    : post.objects.filter(category = 'coding', approved = True, status='published').all().order_by('-hit_count_generic__hits')[0:4],})
        context.update({'worldwide':  post.objects.filter(category = 'worldwide', approved = True, status='published').order_by('-hit_count_generic__hits')[0:4],})
       

        today = datetime.date.today() - timedelta(days=7)
        category_menu = category.objects.all()
        context = super(TagListView, self).get_context_data( **kwargs)
        context["tag"] = self.kwargs.get("slug")
        context.update({'posts': post.objects.filter(tags__slug=Tag)})#, publish__isnull=False, status='published').all().order_by('-publish',)})
        #context.update({'draft': post.objects.filter(publish__isnull=False, status='draft').all().order_by('-publish',)})
        #context.update({'feed': post.objects.filter(approved =True, publish__gt = today, status='published').order_by('-hit_count_generic__hits')[0:4],})
        #context.update({'popular_posts': post.objects.filter(approved =True, status='published').order_by('-hit_count_generic__hits')[0:5],})
        context["category_menu"] = category_menu
        return context

