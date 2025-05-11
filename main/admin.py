from django.contrib import admin
from .models import Product, Category, Discount, \
    ProductImage, Seller, ProductSeller


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductSellerInline(admin.TabularInline):
    model = ProductSeller
    extra = 3


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "description",
        "price",
        "category",
        "stock",
        "is_available",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_available", "category")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    inlines = [ProductImageInline, ProductSellerInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    # Category and product are passed into list_display by default
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
