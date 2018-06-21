def get_names():
    return [g().get_name() for g in generators]


class ModelGenerator:
    def __init__(self):
        pass

    def get_name(self):
        pass

    def generate_model(self, options):
        pass


from . import model_generator_imod
from . import model_generator_wflow

generators = [
    model_generator_imod.ModelGeneratorImod,
    model_generator_wflow.ModelGeneratorWflow
]
