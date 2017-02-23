
from views.utils import ApiResponse


class ApiException(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status

    def to_result(self):
        return ApiResponse({'message': self.message, 'r': 1},
                           status=self.status)
