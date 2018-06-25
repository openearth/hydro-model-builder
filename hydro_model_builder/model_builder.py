# -*- coding: utf-8 -*-

"""Main module."""

# import model_generators as mg

import yaml
import geojson

class ModelBuilder(object):
    def __init__(self, configfile):
        self.config = None
        self.configfile = configfile

    def parse_config(self):
        with open(self.configfile) as f:
            d = yaml.safe_load(f)
        self.config = d
