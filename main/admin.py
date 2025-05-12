from django.contrib import admin
from .models import Procedure, Category, Discount, \
    ProcedureImage, Specialist, ProcedureSpecialist


class ProcedureImageInline(admin.TabularInline):
    model = ProcedureImage
    extra = 3


class ProcedureSpecialistInline(admin.TabularInline):
    model = ProcedureSpecialist
    extra = 3


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name',)


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "description",
        "price",
        "category",
        "is_available",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_available", "category")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    inlines = [ProcedureImageInline, ProcedureSpecialistInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    # Category and procedure are passed into list_display by default
    list_display = (
        "name",
        "slug",
        "percentage",
        "start_date",
        "end_date",
    )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("end_date",)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
