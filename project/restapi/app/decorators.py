from app.utils import user_is_authenticated_with_token, get_response_403_message, user_is_staff


def auth_required(func):
    def wrapped(request, *args, **kwargs):

        if not user_is_authenticated_with_token(request):
            return get_response_403_message(message='Forbidden for you')

        return func(request, *args, **kwargs)

    return wrapped


def is_staff_required(func):
    def wrapped(request, *args, **kwargs):

        if not user_is_staff(request):
            return get_response_403_message(message='Forbidden for you')

        return func(request, *args, **kwargs)

    return wrapped
