from rest_framework import status, filters
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from userApp.models import Xodim
from .models import Ombor, Mahsulot, Mahsulot_tarqatish
from .serializers import OmborSerializer, MahsulotSerializer, Mahsulot_tarqatishSerializer
from userApp.permissions import IsSuperUser


class OmborListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Ombor.objects.filter(deleted=False)
    serializer_class = OmborSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['nom', ]
    search_fields = ['nom', 'manzil']


class OmborDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Ombor.objects.all()
    serializer_class = OmborSerializer


class OmborCashDeleteAPIView(DestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Ombor.objects.all()
    serializer_class = OmborSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response({
            "message": "Ma'umot keshlandi!"
        }, status=status.HTTP_204_NO_CONTENT)


class MahsulotListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Mahsulot.objects.filter(deleted=False)
    serializer_class = MahsulotSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['nom', 'brand']
    search_fields = ['nom', 'brand']


class MahsulotDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Mahsulot.objects.all()
    serializer_class = MahsulotSerializer


class MahsulotCashDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser, ]
    queryset = Mahsulot.objects.all()
    serializer_class = MahsulotSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response({
            "message": "Ma'umot keshlandi!"
        }, status=status.HTTP_204_NO_CONTENT)


class Mahsulot_tarqatishListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, IsAuthenticated]
    queryset = Mahsulot_tarqatish.objects.all()
    serializer_class = Mahsulot_tarqatishSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['mahsulot', 'ombor', 'sana']
    search_fields = ['mahsulot', 'ombor', 'sana']


class Mahsulot_tarqatishDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Mahsulot_tarqatish.objects.all()
    serializer_class = Mahsulot_tarqatishSerializer


# - - - Xodim uchun - - - ###################################################################################################

class MahsulotlarXodimAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['nom', 'brand']
    search_fields = ['nom', 'brand']

    def get(self, request):
        try:
            serializer = None
            mahsulot_tarqatishlar = Mahsulot_tarqatish.objects.filter(
                ombor=Xodim.objects.get(user=request.user).ombor
            )
            mahsulotlar = Mahsulot.objects.filter(id__in=mahsulot_tarqatishlar.values_list('mahsulot', flat=True))
            serializer = MahsulotSerializer(mahsulotlar, many=True)
            data = {
                'success': True,
                'mahsulotlar': serializer.data
            }
            return Response(data)
        except Xodim.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Xodim topilmadi'
            })
        except Exception as e:
            return Response({
                'success': False,
                'errors': str(e)
            })


class MahsulotXodimAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):  # Xodim uchun faqat omborda mavjud Mahsulot ko'rinadi
        try:
            mahsulot_tarqatishlar = Mahsulot_tarqatish.objects.filter(ombor=Xodim.objects.get(user=request.user).ombor)
            list = []
            for i in range(len(mahsulot_tarqatishlar)):
                list.append(mahsulot_tarqatishlar[i].mahsulot.id)
            mahsulotlar = []
            for i in list:
                mahsulotlar.append(Mahsulot.objects.get(id=i))
            mahsulot = Mahsulot.objects.get(id=pk)
            serializer = MahsulotSerializer(mahsulot)
            if pk in list:
                return Response({
                    "success": True,
                    "mahsulot": serializer.data
                })
            else:
                return Response({
                    "success": False,
                    "message": "Tanlangan mahsulot Xodim ishlaydigan Filialda mavjud emas!"
                })
        except Exception:
            return Response({
                "success": False,
                "errors": f"Mahsulot topilmadi!"
            })


class Mahsulot_tarqatishlarXodimAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['mahsulot', 'ombor', 'sana']
    search_fields = ['mahsulot', 'ombor', 'sana']

    def get(self, request):  # Xodim uchun faqat shu omborga tegishli tarqatmalar ko'rinadi!
        try:
            tarqatmalar = Mahsulot_tarqatish.objects.filter(ombor=Xodim.objects.get(user=request.user).ombor)
            serializer = Mahsulot_tarqatishSerializer(tarqatmalar, many=True)
            return Response({
                "success": True,
                "message": f"{len(tarqatmalar)} ta tarqatmalar mavjud!",
                "details": serializer.data
            })
        except Exception:
            return Response({
                "success": False,
                "errors": "So'rovda xatolik mavjud!"
            })


# - - - - - Archive - - - - - - # # # # # # # # # # # # # # # # # # # # #

class OmborlarArchiveListAPIView(ListAPIView):
    permission_classes = [IsSuperUser, ]

    def get_queryset(self):
        return Ombor.objects.filter(deleted=True)

    serializer_class = OmborSerializer

class MahsulotlarArchiveListAPIView(ListAPIView):
    permission_classes = [IsSuperUser, ]

    def get_queryset(self):
        return Mahsulot.objects.filter(deleted=True)

    serializer_class = MahsulotSerializer


