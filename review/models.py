from django.db import models
from django.contrib.auth import get_user_model
import django
from django.conf import settings 
from django.urls.base import reverse_lazy

User = get_user_model()

class Article(models.Model):
    NOT_APPROVED = 'Not Approved'
    GOT_APPROVED = 'Approved'
    REJECT = 'Rejectd'
    
    STATUS_CHOICES = (
        ('u', NOT_APPROVED),
        ('a', GOT_APPROVED),
        ('r', REJECT),
        )
    
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=NOT_APPROVED,
                              max_length=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='articles')
    
    
    
    def get_absolute_url(self):
        
        url = settings.SITE_URL
        path = reverse_lazy('article-edit', args=[self.id])
        
        return '{0}{1}'.format(url, path)
    
    