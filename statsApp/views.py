from datetime import datetime

from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cashApp.models import Sotuv, Chiqim, Maosh
from mainApp.models import Mahsulot, Mahsulot_tarqatish, Ombor
from userApp.models import Xodim
from userApp.permissions import IsSuperUser


class StatsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                description="Boshlang'ich sanaga (YYYY-MM-DD) ko'ra chiqimlarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="Oxirgi sanaga (YYYY-MM-DD) ko'ra chiqimlarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                name='ombor_id',
                in_=openapi.IN_QUERY,
                description='Ombor ID-si bo\'yicha saralash!',
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            ombor_id = request.GET.get('ombor_id')

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if ombor_id is not None:
                sotuvlar = Sotuv.objects.filter(sana__range=[start_date, end_date], ombor=ombor_id)
                jami_sotuvlar = Sotuv.objects.filter(ombor=ombor_id)
                chiqimlar = Chiqim.objects.filter(sana__range=[start_date, end_date], ombor=ombor_id)
                mahsulot_tarqatishlar = Mahsulot_tarqatish.objects.filter(id=ombor_id)
                omborlar = Ombor.objects.filter(id=ombor_id)
                # mahsulotlar = Mahsulot.objects.filter(id=ombor_id, deleted=False)
            else:
                sotuvlar = Sotuv.objects.filter(sana__range=[start_date, end_date])
                jami_sotuvlar = Sotuv.objects.filter()
                chiqimlar = Chiqim.objects.filter(sana__range=[start_date, end_date])
                mahsulot_tarqatishlar = Mahsulot_tarqatish.objects.all()
                omborlar = Ombor.objects.all()
                # mahsulotlar = Mahsulot.objects.filter(deleted=False)
            mahsulot_sotuv = {}
            for i in sotuvlar:
                if i.mahsulot not in mahsulot_sotuv:
                    mahsulot_sotuv.update({
                        i.mahsulot.id: i.miqdor
                    })
                else:
                    mahsulot_sotuv.update({
                        i.mahsulot.id: mahsulot_sotuv[i.mahsulot] + i.miqdor
                    })

            mahsulot_foyda = {}
            for id, miqdor in mahsulot_sotuv.items():
                mahsulot = get_object_or_404(Mahsulot, id=id)
                mahsulot_foyda.update({
                    id: miqdor * (mahsulot.narx2 - mahsulot.narx1)
                })

            umumiy_daromad = sum(mahsulot_foyda.values())
            jami_foyda = umumiy_daromad - sum(chiqimlar.values_list('miqdor', flat=True))

            mahsulotlar = mahsulot_tarqatishlar.values_list('mahsulot', flat=True)

            barcha_tarqatilgan_miqdor = {}
            for ombor in omborlar:
                ombordagi_miqdor = ombor.mahsulot_tarqatmalar.filter(mahsulot__deleted=False).aggregate(
                    total=Sum('miqdor')).get('total') or 0
                barcha_tarqatilgan_miqdor[ombor.id] = ombordagi_miqdor
            barcha_tarqatilgan_miqdor = max(barcha_tarqatilgan_miqdor.values())
            sotilgan_mahsulotlar_miqdori = jami_sotuvlar.aggregate(total=Sum('miqdor')).get('total') or 0
            mahsulotlar_soni = barcha_tarqatilgan_miqdor - sotilgan_mahsulotlar_miqdori
            if mahsulotlar_soni < 0:
                mahsulotlar_soni = 0

            #
            mahsulot_foyda = dict(sorted(mahsulot_foyda.items(), key=lambda x: x[1], reverse=True))
            mahsulot_diagram = {}
            count = 1
            for key, value in mahsulot_foyda.items():
                v = round(value/umumiy_daromad * 100, 2)
                if count < 6:
                    mahsulot_diagram.update({
                        Mahsulot.objects.get(id=key).nom: v
                    })
                elif count == 6:
                    mahsulot_diagram.update({
                        "boshqa": 0
                    })
                    mahsulot_diagram.update({
                        "boshqa": (mahsulot_diagram["boshqa"] + v)
                    })
                else:
                    mahsulot_diagram.update({
                        "boshqa": (mahsulot_diagram["boshqa"] + v)
                    })
                count += 1

            # Filiallar diagramm

            filial_diagram = {}
            for ombor in Ombor.objects.filter(deleted=False):
                sotuvlar = Sotuv.objects.filter(sana__range=[start_date, end_date], ombor=ombor.id)
                mahsulot_sotuv = {}
                for i in sotuvlar:
                    if i.mahsulot not in mahsulot_sotuv:
                        mahsulot_sotuv.update({
                            i.mahsulot.id: i.miqdor
                        })
                    else:
                        mahsulot_sotuv.update({
                            i.mahsulot.id: mahsulot_sotuv[i.mahsulot] + i.miqdor
                        })

                mahsulot_foyda = {}
                for id, miqdor in mahsulot_sotuv.items():
                    mahsulot = get_object_or_404(Mahsulot, id=id)
                    mahsulot_foyda.update({
                        id: miqdor * (mahsulot.narx2 - mahsulot.narx1)
                    })

                umumiy_daromad_ex = sum(mahsulot_foyda.values()) or 0
                filial_diagram.update({
                    ombor.nom: umumiy_daromad_ex
                })


            return Response({
                "umumiy_daromad": umumiy_daromad,
                "jami_foyda": jami_foyda,
                "mahsulot_turi": mahsulotlar.count(),
                "mahsulotlar_soni": mahsulotlar_soni,
                "mahsulot_diagram": mahsulot_diagram,
                "filial_diagram": filial_diagram

            })
        except Exception:
            return Response({
                "success": False,
                "message": "Noto'g'ri sana formati yoki ombor_id kiritildi. Sana formati 'YYYY-MM-DD' bo'lishi kerak."
            })
