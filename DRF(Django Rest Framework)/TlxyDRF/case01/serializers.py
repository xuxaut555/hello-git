from rest_framework import serializers

from case01.models import *

class StudentSer(serializers.ModelSerializer):
    class Meta:
        #告诉序列化器，对应哪个模型
        model =  Student
        fields = '__all__'
