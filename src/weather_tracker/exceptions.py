from rest_framework.exceptions import APIException


class InvalidTokenException(APIException):
    status_code = 400
    default_detail = "Invalid x-token header."
    default_code = "invalid_token"


class InvalidDateFormat(APIException):
    status_code = 400
    default_detail = "Invalid date format."
    default_code = "invalid_date_format"
