from abc import abstractmethod


class ModelGenerator:
    def __init__(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def generate_model(self, options):
        pass


