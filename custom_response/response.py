# class CustomResponse:
#     @classmethod
#     def success_response_token(cls, code, refresh, access, msg, data=None):
#         data = data or {}
#         return cls._build_response(code, msg, data)

#     def successResponse(self, code, msg, data=dict()):
#         context = {
#             "status_code": code,
#             "message": msg,
#             "detail": data,
#             "error": []
#         }
#         return context

#     @classmethod
#     def errorResponse(cls, status_code, msg, error=None):
#         error = error or {}
#         return cls._build_response(status_code, msg, data={}, error=error)

#     @classmethod
#     def _build_response(cls, status_code, msg, data, error=None):
#         return {
#             "status_code": status_code,
#             "message": msg,
#             "data": data,
#             "error": error or [],
#         }






class CustomResponse:
    @classmethod
    def success_response_token(cls, refresh, access, msg, data=None):
        data = data or {}
        return cls._build_response(msg, data)

    def successResponse(self, msg, data=dict()):
        context = {
            "message": msg,
            "detail": data,
            "error": []
        }
        return context

    @classmethod
    def errorResponse(cls, msg, error=None):
        error = error or {}
        return cls._build_response(msg, data={}, error=error)

    @classmethod
    def _build_response(cls, msg, data, error=None):
        return {
            "message": msg,
            "data": data,
            "error": error or [],
        }
