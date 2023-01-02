from enum import unique
from django.forms import ValidationError
from rest_framework import serializers
from .models import User

class UserSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "password",
        ]
    def is_valid(self):
        # Perform any custom validation here
        
        if len(self.initial_data) != 3:
            return False
        if (len(self.initial_data) == 3):
            # to avoid violating the unique constraint, in the serializer.
            if (User.objects.filter(name=self.initial_data.get('name')).count() > 0 and 
                User.objects.filter(email=self.initial_data.get('email')).count() > 0):
                return True
            
        # Call the parent is_valid method to perform default validation
        return super().is_valid()

class UserSerializerPatch(serializers.ModelSerializer):
    
    def is_valid(self, raise_exception_=True):
        # Perform any custom validation here
        if len(self.initial_data) != 2:
            return False
        if (len(self.initial_data) == 2):
            # to avoid violating the unique constraint, in the serializer.
            if (User.objects.filter(name=self.initial_data.get('name')).count() > 0 and 
                User.objects.filter(email=self.initial_data.get('email')).count() > 0):
                
                raise ValidationError
        # Call the parent is_valid method to perform default validation
        return super().is_valid( raise_exception=raise_exception_)


    class Meta:
        model = User
        fields = [
            "name",
            "password",
        ]
        

