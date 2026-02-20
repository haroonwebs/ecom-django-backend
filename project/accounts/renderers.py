from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if data is None:
            return b''

        # Check response status code
        response = renderer_context.get('response')

        if response and response.status_code >= 400:
            data = {'errors': data}

        return json.dumps(data).encode('utf-8')