from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from users.models import DoctorSpeciality, Doctor

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'user_type')

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required = True)
    # phone = serializers.CharField(required = False)
    password = serializers.CharField(required = True)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
         model = User
         fields = ['first_name', 'last_name', 'phone', 'address', 'image']

class ProfileDetailSerializer(serializers.ModelSerializer):
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'phone', 'address', 'email', 'image', 'get_full_name', 'is_active', 'is_verified', 'user_type']

class ProfileSerializer(serializers.ModelSerializer):
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'phone', 'address', 'email', 'image', 'get_full_name', 'is_active', 'is_verified', 'user_type']

        read_only_fields = ['id', 'email', 'is_active', 'is_verified', 'user_type'] # making fields defined here as uneditable


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, password):
        user = self.context['user']  # getting the logged in user in serializers
        if user.check_password(
                password):  # using built in method to check whether the entered password is associated to logged in user or not
            return password
        raise ValidationError('The old password you entered is incorrect')

    def validate_new_password(self, password):
        password_validation.validate_password(
            password)  # using built in method to validate the password field as djangos default password validators
        return password

    def validate(self, attrs):
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        if old_password == new_password:
            raise ValidationError({"new_password": "You have entered the old password as new password"})
        return attrs


class DoctorSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSpeciality
        fields = ['name', 'is_active']

class DoctorSpecialityListSerializer(serializers.ModelSerializer):
    created_by = ProfileDetailSerializer()

    class Meta:
        model = DoctorSpeciality
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    # user = ProfileSerializer()

    class Meta:
        model = Doctor
        fields = ('id', 'license_id', 'speciality', 'license_file', 'degree', 'user')
        read_only_fields = ('id', 'user')
