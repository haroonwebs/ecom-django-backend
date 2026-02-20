from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset= 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        res = ''
        if 'ErrorDetails' in str(data):
            res = json.dumps({'errors': data})
        else:
            res= json.dumps(data)    
        return res