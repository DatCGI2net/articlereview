from django.conf.urls import url, include

from review.views import (HomeView, ArticleCreate, ArticleEdit,
                          ArticleList, )



urlpatterns = [
    
    #url(r'^accounts/login/', LoginView.as_view(
    #    template_name='login.html'), name='login'),
    url('^', include('django.contrib.auth.urls')),
    url('article/create/$', ArticleCreate.as_view(), name='article-create'),
    url('article/(?P<pk>[0-9]+)/', ArticleEdit.as_view(), name='article-edit'),
    url('articles/', ArticleList.as_view(), name='article-list'),              
    url(r'^', HomeView.as_view(), name='home'),
    
]