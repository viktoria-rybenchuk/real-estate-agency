from django.contrib.auth.models import AbstractUser
from django.db import models

PROPERTY_TYPE_CHOICES = (
    ('House', 'House'),
    ('Apartment', 'Apartment'),
    ('Townhouse', 'Townhouse'),
)


class Agent(AbstractUser):
    pass

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Area(models.Model):
    name = models.CharField(max_length=60)
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="areas", null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_name_of_area"
            )
        ]


class Property(models.Model):
    title = models.CharField(max_length=63)
    price = models.IntegerField()
    address = models.CharField(max_length=63, default=True)
    description = models.TextField()
    property_type = models.CharField(
        max_length=60,
        choices=PROPERTY_TYPE_CHOICES
    )
    is_available = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="properties",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "properties"
        verbose_name = "property"

    def __str__(self) -> str:
        return self.title


class Client(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField()
    phone_number = models.IntegerField()
    is_searching_for_property = models.BooleanField()
    search_area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="clients"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
