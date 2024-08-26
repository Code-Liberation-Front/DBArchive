import yaml

def importConfig(filename):
    with open(filename, 'r') as file:
        try:
            conf = yaml.safe_load(file)
            if conf.get("databases", None):
                for database in conf["databases"]:
                    if not conf["databases"][database].get("uri", None):
                        print("No available database URI")
                    if not conf["databases"][database].get("driver", None):
                        conf["databases"][database]["driver"] = "postgres"
                    if not conf["databases"][database].get("backup_interval", None):
                        conf["databases"][database]["backup_interval"] = 1
                    if not conf["databases"][database].get("backup_count", None):
                        conf["databases"][database]["backup_count"] = 5
            else:
                print("databases Keyword is necessary to add a database")
            return conf
        except yaml.YAMLError:
            return None