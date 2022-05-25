import base64

import requests
from datetime import datetime
from typing import Union, Optional

URL = 'http://{ip}:8080/mwapp/services/{type_name}/{service}?token={token}&format={fmt}&timeout={timeout}&isBase64={is_base_64}&_ts={timestamp}'

formats = {
    "empty": 0,
    "xml": 1,
    "param": 2,
    "json": 4,
    "string": 6,
    "swagger": 12,
}


def send_message(ip, type_name, service, token, fmt, data,
                 timeout=-1, is_base_64=False, timestamp=None):
    # type: (str, str, str, Union[str, int], str, str, int, bool, Optional[int]) -> str
    if timestamp is None:
        timestamp = str(int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000))
    if is_base_64:
        data = base64.b64encode(data)
    token = token.upper()
    is_base_64 = is_base_64 and "true" or "false"
    fmt = formats.get(fmt, fmt)
    base_url = URL.format(**locals())
    response = requests.post(url=base_url, data=data)
    print response.url
    return response.text


if __name__ == "__main__":
    send_message(ip="127.0.0.1",
                 type_name='NKDSCTRL',
                 service='NKDSCTRL',
                 token='4038066209',
                 fmt='param',
                 data='1',
                 timeout=5000000)
