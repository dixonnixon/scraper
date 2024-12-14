"""configuration variables."""

from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))



class Config:
    """Set  configuration from .env file."""

    # General Config
    USER = environ.get("D4S_USER")
    PASS = environ.get("D4S_KEY")
    DRV_CHROME = environ.get("SBR_WEBDRIVER")
settings = Config()
