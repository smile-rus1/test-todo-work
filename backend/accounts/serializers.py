from rest_framework import serializers

from todo.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'telegram_id')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            telegram_id=validated_data.get('telegram_id'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
