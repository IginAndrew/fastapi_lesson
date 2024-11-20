import requests
from requests_oauth2client import BearerAuth
from pprint import pprint


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


def add_journal(diary: str, dates_id: int, users_id: int, username, password):
    auth = BearerAuth(tokken(username, password))
    url = "http://127.0.0.1:8000/journals/create/"
    post_params = {"diary": diary, "dates_id": dates_id, "users_id": users_id}
    response = requests.post(
        url,
        json=post_params,
        auth=auth,
    )
    dict_res = response.json()
    return dict_res
    # def all_products(self):
    #     res = requests.get("https://lesson-pk.ru/products/")
    #     dict_res = res.json()
    #     self.x = (dict_res['transaction'])
    #     return self.x

    # def all_products_categories(self, category):
    #     url = f"https://lesson-pk.ru/products/{category}"
    #     res = requests.get(url)
    #     dict_res = res.json()
    #     self.x = (dict_res['transaction'])
    #     return self.x

    # def products_detail(self, name):
    #     url = f"https://lesson-pk.ru/products/detail/{name}"
    #     res = requests.get(url)
    #     dict_res = res.json()
    #     self.x = (dict_res['transaction'])
    #     return self.x


# class ClassPost:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def add_categories(self, name):
#         user = ClassAuth(self.username, self.password)
#         url = 'https://lesson-pk.ru/category/create'
#         post_params = {'name': name}
#         response = requests.post(url, json=post_params, )
#         self.dict_res = response.json()
#         return self.dict_res

#     def add_products(self, name, category=0, description='!!!!', price=0, stock=0, rating=0):
#         self.name = name
#         user = ClassAuth(self.username, self.password)
#         url = 'https://lesson-pk.ru/products/create'
#         post_params = {'name': self.name, 'description': description, 'price': price,
#                        'image_url': f'img/{slugify(self.name)}', 'stock': stock, 'category': category, 'rating': rating}
#         response = requests.post(url, json=post_params, auth=BearerAuth(user.tokken()))
#         self.dict_res = response.json()
#         return self.dict_res

#     def add_user(self, first_name, last_name, username, email, password):
#         url = 'https://lesson-pk.ru/auth/'
#         post_params = {'first_name': first_name, 'last_name': last_name,
#                        'username': username, 'email': email, 'password': password}
#         response = requests.post(url, json=post_params)
#         self.dict_res = response.json()
#         return self.dict_res


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

#     def put_products(self, name, new_name, category=0, description='!!!!', price=0, stock=0, rating=0):
#         user = ClassAuth(self.username, self.password)
#         get = ClassGet()
#         dict_products = (get.all_products())
#         for i, v in enumerate(dict_products):
#             if slugify(name) == v['slug']:
#                 url = f'https://lesson-pk.ru/products/detail/{slugify(name)}'
#                 post_params = {'name': new_name, 'description': description, 'price': price,
#                                'image_url': f'img/{slugify(name)}', 'stock': stock, 'category': category,
#                                'rating': rating}
#                 response = requests.put(url, json=post_params, auth=BearerAuth(user.tokken()))
#                 self.dict_res = response.json()
#                 return self.dict_res
#         return {}


# class ClassDelete:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def delete_categories(self, name):
#         user = ClassAuth(self.username, self.password)
#         get = ClassGet()
#         dict_categories = (get.all_categories()['transaction'])
#         for i, v in enumerate(dict_categories):
#             if slugify(name) == v['slug']:
#                 id = dict_categories[i]['id']
#                 url = f'https://lesson-pk.ru/category/delete?id={id}'
#                 response = requests.delete(url, auth=BearerAuth(user.tokken()))
#                 self.dict_res = response.json()
#                 return self.dict_res
#         return {}

#     def delete_products(self, name):
#         user = ClassAuth(self.username, self.password)
#         get = ClassGet()
#         dict_products = (get.all_products())
#         for i, v in enumerate(dict_products):
#             if slugify(name) == v['slug']:
#                 id = dict_products[i]['id']
#                 url = f'https://lesson-pk.ru/products/delete?id={id}'
#                 response = requests.delete(url, auth=BearerAuth(user.tokken()))
#                 self.dict_res = response.json()
#                 return self.dict_res
#         return {}

#     def delete_user(self, id):
#         user = ClassAuth(self.username, self.password)
#         url = f'https://lesson-pk.ru/permission/delete?user_id={id}'
#         response = requests.delete(url, auth=BearerAuth(user.tokken()))
#         self.dict_res = response.json()
#         return self.dict_res


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
    # user_date("Admin", "1234")  # получить\обновить токен
    # pprint(add_user("Andrew", "1234"))
    # pprint(one_users('Admin', 'Admin', '1234'))
    # pprint(del_users("Andrew", "Admin", "1234"))
    # pprint(all_users("Admin", "1234"))
    pprint(add_journal("test Admin", 1, 6, "Andrew", "1234"))
    pass
