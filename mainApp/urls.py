from django.urls import path
from .views import OmborListCreateAPIView, OmborDetailsAPIView, MahsulotListCreateAPIView, MahsulotDetailsAPIView, \
    Mahsulot_tarqatishListCreateAPIView, Mahsulot_tarqatishDetailsAPIView, MahsulotlarXodimAPIView, \
    MahsulotXodimAPIView, Mahsulot_tarqatishlarXodimAPIView, OmborCashDeleteAPIView, MahsulotCashDeleteAPIView, \
    OmborlarArchiveListAPIView, MahsulotlarArchiveListAPIView

urlpatterns = [
    path('omborlar/', OmborListCreateAPIView.as_view()),
    path('omborlar/archive/', OmborlarArchiveListAPIView.as_view()),
    path('ombor/<int:pk>/', OmborDetailsAPIView.as_view()),
    path('ombor/cash-delete/<int:pk>/', OmborCashDeleteAPIView.as_view()),

    path('mahsulotlar/', MahsulotListCreateAPIView.as_view()),
    path('mahsulotlar/archive/', MahsulotlarArchiveListAPIView.as_view()),
    path('mahsulot/<int:pk>/', MahsulotDetailsAPIView.as_view()),
    path('mahsulot/cash-delete/<int:pk>/', MahsulotCashDeleteAPIView.as_view()),
    path('xodim/mahsulotlar/', MahsulotlarXodimAPIView.as_view()),  # Xodim uchun mahsulotlar
    path('xodim/mahsulot/<int:pk>/', MahsulotXodimAPIView.as_view()),  # Xodim uchun mahsulot

    path('mahsulot_tarqatishlar/', Mahsulot_tarqatishListCreateAPIView.as_view()),
    path('mahsulot_tarqatish/<int:pk>/', Mahsulot_tarqatishDetailsAPIView.as_view()),
    path('xodim/mahsulot_tarqatishlar/', Mahsulot_tarqatishlarXodimAPIView.as_view()),  # Xodim uchun mahsulot_tarqatishlar
]
