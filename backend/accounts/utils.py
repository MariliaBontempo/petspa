from django.contrib.auth import get_user_model

def get_user_by_email(username):
    User = get_user_model()
    return User.objects.get(email=username) 