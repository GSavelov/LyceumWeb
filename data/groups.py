import datetime
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy
from sqlalchemy import orm, Table, Column, Integer, ForeignKey
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')
    exercises = orm.relationship('Exercise', secondary='quest_groups', backref='Group')


Quest_groups = Table('quest_groups',
                     SqlAlchemyBase.metadata,
                     Column('question_id', Integer, ForeignKey('exercises.id')),
                     Column('group_id', Integer, ForeignKey('groups.id'))
                     )
