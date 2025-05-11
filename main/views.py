from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category, Discount, Seller, ProductSeller
from django.db.models import Min, Max


class CatalogView(ListView):
    model = Product
    template_name = "main/product/list.html"
    # Name of the variable to be used in the template for the list of products
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        # read query parameters from URL
        # /catalog/?category=clothing&discount=summer-sale&min_price=10&max_price=50
        seller_names = self.request.GET.getlist('seller')
        category_slugs = self.request.GET.getlist("category")
        discount_slugs = self.request.GET.getlist("discount")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        # filter using query parameters
        if seller_names:
            # filter using the intermediate model's name
            # django creates the property productseller automatically
            queryset = queryset.filter(productseller__seller__name__in=seller_names).distinct()

        if category_slugs:
            queryset = queryset.filter(category__slug__in=category_slugs)

        if discount_slugs:
            discounts = Discount.objects.filter(slug__in=discount_slugs, is_active=True)

            # Gather products directly linked to discounts
            direct_product_ids = Product.objects.filter(
                discount__in=discounts
            ).values_list("id", flat=True)

            # Gather products from discounted categories
            category_ids = discounts.values_list("categories", flat=True)
            category_product_ids = Product.objects.filter(
                category_id__in=category_ids
            ).values_list("id", flat=True)

            all_discounted_ids = set(direct_product_ids) | set(category_product_ids)

            queryset = queryset.filter(id__in=all_discounted_ids)

        if min_price:
            try:
                min_price_value = float(min_price)
                queryset = [p for p in queryset if p.current_price >= min_price_value]
            except ValueError:
                pass

        if max_price:
            try:
                max_price_value = float(max_price)
                queryset = [p for p in queryset if p.current_price <= max_price_value]
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        """Add extra context variables to the template"""
        context = super().get_context_data(**kwargs)
        context["sellers"] = Seller.objects.all()
        context["categories"] = Category.objects.all()
        context["discounts"] = Discount.objects.all()
        context["selected_categories"] = self.request.GET.getlist("category")
        context["selected_discounts"] = self.request.GET.getlist("discount")
        context["selected_sellers"] = self.request.GET.getlist("seller")
        context["min_price"] = self.request.GET.get("min_price", "")
        context["max_price"] = self.request.GET.get("max_price", "")
        # context["lowest_price"] = Product.objects.aggregate(Min("price"))["price__min"] or 0
        # context["highest_price"] = Product.objects.aggregate(Max("price"))["price__max"] or 0
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product/detail.html"
    context_object_name = "product"
    # Name of the field that has SlugField
    slug_field = "slug"
    # <slug:slug>
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        available_sellers = ProductSeller.objects.filter(
            product=product)
        context['available_sellers'] = available_sellers
        return context


def home(request):
    return render(request, "main/home.html")


def artists(request):
    return render(request, "main/artists.html")