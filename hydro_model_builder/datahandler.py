from abc import abstractmethod

class DataHandler:
    def __init__(self):
        pass

    @abstractmethod
    def download(self):
        pass


class HydroEngineDataHandler(DataHandler):
    def download(self, data):
        # he.get_...

        # writer to data.output_path
        pass

class LocalDataHandler(DataHandler):
    def download(self, data):
        pass


