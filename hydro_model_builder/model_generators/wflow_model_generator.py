import os
from model_generator import *

class wflow_model_generator(model_generator):

    def __init__(self):
        """
        Add a template path to a model object

        :return:
        """
        # TODO Think about how to retrieve a path for the template. Hard coded?
        self.template_path = '.'
        # TODO Retrieve template config.ini for an options specified one
        self.template_config = os.path.join(self.template_path, 'config.ini')

    def generate_model_files(self):
        """
        Convert all files into a model

        :return:
        """

    def generate_config_files(self):
        """
        Generate one or multiple configuration or setting files for the model

        :return:
        """
