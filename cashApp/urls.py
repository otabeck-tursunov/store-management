from django.urls import path

from cashApp.views import SotuvListCreateAPIView, SotuvDetailsAPIView, ChiqimListCreateAPIView, ChiqimDetailsAPIView, \
    MaoshListCreateAPIView, MaoshDetailsAPIView, SotuvlarXodimAPIView, ChiqimlarXodimAPIView, MaoshlarXodimListAPIView

urlpatterns = [
    path('sotuvlar/', SotuvListCreateAPIView.as_view()),
    path('sotuv/<int:pk>/', SotuvDetailsAPIView.as_view()),
    path('xodim/sotuvlar/', SotuvlarXodimAPIView.as_view()), # Xodim sotuvlar


    path('chiqimlar/', ChiqimListCreateAPIView.as_view()),
    path('chiqim/<int:pk>/', ChiqimDetailsAPIView.as_view()),
    path('xodim/chiqimlar/', ChiqimlarXodimAPIView.as_view()), # Xodim chiqimlar

    path('maoshlar/', MaoshListCreateAPIView.as_view()),
    path('maosh/<int:pk>/', MaoshDetailsAPIView.as_view()),
    path('xodim/maoshlar/', MaoshlarXodimListAPIView.as_view()), # Xodim maoshlar
]