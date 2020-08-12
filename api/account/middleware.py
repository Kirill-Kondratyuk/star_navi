from django.utils.timezone import now

from account import models


class SetLastUserRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            profile = models.UserProfile.objects.get(user=request.user)
            profile.last_request = now()
            profile.save()

        return response
