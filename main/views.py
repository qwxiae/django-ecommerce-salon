from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Procedure, Category, Discount, Specialist, ProcedureSpecialist
from django.db.models import Min, Max


class CatalogView(ListView):
    model = Procedure
    template_name = "main/procedure/list.html"
    # Name of the variable to be used in the template for the list of procedures
    context_object_name = "procedures"

    def get_queryset(self):
        queryset = super().get_queryset()
        # read query parameters from URL
        # /catalog/?category=clothing&discount=summer-sale&min_price=10&max_price=50
        specialist_names = self.request.GET.getlist('specialist')
        category_slugs = self.request.GET.getlist("category")
        discount_slugs = self.request.GET.getlist("discount")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        # filter using query parameters
        if specialist_names:
            # filter using the intermediate model's name
            # django creates the property procedurespecialist automatically
            queryset = queryset.filter(procedurespecialist__specialist__name__in=specialist_names).distinct()

        if category_slugs:
            queryset = queryset.filter(category__slug__in=category_slugs)

        if discount_slugs:
            discounts = Discount.objects.filter(slug__in=discount_slugs, is_active=True)

            # Gather procedures directly linked to discounts
            direct_procedure_ids = Procedure.objects.filter(
                discount__in=discounts
            ).values_list("id", flat=True)

            # Gather procedures from discounted categories
            category_ids = discounts.values_list("categories", flat=True)
            category_procedure_ids = Procedure.objects.filter(
                category_id__in=category_ids
            ).values_list("id", flat=True)

            all_discounted_ids = set(direct_procedure_ids) | set(category_procedure_ids)

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
        context["specialists"] = Specialist.objects.all()
        context["categories"] = Category.objects.all()
        context["discounts"] = Discount.objects.all()
        context["selected_categories"] = self.request.GET.getlist("category")
        context["selected_discounts"] = self.request.GET.getlist("discount")
        context["selected_specialists"] = self.request.GET.getlist("specialist")
        context["min_price"] = self.request.GET.get("min_price", "")
        context["max_price"] = self.request.GET.get("max_price", "")
        # context["lowest_price"] = Procedure.objects.aggregate(Min("price"))["price__min"] or 0
        # context["highest_price"] = Procedure.objects.aggregate(Max("price"))["price__max"] or 0
        return context


class ProcedureDetailView(DetailView):
    model = Procedure
    template_name = "main/procedure/detail.html"
    context_object_name = "procedure"
    # Name of the field that has SlugField
    slug_field = "slug"
    # <slug:slug>
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procedure = self.object
        available_specialists = ProcedureSpecialist.objects.filter(
            procedure=procedure)
        context['available_specialists'] = available_specialists
        return context


def home(request):
    return render(request, "main/home.html")


def artists(request):
    return render(request, "main/artists.html")