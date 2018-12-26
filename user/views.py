from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from order.models import Order
from user.models import User
# from hashlib import sha1
# Create your views here.


def register(request):
    """注册"""
    if request.method == 'POST':
        # 接收用户信息
        post = request.POST
        name = post.get('user_name')
        password = post.get('pwd')
        password2 = post.get('cpwd')
        email = post.get('email')
        # 判断两次密码
        if password != password2:
            return redirect('/user/register')
        # 密码加密
        # s1 = sha1()
        # s1.update(password.encode("utf-8"))
        # password3 = s1.hexdigest()
        """创建user/models的对象"""
        user = User()
        user.name = name
        user.password = password
        user.email = email
        user.save()
        """注册成功,转到登录页面"""
        return redirect('/user/login')
    return render(request, 'user/register.html')


def register_exist(requset):
    """判断用户是否已经存在"""
    name = requset.GET.get('uname')
    count = User.objects.filter(name=name).count()
    return JsonResponse({'count': count})


def login(request):
    """登录"""
    uname = request.COOKIES.get('uname', '')
    """登录校验"""
    if request.method == 'POST':
        # 接收请求信息
        post = request.POST
        username = post.get('username')
        password = post.get('pwd')
        remember = post.get('jizhu', 0)
        """根据用户名查询对象"""
        user = User.objects.filter(name=username)
        # print(username)
        # 判断如果未查到则用户名错，查到再判断密码是否正确，正确则转到用户中心
        if len(user) == 1:
            # 密码加密
            # s1 = sha1()
            # s1.update(password.encode("utf-8"))
            # password2 = s1.hexdigest()
            # 登录带cookie值   必须 red = HttpResponseRedirect    red.set_cookie  renturn red
            if password == user[0].password:
                red = HttpResponseRedirect('/')
                # print '*'*10
                # print count
                # 记住用户名
                if remember != 0:
                    red.set_cookie('uname', username)
                else:
                    red.set_cookie('uname', '', max_age=-1)

                request.session['user_id'] = user[0].id
                request.session['user_name'] = username
                return red
            else:
                context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': username}
                return render(request, 'user/login.html', context)
        else:
            context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': username}
            return render(request, 'user/login.html', context)

    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'user/login.html', context)


def info(request):
    # 从模型中获取用户的email
    email = User.objects.get(id=request.session['user_id']).email

    context = {'title': '天天生鲜用户中心', 'user_email': email, 'user_name': request.session['user_name']}
    return render(request, 'user/user_center_info.html', context)


def site(request):
    """从模型中获取当前用户信息"""
    user = User.objects.get(id=request.session['user_id'])
    user_address = user.address
    user_addressee = user.addressee
    user_phone = user.phone
    user_post_code = user.post_code
    if request.method == 'POST':
        """接收表单信息"""
        user.address = request.POST.get('uaddress')
        user.addressee = request.POST.get('ushou')
        user.post_code = request.POST.get('uyoubian')
        user.phone = request.POST.get('uphone')
        user.save()

        return HttpResponseRedirect('/user/site/')

    context = {'user_address': user_address, 'user_addressee': user_addressee,
               'user_phone': user_phone, 'user_post_code': user_post_code}
    return render(request, 'user/user_center_site.html', context)


def user_center_order(request, page_id):
    """
    此页面用于展示用户提交的订单,由购物车页面下单后调转过来
    也可以从个人信息页面查看,根据用户订单是否支付,下单顺序进行排序
    """
    user_id = request.session.get('user_id')
    # 订单信息 根据是否支付,下单顺序进行排序
    order = Order.objects.filter(order_user_id=user_id).order_by('order_Pay', '-order_id')
    """分页, 获取order list 以两个为一页的list"""
    paginator = Paginator(order, 2)
    # 获取上面集合的第page_id个值
    order_list = paginator.page(int(page_id))
    # 获取一共多少页
    page_list = paginator.page_range
    """上一页(Previous page) 当前页(current page) 下一页(Next page)"""
    page_previous = 0
    page_next = 0
    page_current = int(page_id)
    len_page_list = len(page_list)
    if page_current > 1:
        page_previous = page_current - 1
    if page_current < len_page_list:
        page_next = page_current + 1

    # 构造上下文
    context = {'page_name': 1, 'title': '全部订单', 'page_id': page_current,
               'order': 1, 'order_list': order_list, 'page_list': page_list, 'page_previous': page_previous,
               'page_next': page_next, 'len_page_list': len_page_list}

    return render(request, 'user/user_center_order.html', context)


def logout(request):
    """清除session"""
    request.session.flush()

    return HttpResponseRedirect(reverse('index'))
