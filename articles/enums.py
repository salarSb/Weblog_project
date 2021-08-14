from django.db import models


class ArticleStatuses(models.TextChoices):
    DRAFT = 'DRAFT', 'draft'
    PUBLISHED = 'PUBLISHED', 'published'
