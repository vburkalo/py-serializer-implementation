import io

from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from car.models import Car
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    manufacturer = serializers.CharField(max_length=64, required=True)
    model = serializers.CharField(max_length=64, required=True)
    horse_powers = serializers.IntegerField(
        required=True,
        validators=[MinValueValidator(1),
                    MaxValueValidator(1914)])
    is_broken = serializers.BooleanField(required=True)
    problem_description = serializers.CharField(allow_null=True,
                                                allow_blank=True,
                                                required=False)

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance: Car, validated_data):
        instance.manufacturer = validated_data.get(
            "manufacturer", instance.manufacturer
        )
        instance.model = validated_data.get("model", instance.model)
        instance.horse_powers = validated_data.get(
            "horse_powers", instance.horse_powers
        )
        instance.is_broken = validated_data.get(
            "is_broken", instance.is_broken
        )
        instance.problem_description = validated_data.get(
            "problem_description", instance.problem_description
        )
        instance.save()
        return instance


def serialize_car_object(car: Car) -> bytes:
    serializer = CarSerializer(car)
    json = JSONRenderer().render(serializer.data)
    return json


def deserialize_car_object(json: bytes) -> Car:
    stream = io.BytesIO(json)
    data = JSONParser().parse(stream)
    serializer = CarSerializer(data=data)
    if serializer.is_valid():
        return serializer.save()
    else:
        raise ValueError(
            "Invalid data provided to serializer: {}".format(serializer.errors)
        )
