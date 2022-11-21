from rest_framework import pagination
from rest_framework.response import Response
class Pagination(pagination.LimitOffsetPagination):
    default_limit =10
    # def get_paginated_response(self, data):
    #     return Response({
    #         'links': {
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link()
    #         },
    #         'count': self.page.paginator.count,
    #         'results': data,
    #         # 'page_size':self.page_size,
    #         # 'max_page_size':self.max_page_size
    #     })