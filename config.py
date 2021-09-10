from collections.abc import MutableMapping
from ruamel.yaml import YAML

class Config(MutableMapping):
    def __init__(self, cfg_file="config.yaml"):
        self.yaml  = yaml=YAML(typ='safe')
        self.store = yaml.load(cfg_file)

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        pass # Read Only

    def __delitem__(self, key):
        pass # Read Only

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    
