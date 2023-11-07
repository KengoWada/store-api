from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin


class BaseModelAdmin(SimpleHistoryAdmin):
    actions = ["mark_as_read"]
    history_list_display = ["changed_fields","list_changes"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return ", ".join(delta.changed_fields)
        return None

    def list_changes(self, obj):
        if obj.prev_record:
            fields = ""
            delta = obj.diff_against(obj.prev_record)

            for change in delta.changes:
                fields += (
                    f"<strong>{change.field}</strong> changed from "
                    f"<span style='background-color:#ffb5ad'>{change.old}</span> to "
                    f"<span style='background-color:#b3f7ab'>{change.new}</span>. <br/>"
                )
            return format_html(fields)
        return None

    @admin.action(description="Mark selected objects as removed.")
    def mark_as_read(self, request, queryset):
        queryset.update(is_removed=True)
