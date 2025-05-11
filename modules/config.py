import os
import yaml
import modules.error as error

# Reads in the config file
def importConfig(filename):
    with open(filename, 'r') as file:
        try:
            conf = yaml.safe_load(file)
            if conf.get("databases", None):
                for database in conf["databases"]:
                    if not conf["databases"][database].get("uri", None):
                        raise error.ConfigError("No available database URI, add to the config.yaml")
                    if not conf["databases"][database].get("excluded_tables", None):
                        conf["databases"][database]["excluded_tables"] = 0
                    if not conf["databases"][database].get("driver", None):
                        conf["databases"][database]["driver"] = "postgres"
            else:
                raise error.ConfigError("No Databases Provided")

            if not conf.get("args", None):
                conf["args"] = {}

            if not conf["args"].get("backup_interval", None):
                conf["args"]["backup_interval"] = -1
            elif not str(conf["args"].get("backup_interval")).isnumeric():
                raise error.ConfigError("Invalid Backup Interval Provided")

            if not conf["args"].get("backup_count", None):
                conf["args"]["backup_count"] = -1
            elif not str(conf["args"].get("backup_count")).isnumeric():
                raise error.ConfigError("Invalid Backup Count Provided")

            if not conf["args"].get("backup_location", None):
                conf["args"]["backup_location"] = os.path.join(str(os.getcwd()), "Backups")
            if not conf["args"].get("tz", None):
                conf["args"]["tz"] = 'America/New_York'
            return conf
        except yaml.YAMLError:
            print(f"{error.color.RED}{error.color.BOLD}ConfigurationError: The Provided Yaml File is Invalid{error.color.END}")
            error.exit_program()
        except error.ConfigError as e:
            print(e)
            error.exit_program()