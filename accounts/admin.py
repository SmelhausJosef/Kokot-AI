from django.contrib import admin

from .models import Invitation, Organization, OrganizationMembership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "created_at")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role", "created_at")
    list_filter = ("role", "organization")
    search_fields = ("user__username", "user__email", "organization__name")
    ordering = ("organization", "role")


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "organization", "role", "invited_by", "created_at", "expires_at", "accepted_at")
    list_filter = ("role", "organization", "accepted_at")
    search_fields = ("email", "organization__name")
    readonly_fields = ("token", "created_at", "accepted_at")
    ordering = ("-created_at",)
