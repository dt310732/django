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


class Part(models.Model):
    PART_UNITS = [
        ("M2", "Square Meters"),
        ("M3", "Cubic Meters"),
        ("SZT", "Sztuki"),
        ("L", "Litres"),
    ]
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="parts",
        null=False
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        related_name="parts",
        null=True
    )
    item_code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    unit = models.CharField(max_length=3, choices=PART_UNITS)
    minimum_stock = models.PositiveIntegerField() # zrobić większe od 0 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        supplier_name = self.supplier.name if self.supplier else "No Supplier"
        return f'{self.name} - {self.category.name} - {supplier_name}'
    

class Location(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
    ("IN", "Przyjęcie"),
    ("OUT", "Wydanie"),
    ("MOVE", "Przesunięcie"),
    ("SCRAP", "Złomowanie"),
    ]
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(null=False)
    note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.part.name} -> {self.location.code}'
    