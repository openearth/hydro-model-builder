# -*- coding: utf-8 -*-

"""Main module."""

import yaml
from hydro_model_generator_wflow import ModelGeneratorWflow

class ModelBuilder(object):
    """
    TODO: remove direct references to generators, instantiate
    ModelGeneratorProxy instead
    """

    generators = [
        # ModelGeneratorImod,
        ModelGeneratorWflow
    ]

    def __init__(self):
        pass

    def parse_config(self, configfile):
        with open(configfile) as f:
            return list(yaml.safe_load_all(f))

    def get_generator_names(self):
        return [g().get_name() for g in self.generators]
