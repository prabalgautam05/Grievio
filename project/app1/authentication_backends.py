from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Assign

class AssignBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            worker = Assign.objects.get(email=username)
            user = worker.user  # Get the associated User instance
            if user and user.check_password(password):
                # Return the User instance on successful authentication
                return user
        except Assign.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
