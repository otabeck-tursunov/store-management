from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Sotuv, Chiqim, Maosh

class SotuvSerializer(ModelSerializer):
    ombor_nomi = serializers.CharField(source='ombor.nom', read_only=True)
    mahsulot_nomi = serializers.CharField(source='mahsulot.nom', read_only=True)
    xodim_ism = serializers.CharField(source='xodim.ism', read_only=True)
    class Meta:
        model = Sotuv
        fields = '__all__'

    def validate_miqdor(self, value):
        if value < 0:
            raise serializers.ValidationError("miqdor nol dan kichik bo'lishi mumkin emas")
        return value


class ChiqimSerializer(ModelSerializer):
    ombor_nomi = serializers.CharField(source='ombor.nom', read_only=True)
    class Meta:
        model = Chiqim
        fields = '__all__'


class MaoshSerializer(ModelSerializer):
    class Meta:
        model = Maosh
        fields = '__all__'