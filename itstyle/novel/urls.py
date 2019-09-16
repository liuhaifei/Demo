from django.urls import path
from django.contrib import admin
from view import index

urlpatterns=[

    path('', index.main),  # new
    path('admin/', admin.site.urls),
    path('chapter/<int:novel_id>/', index.chapter),  # new
]