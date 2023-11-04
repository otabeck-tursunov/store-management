from django.contrib.auth import authenticate, login, logout
from rest_framework import status, filters
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Xodim
from .serializers import XodimSerializer
from .permissions import IsSuperUser


# Admin tomonidan Xodim qo'shish, ko'rish, tahrirlash, o'chirish
class XodimlarListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, IsAuthenticated]
    queryset = Xodim.objects.filter(deleted=False)
    serializer_class = XodimSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['username', 'ism', 'fam', 'ombor', 'kpi']
    search_fields = ['username', 'ism', 'fam', 'ombor', 'kpi']


class XodimDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, IsAuthenticated]
    queryset = Xodim.objects.all()
    serializer_class = XodimSerializer


class XodimCashDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser, ]
    queryset = Xodim.objects.all()
    serializer_class = XodimSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response({
            "message": "Ma'umot keshlandi!"
        }, status=status.HTTP_204_NO_CONTENT)


# - - - - Xodim uchun - - - #################################################################################################################################
# Xodim tomonidan Profile ma'lumotlarini ko'rish va tahrirlash
class XodimProfileAPiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            xodim = Xodim.objects.get(user=request.user)
            serializer = XodimSerializer(xodim)
            data = {
                'success': True,
                'details': serializer.data
            }
            return Response(data)
        except Exception:
            return Response({
                'success': False,
                'errors': "Xodim topilmadi!"
            })

    def put(self, request):
        try:
            xodim = Xodim.objects.get(user=request.user)
            kpi = xodim.kpi
            ombor = xodim.ombor
            serializer = XodimSerializer(xodim, data=request.data)
            if serializer.is_valid():
                serializer.save(kpi=kpi,
                                ombor=ombor)
                return Response({
                    "success": True,
                    "details": serializer.data
                })
            else:
                return Response({
                    "success": False,
                    "errors": serializer.errors
                })
        except Xodim.DoesNotExist:
            return Response({
                'success': False,
                'errors': "Bad request!"
            })


# - - - - - Archive - - - - - - # # # # # # # # # # # # # # # # # # # # #

class XodimlarArchiveListAPIView(ListAPIView):
    permission_classes = [IsSuperUser, ]

    def get_queryset(self):
        return Xodim.objects.filter(deleted=True)

    serializer_class = XodimSerializer
