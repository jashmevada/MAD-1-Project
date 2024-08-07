from typing import Optional


class ValidationData:
    def __init__(self, *args, **kwargs):

        if len(args) > 0:
            if isinstance(args[0], (str, int)):
                print(args[0])
            elif isinstance(args[0], list):
                self.__arr(args[0])
            elif isinstance(args[0], dict):
                self.__dict(args[0])

    @staticmethod
    def __arr(lst):
        print(f'[INFO]: Given List as Input :: {lst}')

    @staticmethod
    def __dict(lst):
        print(f'[INFO]: Given Dictionary as Input :: {lst}')
