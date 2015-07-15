import ConfigParser as configparser
import os.path


def get_config(filenames=None):
    if filenames is None:
        filenames = [
            "eerie_gator.conf",
            os.path.expanduser("~/eerie_gator.conf"),
            "/etc/eerie_gator.conf",
            ]

    parser = configparser.RawConfigParser()
    parser.read(filenames)
    config = {}

    # The config file uses 1-based indexes, like the numbers on the OSPi
    # case. However, we use 0-based indexes internally.
    config["zones"] = {
        name: int(index) - 1
        for (name, index) in parser.items("Zones")
        }

    config["url"] = parser.get("Google Calendar", "url")
    config["cache"] = os.path.expanduser(parser.get("Google Calendar", "cache"))
    config["max size"] = parser.getint("Google Calendar", "max size")

    config["host"] = parser.get("Gateway", "host")
    config["port"] = parser.getint("Gateway", "port")
    config["debug"] = parser.getboolean("Gateway", "debug")
    config["log"] = parser.get("Gateway", "log")

    return config
