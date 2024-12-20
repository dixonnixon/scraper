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
    WS_KEY= environ.get("WS_KEY")

    def __init__(self):
        import streamlit as st
        print(st.secrets)
        if not path.exists("config.yaml"):
            raise Exception("You could not create modules! Descripe it please in config.yaml")
settings = Config()