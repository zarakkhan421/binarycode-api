from django.db import models
from utils.BaseModel import BaseModel
from django.conf import settings
from post.models import Post
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Comment(MPTTModel,BaseModel):
    content = models.TextField(max_length=50,null=False)
    user_id=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='User'
    )
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE,null=False,verbose_name='Post')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    def __str__(self) -> str:
        return self.content[:9]