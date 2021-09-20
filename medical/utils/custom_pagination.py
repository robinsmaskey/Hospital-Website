from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1


class CustomPagination(LimitOffsetPagination):
    page = DEFAULT_PAGE
    default_limit = 2
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        offset = self.request.query_params.get('offset')
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.count,
            'offset': offset,
            'results': data
        })