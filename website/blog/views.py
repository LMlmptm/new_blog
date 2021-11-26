from django.shortcuts import render
from blog.models import Entry, Category, Tag
import markdown
from django import forms
from django.db.models import Q
from django.core.paginator import Paginator
import pygments
from django.shortcuts import get_object_or_404
from django_comments.models import Comment
from django_comments import models as comment_models

import re
from blog.models import User, FileUpdate
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as log
from utils.mixin import LoginRequiredMixin
# Create your views here.

# def make_paginator(objects, page, num=5):
#     paginator = Paginator(objects, num)
#     try:
#         object_list = paginator.page(page)
#     except PageNotAnInteger:
#         object_list = paginator.page(1)
#     except EmptyPage:
#         object_list = paginator.page(paginator.num_pages)
#     return object_list, paginator


# def pagination_data(paginator, page):
#     """
#     用于自定义展示分页页码的方法
#     :param paginator: Paginator类的对象
#     :param page: 当前请求的页码
#     :return: 一个包含所有页码和符号的字典
#     """
#     if paginator.num_pages == 1:
#         # 如果无法分页，也就是只有1页不到的内容，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
#         return {}
#     # 当前页左边连续的页码号，初始值为空
#     left = []
#
#     # 当前页右边连续的页码号，初始值为空
#     right = []
#
#     # 标示第 1 页页码后是否需要显示省略号
#     left_has_more = False
#
#     # 标示最后一页页码前是否需要显示省略号
#     right_has_more = False
#
#     # 标示是否需要显示第 1 页的页码号。
#     # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
#     # 其它情况下第一页的页码是始终需要显示的。
#     # 初始值为 False
#     first = False
#
#     # 标示是否需要显示最后一页的页码号。
#     # 需要此指示变量的理由和上面相同。
#     last = False
#
#     # 获得用户当前请求的页码号
#     try:
#         page_number = int(page)
#     except ValueError:
#         page_number = 1
#     except:
#         page_number = 1
#
#     # 获得分页后的总页数
#     total_pages = paginator.num_pages
#
#     # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
#     page_range = paginator.page_range
#
#     if page_number == 1:
#         # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
#         # 此时只要获取当前页右边的连续页码号，
#         # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
#         # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
#         right = page_range[page_number:page_number + 4]
#
#         # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
#         # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
#         if right[-1] < total_pages - 1:
#             right_has_more = True
#
#         # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
#         # 所以需要显示最后一页的页码号，通过 last 来指示
#         if right[-1] < total_pages:
#             last = True
#
#     elif page_number == total_pages:
#         # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
#         # 此时只要获取当前页左边的连续页码号。
#         # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
#         # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
#         left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
#
#         # 如果最左边的页码号比第 2 页页码号还大，
#         # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
#         if left[0] > 2:
#             left_has_more = True
#
#         # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
#         # 所以需要显示第一页的页码号，通过 first 来指示
#         if left[0] > 1:
#             first = True
#     else:
#         # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
#         # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
#         left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
#         right = page_range[page_number:page_number + 2]
#
#         # 是否需要显示最后一页和最后一页前的省略号
#         if right[-1] < total_pages - 1:
#             right_has_more = True
#         if right[-1] < total_pages:
#             last = True
#
#         # 是否需要显示第 1 页和第 1 页后的省略号
#         if left[0] > 2:
#             left_has_more = True
#         if left[0] > 1:
#             first = True
#
#     data = {
#         'left': left,
#         'right': right,
#         'left_has_more': left_has_more,
#         'right_has_more': right_has_more,
#         'first': first,
#         'last': last,
#     }
#     return data

def login(request):
    """登陆"""
    if 'username' in request.COOKIES:  # 如果用户前次登陆勾选记住用户名
        username = request.COOKIES.get('username')
        checked = 'checked'
    else:
        username = ''
        checked = ''
    return render(request, 'blog/login.html', {'username': username, 'checked': checked})

def Logout(request):
    """注销"""
    logout(request)
    return redirect(reverse('blog:index'))


def register(request):
    """注册"""

    return render(request,'blog/register.html',locals())



def register_handle(request):
    '''用户注册验证'''
    #获取注册信息
    username=request.POST.get('user_name')
    password=request.POST.get('pwd')
    cpassword=request.POST.get('cpwd')
    email=request.POST.get('email')
    allow=request.POST.get('allow')

    #进行用户信息校验 all方法就是用来判断3个信息是否一致，都一致为真返回true，否之，false
    if not all([username,password,email]):
        return render(request,'blog/register.html',{'errmsg':'数据不完整'})
    
    #用户密码校验
    if password !=cpassword:
        return render(request,'blog/register.html',{'errmsg':'前后输入密码不一致'})

    if len(password)<=6:
        return render(request,'blog/register.html',{'errmsg':'用户密码最少6位'})

    if len(password)>=12:
        return render(request,'blog/register.html',{'errmsg':'用户密码最多12位'})


    #主要就是用来校验邮箱是否合法，
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request,'blog/register.html',{'errmsg':'邮箱不合法'})

    #校验用户是否勾选同意协议
    if allow!='on':
        return render(request,'blog/register.html',{'errmsg':'请勾选协议'})
