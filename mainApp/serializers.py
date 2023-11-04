from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ombor, Mahsulot, Mahsulot_tarqatish


class OmborSerializer(ModelSerializer):
    class Meta:
        model = Ombor
        fields = '__all__'


class MahsulotSerializer(ModelSerializer):
    class Meta:
        model = Mahsulot
        fields = '__all__'

    def validate_narx1(self, value):
        if value < 0:
            raise serializers.ValidationError("narx1 nol dan kichik bo'lishi mumkin emas")
        return value

    def validate_narx2(self, value):
        if value < 0:
            raise serializers.ValidationError("narx2 nol dan kichik bo'lishi mumkin emas")
        return value


class Mahsulot_tarqatishSerializer(ModelSerializer):
    ombor_nomi = serializers.CharField(source='ombor.nom', read_only=True)
    mahsulot_nomi = serializers.CharField(source='mahsulot.nom', read_only=True)
    class Meta:
       model = Mahsulot_tarqatish
       fields = '__all__'

    def validate_miqdor(self, value):
        if value < 0:
            raise serializers.ValidationError("miqdor nol dan kichik bo'lishi mumkin emas")
        return value