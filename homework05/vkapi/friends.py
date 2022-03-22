import dataclasses
import math
import json
import time
import typing as tp
from typing import Dict, Union, Any, List

from homework05.vkapi import config
from homework05.vkapi.session import Session
from homework05.vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: int, count: int = 5000, offset: int = 0, fields: tp.Any = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    access_token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]
    # fields = ", ".join(fields) if fields else ""
    response = FriendsResponse(0, [0])
    domain = config.VK_CONFIG["domain"]
    inizio = Session(domain)

    try:
        friends_list = inizio.get(
            "friends.get",
            params={
                "access_token": access_token,
                "v": v,
                "user_id": user_id,
                "count": count,
                "offset": offset,
                "fields": fields,
            },
        )

        response = FriendsResponse(
            friends_list.json()["response"]["count"],
            friends_list.json()["response"]["items"],
        )

    except:
        pass
    return response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
        source_uid: tp.Optional[int] = None,
        target_uid: tp.Optional[int] = None,
        target_uids: tp.Optional[tp.List[int]] = None,
        order: str = "",
        count: tp.Optional[int] = None,
        offset: int = 0,
        progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    access_token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]
    domain = config.VK_CONFIG["domain"]
    # target_uids_ = ",".join(list(map(str, target_uids)))
    count_ = 100

    inizio = Session(domain)
    # lenn_ = 1 + ((len(target_uids) - 1) // 100)
    result = []

    if target_uids:
        lenn_ = ((len(target_uids) - 1) // 100) + 1
        for i in range(lenn_):
            try:
                mutual_friends = inizio.get(
                    "friends.getMutual",
                    params={
                        "access_token": access_token,
                        "v": v,
                        "source_uid": source_uid,
                        "target_uid": target_uid,
                        "target_uids": ",".join(list(map(str, target_uids))),
                        "order": order,
                        "count": count_,
                        "offset": i * count_,
                    },
                )
                # print(mutual_friends.json())
                for friend in mutual_friends.json()["response"]:
                    result.append(
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                    )
            except:
                pass
            time.sleep(0.5)
        return result

    try:
        mutual_friends = inizio.get(
            "friends.getMutual",
            params={
                "access_token": access_token,
                "v": v,
                "source_uid": source_uid,
                "target_uid": target_uid,
                "target_uids": target_uids,
                "order": order,
                "count": count,
                "offset": offset,
            },
        )
        result.extend(mutual_friends.json()["response"])

    except:
        pass
    return result


if __name__ == "__main__":
    friends: Union[list[int], list[MutualFriends]] = get_mutual(source_uid=269738261, target_uids=[72752245])
    friends = get_friends(269738261)
    print(friends)

if __name__ == "__main__":
    friends = get_friends(user_id=201856650).items
    print(friends)
    print(get_mutual(201856650, target_uid=12141927))

