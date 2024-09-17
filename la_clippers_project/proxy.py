from django.http import HttpResponse
import requests

def proxy_vite(request, path):
    response = requests.get(f'http://web:5173/{path}')
    content_type = response.headers.get('Content-Type', '')
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=content_type
    )
