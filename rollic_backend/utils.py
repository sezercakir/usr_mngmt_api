
from enum import IntEnum


class StatusCodes(IntEnum):
   StatusCode200 = 1
   StatusCode400 = 0
   StatusCode403 = 2
   StatusCode500 = 3


def check_request(request):
   pass


def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False