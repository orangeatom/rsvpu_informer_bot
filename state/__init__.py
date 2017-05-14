# todo
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
          'Menu': 1,  # complete
          'Set_sub_schedule': 2,  # complete
          'Settings': 3,
          'Timeline_login': 4,
          'Get_self_schedule_date': 5,
          'Get_timetable': 6,  # complete
          'Get_search_schedule': 7,
          'Get_academic_buildings': 8}
