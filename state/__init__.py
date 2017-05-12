

class BaseState:
    """
    Base State
    """

    @classmethod
    def enter(cls, user):
        pass

    @classmethod
    def handle(cls, user):
        pass

    @classmethod
    def change_state(cls, new_state):
        pass


states = {'Menu': 1}
