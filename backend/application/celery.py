#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
在Django项目中，celery.py文件用于配置Celery，这是一个异步任务队列/作业队列，
基于分布式消息传递进行工作。Celery允许你异步执行后台和定时任务，这对于执行耗时的操作（如发送电子邮件、图像处理等）非常有用，
可以提高Web应用的性能和响应速度。
"""

import functools
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

from django.conf import settings
from celery import platforms

# 租户模式
if "django_tenants" in settings.INSTALLED_APPS:
    from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

    app = TenantAwareCeleryApp()
else:
    from celery import Celery

    app = Celery(f"application")
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True


def retry_base_task_error():
    """
    celery 失败重试装饰器
    :return:
    """

    def wraps(func):
        @app.task(bind=True, retry_delay=180, max_retries=3)
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                raise self.retry(exc=exc)

        return wrapper

    return wraps
