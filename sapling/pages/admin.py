from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin

from models import Page


class PageAdminForm(BaseDynamicEntityForm):
    model = Page


class PageAdmin(BaseEntityAdmin, GuardedModelAdmin):
    form = PageAdminForm


admin.site.register(Page, PageAdmin)
