from django.urls import path, include
from . import views
from .views import  (HomeView,
                     ArticleView,
                     AddPostView,
                     UpdatePostView,
                     DeletePostView,
                     CategoryView,
                     LikeView,
                     CategoryList,
                     index1,
                     validate_email,
                     tag_detail,
                     TagListView
                     ,)
from .views import link

#app_name = 'theblog'



urlpatterns = [

    path('',HomeView.as_view(), name='index'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace ='hitcount')),
    path('newsletter/', views.index1, name='index1'),
    path('validate/', views.validate_email, name='validate_email'),

    path('add_post/',AddPostView.as_view(), name='add_post'),
    path('<slug:slug>',ArticleView.as_view(), name='article_detail'),#path('article/<slug:slug>',ArticleView.as_view(), name='article_detail'),
    path('article/edit/<int:pk>',UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/delete',DeletePostView.as_view(), name='delete_post'),
    path('category/<str:categories>/',CategoryView, name='category'),
    path('category/',CategoryList, name='category_list'),
    #path('like/<slug:slug>',LikeView,name="post_likes"), 
    path('like/<int:pk>',LikeView,name="post_likes"),
    #path('tag/<slug:tag>/', TagListView.as_view(),name='tag_detail'),
    path('tag/<slug:tag>/', tag_detail,name='tag_detail'),


    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('videos/' , views.videos , name='videos'),
    path('gadgets/', views.gadgets, name='gadgets'),
    path('author/' , views.author , name='author'),
    path('single/' , views.single , name='single'),

    path('help_support/' , views.help_support , name='help_support'),
    path('about_us/' , views.about_us , name='about_us'),
    path('term_privacy/' , views.term_privacy , name='term_privacy'),
    path('cookies/' , views.cookies , name='cookies'),
    path('faq/' , views.faq , name='faq'),

   
]