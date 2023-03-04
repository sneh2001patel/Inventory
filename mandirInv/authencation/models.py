from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# from inventory.models import Area

class UserManager(BaseUserManager):
    def create_user(self, email, area_incharge=None, full_name=None, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError("Users must have an email address.")
        if not password:
            raise ValueError("Users must have a password.")
        if not full_name:
            raise ValueError("Users must have a name.")

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user_obj.area_incharge = area_incharge
        user_obj.set_password(password)  # chng password from null to user choice
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(email, full_name, password=password, is_staff=True)
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(email, full_name, password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    area_incharge = models.CharField(max_length=300, blank=True, null=True)
    # area_incharge = models.ManyToManyField(invmodel.Area)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_area_incharge(self):
        s = str(self.area_incharge)
        arr = s.split(", ")
        return arr

    def get_full_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
