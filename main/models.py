from django.db import models
from datetime import datetime, timedelta


class Staff(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    bank_account = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='staffs/', blank=True, null=True)

    def __str__(self):
        return self.name


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

    @property
    def total_hours(self):
        from datetime import datetime, timedelta
        time_format = "%H:%M"

        if not self.start_time or not self.end_time:
            return 0  # yoki None, yoki "Noma'lum", holatga qarab

        start = datetime.strptime(self.start_time, time_format)
        end = datetime.strptime(self.end_time, time_format)

        if end < start:
            end += timedelta(days=1)

        difference = end - start
        return difference.total_seconds() / 3600


class Day(models.Model):
    date = models.DateField(unique=True)

    class Meta:
        verbose_name = "Day"
        verbose_name_plural = "Days"

    def __str__(self):
        return str(self.date)

    def worktimes(self):
        return WorkTime.objects.filter(date=self.date)



