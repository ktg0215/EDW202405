# user/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class IDBackend(ModelBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
