from rest_framework import serializers

from api.models import User


# class RegistrationSerializer(serializers.ModelSerializer):
#     """Serializers registration requests and creates a new user."""

#     # Ensure passwords are at least 8 characters long, no longer than 128
#     # characters, and can not be read by the client.
#     password = serializers.CharField(
#         max_length=128,
#         min_length=6,
#         write_only=True
#     )

#     class Meta:
#         model = User
#         # List all of the fields that could possibly be included in a request
#         # or response, including fields specified explicitly above.
#         fields = ['email', 'password']

#     def create(self, validated_data):
#         # Use the `create_user` method we wrote earlier to create a new user.
#         return User.objects.create_user(**validated_data)
