import psycopg, yaml

# config file related
def update_config(config:dict):
    with open("config.yaml", "w+") as config_file:
        yaml.dump(config, config_file)
    return config

try:
    with open("config.yaml") as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    print("Config file does not exist, creating it...")
    config = update_config({"db_exists": False})