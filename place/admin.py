from django.contrib import admin

# Register your models here.
from .models import Area, Location

class LocationInline(admin.TabularInline):
    model = Location
    extra = 3

class AreaAdmin(admin.ModelAdmin):
    #     search_fields = ['question_text']
    #     list_filter = ['pub_date']
    #     list_display = ('question_text', 'pub_date', 'was_published_recently')
    #     fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
        inlines = [LocationInline]

admin.site.register(Area, AreaAdmin)