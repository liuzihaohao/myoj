from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from .models import *

# Register your models here.
class ProblemTagAdmin(admin.ModelAdmin):
	list_display = ['id','text','color']
	list_display_links = ['id']
	search_fields = ['text','color']
	list_filter=['color']
admin.site.register(ProblemTag,ProblemTagAdmin)

class TaskAdmin(admin.ModelAdmin):
	list_display = ['id','inp','ans']
	list_display_links = ['id']
admin.site.register(Task,TaskAdmin)

class ProblemAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,{'fields':[
            'title','text'
        ]}),
        ('其他设置',{'fields':[
            'max_time','max_memory','islookans','tags','foruser'
        ]}),
        ('关联的测试点',{'fields':[
            'tasks'
        ]}),
    ]
    filter_horizontal=[
        'tasks','tags'
    ]
    list_display = ['id','title','islook']
    list_display_links = ['id']
    search_fields = ['title','text']
admin.site.register(Problem,ProblemAdmin)

class LanguageAdmin(admin.ModelAdmin):
	list_display = ['id','name','objname','isok']
	list_display_links = ['id']
	search_fields = ['name','objname']
admin.site.register(Language,LanguageAdmin)

# class Record_TasksAdmin(admin.ModelAdmin):
# 	list_display = ['id','use_time','use_memory','stats','stdins','stdouts','stdanss']
# 	list_display_links = ['id']
# 	list_filter=['stats']
# admin.site.register(Record_Tasks,Record_TasksAdmin)


@admin.action(description='重新测评')
def run_ag(modeladmin, request, queryset):
    queryset.update(isok=False)

@admin.action(description='判零分')
def run_ag(modeladmin, request, queryset):
    queryset.update(score=0)
    queryset.update(stats='UC')

class RecordAdmin(admin.ModelAdmin):
	actions=[
		run_ag,
	]
	list_display = ['id','forproblem','foruser'\
	,'forlanguage','islook','islookans','isok','use_time'\
	,'use_memory','upcode','stats','crtime']
	list_display_links = ['id']
	search_fields = ['forproblem','foruser','upcode']
	list_filter=['forlanguage','islook','islookans','isok','stats']
admin.site.register(Record,RecordAdmin)

admin.site.site_title="oj Admin"
admin.site.site_header="oj Admin"

# class LogEntryAdmin(admin.ModelAdmin):
# 	list_display = ['action_time','user','content_type','object_id','object_repr','action_flag','change_message']
# admin.site.register(LogEntry,LogEntryAdmin)

# class SessionAdmin(admin.ModelAdmin):
# 	list_display = ['session_key','session_data','expire_date']
# admin.site.register(Session,SessionAdmin)

# class ContentTypeAdmin(admin.ModelAdmin):
# 	list_display = ['app_label','model']
# admin.site.register(ContentType,ContentTypeAdmin)
