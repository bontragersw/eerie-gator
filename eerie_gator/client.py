from urllib2 import Request, urlopen
import json


class EerieGatewayClient:
    def __init__(self, config_factory):
        self._config_factory = config_factory

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def _url(self, path):
        config = self._config_factory()
        return "http://localhost:%d/%s" % (config["port"], path)

    def get_active_station(self):
        url = self._url("active_station")
        request = Request(url, method="GET")
        response = urlopen(request)
        status = response.getcode()
        assert status == 200, status
        data = json.loads(response.read().decode())
        return data["station"]

    def set_active_station(self, value):
        url = self._url("active_station")
        if value is None:
            request = Request(url, method="DELETE")
        else:
            data = json.dumps({"station": value})
            request = Request(url, method="PUT", data=data.encode())
        response = urlopen(request)
        status = response.getcode()
        assert status == 200, status

    active_station = property(get_active_station, set_active_station)
