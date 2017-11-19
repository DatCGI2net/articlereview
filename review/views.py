from django.shortcuts import render, redirect, resolve_url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin,\
    LoginRequiredMixin
from review.forms import ArticleFormCreate, ArticleFormApprove
from review.models import Article
from django.contrib.auth.models import Permission
from django.template.loader import render_to_string



APP_NAME = 'review'
REQ_PERM = 'change_article'

class HomeView(TemplateView):
    template_name='home.html'
    
    
    
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class  = ArticleFormCreate
    
    
    def send_editor_email(self):
        perm = Permission.objects.get(codename=REQ_PERM)
        subject_tpl = '{0}/emails/to_approve_subject.txt'.format(APP_NAME)
        message_tpl = '{0}/emails/to_approve_message.txt'.format(APP_NAME)
        
        data = {'article': self.object}
        
        for u in perm.user_set.all():
            data.update({'user': u})
            
            subject = render_to_string(subject_tpl,data)
            message = render_to_string(message_tpl,data)
            print('message:', message)
            try:
                
                u.email_user(subject, message)
            except Exception as err:
                print('email_user err:', err)
                
    
    def form_valid(self, form):
        # return CreateView.form_valid(self, form)
        if form.is_valid():
            
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
            
            # Send editor an email
            self.send_editor_email()
            
            return redirect('home')
        
        else:
            
            return  super(ArticleCreate, self).form_valid(form)
        
        
    

class ArticleEdit(PermissionRequiredMixin, UpdateView):
    model = Article
    # see tests.py to see how can setup the authorzied user
    permission_required = ('{0}.{1}'.format(APP_NAME, REQ_PERM))
    form_class = ArticleFormApprove
    template_name_suffix = '_form_approve'
    success_url = '/articles/'
    
class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    