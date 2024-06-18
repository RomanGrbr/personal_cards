import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import SAFE_METHODS

from .constants import CREATE, READ, UPDATE, DELETE, FAILED, SUCCESS


class ActivityLogMixin:
    """Mixin для регистрации действий пользователя."""

    log_message = None

    def _get_action_type(self, request) -> str:
        return self.action_type_mapper().get('{}'.format(request.method.upper()))

    def _build_log_message(self, request) -> str:
        return 'Пользователь: {} -- Тип запроса: {} -- Адрес: {} -- Имя пути: {}'.format(
            self._get_user(request),
            self._get_action_type(request),
            request.path,
            request.resolver_match.url_name
        )

    def get_log_message(self, request) -> str:
        return self.log_message or self._build_log_message(request)

    @staticmethod
    def action_type_mapper():
        return {
            'GET': READ,
            'POST': CREATE,
            'PUT': UPDATE,
            'PATCH': UPDATE,
            'DELETE': DELETE,
        }

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return (
            x_forwarded_for.split(",")[0]
            if x_forwarded_for
            else request.META.get('REMOTE_ADDR')
        )

    @staticmethod
    def _get_user(request):
        return request.META.get(
            'REMOTE_USER', request.META.get('HTTP_X_REMOTE_USER'))

    def _write_log(self, request, response, *args, **kwargs):
        actor = self._get_user(request)

        data = {
                'actor': actor,
                'action_type': self._get_action_type(request),
                'remarks': self.get_log_message(request),
                'status': response.status_code,
                'ip': self.get_client_ip(request),
                'content_type': ContentType.objects.get_for_model(
                    self.get_queryset().model
                ),
                'pk': None,
                'data': {},
                'attrs': []
            }
        try:
            if request.method not in SAFE_METHODS:
                data['data'] = response.data
                data['pk'] = response.data.get('id')
            if request.method in ['POST', 'PUT', 'PATCH']:
                if self.__class__.__name__ == 'CardViewSet':
                    data['attrs'] = [
                        str(attr) for attr in
                            self.get_queryset().get(pk=data['pk']).attrs.all()]
        except Exception:
            pass
        finally:
            pass

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response, *args, **kwargs)
        return response
