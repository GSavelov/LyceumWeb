import datetime
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Exercise(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'exercises'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user = orm.relationship('User')
    groups = orm.relationship('Group', secondary='quest_groups', backref='Exercise')