#判断注册用户是否以存在，如果不存在就值为空，因为如果查找不到回抛出异常
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user=None
    if user:
        return render(request,'blog/register.html',{'errmsg':'用户名已存在'})

    #将注册信息添加到数据库表中
    user=User.objects.create_user(username,email,password)
    # user=User()
    # user.username=username
    # user.password=password
    # user.email=email
    # #将用户激活状态值为0，因为我们创建默认是激活的
    user.is_active=0
    user.save()
    #用户邮箱发送激活验证，验证通过就激活，根据唯一标识id来判断是哪个用户
    #发送的，对用户的id进行加密，防止发生安全隐患
    serializer=Serializer(settings.SECRET_KEY,3600)#加密方式，加密时间
    info={'confirm':user.id}#获取用户id
    token=serializer.dumps(info)#对用户id进行加密
    token=token.decode()#默认加密后是byte类型，解密为utf8
    #发送邮件
    subject='懿曼博客给你一封邮件'#邮件主题
    message=''#邮件内容
    sendir=settings.EMAIL_FROM#发送方
    receiver=[email]
    html_message='<h1>%s,懿曼博客欢迎你到来</h1>请点击以下链接进行激活<br/><a href="http://www.yiman.info/active/%s">点击我进行激活</a>'%(username,token)
    send_mail(subject=subject,message=message,from_email=sendir,recipient_list=receiver,html_message=html_message)

    #防止url逆向，
    return redirect(reverse('blog:index'))

def Active(request,token):
    """激活用户"""
    #对用户信息进行解密
    serializer=Serializer(settings.SECRET_KEY,3600)
    try:
        info=serializer.loads(token)
        user_id=info['confirm']#获取解密id
        user=User.objects.get(id=user_id)#获取用户信息
        user.is_active=1#激活
        user.save()
        #跳转到登陆页面
        return redirect(reverse('blog:login'))
    except SignatureExpired as e:
        return HttpResponse('对不起，激活时间过期')

def login_active(request):
    """登陆验证"""
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    remember = request.POST.get('remember')
    # 判断用户数据的完整性
    if not all([username, password]):
        return render(request, 'blog/login.html', {'errmsg': '请输入登陆账号或者密码'})
    # 判断用户信息是否正确，这里我们使用django默认的认证系统，可以对我们加密的用户密码进行解码
    user = authenticate(username=username, password=password)

    if user is not None:
        # 表示用户信息正确
        if user.is_active:
            # 记录用户的登陆状态，如果用户已经激活 login是django默认的
            log(request, user)
            # 获取登陆后要跳转的地址 next对应的值就是要跳转的下一个地址，如果没有那个地址了，默认跳到主页
            next_url = request.GET.get('next', reverse('blog:index'))
            response = redirect(next_url)
            if remember == 'on':  # 如果勾选记住用户名
                response.set_cookie('username', username, max_age=20)
            else:
                response.delete_cookie(username)
            # 跳转到首页
            return response

        else:  # 用户没有激活
            return render(request, 'blog/login.html', {'errmsg': '你好你的账户未激活'})

    else:  # 用户信息不正确
        return render(request, 'blog/login.html', {'errmsg': '密码或者账号不正确'})
#import pysnooper
#@pysnooper.snoop()
def index(request):
    """首页"""
    entries = Entry.objects.all().order_by('-id')
    # print(entries)
    # page = request.GET.get('page')
    # print(page)
    # paginator = Paginator(entries, 2)
    # try:
    #     int(page)
    # except Exception as e:
    #     page = 1
    # if int(page) > paginator.num_pages:
    #     page = 1
    # entry_list = paginator.page(page)  # 获取当前页面的所有商品
    # number_pages = paginator.num_pages  # 获取总页数
    # if number_pages <= 5:
    #     pages = range(1, number_pages + 1)
    # elif int(page) <= 3:
    #     pages = range(1, 6)
    # elif number_pages - int(page) <= 2:
    #     pages = range(number_pages - 4, number_pages + 1)
    # else:
    #     pages = range(int(page) - 2, int(page) + 3)
    #
    # print(pages)
    #
    # content = {'entries': entries,
    #            'pages': pages,
    #            'entry_list': entry_list}

    return render(request, 'blog/index.html', locals())


# def index(request):
#     entries = Entry.objects.all()
#     page = request.GET.get('page', 1)
#     entry_list, paginator = make_paginator(entries, page)
#     page_data = pagination_data(paginator, page)
#
#     return render(request, 'blog/index.html', locals())

def detail(request, blog_id):
    """详情页"""
    # entry = Entry.objects.get(id=blog_id)
    # user=request.user
    # if not user.is_authenticated:
    #     return render(request,'blog/login.html',{})
    comments = Comment.objects.filter(object_pk=blog_id)
    entry=get_object_or_404(Entry,id=blog_id)
    entry.increase_visiting()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',      
    ])
    entry.body = md.convert(entry.body)
    return render(request, 'blog/detail.html', locals())


