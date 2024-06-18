import subprocess
import os

from django.http import JsonResponse

from .settings import DATABASES


class MacObtain:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            res = subprocess.check_output(["pdp-id", "-l"])
            mac_label = res.decode().strip()
        except:
            mac_label = None

        if mac_label:
            request.META["Mac-Label"] = mac_label
        else:
            request.META["Mac-Label"] = "0"
        os.environ['MACLABEL'] = request.META["Mac-Label"]

        if 'REMOTE_USER' in request.META and "@" in request.META['REMOTE_USER']:
            request.META['REMOTE_USER'] = request.META[
                'REMOTE_USER'].rpartition("@")[0]
        if 'HTTP_X_REMOTE_USER' in request.META and "@" in request.META['HTTP_X_REMOTE_USER']:
            request.META['REMOTE_USER'] = request.META[
                'HTTP_X_REMOTE_USER'].rpartition("@")[0]
        # if request.META.get('KRB5CCNAME'):
        #     os.environ['KRB5CCNAME'] = request.META.get('KRB5CCNAME')
        #     DATABASES['default']['USER'] = request.META.get('REMOTE_USER')
    
        # if not request.META.get('REMOTE_USER'):
        #     return JsonResponse({"err": "Пользователь не авторизован"}, status=401)
        request.META['REMOTE_USER'] = 'Роман Гербер'
        
        response = self.get_response(request)

        if mac_label:
            response['Mac-Label'] = mac_label

        return response
