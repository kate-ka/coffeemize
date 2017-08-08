from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser


class User(AbstractUser):
    """
    Our a bit changed User model for auth0 purposes.
    We always expect to have email as username.
    """

    def save(self, *args, **kwargs):
        # TODO: check that username is really email
        self.email = self.username
        super(User, self).save(*args, **kwargs)
