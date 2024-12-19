"""configuration variables."""

from os import environ, path
from os.path import exists

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
env_path = path.join(basedir, ".env")
load_dotenv(env_path)


# if not exists(env_path):
#     #raise Exception(".env is absent")
#     print(".env is absent")
#     import streamlit as st
    

print(path.join(basedir, ".env"))

class Config(object):
    """Set  configuration from .env file."""

    # General Config
    USER = environ.get("D4S_USER")
    PASS = environ.get("D4S_KEY")
    DRV_CHROME = environ.get("SBR_WEBDRIVER")
    WS_KEY= environ.get("WS_KEY")

    def __init__(self):
        for attr_name in dir(self):
            if not attr_name.startswith('_'):  # Avoid private attributes
                attr_value = getattr(self, attr_name)
                if attr_value == None:
                    import streamlit as st
                    print("sec", st.secrets)
                print(f"{attr_name}: {attr_value}")
        pass
        
settings = Config()
