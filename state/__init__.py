# todo
from telebot import types

class BaseState:
    """
    Base State
    """

    @classmethod
    def enter(cls, user, *args, **kwargs):
        pass

    @classmethod
    def handle(cls, user, *args, **kwargs):
        pass

    @classmethod
    def change_state(cls, new_state, *args, **kwargs):
        pass


class Menu:
    pass
    """
    Main Menu State
    """
    @classmethod
    def enter(cls, user, *args, **kwargs):
        pass

    @classmethod
    def hande(cls):
        pass

    @classmethod
    def change_state(cls, new_state, *args, **kwargs):
        pass


states = {'StartMenu': 0,
          'Menu': 1,
          'Set_sub_schedule': 2,
          'Set_sub_news': 3,
          'timeline_login': 4}