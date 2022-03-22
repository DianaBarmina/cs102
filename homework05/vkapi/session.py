import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:

        self.base_url = base_url
        self.timeout = timeout
        self.ses = requests.Session()

        st_ls = []
        for i in range(400, 600):
            st_ls.append(i)

        retry = Retry(
            total=max_retries,
            status_forcelist=st_ls,
            backoff_factor=backoff_factor,
            method_whitelist=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.ses.mount(base_url, adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        if "timeout" in kwargs:
            kwargs["timeout"] = kwargs["timeout"]
        else:
            kwargs["timeout"] = self.timeout
        response = self.ses.get(self.base_url + "/" + url, *args, **kwargs)
        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]

        return_ = self.ses.post(self.base_url + "/" + url, *args, **kwargs)

        return return_
