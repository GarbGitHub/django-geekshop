from locust import HttpUser, TaskSet, task
from geekshop.settings import SUPER_USER_LOGIN, SUPER_USER_PASSWORD


# https://locust.io/

def login(l):
    l.client.post("/auth/login/", {"username": SUPER_USER_LOGIN, "password": SUPER_USER_PASSWORD})
    print({"username": SUPER_USER_LOGIN, "password": SUPER_USER_PASSWORD})


def logout(l):
    l.client.post("/auth/logout/", {"username": SUPER_USER_LOGIN, "password": SUPER_USER_PASSWORD})


def index(l):
    l.client.get("/")


# def profile(l):
#     l.client.get("auth/edit/")


def products(l):
    l.client.get("/products/")


@task
class UserBehavior(TaskSet):
    tasks = {index: 2, products: 5}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 500  # минимальное время ожидания между вызовами отдельных task каждым пользователем
    max_wait = 900  # максимальное  время ожидания между вызовами отдельных task каждым пользователем

# Для запуска в командной строке надо выполнить команду
# locust -f hv_test.py --host=http://193.124.206.148
# где host — адрес тестируемого ресурса. Именно к нему будут добавлены адреса сервисов, указанные в тесте.
# Если никаких ошибок в тесте нет, нагрузочный сервер запустится и будет доступен по адресу http://localhost:8089/
