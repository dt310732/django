from django.contrib import admin
from .models import Category, Supplier, Part, Location, StockMovement, PartLocation

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(StockMovement)

class PartLocationInline(admin.TabularInline):
    model = PartLocation
    extra = 1

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("item_code", "name", "unit", "is_active")
    search_fields = ("item_code", "name")
    inlines = [PartLocationInline]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    search_fields = ("code", "name")
    inlines = [PartLocationInline]

@admin.register(PartLocation)
class PartLocationAdmin(admin.ModelAdmin):
    list_display = ("part", "location", "quantity", "is_default")
    search_fields = ("part__item_code", "part__name", "location__code")