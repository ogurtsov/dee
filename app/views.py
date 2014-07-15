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
from django.contrib.auth.decorators import login_required

from .helpers import *

import os
from operator import itemgetter

import logging
logger = logging.getLogger(__name__)


@login_required
@csrf_exempt
def api_router(request, resource):
    resource_fn = {
      'file': file_api,
      'directory': dir_api
    }.get(resource, placeholder)
    return resource_fn(request)

def placeholder(request):
    return json_response({'msg': 'wrong resource'})

def file_api(request):
    response = {}
    if request.method == 'GET':
        filepath = request.GET.get('path')
        if filepath is not None and is_file(filepath):
            response = {
                'path': filepath,
                'name': filepath.split('/')[len(filepath.split('/')) - 1],
                'content': open(filepath, 'r').read()
            }
        else:
            raise Http404
    elif request.method == 'POST':
        data = PayloadParser(request.body)
        path = data.get('path')
        content = data.get('content')
        name = data.get('name')
        with open(path, 'w') as file:
            file.write(content)
            file.close()
            response = {'msg': 'Ok'}
    return json_response(response)

def dir_api(request):
    response = {}
    if request.method == 'GET':
        root = request.GET.get('dir')
        if root is not None and is_dir(root):
            children = [{'type': 'file' if is_file(os.path.join(root, x)) else 'directory',
                    'name': x,
                    'path': os.path.join(root, x)} for x in os.listdir(root)]
            children = sorted(children, key=itemgetter('name')) 
            response = {
                'path': root,
                'children': children
            }
        else:
            raise Http404
    return json_response(response)


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


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', locals())
