from rest_framework import serializers
from myapp.models import user

class auth(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = (
            'id',
            'name',
            'email',
            'password',
        )
    def create(self,validate_data):
        password = validate_data.pop('password',None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance