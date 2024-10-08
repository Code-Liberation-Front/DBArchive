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
                        print("No available database URI, add to the config.yaml")
                        error.exit_program()
                    if not conf["databases"][database].get("excluded_tables", None):
                        conf["databases"][database]["excluded_tables"] = 0
                    if not conf["databases"][database].get("driver", None):
                        conf["databases"][database]["driver"] = "postgres"
                    if not conf["databases"][database].get("backup_interval", None):
                        conf["databases"][database]["backup_interval"] = -1
                    if not conf["databases"][database].get("backup_count", None):
                        conf["databases"][database]["backup_count"] = -1
                    if not conf["databases"][database].get("backup_location", None):
                        conf["databases"][database]["backup_location"] = str(os.getcwd())+"/Backups"
                    if not conf["databases"][database].get("tz", None):
                        conf["databases"][database]["tz"] = 'America/New_York'
            else:
                print("databases Keyword is necessary to add a database")
            return conf
        except yaml.YAMLError:
            return None