from flask_restful import abort, Resource, reqparse
from flask import jsonify
from sqlalchemy import select, insert
from data import db_session
from data.users import User
from data.groups import Group, Quest_groups
from data.exercises import Exercise


def abort_if_group_not_found(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404, message=f"Group {group_id} not found")


def abort_if_question_not_found(que_id):
    session = db_session.create_session()
    que = session.query(Group).get(que_id)
    if not que:
        abort(404, message=f"Question {que_id} not found")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('question')
parser.add_argument('answer')
parser.add_argument('group_name')
parser.add_argument('questions', action='append')
parser.add_argument('user_id')
parser.add_argument('user_name')
parser.add_argument('email')


class GroupsResource(Resource):
    def get(self, group_id):
        abort_if_group_not_found(group_id)
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        que_ids = session.execute(select(Quest_groups).where(Quest_groups.c.group_id == group_id)).all()
        return jsonify({'group': group.to_dict(
            only=('id', 'name', 'user_id')), 'questions': [que[0] for que in que_ids]})


class GroupsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        groups = session.query(Group).all()
        return jsonify([item.to_dict(
            only=('id', 'name', 'user_id')) for item in groups])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        group = Group(
            name=args.group_name,
            user_id=args.user_id
        )
        session.add(group)
        session.commit()
        for i in args.questions:
            session.execute(insert(Quest_groups).values(question_id=i, group_id=group.id))
            session.commit()
        return jsonify({"id": group.id})


class QuestionsResource(Resource):
    def get(self, que_id):
        abort_if_question_not_found(que_id)
        session = db_session.create_session()
        question = session.query(Exercise).get(que_id)
        return jsonify(question.to_dict(
            only=('question', 'answer')))


class QuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        questions = session.query(Exercise).all()
        return jsonify([item.to_dict(
            only=('id', 'question', 'answer', 'user_id')) for item in questions])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        exercise = Exercise(
            question=args.question,
            answer=args.answer,
            user_id=args.user_id
        )
        session.add(exercise)
        session.commit()
        return jsonify({"id": exercise.id})


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(user.to_dict(
            only=('name', 'email')))


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify([item.to_dict(
            only=('id', 'name', 'email')) for item in users])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args.user_name,
            email=args.email
        )
        session.add(user)
        session.commit()
        return jsonify({"id": user.id})
