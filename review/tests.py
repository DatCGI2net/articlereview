from django.test import TestCase, Client
from review.models import Article
from django.contrib.auth import get_user_model
from review.forms import ArticleFormCreate, ArticleFormApprove
from django.urls import reverse

from django.contrib.auth.models import Permission



User = get_user_model()
##

class TestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        ##super(TestModels, cls).setUpTestData()
        cls.user_name = 'testuser'
        cls.user_pw = 'test1234'
        cls.user = User.objects.create_user(cls.user_name, 
                                            password=cls.user_pw)
        #cls.user.set_password(cls.user_pw)
        ##cls.user.set_password('dat12345')        
        cls.article_data  = {'title': 'Test', 'url':'http://cgito.net'}
        cls.article = Article(**cls.article_data)
        cls.article.owner = cls.user
        cls.article.save()
        cls.client = Client()
        
        cls.editor_name = 'testeditor'
        cls.editor = User.objects.create_user(cls.editor_name, 
                                              password=cls.user_pw)
        
        p, created = Permission.objects.get_or_create(codename='change_article')
        cls.editor.user_permissions.add(p)
        
        
        ##print('data is initialized')
        
class TestModels(TestData):
        
    def test_article_error(self):
        
        try:
            article = Article.objects.create(**self.article_data)
            self.assertNotEqual(article , Article, "Article instance is not created")
        except Exception as error:
            self.assertNotEqual(error , Article, "Article instance is not created")
        
    def test_article_ok(self):
        
        self.article_data.update({'owner': self.user})
        article = Article.objects.create(**self.article_data)
        ##print('article:', article)
            
        self.assertTrue(isinstance( article , Article), "got Article instance")
        self.assertTrue(article.title == 'Test', "Got correct ti5tle")
        

class TestForms(TestData):
    def test_articel_createform_invalid(self):
        f = ArticleFormCreate()
        
        self.assertEqual(False, f.is_valid(), "For is invalid")
        
        self.article_data.update({'owner': self.user, 'is_approved': True})
        f = ArticleFormCreate(self.article_data)
        self.assertEqual(True, f.is_valid(), "For is invalid")
        ##valid but save will be error
        try:
            article = f.save()
            self.assertNotEquals(article, Article, "Should not reach here")
        except Exception as error:
            self.assertNotEquals(error, Article, "Should not reach here")
        
    
    def test_articel_createform_valid(self):
        ##self.article_data.update({'owner': self.user})
        article = Article(owner=self.user)
        f = ArticleFormCreate(self.article_data, instance=article)
        self.assertEqual(True, f.is_valid(), "For is valid")
        
        article = f.save()
        self.assertNotEquals(article, Article, "Should reach here")
    
    def test_article_approve_form(self):
        f = ArticleFormApprove()
        self.assertEqual(False, f.is_valid(), "For is invalid")
        
        f = ArticleFormApprove({'is_approved':True}, instance=self.article)
        x = f.is_valid()
        ##print('errors:', f.errors)
        self.assertEqual(True, x , "For is invalid")

class TestViews(TestData):
    #appname = 'review'
    def setUp(self):
        super(TestViews, self).setUp()
        self.article_url = reverse('article-edit', args=[self.article.id])
               
    
    def test_home(self):
        res = self.client.get(reverse('home'))
        self.assertTrue(res.status_code == 200, "Home page is up")
        self.assertContains(res, "User is not")
        
        # Test not login
        #print('html:', res.content)
        self.assertNotContains(res, 'List Aritcle</a>', status_code=200)
        
        
    def test_home_login(self):
        self.client.force_login(self.user) 
        res = self.client.get(reverse('home'))
        ##print('html:', res.content)
        self.assertContains(res, 'List Aritcle</a>', status_code=200)
        
        
    def test_create_article(self):
        
        ###self.assertTrue(self.user.is_active)
        self.client.force_login(self.user)        
        res = self.client.get(reverse('article-create'))
        ##print('html:', res.context)
        
        self.assertTrue(res.status_code == 200)
        self.client.login(username=self.user_name, password=self.user_pw)
        res = self.client.get(reverse('article-create'))
        self.assertContains(res, 'name="title"', status_code=200)
        test_article = {'title': 'testing article', 
                       'description': "From testing case",
                       'url': 'http://www.cholarsip.com/1234324/'}
        
        res = self.client.post(reverse('article-create'), test_article)
        self.assertTrue(res.status_code == 302, res.status_code)
    
    def test_approve_article(self):
        self.client.force_login(self.user)        
        res = self.client.get(self.article_url)
        self.assertTrue(res.status_code == 302, res.status_code)
        
    def test_approve_article_editor(self):
        self.client.force_login(self.editor)
        ##print('self.editor groups:', self.editor.user_permissions.all()[0])        
        res = self.client.get(self.article_url)
        ##self.assertTrue(res.status_code == 200, res.status_code)
        self.assertContains(res, 'name="status"', status_code=200)
        
        
        res = self.client.post(self.article_url, {'status': 'a'})
        self.assertTrue(res.status_code == 302, res.status_code)
        
    
    def test_list_article(self):
        article_list_url = reverse('article-list')
        res = self.client.get(article_list_url)
        self.assertTrue(res.status_code == 302, res.status_code)
        self.client.force_login(self.editor)
        res = self.client.get(article_list_url)
        self.assertTrue(res.status_code == 200, res.status_code)
