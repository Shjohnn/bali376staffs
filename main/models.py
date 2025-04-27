from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 'Staff'  'User' bilan bog'lanadi.
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    bank_account = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='staffs/', blank=True, null=True)

    def __str__(self):
        return self.user.username  # Xodimni username orqali ko‘rsatadi


class WorkTime(models.Model):
    TIME_CHOICES = [
        (f"{hour:02}:{minute:02}", f"{hour:02}:{minute:02}")
        for hour in range(7, 25)
        for minute in [0, 30]
    ]
    date = models.DateField()
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES, blank=True, null=True)
    end_time = models.CharField(max_length=5, choices=TIME_CHOICES, blank=True, null=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE, related_name='worktimes', blank=True, null=True)
    break_time = models.FloatField(default=0)
    @property
    def total_hours(self):
        from datetime import datetime, timedelta
        time_format = "%H:%M"

        if not self.start_time or not self.end_time:
            return 0  # yoki None, yoki "Noma'lum", holatga qarab

        start = datetime.strptime(self.start_time, time_format)
        end = datetime.strptime(self.end_time, time_format)

        # Tugash vaqtining boshlanishdan oldin bo'lishini ko'rib chiqamiz
        if end < start:
            end += timedelta(days=1)

        difference = end - start
        total_hours = difference.total_seconds() / 3600  # Umumiy soatlar hisoblash

        # Dam olish vaqtini ayirish
        if self.break_time and self.break_time > 0:
            total_hours -= self.break_time

        return max(total_hours, 0)  # Salbiy bo'lib qolmasligi uchun 0'dan katta bo'lishini ta'minlash




class Day(models.Model):
    date = models.DateField(unique=True)

    class Meta:
        verbose_name = "Day"
        verbose_name_plural = "Days"

    def __str__(self):
        return str(self.date)

    def worktimes(self):
        return WorkTime.objects.filter(date=self.date)
