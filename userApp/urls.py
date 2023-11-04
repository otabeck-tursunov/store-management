from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import XodimlarListCreateAPIView, XodimDetailsAPIView, XodimProfileAPiView, XodimCashDeleteAPIView, \
    XodimlarArchiveListAPIView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('xodimlar/', XodimlarListCreateAPIView.as_view()),
    path('xodimlar/archive/', XodimlarArchiveListAPIView.as_view()),
    path('xodim/<int:pk>/', XodimDetailsAPIView.as_view()),
    path('xodim/cash-delete/<int:pk>/', XodimCashDeleteAPIView.as_view()),
    path('xodim/details/', XodimProfileAPiView.as_view()),
]
