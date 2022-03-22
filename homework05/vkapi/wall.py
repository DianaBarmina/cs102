import json
import textwrap
import time
import typing as tp
from string import Template
import pandas as pd
from pandas import json_normalize

from homework05.vkapi import config
from homework05.vkapi.exceptions import APIError
from homework05.vkapi.session import Session


def get_posts_2500(
        owner_id: str = "",
        domain: str = "",
        offset: int = 0,
        count: int = 10,
        max_count: int = 2500,
        filter: str = "owner",
        extended: int = 0,
        fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
        owner_id: str = "",
        domain: str = "",
        offset: int = 0,
        count: int = 10,
        max_count: int = 2500,
        filter: str = "owner",
        extended: int = 0,
        fields: tp.Optional[tp.List[str]] = None,
        progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    access_token = config.VK_CONFIG["access_token"]
    version = config.VK_CONFIG["version"]
    domain = config.VK_CONFIG["domain"]
    inizio = Session(domain)
    lenn_ = 1 + ((count - 1) // (max_count))
    posts_list = []

    for i in range(lenn_):
        try:
            code = Template("""var k = 0;
                            var post = [];
                            while(k < $trying){
                            post = post + API.wall.get({"owner_id":$owner_id,
                                                        "domain":"$domain",
                                                        "offset":$offset + k*100,
                                                        "count":"$count",
                                                         "filter":"$filter",
                                                        "extended":$extended,
                                                        "fields":"$fields",
                                                        "v":$version})["items"];
                                                        k=k+1;}
                            return {"count": posts.length,
                                    "items": posts};""").substitute(
                owner_id=owner_id,
                domain=domain,
                offset=offset + max_count * i,

                count=count - max_count * i
                if count - max_count * i < 101
                else 100,

                trying=(count - max_count * i - 1) // 100 + 1
                if count - max_count * i < max_count + 1
                else max_count // 100,

                filter=filter,
                extended=extended,
                fields=fields,
                version=str(version),
            )

            taken_posts = inizio.post(
                "execute",
                data={"code": code,
                      "access_token": access_token,
                      "v": version}, )

            time.sleep(1)

            for j in taken_posts.json()["response"]["items"]:
                posts_list.append(j)

        except:
            pass
    return json_normalize(posts_list)
