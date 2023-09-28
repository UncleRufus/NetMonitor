# Utils
from django.contrib.auth.models import BaseUserManager, Group


class DogmaUserManager(BaseUserManager):
    """Custom user model manager"""

    def create_user(self, email: str, password: str, **extra_fileds):
        """Create custom user"""

        extra_fileds.setdefault(
            'is_staff',
            True
        )

        extra_fileds.setdefault(
            'is_active',
            True
        )

        user = self.model(email=email, **extra_fileds)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fileds):
        """Create custom superuser"""

        extra_fileds.setdefault(
            'is_staff',
            True
        )

        extra_fileds.setdefault(
            'is_superuser',
            True
        )

        extra_fileds.setdefault(
            'is_active',
            True
        )

        if extra_fileds.get('is_staff') is not True:
            raise ValueError('SuperUser must have "is_staff"')

        if extra_fileds.get('is_superuser') is not True:
            raise ValueError('SuperUser must have "is_superuser"')

        user = self.create_user(
            email=email,
            password=password,
            **extra_fileds
        )

        administration_group, created = Group.objects.get_or_create(
            name = 'Administaion'
        )

        administration_group.user_set.add(
            user
        )
        return user
