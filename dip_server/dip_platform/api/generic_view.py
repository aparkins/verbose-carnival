from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View

from dip_platform.management import exceptions


class GenericViewMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        _METHOD_MAPPINGS = {
            'handle_get':     'get',
            'handle_post':    'post',
            'handle_put':     'put',
            'handle_patch':   'patch',
            'handle_delete':  'delete',
            'handle_head':    'head',
            'handle_trace':   'trace',
        }

        cls.http_method_names = [
            _METHOD_MAPPINGS[method]
            for method in _METHOD_MAPPINGS.keys()
            if method in namespace.keys()
        ]

        return cls


class GenericView(View, metaclass=GenericViewMeta):
    def get(self, request, *args, **kwargs):
        return _build_response(self.handle_get, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return _build_response(self.handle_post, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return _build_response(self.handle_put, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return _build_response(self.handle_patch, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return _build_response(self.handle_delete, request, *args, **kwargs)

    def head(self, request, *args, **kwargs):
        return _build_response(self.handle_head, request, *args, **kwargs)

    def trace(self, request, *args, **kwargs):
        return _build_response(self.handle_trace, request, *args, **kwargs)


def _build_response(handler, request, *args, **kwargs):
    try:
        status, payload, headers = handler(request, *args, **kwargs)
    except Exception as e:
        status, payload, headers = _handle_exception(e)

    if payload is None:
        response = HttpResponse(status=status)
    else:
        response = JsonResponse(payload, status=status)
    for header, value in headers.items():
        response[header] = value

    return response


def _handle_exception(e):
    ERROR_MESSAGE_HEADER = 'dip-error-message'
    if isinstance(e, exceptions.NotFoundError):
        status = 404
        payload = None
        headers = { ERROR_MESSAGE_HEADER: str(e) }
    elif isinstance(e, exceptions.BadRequestError):
        status = 400
        payload = None
        headers = { ERROR_MESSAGE_HEADER: str(e) }
    else:
        raise e

    return status, payload, headers
