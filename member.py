class Member:

    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return '{}'.format(self.__name)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
