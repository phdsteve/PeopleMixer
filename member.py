class Member:

    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return '{}'.format(self.__name)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


class Pair:
    def __init__(self, first, second):
        self.__pair = (first, second)

    def __str__(self):
        return '{} - {}'.format(self.__pair[0], self.__pair[1])

    def get_pair(self):
        return self.__pair

    def set_pair(self, first, second):
        self.__pair = (first, second)
