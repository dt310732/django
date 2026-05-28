from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    tax_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30, blank=True)
    website = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Part(models.Model):
    PART_UNITS = [
        ("M2", "Square Meters"),
        ("M3", "Cubic Meters"),
        ("SZT", "Sztuki"),
        ("L", "Litres"),
    ]
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="parts",
        null=False
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        related_name="parts",
        null=True
    )
    locations = models.ManyToManyField(
        Location,
        through="PartLocation",
        related_name="parts",
        blank=True
    )
    item_code = models.CharField(max_length=100 ,unique=True, blank=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    unit = models.CharField(max_length=3, choices=PART_UNITS)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
class PartLocation(models.Model):
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name="part_locations"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="part_locations"
    )


    quantity = models.PositiveIntegerField(default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["part", "location"],
                name= "unique_part_location"
            )
        ]

    def __str__(self):
        return f"{self.part.item_code} - {self.location.code} - {self.quantity}"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
    ("IN", "Przyjęcie"),
    ("OUT", "Wydanie"),
    ("MOVE", "Przesunięcie"),
    ("SCRAP", "Złomowanie"),
    ]

    part_location = models.ForeignKey(
        PartLocation,
        on_delete=models.PROTECT,
        related_name="stock_movement",
        null=True,
        blank=True
    )
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(null=False)
    note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.part.name} -> {self.location.code}'
    