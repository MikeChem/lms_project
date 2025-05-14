from rest_framework import serializers
import re


def validate_youtube_url(value):
    """
    Валидатор для проверки, что URL принадлежит youtube.com
    """
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be|music.youtube.com|gaming.youtube.com)/.+'
    )
    youtube_pattern = re.compile(youtube_regex)

    if not youtube_pattern.match(value):
        raise serializers.ValidationError(
            "Можно добавлять только ссылки с домена youtube.com"
        )
    return value