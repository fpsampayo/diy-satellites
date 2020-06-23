from password import uri


class Config():
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
