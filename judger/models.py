from django.db import models
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User

# Create your models here.
class ProblemTag(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    text=models.CharField(max_length=100,verbose_name='内容')
    color=models.CharField(max_length=20,verbose_name="颜色",default="#6DEF8D")
    class Meta:
        verbose_name='题目标签'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.text

class Task(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    inp=models.TextField(verbose_name='输入',null=True, blank=True)
    ans=models.TextField(verbose_name='答案',null=True, blank=True)
    score=models.IntegerField(default=0)
    class Meta:
        verbose_name='测试点'
        verbose_name_plural=verbose_name
    def __str__(self):
        return str(self.id)

class Problem(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    title=models.CharField(max_length=100,verbose_name='标题')
    text=MDTextField(verbose_name="内容",default="",editable=True)
    islook=models.BooleanField(verbose_name="是否可查看",default=True)
    foruser=models.ForeignKey('auth.User',on_delete=models.DO_NOTHING)
    tags=models.ManyToManyField('ProblemTag')
    tasks=models.ManyToManyField('Task')
    max_time=models.IntegerField(verbose_name="最大时间(ms)",default=1000)
    max_memory=models.IntegerField(verbose_name="最大内存(MB)",default=128)
    islookans=models.BooleanField(verbose_name="是否可查看答案",default=False)
    class Meta:
        verbose_name='题目'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title

class Language(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    name=models.CharField(max_length=100,verbose_name='名称')
    objname=models.CharField(max_length=100,verbose_name='类名')
    isok=models.BooleanField(verbose_name="是否可用",default=True)
    class Meta:
        verbose_name='测评语言'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

Stats_Tasks=(
    ('AC','Accept'),
    ('WA','Wrong Answer'),
    ('CE','Compile Error'),
    ('PC','Partially Correct'),
    ('RE','Runtime Error'),
    ('TLE','Time Limit Exceeded'),
    ('MLE','Memory Limit Exceeded'),
    ('OLE','Output Limit Exceeded'),
    ('UKE','Unknown Error'),
    ('LBE','Libray Error'),
    ('SVE','Sever Error'),
    ('DBE','Databases Error'),
    ('WI','Waiting'),
)

Stats_Record=(
    ('AC','Accept'),
    ('UC','Unaccepted'),
    ('CE','Compile Error'),
    ('JI','Judging'),
)

class Record_Tasks(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    use_time=models.IntegerField(verbose_name="使用时间(s)",default=0)
    use_memory=models.IntegerField(verbose_name="使用内存(MB)",default=0)
    stats=models.CharField(max_length=15,verbose_name="状态",choices=Stats_Tasks,default='WI')
    stdins=models.TextField(verbose_name="输入",null=True, blank=True)
    stdouts=models.TextField(verbose_name="输出",null=True, blank=True)
    stdanss=models.TextField(verbose_name="答案",null=True, blank=True)
    score=models.IntegerField(default=0)
    class Meta:
        verbose_name='子测试点'
        verbose_name_plural=verbose_name
    def __str__(self):
        return str(self.id)

class Record(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    forproblem=models.ForeignKey('Problem',on_delete=models.DO_NOTHING)
    foruser=models.ForeignKey('auth.User',on_delete=models.DO_NOTHING)
    forlanguage=models.ForeignKey('Language',on_delete=models.DO_NOTHING)
    islook=models.BooleanField(verbose_name="是否可查看",default=True)
    islookans=models.BooleanField(verbose_name="是否可查看答案",default=False)
    isok=models.BooleanField(verbose_name="是否测评",default=False)
    use_time=models.IntegerField(verbose_name="使用时间(s)",default=0)
    use_memory=models.IntegerField(verbose_name="使用内存(MB)",default=0)
    upcode=models.TextField(verbose_name="提交代码",null=True, blank=True)
    stats=models.CharField(max_length=15,verbose_name="状态",choices=Stats_Record,default='JI')
    childtask=models.ManyToManyField('Record_Tasks',null=True, blank=True)
    crtime=models.DateTimeField(auto_now=True)
    score=models.IntegerField(default=0)
    outhertings=models.TextField(verbose_name="stderr",null=True, blank=True)
    class Meta:
        verbose_name='测评任务'
        verbose_name_plural=verbose_name
        ordering = ['-crtime']
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        try:
            self.outhertings = self.outhertings.replace("\r\n", "\n")
            self.outhertings = self.outhertings.replace("\n","</br>")
        except Exception as e:
            print(e)
        super(Record, self).save(*args, **kwargs)