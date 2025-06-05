from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # Default number of items per page
    max_limit = 100     # Maximum number of items allowed per page
    # The 'limit' query parameter can be used to specify the page size
    # The 'offset' query parameter can be used to specify the starting point 