from django.contrib.auth.decorators import login_required
#主要就是来做一个默认的登陆跳转，如果你没有登陆访问其他页面会自动跳转到登陆页面
#只需要用到的页面继承他就可以了
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        #调用父类的as_view
        view=super(LoginRequiredMixin,cls).as_view(**initkwargs)
        return login_required(view)