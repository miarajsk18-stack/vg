from django.contrib import admin
from django.utils.html import format_html
from . models import Category, Vegetable, Order

# Register your models here.
@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display=('category_name', )
    ordering=('category_name',)

@admin.register(Vegetable)
class AdminVegetable(admin.ModelAdmin):
    list_display=('name', 'category', 'description', 'price', 'stock', 'image_preview', 'unit')

    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__category_name')
    list_editable = ('price', 'stock')
    ordering = ('-created_at',)

    def image_preview(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return format_html(
                    '<img src="{}" width="50" height="60" style="object-fit:cover;" />',
                    obj.image.url
                )
        except Exception:
            pass
        return "No Image"

    image_preview.short_description = 'Image'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'product', 'quantity', 'payment_status', 'address', 'date_ordered')
    list_filter = ('payment_status', 'date_ordered')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'product__name', 'address')
    ordering = ('-date_ordered',)

    # Custom method to show full name
    def get_user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username  # Fallback to username if name is empty
    get_user_full_name.short_description = 'Order By'