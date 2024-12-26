"""configuration variables."""
import inspect

from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))



class Config:
    """Set  configuration from .env file."""

    # General Config
    D4S_USER = environ.get("D4S_USER")
    D4S_KEY = environ.get("D4S_KEY")
    SBR_WEBDRIVER = environ.get("SBR_WEBDRIVER")
    WS_KEY = environ.get("WS_KEY")

    def __init__(self):
        from streamlit import secrets
        print(secrets)
        if not path.exists("config.yaml"):
            raise Exception("You could not create modules! Descripe it please in config.yaml")

        print(secrets)
        for name, value in inspect.getmembers(self):
            if not name.startswith('_') and not inspect.ismethod(value): #Exclude internal attributes and methods
                print(f"  {name}: {value}")
                if name not in secrets:
                    raise KeyError("Try somewhere else, please")
                elif value is None:
                    setattr(self, name, secrets[name])
                
        #if not settings.WS_KEY:
        #settings.WS_KEY = secrets.WS_KEY

settings = Config()
