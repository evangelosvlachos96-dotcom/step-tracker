from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    phone = models.IntegerField(null=True, blank=True)


class DaySteps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps_counter = models.BigIntegerField(
        validators=[MaxValueValidator(50000), MinValueValidator(1)])
    day = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'day'],
                name='unique chapter'
            )
        ]

    def __str__(self):
        return "{} | steps: {} | day: {}".format(self.user, self.steps_counter, self.day)
