from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from utils.response import success_response

class CustomPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response(success_response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "results": data
        }, "Notes fetched"))