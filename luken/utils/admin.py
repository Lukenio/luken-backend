from django.contrib import admin


class ReadonlyTabularInline(admin.TabularInline):
    can_delete = False
    extra = 0
    editable_fields = []

    def get_readonly_fields(self, request, obj=None):
        fields = []
        for field in self.model._meta.get_fields():
            if not field.name == 'id':
                if field not in self.editable_fields:
                    fields.append(field.name)
        return fields

    def has_add_permission(self, request):
        return False
