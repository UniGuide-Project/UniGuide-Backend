from django.contrib import admin
from .models import University, Faculty


class FacultyInline(admin.TabularInline):
    """Universitet ichida fakultetlarni ko'rsatish."""
    model = Faculty
    extra = 1
    fields = ['name', 'description', 'min_score', 'grant_score']


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'location', 'university_type', 'faculties_count']
    search_fields = ['name', 'location']
    list_filter = ['university_type', 'rating']
    ordering = ['-rating']
    inlines = [FacultyInline]

    def faculties_count(self, obj):
        return obj.faculties.count()
    faculties_count.short_description = "Fakultetlar soni"


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'min_score', 'grant_score']
    search_fields = ['name', 'university__name']
    list_filter = ['university']
    ordering = ['university', 'name']
