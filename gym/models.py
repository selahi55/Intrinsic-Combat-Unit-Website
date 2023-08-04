from django.db import models
from accounts.models import Trainer, Client

class Course(models.Model):
    name     = models.CharField(max_length=150, unique=True, null=True)
    clients  = models.ManyToManyField(Client, related_name='classes')
    trainers = models.ManyToManyField(Trainer, related_name='courses')

    def __str__(self):
        return self.name   

    # def calculate_client 

    # def calculate_fees_trainers(self):
    #     if self.trainers:
    #         for trainer in self.trainers:
    #             trainer_percent = trainer.percent

class Schedule(models.Model):
    class Days(models.TextChoices):
        MONDAY    = 'M', 'Monday'
        TUESDAY   = 'T', 'Tuesday'
        WEDNESDAY = 'W', 'Wednesday'
        THURSDAY  = 'TH', 'Thursday'
        FRIDAY    = 'F', 'Friday'
        SATURDAY  = 'S', 'Saturday'
        SUNDAY    = 'SU', 'Sunday'
    course        = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="schedules")
    time          = models.TimeField()
    day           = models.CharField(max_length=2, choices=Days.choices)

    # Ensures two courses cannot be scheduled on the same day and time
    class Meta:
        unique_together = (('day', 'time'))

    def __str__(self):
        return f"{self.get_day_display()} at {self.time}"
    
class Video(models.Model):
    caption   = models.CharField(max_length=100)
    videofile = models.FileField(upload_to='videos/', null=True)
    
    def __str__(self):
        return self.caption + ": " + str(self.videofile)


class Post(models.Model):
    pass