"""configuration variables."""

from os import environ, path
from os.path import exists

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
env_path = path.join(basedir, ".env")
load_dotenv(env_path)

st.secrets

if not exists(env_path):
    raise Exception(".env is absent")


print(path.join(basedir, ".env"))

class Config(object):
    """Set  configuration from .env file."""

    # General Config
    USER = environ.get("D4S_USER")
    PASS = environ.get("D4S_KEY")
    DRV_CHROME = environ.get("SBR_WEBDRIVER")
    WS_KEY= environ.get("WS_KEY")

    def __init__(self):
        print(self, vars(self).items())
        for name, value in vars(self).items():
            print(f"  {name}: {value}")
        
settings = Config()
