from django.db import models

from core.models import ContactsGroup, GalleryBaseModel, ImageBaseModel
from rating.models import ReviewGroup


class Troupe(models.Model):
    class Meta:
        verbose_name = "Труппа"
        verbose_name_plural = "Труппы"


class TroupeMember(models.Model):
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", related_name="members", on_delete=models.CASCADE)
    profile = models.ForeignKey(
        to="users.ActorProfile", verbose_name="Профиль", on_delete=models.CASCADE, related_name="troupe_members"
    )
    role = models.CharField(verbose_name="Роль", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Участник труппы"
        verbose_name_plural = "Участники трупп"


class City(models.Model):
    name = models.CharField("Название", max_length=100)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Location(models.Model):
    """
    Информация о местоположении.
    Полем `query` следует пользоваться лишь в тех случаях, когда идентификатор ФИАС устарел.
    """

    #: Адрес одной строкой
    query = models.CharField("Адрес", max_length=250)

    #: Город
    city = models.ForeignKey(City, verbose_name="Город", on_delete=models.CASCADE)

    #: Уникальный идентификатор ФИАС
    fias = models.CharField("ФИАС", max_length=50)

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"


class TheatreQuerySet(models.QuerySet):
    def theatres_list(self):
        return self.only("id", "image", "name", "description", "location__query").order_by("name")

    def theatre_details(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related("gallery_images", "reviews__reviews", "events__meetups", "events__meetups__host")
            .only("name", "description")
            .annotate(
                reviews_count=models.Count("reviews__reviews"),
                reviews_average_score=models.Avg("reviews__reviews__star"),
                events_count=models.Count("events"),
            )
        )

    def theatre_ratings(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related("reviews__reviews")
            .only("id", "name", "image", "location__query", "description")
        )


class Theatre(ImageBaseModel):
    name = models.CharField("Название", max_length=150)
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name="Местоположение", on_delete=models.CASCADE)
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(ReviewGroup, verbose_name="Отзывы", on_delete=models.SET_NULL, null=True, blank=True)
    contacts = models.ForeignKey(
        ContactsGroup, verbose_name="Контакты", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = models.Manager()
    theatres = TheatreQuerySet.as_manager()

    class Meta:
        verbose_name = "Театр"
        verbose_name_plural = "Театры"

    def __str__(self):
        return self.name


class TheatreImage(GalleryBaseModel):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="gallery_images")


class EventQuerySet(models.QuerySet):
    def events_list(self):
        return self.only(
            "id", "image", "name", "description", "theatre__id", "theatre__name", "theatre__location__query"
        ).order_by("name")

    def event_details(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related("troupe__members", "reviews__reviews")
            .only("id", "image", "name", "description", "theatre__id", "theatre__name", "theatre__location__query")
            .annotate(
                reviews_count=models.Count("reviews__reviews"),
                reviews_average_score=models.Avg("reviews__reviews__star"),
            )
        )

    def event_ratings(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related("reviews__reviews")
            .only(
                "id",
                "name",
                "image",
                "description",
                "theatre__id",
                "theatre__name",
                "theatre__image",
                "theatre__location__query",
            )
        )


class Event(ImageBaseModel):
    name = models.CharField("Название", max_length=150)
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)
    theatre = models.ForeignKey(Theatre, verbose_name="Театр", on_delete=models.CASCADE, related_name="events")
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(ReviewGroup, verbose_name="Отзывы", on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()
    events = EventQuerySet.as_manager()

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return self.name


class EventImage(GalleryBaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="gallery_images")
