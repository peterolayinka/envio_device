from django.contrib import admin

# Register your models here.

from .models import Customer, Device, Reading

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    raw_id_fields = ["device", "customer"]


admin.site.register(Customer)
admin.site.register(Device)