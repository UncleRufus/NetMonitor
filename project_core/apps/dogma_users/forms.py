# Utils
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class DogmaUserCreateForm(UserCreationForm):
    """Base user creation form"""

    pass


class DogmaUserCdhangeForm(UserChangeForm):
    """Base user change form"""

    pass
