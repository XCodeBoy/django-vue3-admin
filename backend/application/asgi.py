#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ASGI config for application project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/

在Django项目中，asgi.py文件是用来配置异步服务器接口（ASGI）的。
ASGI是WSGI（Web Server Gateway Interface）的异步版本，
它允许你使用异步编程来处理Web请求，
这对于提高性能特别是在处理大量并发请求时非常有用。
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

http_application = get_asgi_application()

from application.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": http_application,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns  # 指明路由文件是devops/routing.py
            )
        )
    ),
})
