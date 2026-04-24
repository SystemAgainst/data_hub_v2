from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """Main project entity."""

    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_("Название проекта"),
    )
    address = models.CharField(
        _("Address"),
        max_length=500,
        blank=True,
        help_text=_("Адрес по ЕГРН / ориентир"),
    )

    # Links to external storages (Google Drive, Yandex Disk, internal file service, etc.)
    documents_storage = models.URLField(
        _("Documents storage"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_("Ссылка на папку или облачное хранилище с документами"),
    )
    expenses_sheet = models.URLField(
        _("Expenses sheet"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_("Ссылка на таблицу с расходами"),
    )

    # Images — one or many
    images = models.ManyToManyField(
        "Image",
        related_name="projects",
        blank=True,
        verbose_name=_("Images"),
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Статус проекта / описание"),
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class Image(models.Model):
    """Helper model to store uploaded images for projects."""

    image = models.ImageField(
        _("Image"),
        upload_to="projects/images/%Y/%m/%d/",
        help_text=_("Загрузить одно или несколько изображений"),
    )
    uploaded_at = models.DateTimeField(_("Uploaded at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image {self.id} — {self.uploaded_at.date()}"
