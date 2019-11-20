from http.client import HTTPResponse, HTTPException
from typing import Union
from io import BytesIO


class FakeSocket:
    def __init__(self, response_str):
        self._file = BytesIO(response_str)

    def makefile(self, *args, **kwargs):
        return self._file


def get_response_object(data) -> Union[HTTPResponse, None]:
    try:
        source = FakeSocket(data)
        response = HTTPResponse(source)
        response.begin()
        return response
    except HTTPException:
        return None
