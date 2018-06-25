# -*- coding: utf-8 -*-

"""Main module."""

# import model_generators as mg

import yaml

class ModelBuilder(object):
    """
    TODO: remove direct references to generators, instantiate
    ModelGeneratorProxy instead
    """
    generators = [
        # model_generator_imod.ModelGeneratorImod,
        # model_generator_wflow.ModelGeneratorWflow
    ]

    def __init__(self):
        pass

    def parse_config(self, configfile):
        with open(configfile) as f:
            return yaml.safe_load(f)

    def get_generator_names(self):
        return [g().get_name() for g in self.generators]
