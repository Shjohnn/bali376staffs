from django.contrib import admin
from .models import WorkTime, Staff, Day


# Day sahifasi uchun (staff kerak)
class WorkTimeDayInline(admin.TabularInline):
    model = WorkTime
    extra = 1  # yangi qo'shish uchun qulay bo'ladi
    fields = ('staff', 'start_time', 'end_time', 'total_hours')
    readonly_fields = ('total_hours',)

    def total_hours(self, obj):
        return obj.total_hours if obj else None

    total_hours.short_description = "Total Hours"


# Staff sahifasi uchun (staff kerak emas)
class WorkTimeStaffInline(admin.TabularInline):
    model = WorkTime
    extra = 0
    fields = ('date', 'start_time', 'end_time', 'total_hours')
    readonly_fields = ('date', 'start_time', 'end_time', 'total_hours')
    ordering = ('-date',)

    def total_hours(self, obj):
        return obj.total_hours

    total_hours.short_description = "Total Hours"


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    inlines = [WorkTimeDayInline]  # bu yerda Dayga kirib yangi WorkTime qo'shish mumkin
    list_display = ('date',)


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'start_time', 'end_time', 'total_hours')

    def total_hours(self, obj):
        return obj.total_hours

    total_hours.short_description = "Total Hours"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'bank_account')
    inlines = [WorkTimeStaffInline]  # bu yerda Staffga kirib WorkTime ko'rish mumkin
