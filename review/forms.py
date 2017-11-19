from django.forms import ModelForm
from review.models import Article


        
        
class ArticleFormCreate(ModelForm):
    
    class Meta:
        exclude = ('status', 'owner', )
        model = Article
        
        
class ArticleFormApprove(ModelForm):
    class Meta:
        fields = ('status',)
        model = Article
    