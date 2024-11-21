import requests
from requests_oauth2client import BearerAuth
from pprint import pprint
from datetime import date


def tokken(username, password):
    post_params = {"username": username, "password": password}
    response = requests.post("http://127.0.0.1:8000/auth/token", data=post_params)
    dict_res = response.json()["access_token"]
    return dict_res


def user_date(username, password):
    url = "http://127.0.0.1:8000/auth/read_current_user"
    response = requests.get(url, auth=BearerAuth(tokken(username, password)))
    dict_res = response.json()
    return dict_res


def all_users(username, password):
    res = requests.get(
        "http://127.0.0.1:8000/users/all", auth=BearerAuth(tokken(username, password))
    )
    dict_res = res.json()
    return dict_res


def one_users(login, username, password):
    res = requests.get(
        f"http://127.0.0.1:8000/users/detail/{login}",
        auth=BearerAuth(tokken(username, password)),
    )
    dict_res = res.json()
    return dict_res


def add_user(login, psw):
    url = "http://127.0.0.1:8000/auth/"
    post_params = {"login": login, "psw": psw}
    response = requests.post(
        url,
        json=post_params,
    )
    dict_res = response.json()
    return dict_res


def del_users(login, username, password):
    res = requests.delete(
        f"http://127.0.0.1:8000/users/delete/{login}",
        auth=BearerAuth(tokken(username, password)),
    )
    dict_res = res.json()
    return dict_res


def add_journal(diary: str, username, password):
    today = date.today()
    auth = BearerAuth(tokken(username, password))
    add_date(str(today))
    id_user = user_date(username, password)["User"]["id"]
    id_date = [i["id"] for i in all_date()["transaction"] if i["date"] == str(today)]
    print(id_date)
    url = "http://127.0.0.1:8000/journals/create/"
    post_params = {
        "diary": diary,
        "dates_id": int(id_date[0]),
        "users_id": int(id_user),
    }
    response = requests.post(
        url,
        json=post_params,
        auth=auth,
    )
    dict_res = response.json()
    return dict_res


def add_date(date_new: str):
    today = date.today()
    url = "http://127.0.0.1:8000/dates/create/"
    if date_new != str(today) and date_new not in [
        i["date"] for i in all_date()["transaction"]
    ]:
        post_params = {"date": date_new}
        response = requests.post(
            url,
            json=post_params,
        )
        dict_res = response.json()
        return dict_res
    else:
        if str(today) not in [i["date"] for i in all_date()["transaction"]]:
            post_params = {"date": str(today)}
            response = requests.post(
                url,
                json=post_params,
            )
            dict_res = response.json()
            return dict_res


def all_date():
    url = "http://127.0.0.1:8000/dates/all/"
    response = requests.get(
        url,
    )
    dict_res = response.json()
    return dict_res


def one_journal(login: str, data: str, password):
    auth = BearerAuth(tokken(login, password))
    id_date = [i["id"] for i in all_date()["transaction"] if i["date"] == data]
    id_user = user_date(login, password)["User"]["id"]
    if data in [i["date"] for i in all_date()["transaction"]]:
        res = requests.get(
            f"http://127.0.0.1:8000/journals/journal_one?users_id={int(id_user)}&dates_id={int(id_date[0])}",
            auth=auth,
        )
        dict_res = res.json()
        return dict_res
    else:
        return {}


# def auto_add_date():
#     today = date.today()
#     if str(today) not in [i["date"] for i in all_date()["transaction"]]:
#         add_date(str(today))


# class ClassPut:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def put_categories(self, name, new_name):
#         user = ClassAuth(self.username, self.password)
#         get = ClassGet()
#         dict_categories = (get.all_categories()['transaction'])
#         for i, v in enumerate(dict_categories):
#             if slugify(name) == v['slug']:
#                 id = dict_categories[i]['id']
#                 url = f'https://lesson-pk.ru/category/update_category?id={id}'
#                 post_params = {'name': new_name}
#                 response = requests.put(url, json=post_params, auth=BearerAuth(user.tokken()))
#                 self.dict_res = response.json()
#                 return self.dict_res
#         return {}


# class ClassPath:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def path_uswers(self, id):
#         user = ClassAuth(self.username, self.password)
#         url = f'https://lesson-pk.ru/permission/?user_id={id}'
#         response = requests.patch(url, auth=BearerAuth(user.tokken()))
#         self.dict_res = response.json()
#         return self.dict_res


if __name__ == "__main__":
    # pprint(user_date("Andrew", "1234"))  # получить\обновить токен
    # pprint(add_user("Andrew", "1234"))
    # pprint(one_users('Admin', 'Admin', '1234'))
    # pprint(del_users("Andrew", "Admin", "1234"))
    # pprint(all_users("Admin", "1234"))
    # pprint(add_journal("test Andrew auto 21", "Andrew", "1234"))
    # pprint(add_date("2024-11-20"))
    # pprint(one_journal("Andrew", "2024-11-21", "1234"))
    pass
