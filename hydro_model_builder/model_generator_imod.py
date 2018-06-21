from . import model_generator


class ModelGeneratorImod(model_generator.ModelGenerator):

    def __init__(self):
        super(ModelGeneratorImod, self).__init__()

    def get_name(self):
        return "iMod"

    def generate_model(self, options):
        super(ModelGeneratorImod, self).generate_model(options)
