from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("email must requierd")
        user=self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)

        return user
    

# custom user 

   
class CustomUser(AbstractBaseUser):
    TEACHER =1
    STUDENT =2
    ROLE_CHOICE = (
        (TEACHER,'teacher'),
        (STUDENT,'student'),
    )
    email=models.EmailField(unique=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # requierd fields 
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)   
    is_active=models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]

    objects=UserManager()

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True
