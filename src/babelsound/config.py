import yaml


with open('babelsound.config') as f:
    locals().update(yaml.load(f))
