from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class ExerciseForm(FlaskForm):
    question = StringField('Вопрос', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class GroupForm(FlaskForm):
    name = StringField('Название группы', validators=[DataRequired()])
    picks = SelectMultipleField('Выберите вопросы', validators=[DataRequired()])
    submit = SubmitField('Добавить')
