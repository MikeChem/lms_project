from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # ← вывод списка уроков
    lessons_count = serializers.SerializerMethodField()     # ← количество уроков

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'preview',
            'owner', 'lessons', 'lessons_count'
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
