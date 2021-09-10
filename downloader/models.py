from django.db import models

from .utils import parse_url


class Parse(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    times_followed = models.PositiveIntegerField(default=0)
    raw_url = models.URLField()
    downloadable_url = models.CharField(max_length=1000)

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.downloadable_url:
            self.downloadable_url = parse_url(self.raw_url)
        super().save(*args, **kwargs)
