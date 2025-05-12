from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Specialist(models.Model):
    name = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to="media/procedure/Y/%m/%d", blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]
        # speed up queries sorted by name
        indexes = [models.Index(fields=["name"])]
        verbose_name = "category"
        verbose_name_plural = "categories"


class Discount(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    procedures = models.ManyToManyField("Procedure", blank=True)
    categories = models.ManyToManyField("Category", blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.is_active = self.start_date <= timezone.now() <= self.end_date
        super().save(*args, **kwargs)


class Procedure(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    specialist = models.ManyToManyField(
        Specialist, through="ProcedureSpecialist",
        related_name="procedure",
        blank=True
    )
    # Textfield is longer and unbounded
    description = models.TextField(blank=True)
    # If it’s invalid, the validator raises a ValidationError
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="procedure"
    )
    image = models.ImageField(upload_to="media/procedure/Y/%m/%d", blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        """Return the price after applying active seasonal discounts."""

        price = self.price
        now = timezone.now()

        discounts = Discount.objects.filter(
            start_date__lte=now, end_date__gte=now
        ).filter(models.Q(procedures=self) | models.Q(categories=self.category))

        if discounts.exists():
            for discount in discounts:
                discount_percentage = Decimal(discount.percentage) / Decimal(100)
                if Decimal(0) <= discount_percentage <= Decimal(1):
                    price = price * (1 - discount_percentage)

        # quantize is more precise than round
        return price.quantize(Decimal("0.01"))


class ProcedureImage(models.Model):
    procedure = models.ForeignKey(
        Procedure, related_name="procedure_image", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="media/procedure/Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.procedure.name} - {self.image.name}"


class ProcedureSpecialist(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)

    class Meta:
        # todo: do not allow them to repeat specialists
        unique_together = ("procedure", "specialist")
