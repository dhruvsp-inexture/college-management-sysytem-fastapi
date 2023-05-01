from fastapi import HTTPException


class Response:
    """
    Return success and error response.
    """

    def __init__(self, status_code, message, data=None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def send_success_response(self):
        """
       Return success response with status RESPONSE_STATUS_SUCCESS
       :return: success response
       """
        return {'message': self.message or 'Success', "data": self.data, "status_code": self.status_code}

    def send_error_response(self):
        """
        Return error response with status RESPONSE_STATUS_ERROR
        :return: error response
        """
        raise HTTPException(detail=self.message, status_code=self.status_code)
