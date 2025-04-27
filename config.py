import os 



class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["BLOG_PRACTICE_DATABASE_URL"]
    SECRET_KEY = os.environ["SECRET_KEY"]


