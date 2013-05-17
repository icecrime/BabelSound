import os.path
import yaml


script_location = os.path.dirname(os.path.abspath(__file__))
config_location = os.path.join(script_location, 'config')
with open(os.path.join(config_location, 'babelsound.config')) as f:
    locals().update(yaml.load(f))
