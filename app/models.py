from datetime import datetime, timezone 
from typing import Optional

from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash


from app import db, login 



@login.user_loader
def load_user(email):
    return db.session.get(User, email)


class User(UserMixin, db.Model):

    __tablename__ = "user"

    email = so.mapped_column(sa.String, primary_key=True)
    call_user_by_name = so.mapped_column(sa.String)
    password = so.mapped_column(sa.String)
    registered_at_datetime = so.mapped_column(sa.DateTime)
    row_insert_datetime = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    row_update_datetime = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    article_relation = so.relationship("Article", back_populates="user_relation")

    def set_password(self, psswrd):
        self.password_hash = generate_password_hash(psswrd)

    def check_password(self, psswrd):
        return check_password_hash(self.password, psswrd)

    def __repr__(self):
        return "<" + self.call_user_by_name + ": " + self.email + ">"

    @property
    def id(self):
        return self.email


class Article(db.Model):

    __tablename__ = "article"

    id = so.mapped_column(sa.String, primary_key=True)
    title = so.mapped_column(sa.String)
    content = so.mapped_column(sa.String)
    primary_category = so.mapped_column(sa.String)
    primary_sub_category = so.mapped_column(sa.String)
    publish_status = so.mapped_column(sa.String)
    publisher_email = so.mapped_column(sa.String, sa.ForeignKey(User.email), index=True)
    row_insert_datetime = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    row_update_datetime = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_relation = so.relationship("User", back_populates="article_relation")

    def __repr__(self):
        return "<Article: " + self.title + ">"

