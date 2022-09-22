from django.db import models


# Create your models here.
class TestApp(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()

    def __str__(self) -> str:
        return self.name
