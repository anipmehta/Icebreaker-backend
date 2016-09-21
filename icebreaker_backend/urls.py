"""icebreaker_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


from icebreaker_backend.views import testing, send, signup, block, block_list, random_chat, search, removeRandom, \
    delivered, upload_pic, show_image

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('gcm.urls')),
    url(r'^test/',testing,name='tets'),
    url(r'^send/',send,name='send'),
    url(r'^signup/',signup,name='signup'),
    url(r'^block/',block,name='block'),
    url(r'^blockList/',block_list,name='block_list'),
    url(r'^random/',random_chat,name='random'),
    url(r'^add/', search,name='random'),
    url(r'^remove/', removeRandom,name='random_remove'),
    url(r'^deliver/', delivered,name='deliver'),
    url(r'^upload/(?P<enroll>\w{0,50})/', upload_pic,name='upload'),
    url(r'^image/(?P<enroll>\w{0,50})', show_image,name='upload')
]
