from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User, Team


class JWTSignupSerializer(serializers.ModelSerializer):
    """
    회원가입 시리얼라이저
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'team',
            'password',
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            team=validated_data['team'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class JWTLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    # class Meta:
    #     model = User
    #     fields = ('email', 'password',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name',)
        # depth = 2


class UserInfoSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'username', 'team')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('team_id', 'name',)
        # depth = 2
