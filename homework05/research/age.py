import datetime as dt
import statistics
import typing as tp

from dateutil.relativedelta import relativedelta

from homework05.vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    age_list = []
    today = dt.datetime.now()
    today_year = float(today.year)
    friends_list = get_friends(user_id=user_id, fields="bdate")
    for friend in friends_list.items:
        print(friend)
        try:
            date_of_birth = friend["bdate"].split(".")
            if len(date_of_birth) == 3:
                age = today_year - int(date_of_birth[2])
                age_list.append(age)
        except:
            pass
    if len(age_list) == 0:
        return None
    else:
        response = statistics.median(age_list)
        return response

if __name__ == "__main__":
    print(age_predict(user_id=8086321))
