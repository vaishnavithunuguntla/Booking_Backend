from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows login with email instead of username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        # Support both "username" and "email" keys
        email = kwargs.get("email", username)
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get(email__iexact=email)  # case-insensitive
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
