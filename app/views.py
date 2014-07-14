# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os

import logging
logger = logging.getLogger(__name__)


class Directories(APIView):

    def _is_dir(self, path):
        return os.path.isdir(path)

    def get(self, request, *args, **kw):
        result = {}
        root = request.GET.get('dir')

        if root is not None and self._is_dir(root):
            logger.info(os.listdir(root))
            result = {
                'path': root,
                'children': [{'type': 'file' if os.path.isfile(os.path.join(root, x)) else 'directory',
                    'name': x,
                    'path': os.path.join(root, x)} for x in os.listdir(root)]
            }
        else:
            raise Http404
        response = Response(result, status=status.HTTP_200_OK)
        return response


class Files(APIView):

    def _is_file(self, path):
        return os.path.isfile(path)

    def get(self, request, *args, **kwargs):
        result = {}
        filepath = request.GET.get('path')
        print(filepath)
        if filepath is not None and self._is_file(filepath):
            result = {
                'path': filepath,
                'name': filepath.split('/')[len(filepath.split('/')) - 1],
                'content': open(filepath, 'r').read()
            }
        else:
            raise Http404
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
      return HttpResponse("{}")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Files, self).dispatch(*args, **kwargs)


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, _('Authentication failed'))
    return render(request, 'login-form.html', locals())


def dashboard(request):
    return render(request, 'dashboard.html', locals())
