import os, time
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length
import models

# sec_key = os.environ['SEC_KEY']
SECRET_KEY = os.urandom(32)

print("Preparing classifier")
start_time = time.time()
spam_classifier = models.SentimentClassifier()
tone_classifier = models.ToneSentimentClassifier()
print("Classifier is ready")
print(time.time() - start_time, "seconds")


class DemoModel(FlaskForm):
    """
    analis_text: поле формы для ввода текста для анализа
    submit: кнопка отправки текста на обработку
    """
    analis_text = TextAreaField('Текст для анализа на спам', validators=[Length(min=0, max=250)])
    analis_text_tone = TextAreaField('Текст для анализа тональности', validators=[Length(min=0, max=250)])
    submit = SubmitField('Отправить на обработку')


app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def render_main():
    form = DemoModel()
    if request.method == "POST":

        # for SPAM
        user_text = form.analis_text.data
        if user_text != '':
            predictions = spam_classifier.get_prediction_message(user_text).split(',')
            if predictions[1] == 'positive':  # class 1 - SPAM
                class_res = 'SPAM'
                persent = predictions[2]
            elif predictions[1] == 'negative':
                class_res = 'NOT SPAM'
                persent = str(100 - float(predictions[2]))
            else:
                class_res = 'NEUTRAL'
                persent = predictions[2]
            prediction_message = 'Ваш текст классифицирован как: {} c вероятностью: {} %'.format(class_res, persent)
        else:
            prediction_message = None

        # for tone analysis
        user_text_tone = form.analis_text_tone.data
        if user_text_tone != '':
            predictions_tone = tone_classifier.get_prediction_message(user_text_tone).split(',')
            if predictions_tone[1] == 'positive':  # class 1 - positive feedback
                class_res_tone = 'POSITIVE FEEDBACK'
                persent_tone = predictions_tone[2]
            elif predictions_tone[1] == 'negative':
                class_res_tone = 'NEGATIVE FEEDBACK'
                persent_tone = str(100 - float(predictions_tone[2]))
            else:
                class_res_tone = 'NEUTRAL'
                persent_tone = predictions_tone[2]
            prediction_message_tone = 'Ваш отзыв классифицирован как: {} c вероятностью: {} %'.format(class_res_tone,
                                                                                                      persent_tone)
        else:
            prediction_message_tone = None

        return render_template('demo.html', form=form, result=prediction_message, result_tone=prediction_message_tone)
    else:
        return render_template('demo.html', form=form, result=None, result_tone=None)


@app.route('/about/')
def render_about():
    """
    Представление страницы "О сервисе"
    :return: Описание сервиса
    """
    return render_template('about.html')


if __name__ == '__main__':
    #app.run('127.0.0.1', 7799, debug=True)
    app.run()  # for gunicorn server
