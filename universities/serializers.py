from rest_framework import serializers
from .models import University, Faculty


class FacultySerializer(serializers.ModelSerializer):
    """Fakultet serializer."""

    class Meta:
        model = Faculty
        fields = ['id', 'university', 'name', 'description', 'min_score', 'grant_score']
        read_only_fields = ['id']


class FacultyListSerializer(serializers.ModelSerializer):
    """Fakultetlar ro'yxati uchun serializer (university nomi bilan)."""

    university_name = serializers.CharField(source='university.name', read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'university', 'university_name', 'name', 'description', 'min_score', 'grant_score']
        read_only_fields = ['id']


class UniversityListSerializer(serializers.ModelSerializer):
    """Universitetlar ro'yxati uchun serializer."""

    faculties_count = serializers.IntegerField(source='faculties.count', read_only=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'description', 'img', 'rating', 'website', 'faculties_count']
        read_only_fields = ['id']


class UniversityDetailSerializer(serializers.ModelSerializer):
    """Bitta universitet batafsil — fakultetlari bilan birga."""

    faculties = FacultySerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'description', 'img', 'rating', 'website', 'faculties']
        read_only_fields = ['id']
