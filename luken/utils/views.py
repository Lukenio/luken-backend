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
