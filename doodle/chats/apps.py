from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'

class ChatMessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_messages'

class CodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'code'