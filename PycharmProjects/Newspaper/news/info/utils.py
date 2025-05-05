# myapp/utils.py
from django.contrib.auth.models import User

def get_user_display(user):
    return user.get_full_name() or user.username