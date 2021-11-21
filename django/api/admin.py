from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin
from .models import User, CommunicateInformation

#@admin.register(User_Comm_Info)
class CommunicateInformationInfoInline(admin.StackedInline):
    model = CommunicateInformation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_title', '_email', '_mobile']
    inlines = [CommunicateInformationInfoInline,]

    def _email(self, obj):
        qs = CommunicateInformation.objects.filter(user=obj.id)
        return qs[0].email

    def _mobile(self, obj):
        qs = CommunicateInformation.objects.filter(user=obj.id)
        return qs[0].mobile
