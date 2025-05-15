from .models import Course, Lesson
from .validators import validate_youtube_url  # ← Импортируем валидатор
from rest_framework import serializers
from .models import Course, Subscription
from drf_spectacular.utils import extend_schema_serializer
class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])  # ← валидация

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(exclude_fields=['is_subscribed', 'lessons_count'])
class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    stripe_product_id = serializers.CharField(read_only=True)
    stripe_price_id = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner', 'lessons', 'lessons_count', 'is_subscribed','stripe_product_id', 'stripe_price_id']

    def get_lessons_count(self, obj):
        return obj.course.count()  # или .lessons.count(), если есть related_name='lessons'

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

lessons_count = serializers.SerializerMethodField()

def get_lessons_count(self, obj):
    return obj.lessons.count()
