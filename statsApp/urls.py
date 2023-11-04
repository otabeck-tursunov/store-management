from django.urls import path

from statsApp.views import StatsAPIView

urlpatterns = [
    path('', StatsAPIView.as_view()),

]