from pydantic import BaseSettings
from pydantic import SecretStr

class Vereficator(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file=".env"
        env_file_encoding="utf-8"

configs = Vereficator()
