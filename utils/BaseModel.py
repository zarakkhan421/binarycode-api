
from django.db import models
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    updated = models.DateTimeField(auto_now_add=True)
    created= models.DateTimeField(auto_now=True)    
    class Meta:
        abstract=True
