from django.db import transaction

import reversion


class PermissionByActionMixin(object):
    """
    Allows to setup permission classes per action.
    """
    permission_classes_by_action = {
        "create": [],
        "retrieve": [],
        "default": [],
    }

    def get_permissions(self):
        try:
            classes = self.permission_classes_by_action[self.action]
        except KeyError:
            classes = self.permission_classes_by_action["default"]

        return [p() for p in classes]


class ReversionViewMixin(object):
    """
    Tracks changes for registered in 'reversion' models in View.
    """
    def dispatch(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            response = super(ReversionViewMixin, self).dispatch(*args, **kwargs)
            if not self.request.user.is_anonymous:
                reversion.set_user(self.request.user)
            return response
