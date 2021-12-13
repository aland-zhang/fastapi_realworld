from pydantic import BaseSettings
from pydantic.networks import AnyUrl


class PostgresDsnPsycopg(AnyUrl):
    allowed_schemes = {"postgresql+psycopg2"}
    user_required = True


class Settings(BaseSettings):
    SECRET: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: PostgresDsnPsycopg = None
    DATABASE_URL_TEST: PostgresDsnPsycopg = None
    API_KEY_SCHEME: str = "Token"
    API_KEY_NAME: str = "Authorization"
    DESCRIPTION_TOKEN: str = """
    For accessing the protected API resources, you must have received a a valid JWT token after registering or logging in. This JWT token must then be used for all protected resources by passing it in via the 'Authorization' header.

    A JWT token is generated by the API by either registering via /users or logging in via /users/login.

    The following format must be in the 'Authorization' header :

    Token xxxxxx.yyyyyyy.zzzzzz
    """

    @property
    def sqlalchemy_db(self) -> str:
        return (
            str(self.DATABASE_URL) if self.DATABASE_URL else str(self.DATABASE_URL_TEST)
        )

    @property
    def sqlalchemy_db_test(self) -> str:
        return (
            str(self.DATABASE_URL_TEST)
            if self.DATABASE_URL_TEST
            else str(self.DATABASE_URL)
        )

    class Config:
        env_file = ".env"


config = Settings()
