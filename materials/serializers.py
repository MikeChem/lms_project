from .validators import validate_youtube_url  # ← Импортируем валидатор
from rest_framework import serializers

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])  # ← валидация

    class Meta:
        model = Lesson


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False