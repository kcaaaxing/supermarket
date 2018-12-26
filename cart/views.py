from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from user.islogin import is_login

# Create your views here.


@is_login
def cart(request):
    """购物车"""
    uid = request.session['user_id']
    cart_o = Cart.objects.filter(cart_user_id=uid)
    length = len(cart_o)

    context = {'carts': cart_o, 'title': '购物车', 'page_name': 1, 'len': length}
    return render(request, 'cart/cart.html', context)


@is_login
def add(request, goods_id, count):
    """添加商品"""
    # 用户uid购买了goods_id商品,数量为count
    uid = request.session['user_id']
    goods_id = int(goods_id)
    count = int(count)
    # 查询购物车是否已经有此商品,有则增加
    carts = Cart.objects.filter(cart_user_id=uid, cart_goods_id=goods_id)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        # 不存在则直接加
        cart = Cart()
        cart.cart_user_id = uid
        cart.cart_goods_id = goods_id
        cart.count = count

    cart.save()
    count_o = Cart.objects.filter(cart_user_id=uid).count()
    request.session['count'] = count_o
    # 如果ajax请求则返回json,否则转向购物车
    if request.is_ajax():
        return JsonResponse({'count': count_o})
    else:
        return redirect('/cart/')


@is_login
def edit(request, cart_id, count):
    """编辑"""
    try:
        cart = Cart.objects.get(pk=int(cart_id))
        count_o = cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count_o}
    return JsonResponse(data)


@is_login
def delete(request, cart_id):
    """删除"""
    cart = Cart.objects.get(pk=int(cart_id))
    cart.delete()
    count = Cart.objects.filter(cart_user_id=request.session['user_id']).count()
    request.session['count'] = count
    data = {'count': count}
    return JsonResponse(data)
