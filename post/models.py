from django.db import models
from utils.BaseModel import BaseModel
from common.models import Category
from django.conf import settings
# Create your models here.

STATUSES = [
    ('published', 'Published'),
    ('draft', 'Draft'),    
    ('unpublished', 'Unpublish'),    
]

class Post(BaseModel):
    title = models.CharField(max_length = 50, null=False)
    content = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=15,choices=STATUSES,default=STATUSES[1][0])
    views = models.PositiveIntegerField(default=0)
    excerpt= models.TextField(max_length=200,null=True)
    category_id = models.ManyToManyField(Category,verbose_name = 'Categories',blank=True,related_name='posts')
    user_id=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='User'
    )
    comment_count = models.PositiveIntegerField(default=0)
    def __str__(self) -> str:
        return self.title
    
