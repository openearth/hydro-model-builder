# -*- coding: utf-8 -*-
import json
import geojson

class model_generator(object):
    def __init__(self, region_fn, options_fn):
        self.region_fn = region_fn
        self.options_fn = options_fn

    def parse_config(self):
        self.options = json.loads(self.option_fn)

    def parse_location(self):
        self.location = geojson.loads(self.region_fn)

    def __init__(self, ):
