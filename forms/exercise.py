from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired


class ExerciseForm(FlaskForm):
    question = StringField('Вопрос', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class GroupForm(FlaskForm):
    pass
