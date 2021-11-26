from django.db import models
# from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    '''用户模型类'''
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateField(auto_now=True, verbose_name='更新时间')
    is_detele = models.BooleanField(default=False, verbose_name='删除标记')
    class Meta:
        db_table='df_user'
        verbose_name='用户'#这个生成的是“用户s”
        verbose_name_plural=verbose_name#这个可以将后面s去掉

#导航分类
class Category(models.Model):
    name=models.CharField(max_length=128,verbose_name='博客分类')
    def __str__(self):#返回对象的名称
        return self.name
    class Meta:#返回表的名称
        verbose_name='博客分类'
        verbose_name_plural='博客分类'

#标签
class Tag(models.Model):
    name=models.CharField(max_length=128,verbose_name='博客标签')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='博客标签'
        verbose_name_plural='博客标签'

#文章
class Entry(models.Model):
    # user = models.ForeignKey('User', verbose_name='作者', on_delete=models.CASCADE)
    title=models.CharField(max_length=128,verbose_name='博客标题')
    user=models.ForeignKey('User',verbose_name='博客作者',on_delete=models.CASCADE)
    img=models.ImageField(upload_to='blog_images',null=True,blank=True,verbose_name='博客图片')
    body = models.TextField(verbose_name='博客正文')
    abstract=models.TextField(max_length=256,null=True,blank=True,verbose_name='博客摘要')
    visiting=models.PositiveIntegerField(default=0,verbose_name='博客访问量')
    category=models.ManyToManyField('Category',verbose_name='博客分类')
    tag=models.ManyToManyField('Tag',verbose_name='博客标签')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modified_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_id': self.id})  # http://127.0.0.1/blog/3

    # def  get_absolute_url(self):
    #     return

#访问量增加
    def increase_visiting(self):
        self.visiting+=1
        self.save(update_fields=['visiting'])

    class Meta:
        ordering=['-created_time']#排序
        verbose_name='博客'
        verbose_name_plural='博客'



#文件上传
class FileUpdate(models.Model):
    name=models.CharField(max_length=128,verbose_name='文件名称')
    update_time=models.DateTimeField(auto_now_add=True,verbose_name='提交时间')
    files = models.FileField(upload_to='blog_images',null=True,blank=True,verbose_name='博客文件')
    def __str__(self):#返回对象的名称
        return self.name
    class Meta:#返回表的名称
        verbose_name='博客文件'
        verbose_name_plural='博客文件'
