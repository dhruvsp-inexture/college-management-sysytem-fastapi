from datetime import timedelta
from fastapi_jwt_auth import AuthJWT
from config import JWTConfig


@AuthJWT.load_config
def get_config():
    return JWTConfig()


class Token:

    def __init__(self, sub: int, authorize: AuthJWT):
        self.access_expires: int = JWTConfig().ACCESS_TOKEN_EXPIRE_TIME_MINUTES
        self.refresh_expires: int = JWTConfig().REFRESH_TOKEN_EXPIRE_TIME_HOURS
        self.algorithm = JWTConfig().JWT_ALGORITHM
        self.subject = sub
        self.Authorize = authorize

    def create_access_token(self):
        """
        This method is used to create the access token.
        :return: access token
        """
        return self.Authorize.create_access_token(subject=str(self.subject),
                                                  expires_time=timedelta(minutes=self.access_expires),
                                                  algorithm=self.algorithm)

    def create_refresh_token(self):
        """
        This method is used to create the refresh token.
        :return: refresh token
        """
        return self.Authorize.create_refresh_token(subject=str(self.subject),
                                                   expires_time=timedelta(hours=self.refresh_expires),
                                                   algorithm=self.algorithm)

    def get_tokens(self):
        return {"access_token": self.create_access_token(), "refresh_token": self.create_refresh_token()}
