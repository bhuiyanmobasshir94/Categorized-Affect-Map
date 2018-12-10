from django.contrib import admin

# Register your models here.

from .models import Category,Feature

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    #     search_fields = ['question_text']
    #     list_filter = ['pub_date']
    #     list_display = ('question_text', 'pub_date', 'was_published_recently')
    #     fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
        inlines = [FeatureInline]

admin.site.register(Category, CategoryAdmin)