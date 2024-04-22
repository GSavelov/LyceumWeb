from flask_restful import abort, Resource, reqparse
from flask import jsonify
from sqlalchemy import select
from data import db_session
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


parser = reqparse.RequestParser()
parser.add_argument('question')
parser.add_argument('answer')
parser.add_argument('user_id')
parser.add_argument('group_name')


class GroupsResource(Resource):
    def get(self, group_id):
        abort_if_group_not_found(group_id)
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        return jsonify({'group': group.to_dict(
            only=('id', 'name', 'user_id'))})


class GroupsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        groups = session.query(Group).all()
        return jsonify({'groups': [item.to_dict(
            only=('id', 'name', 'user_id')) for item in groups]})


class QuestionsResource(Resource):
    def get(self, que_id):
        abort_if_question_not_found(que_id)
        session = db_session.create_session()
        question = session.query(Exercise).get(que_id)
        return jsonify({'group': question.to_dict(
            only=('id', 'question', 'answer', 'user_id'))})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        exercise = Exercise(
            question=args.question,
            answer=args.answer,
            user_id=args.user_id
        )
        session.add(Exercise)
        session.commit()
        return jsonify({"id": exercise.id})


class QuestionsListResource(Resource):
    def get(self, group_id):
        abort_if_group_not_found(group_id)
        session = db_session.create_session()
        que_ids = session.execute(select(Quest_groups).where(Quest_groups.c.group_id == group_id)).all()
        return jsonify({'questions': [que[0] for que in que_ids]})
