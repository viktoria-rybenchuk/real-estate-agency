from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaulttags import url
from django.urls import reverse


class Agent(AbstractUser):
    pass

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> url:
        return reverse("agency:agent-detail", kwargs={"pk": self.pk})


class Deal(models.Model):
    deal = models.CharField(max_length=63, blank=True)
    date = models.DateField(auto_now_add=True)
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="deals"
    )

    def __str__(self) -> str:
        return f"{self.deal} {self.agent} {self.date}"


class Area(models.Model):
    name = models.CharField(max_length=60)
    agent = models.ForeignKey(
        Agent, on_delete=models.SET_NULL,
        null=True,
        related_name="areas"
    )

    def __str__(self) -> str:
        return self.name


class Property(models.Model):
    class PropertyTypeChoices(models.TextChoices):
        House = "House",
        Apartment = "Apartment",
        Townhouse = "Townhouse"

    address = models.CharField(max_length=63)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    property_type = models.CharField(
        max_length=63,
        choices=PropertyTypeChoices.choices
    )
    is_available = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="properties",
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="properties",
        blank=True,
    )

    class Meta:
        verbose_name_plural = "properties"
        verbose_name = "property"

    def __str__(self) -> str:
        return self.address


class Client(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    is_searching_for_property = models.BooleanField()
    additional_info = models.CharField(max_length=255, blank=True)
    search_area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="clients",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email", "phone_number"],
                name="unique_email_and_phone_number"
            )
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
