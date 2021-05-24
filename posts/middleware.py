from .models import Profile

from django.contrib.auth.models import User


class SetLastRequestMiddleware:
    """The middleware for set user`s last request"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            user.profile = Profile.objects.get_or_create(user=user)[0]
            user.profile.save()
            user.save()
        return response
