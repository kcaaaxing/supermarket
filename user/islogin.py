from django.http import HttpResponseRedirect


def is_login(func):
    """如果登录则转到登录页面"""
    def login_fun(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('url', request.get_full_path)
            return red

    return login_fun
