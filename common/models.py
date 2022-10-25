from email.policy import default
from random import choices
from django.db import models
from utils.BaseModel import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils.translation import gettext_lazy as _

# Create your models here.

ROLES=[
    ('admin','Admin'),
    ('editor',"Editor"),
    ('writer','Writer'),
    ('reader',"Reader")
]   
#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(BaseModel,AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  role = models.CharField(max_length=15,null=False,blank=False,choices=ROLES,default=ROLES[3][0])
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
class Category(MPTTModel,BaseModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class Meta:
        verbose_name_plural='Categories'
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __str__(self) -> str:
        return self.name
    