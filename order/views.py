from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from cart.models import Cart
from goods.models import Goods
from order.models import Order, OrderDetail
from user.islogin import is_login
from user.models import User
# Create your views here.


@is_login
def order(request):
    """
    订单
    此函数给用户下订单页面展示数据
    接收购物车页面GET方法发过来的购物车中物品的id,构造购物车对象供订单使用
    """
    uid = request.session.get('user_id')
    user = User.objects.get(id=uid)
    # 获取勾选的每一个订单对象,构造成list,作为上下文传入下单页面
    order_id = request.GET.getlist('orderid')
    orderlist = []

    for id in order_id:
        orderlist.append(Cart.objects.get(id=int(id)))
    # 判断用户手机号是否为空,分别做展示
    if user.phone == '':
        phone = ''
    else:
        phone = user.phone[0:4] + '****' + user.phone[-4:]
    # 构造上下文
    context = {'title': '提交订单', 'page_name': 1, 'orderlist': orderlist,
               'user': user, 'ureceive_phone': phone}
    return render(request, 'order/place_order.html', context)


# 装饰器 事务回滚 一旦有一步操作失败,则回滚全部操作
@transaction.atomic()
@is_login
def order_handle(request):
    """订单处理"""
    # 保存一个事物点
    tran_id = transaction.savepoint()
    # 接收购物车编号
    # 根据POST和session获取信息
    # cart_ids = post.get('cart_ids')
    try:
        post = request.POST
        order_list = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')

        order = Order()
        now = datetime.now()
        uid = request.session.get('user_id')
        order.order_id = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.order_user_id = uid
        order.order_date = now
        order.order_total = Decimal(total)
        order.order_address = address
        order.save()

        # 遍历购物车中提交信息,创建订单详情表
        for order_id in order_list:
            cart_o = Cart.objects.get(id=order_id)
            goods_o = Goods.objects.get(pk=cart_o.cart_goods_id)
            # 判断库存是否够
            if int(goods_o.goods_inventory) >= int(cart_o.count):
                # 库存够的话,减去购买的数量并保存
                goods_o.goods_inventory -= int(cart_o.count)
                goods_o.save()
                # 创建订单详情表
                detail = OrderDetail()
                detail.order_goods_id = int(goods_o.id)
                detail.order_id = int(order.order_id)
                detail.order_price = Decimal(int(goods_o.goods_price))
                detail.order_count = int(cart_o.count)
                detail.save()
                # 循环删除购物车对象
                cart_o.delete()
            else:
                # 库存不够触发事务回滚
                transaction.savepoint_rollback(tran_id)
                # 返回json供前台提示失败
                return JsonResponse({'status': 2})
    except Exception as e:
        transaction.savepoint_rollback(tran_id)
    # 返回json供前台提示成功
    return JsonResponse({'status': 1})


@is_login
def pay(request, order_id):
    """支付"""
    tran_id = transaction.savepoint()
    order = Order.objects.get(order_id=order_id)
    order.order_Pay = 1
    order.save()

    context = {'oid': order_id}
    return render(request, 'order/pay.html', context)
