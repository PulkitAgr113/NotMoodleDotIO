from django.apps import AppConfig

class ChatMessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_messages'

class RoomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'room'

class ScoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'score'
