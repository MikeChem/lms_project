from rest_framework.pagination import PageNumberPagination


class CourseLessonPagination(PageNumberPagination):
    page_size = 5  # ← количество элементов на странице
    page_size_query_param = 'page_size'  # ← пользователь может изменить размер страницы
    max_page_size = 100  # ← максимальное значение page_size

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)