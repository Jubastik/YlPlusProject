from django.contrib import admin

from theatres.models import (
    City,
    Event,
    EventImage,
    Location,
    Theatre,
    TheatreImage,
    Troupe,
    TroupeMember,
)


@admin.register(Troupe)
class TroupeAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(TroupeMember)
class TroupeMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "troupe", "profile", "role")
    fields = ("troupe", "profile", "role")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "city", "fias")
    fields = ("query", "city", "fias")


class TheatreImageInline(admin.TabularInline):
    model = TheatreImage
    verbose_name_plural = "Галерея"


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "troupe", "reviews", "contacts", "image_tmb")
    fields = ("name", "location", "troupe", "reviews", "contacts", "image")
    inlines = [TheatreImageInline]


class EventImageInline(admin.TabularInline):
    model = EventImage
    verbose_name_plural = "Галерея"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "theatre", "troupe", "reviews", "image_tmb")
    fields = ("name", "theatre", "troupe", "reviews", "image")
    inlines = [EventImageInline]
