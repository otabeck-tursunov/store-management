from django.shortcuts import render
from rest_framework import filters, status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from mainApp.models import Ombor, Mahsulot, Mahsulot_tarqatish
from userApp.models import Xodim
from userApp.permissions import IsSuperUser
from rest_framework.permissions import *

from .models import Sotuv, Chiqim, Maosh
from .serializers import SotuvSerializer, ChiqimSerializer, MaoshSerializer


class SotuvListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Sotuv.objects.all()
    serializer_class = SotuvSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tarqatmalar = Mahsulot_tarqatish.objects.filter(ombor=request.data['ombor'], mahsulot=request.data['mahsulot'])
        print(tarqatmalar)
        tarqatmalar_miqdori = 0
        for tarqatma in tarqatmalar:
            tarqatmalar_miqdori += tarqatma.miqdor

        sotuvlar = Sotuv.objects.filter(ombor=request.data['ombor'], mahsulot=request.data['mahsulot'])
        print(sotuvlar)
        sotuvlar_miqdori = 0
        for sotuv in sotuvlar:
            sotuvlar_miqdori += sotuv.miqdor

        mahsulot_miqdori = tarqatmalar_miqdori - sotuvlar_miqdori
        if mahsulot_miqdori < 0:
            mahsulot_miqdori = 0

        if mahsulot_miqdori < request.data['miqdor']:
            return Response({
                "success": False,
                "message": f"Ombordagi {Mahsulot.objects.get(id=request.data['mahsulot']).nom}lar soni {mahsulot_miqdori} ta."
                           f" Siz {request.data['miqdor']} ta sotmoqchi bo'lyapsiz!"
            }, status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['mahsulot', 'ombor', 'xodim' 'sana']
    search_fields = ['mahsulot', 'ombor', 'xodim', 'sana']


class SotuvDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Sotuv.objects.all()
    serializer_class = SotuvSerializer


class ChiqimListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['izoh', 'ombor', 'sana']
    search_fields = ['izoh', 'ombor', 'sana']


class ChiqimDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer


class MaoshListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Maosh.objects.all()
    serializer_class = MaoshSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['xodim', 'izoh', 'sana']
    search_fields = ['xodim', 'izoh', 'sana']


class MaoshDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser, ]
    queryset = Maosh.objects.all()
    serializer_class = MaoshSerializer


# - - - Xodim uchun - - - ###################################################################################################

class SotuvlarXodimAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['mahsulot', 'ombor', 'xodim' 'sana']
    search_fields = ['mahsulot', 'ombor', 'xodim', 'sana']

    def get(self, request):
        xodim = get_object_or_404(Xodim, user=request.user)
        sotuvlar = Sotuv.objects.filter(ombor=xodim.ombor)
        serializer = SotuvSerializer(sotuvlar, many=True)
        data = {
            'success': True,
            'details': serializer.data
        }
        return Response(data)

    def post(self, request):
        try:
            sotuv = request.data
            serializer = SotuvSerializer(data=sotuv)

            mahsulot_tarqatishlar = Mahsulot_tarqatish.objects.filter(ombor=Xodim.objects.get(user=request.user).ombor)
            list = []
            for i in range(len(mahsulot_tarqatishlar)):
                list.append(mahsulot_tarqatishlar[i].mahsulot.id)
            mahsulot_id = int(sotuv.get("mahsulot"))

            if serializer.is_valid() and mahsulot_id in list:
                serializer.save(xodim=Xodim.objects.get(user=request.user),
                                ombor=Xodim.objects.get(user=request.user).ombor)
                return Response({
                    'success': True,
                    'details': serializer.data
                })
            else:
                return Response({
                    'success': False,
                    'errors': f"Kiritishda xatolik yoki Xodimning filialida bunday mahsulot tarqatilmagan bo'lishi mumkin | "
                              f"{serializer.errors}"
                })

        except Exception:
            return Response({
                'success': False,
                'errors': "Xatolik mavjud, Sotuv saqlanmadi!"
            })


class ChiqimlarXodimAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['izoh', 'ombor', 'sana']
    search_fields = ['izoh', 'ombor', 'sana']

    def get(self, request):
        ombor = get_object_or_404(Ombor, id=get_object_or_404(Xodim, user=request.user).ombor.id)
        chiqimlar = Chiqim.objects.filter(ombor=ombor)
        serialzier = ChiqimSerializer(chiqimlar, many=True)
        data = {
            "success": True,
            "details": serialzier.data
        }
        return Response(data)

    def post(self, request):
        chiqim = request.data
        serializer = ChiqimSerializer(data=chiqim)
        if serializer.is_valid():
            serializer.save(ombor=Xodim.objects.get(user=request.user).ombor)
            return Response({
                "success": True,
                "data": serializer.data
            })
        return Response({
            "success": False,
            "message": "Ma'lumot noto'g'ri jo'natildi!",
            "errors": serializer.errors
        })


class MaoshlarXodimListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Maosh.objects.filter(xodim=get_object_or_404(Xodim, user=self.request.user))

    serializer_class = MaoshSerializer
