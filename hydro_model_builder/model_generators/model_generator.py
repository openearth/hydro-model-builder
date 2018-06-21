# -*- coding: utf-8 -*-
import yaml
import geojson

class ModelGenerator(object):
    def __init__(self, configfile):
        self.configfile = configfile

    def parse_config(self):
        with open(self.configfile) as f:
            d = yaml.safe_load(f)
        self.config = d
