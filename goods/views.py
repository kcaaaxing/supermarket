from django.core.paginator import Paginator
from django.shortcuts import render
from goods.models import Goods, Type


# Create your views here.
# 查询每类商品最新的4个和点击率最高的4个


def index(request):
    """
    index函数负责查询页面中需要展示的商品内容,
    主要是每类最新的4种商品和4种点击量最高的商品
    每类商品需要查询2次
    """
    goods = Goods()
    carts_count = request.session.get('count')
    fruit = Goods.objects.filter(goods_type_id=2).order_by('-id')[:4]
    fruit_click = Goods.objects.filter(goods_type_id=2).order_by('-goods_click')[:4]
    seafood = Goods.objects.filter(goods_type_id=4).order_by('-id')[:4]
    seafood_click = Goods.objects.filter(goods_type_id=4).order_by('-goods_click')[:4]
    meat = Goods.objects.filter(goods_type_id=1).order_by('-id')[:4]
    meat_click = Goods.objects.filter(goods_type_id=1).order_by('-goods_click')[:4]
    egg = Goods.objects.filter(goods_type_id=5).order_by('-id')[:4]
    egg_click = Goods.objects.filter(goods_type_id=5).order_by('-goods_click')[:4]
    vegetables = Goods.objects.filter(goods_type_id=3).order_by('-id')[:4]
    vegetables_click = Goods.objects.filter(goods_type_id=3).order_by('-goods_click')[:4]
    frozen = Goods.objects.filter(goods_type_id=6).order_by('-id')[:4]
    frozen_click = Goods.objects.filter(goods_type_id=6).order_by('-goods_click')[:4]
    # 构造上下文
    context = {
        'title': '首页', 'fruit': fruit, 'fish': seafood, 'meat': meat, 'egg': egg,
        'vegetables': vegetables, 'frozen': frozen, 'fruit2': fruit_click, 'fish2': seafood_click,
        'meat2': meat_click, 'egg2': egg_click, 'vegetables2': vegetables_click, 'frozen2': frozen_click,
        'guest_cart': 1, 'page_name': 0, 'count': carts_count, 'g': goods
    }

    return render(request, 'goods/index.html', context)


def detail(request, n):
    """
    显示商品的详细信息
    """
    # 建立商品模型的对象
    goods = Goods.objects.get(pk=int(n))
    goods.goods_click = goods.goods_click + 1
    goods.save()
    # type = TypeInfo
    gtype = goods.goods_type
    count = request.session.get('count')
    news = goods.goods_type.goods_set.order_by('-id')[0:2]

    context = {
        'g': goods, 'title': gtype.title, 'guest_cart': 1,
        'newgood': news, 'id': id, 'isDetail': True, 'list': 1,
        'goodtype': gtype, 'count': count
    }

    response = render(request, 'goods/detail.html', context)

    """
    使用cookies记录最近浏览的商品id
    获取cookies
    获取当前点击商品id
    判断cookies中商品id是否为空
    分割出每个商品id
    判断商品是否已经存在于列表
    存在则移除
    在第一位添加
    判断列表数是否超过5个
    超过五个则删除第6个
    添加商品id到cookies
    第一次添加,直接追加
    """
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d' % goods.id
    if goods_ids != '':
        goods_id_list = goods_ids.split(',')
        if goods_id_list.count(goods_id) >= 1:
            goods_id_list.remove(goods_id)
        goods_id_list.insert(0, goods_id)
        if len(goods_id_list) >= 6:
            del goods_id_list[5]
        goods_ids = ','.join(goods_id_list)
    else:
        goods_ids = goods_id

    response.set_cookie('goods_ids', goods_ids)
    return response


# 商品列表
def goods_list(request, typeid, page_id, sort):
    """
    goodlist函数负责展示某类商品的信息。
    url中的参数依次代表
    typeid:商品类型id;selectid:查询条件id，1为根据id查询，2位根据价格查询，3位根据点击量查询
    """
    goods = Goods()
    count = request.session.get('count')
    # 获取最新发布的商品
    new_good = Goods.objects.all().order_by('-id')[:2]
    # 根据条件查询所有商品
    if sort == '1':  # 按最新   gtype_id  , gtype__id  指typeinfo_id
        sum_good_list = Goods.objects.filter(
            goods_type_id=typeid).order_by('-id')
    elif sort == '2':  # 按价格
        sum_good_list = Goods.objects.filter(
            goods_type_id=typeid).order_by('goods_price')
    elif sort == '3':  # 按点击量
        sum_good_list = Goods.objects.filter(
            goods_type_id=typeid).order_by('-goods_click')
    # 分页
    paginator = Paginator(sum_good_list, 15)
    good_list = paginator.page(int(page_id))
    index_list = paginator.page_range
    # print index_list    xrange(1,2)
    # 确定商品的类型
    goodtype = Type.objects.get(id=typeid)
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()
    # 构造上下文  'count': count,
    context = {'title': '商品详情',  'list': 1,
               'guest_cart': 1, 'goodtype': goodtype,
               'newgood': new_good, 'goodList': good_list,
               'typeid': typeid, 'sort': sort,
               'pindexlist': index_list, 'pageid': int(page_id), 'count': count, 'g': goods}

    # 渲染返回结果
    return render(request, 'goods/list.html', context)