def category(request,category_id):
    """分类"""
    # categories=Category.objects.get(id=category_id)
    categories=get_object_or_404(Category,id=category_id)
    entries=Entry.objects.filter(category=categories)
    # page = request.GET.get('page')
    # print(page)
    # paginator = Paginator(entries, 2)
    # try:
    #     int(page)
    # except Exception as e:
    #     page = 1
    # if int(page) > paginator.num_pages:
    #     page = 1
    # entry_list = paginator.page(page)  # 获取当前页面的所有商品
    # number_pages = paginator.num_pages  # 获取总页数
    # if number_pages <= 5:
    #     pages = range(1, number_pages + 1)
    # elif int(page) <= 3:
    #     pages = range(1, 6)
    # elif number_pages - int(page) <= 2:
    #     pages = range(number_pages - 4, number_pages + 1)
    # else:
    #     pages = range(int(page) - 2, int(page) + 3)
    #
    # print(pages)
    #
    # content = {'entries': entries,
    #            'pages': pages,
    #            'entry_list': entry_list}

    return render(request, 'blog/index.html', locals())


def tag(request,tag_id):
    """标签"""
    # tags=Tag.objects.get(id=tag_id)
    tags=get_object_or_404(Tag,id=tag_id)
    if tags.name=='全部':
        entries=Entry.objects.all()
    else:
     entries=Entry.objects.filter(tag=tags)
    # page = request.GET.get('page')
    # print(page)
    # paginator = Paginator(entries, 2)
    # try:
    #     int(page)
    # except Exception as e:
    #     page = 1
    # if int(page) > paginator.num_pages:
    #     page = 1
    # entry_list = paginator.page(page)  # 获取当前页面的所有商品
    # number_pages = paginator.num_pages  # 获取总页数
    # if number_pages <= 5:
    #     pages = range(1, number_pages + 1)
    # elif int(page) <= 3:
    #     pages = range(1, 6)
    # elif number_pages - int(page) <= 2:
    #     pages = range(number_pages - 4, number_pages + 1)
    # else:
    #     pages = range(int(page) - 2, int(page) + 3)
    #
    # print(pages)
    #
    # content = {'entries': entries,
    #            'pages': pages,
    #            'entry_list': entry_list}

    return render(request, 'blog/index.html', locals())


def search(request):
    """搜索"""
    keyword=request.GET.get('keyword',None)
    if not keyword:
        errormsg='请输入关键字搜索'
        return render(request,'blog/index.html',locals())
    entries=Entry.objects.filter(Q(title__icontains=keyword)|Q(body__icontains=keyword)|Q(abstract__icontains=keyword))
    return render(request,'blog/index.html',locals())


def archives(request,year,month):
    """归档"""
    entries=Entry.objects.filter(created_time__year=year,created_time__month=month)
    return render(request,'blog/index.html',locals())


def Not_page_found_404(request,exception):
    """404"""
    return render(request,'404.html',locals())

def Page_error_500(request):
    """500"""
    entries=Entry.objects.filter()
    return render(request,'500.html',locals())

def Not_page_found_403(request,exception):
    """403"""
    return render(request,'403.html',locals())


def reply(request, comment_id):
    """回复"""
    user = request.user
    if not user.is_authenticated:
        return render(request, 'blog/login.html', locals())
    parent_comment = get_object_or_404(comment_models.Comment, id=comment_id)
    return render(request, 'blog/reply.html', locals())


def My_blog(request):
    """我的博客"""
    return render(request,'blog/my_blog.html',locals())


def myimages(request):
    """我的博客"""
    return render(request,'blog/man.html',locals())


class UserForm(forms.Form):
    name = forms.CharField()
    # update_time = forms.DateTimeField()
    files = forms.FileField()

# import pysnooper
# @pysnooper.snoop()
def register_form(request):
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            #获取表单信息
            name = uf.cleaned_data['name']
            files = uf.cleaned_data['files']
            #写入数据库
            user = FileUpdate()
            user.name = name
            user.files = files
            user.save()
            entries = Entry.objects.all().order_by('-id')
            return render(request,'blog/index.html',locals())
    else:
        uf = UserForm()
        ur= User.objects.order_by('id')
        return render(request,'blog/upload_file.html',{'uf':uf})

def File_Show(request):
    file_objs = FileUpdate.objects.all()
    print("file_objs_id",file_objs[0].id)
    return render(request,'blog/file_download.html',locals())

def File_Download(request, file_id):
    from django.http import StreamingHttpResponse
    from website.settings import MEDIA_ROOT
    import os
    files = FileUpdate.objects.filter(id=file_id)

    file_name = files[0].files
    file_path = os.path.join(MEDIA_ROOT, str(file_name))  # 下载文件的绝对路径

    if not os.path.isfile(file_path):  # 判断下载文件是否存在
        return HttpResponse("Sorry but Not Found the File")

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = StreamingHttpResponse(file_iterator(file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
    except:
        return HttpResponse("Sorry but Not Found the File")

    return response



