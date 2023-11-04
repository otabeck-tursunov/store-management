from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Xodim


class XodimSerializer(ModelSerializer):
    ombor_nomi = serializers.CharField(source='ombor.nom', read_only=True)
    class Meta:
        model = Xodim
        fields = ('id', 'username', 'password', 'ism', 'fam', 'ombor', 'ombor_nomi','tel', 'kpi', 'deleted')

    def validate_kpi(self, value):
        if value < 0:
            raise serializers.ValidationError("kpi nol dan kichik bo'lishi mumkin emas")
        return value

    def create(self, validated_data):
        try:
            user_data = {
                'username': validated_data['username'],
                'password': validated_data['password'],
                'first_name': validated_data['ism'],
                'last_name': validated_data['fam']
            }

            user = User.objects.create_user(**user_data)

            xodim_data = {
                'username': validated_data['username'],
                'password': validated_data['password'],
                'ism': validated_data['ism'],
                'fam': validated_data['fam'],
                'ombor': validated_data['ombor'],
                'tel': validated_data['tel'],
                'kpi': validated_data.get('kpi'),
                'deleted': validated_data['deleted'],
                'user': user
            }
            xodim = Xodim.objects.create(**xodim_data)
        except:
            user_data = {
                'username': validated_data['username'],
                'password': validated_data['password'],
                'first_name': validated_data['ism'],
                # 'last_name': validated_data['fam']
            }
            user = User.objects.create_user(**user_data)

            xodim_data = {
                'username': validated_data['username'],
                'password': validated_data['password'],
                'ism': validated_data['ism'],
                # 'fam': validated_data['fam'],
                'ombor': validated_data['ombor'],
                'tel': validated_data['tel'],
                'kpi': validated_data.get('kpi'),
                'deleted': validated_data['deleted'],
                'user': user
            }
            xodim = Xodim.objects.create(**xodim_data)

        return xodim

