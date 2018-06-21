from . import model_generator


class ModelGeneratorWflow(model_generator.ModelGenerator):

    def __init__(self):
        super(ModelGeneratorWflow, self).__init__()

    def get_name(self):
        return 'WFlow'

    def generate_model(self, options):
        # TODO: implement logic, options will be an instance of ModelGeneratorsOptions class
        pass
