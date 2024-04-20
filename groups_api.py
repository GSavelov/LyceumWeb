import flask
from flask import jsonify, make_response, request
from data import db_session
from data.groups import Group

blueprint = flask.Blueprint(
    'groups_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/groups', methods=['GET'])
def get_groups():
    return '1'


# @blueprint.route('/jobs/<int:jobs_id>', methods=['GET'])
# def get_one_jobs(jobs_id):
#     db_sess = db_session.create_session()
#     job = db_sess.query(Group).get(jobs_id)
#     if not job:
#         return make_response(jsonify({'error': 'Not found'}), 404)
#     return jsonify(
#         {
#             'job': job.to_dict(rules=('-team_lead_user.jobs',))
#         }
#     )
#
#
# @blueprint.route('jobs', methods=['POST'])
# def create_job():
#     if not request.json:
#         return make_response(jsonify({'error': 'Empty request'}), 400)
#     elif not all(key in request.json for key in
#                  ['job', 'team_lead', 'work_size']):
#         return make_response(jsonify({'error': 'Bad request'}), 400)
#     db_sess = db_session.create_session()
#     job = Group(**request.json)
#     db_sess.add(job)
#     db_sess.commit()
#     return jsonify({'id': job.id})
