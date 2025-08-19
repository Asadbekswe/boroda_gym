from django.urls import path

from apps.views import UserCreateApiView

urlpatterns = [

    path('user-create/', UserCreateApiView.as_view()),
]
