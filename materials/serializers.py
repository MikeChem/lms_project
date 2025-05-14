from .models import Course, Lesson
from .validators import validate_youtube_url  # ← Импортируем валидатор
from rest_framework import serializers
from .models import Course, Subscription

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])  # ← валидация

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner', 'lessons_count', 'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        return obj.lessons.count()
