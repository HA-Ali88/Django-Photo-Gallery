from django.contrib.auth.models import User
from account.models import Profile

def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    Profile.objects.get_or_create(user=user)
    
class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        

    def get_user(self, uid):
        try:
            user = User.objects.get(pk=uid)
            return user
        except User.DoesNotExist:
            return None
    