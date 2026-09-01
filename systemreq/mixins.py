from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated  and (self.request.user.is_staff or self.request.user.is_superuser)
        

    def handle_no_permission(self):
        raise PermissionDenied("Ви не маєте доступу до цієї сторінки.")