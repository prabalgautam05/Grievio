# app1/authentication_backends.py
from django.contrib.auth.backends import BaseBackend
from .models import Assign

class AssignBackend(BaseBackend):
    def authenticate(self, request, email=None, id=None):
        try:
            user = Assign.objects.get(email=email, id=id)
            return user
        except Assign.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Assign.objects.get(pk=user_id)
        except Assign.DoesNotExist:
            return None
