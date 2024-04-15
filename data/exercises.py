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
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')


