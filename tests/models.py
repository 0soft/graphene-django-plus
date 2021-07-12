from typing import TYPE_CHECKING

from django.db import models

from graphene_django_plus.models import GuardedModel, GuardedModelManager

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Project(models.Model):

    objects = models.Manager["Project"]()

    if TYPE_CHECKING:
        milestones = RelatedManager["Milestone"]()

    id = models.BigAutoField(  # noqa: A003
        verbose_name="ID",
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        default=None,
    )
    cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
    )


class Milestone(models.Model):

    objects = models.Manager["Milestone"]()

    if TYPE_CHECKING:
        issues = RelatedManager["Issue"]()

    id = models.BigAutoField(  # noqa: A003
        verbose_name="ID",
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        default=None,
    )
    project = models.ForeignKey[Project](
        Project,
        related_name="milestones",
        related_query_name="milestone",
        on_delete=models.CASCADE,
    )


class Issue(GuardedModel):
    class Meta:
        permissions = [
            ("can_read", "Can read the issue's information."),
            ("can_write", "Can update the issue's information."),
        ]

    objects = GuardedModelManager["Issue"]()

    kinds = {
        "b": "Bug",
        "f": "Feature",
    }

    id = models.BigAutoField(  # noqa: A003
        verbose_name="ID",
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
    )
    kind = models.CharField(
        verbose_name="kind",
        help_text="the kind of the issue",
        max_length=max(len(t) for t in kinds),
        choices=list(kinds.items()),
        default=None,
        blank=True,
        null=True,
    )
    priority = models.IntegerField(
        default=0,
    )
    milestone = models.ForeignKey[Milestone](
        Milestone,
        related_name="issues",
        related_query_name="issue",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )


class MilestoneComment(models.Model):

    objects = models.Manager["MilestoneComment"]()

    id = models.BigAutoField(  # noqa: A003
        verbose_name="ID",
        primary_key=True,
    )
    text = models.CharField(
        max_length=255,
    )
    milestone = models.ForeignKey(
        Milestone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
