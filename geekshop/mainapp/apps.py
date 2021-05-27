from django.apps import AppConfig

# app_name = 'mainapp'  # имя приложения уже прописано ниже  name = 'mainapp'


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'
