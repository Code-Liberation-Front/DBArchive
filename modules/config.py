import os
import yaml
import modules.error as error

# Reads in the config file
def import_configuration(filename):

    # First, it opens the file in read only mode and reads the individual database items
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

            # Then it loads global configuration items
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

        # If there is an error with the yaml file or an error with the configuration provided, it raises an error and
        # exits the program
        except yaml.YAMLError:
            print(f"{error.color.RED}{error.color.BOLD}ConfigurationError: The Provided Yaml File is Invalid{error.color.END}")
            error.exit_program()
        except error.ConfigError as e:
            print(e)
            error.exit_program()