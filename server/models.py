from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Pathole(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    address = models.CharField(max_length=200)
    size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    location = models.CharField(max_length=50)
    district = models.CharField(max_length=200)
    priority = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)])

    @classmethod
    def create(cls, user, address, size, location, district, priority):
        try:
            pathole = cls(
                user = user, 
                address = address, 
                size = size,
                location = location, 
                district = district, 
                priority = priority)
            pathole.clean_fields()
        except (ValidationError, ValueError):
            return None
        return pathole
