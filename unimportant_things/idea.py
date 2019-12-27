from watsontalker import sayWords
import yaml
#try to read the config data from config.yaml
config = []
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

sayWords("What is your name?", config, True)
sayWords("Andrew", config, True)


