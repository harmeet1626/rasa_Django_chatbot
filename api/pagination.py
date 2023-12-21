from rest_framework.pagination import PageNumberPagination

class paginator(PageNumberPagination):
    page_size = 30
    page_size_query_param = "size"
