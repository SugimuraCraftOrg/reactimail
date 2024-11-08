"""
URL configuration for reactimail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, re_path, path

urlpatterns = [
    re_path(r"", include(("home.urls", "home"), namespace="home")),
    re_path(r"", include(("account.urls", "account"), namespace="account")),
    path("tags/", include("tag.urls", namespace="tag")),
    path(
        "message-templates/",
        include("message_template.urls", namespace="message_template"),
    ),
    path("admin/", admin.site.urls),
]
