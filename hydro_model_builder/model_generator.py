from abc import abstractmethod


def get_names():
    return [g().get_name() for g in generators]


class ModelGenerator:
    def __init__(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def generate_model(self, options):
        pass


from hydro_model_builder import model_generator_imod
from hydro_model_builder import model_generator_wflow

generators = [
    model_generator_imod.ModelGeneratorImod,
    model_generator_wflow.ModelGeneratorWflow
]
