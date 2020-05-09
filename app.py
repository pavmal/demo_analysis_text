import os, time
import pickle
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length

sec_key = os.environ['SEC_KEY']


class SentimentClassifier(object):
    def __init__(self):
        with open('model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        self.classes_dict = {0: "negative", 1: "positive", -1: "prediction error"}

    @staticmethod
    def get_probability_words(probability):
        if probability < 0.55:
            return "neutral or uncertain"
        if probability < 0.7:
            return "probably"
        if probability > 0.95:
            return "certain"
        else:
            return ""

    def predict_text(self, text):
        try:
            return self.model.predict(text)[0], self.model.predict_proba(text)[0][1]
        except:
            print("prediction error")
            return -1, 0.8

    def predict_list(self, list_of_texts):
        try:
            return self.model.predict([list_of_texts]), self.model.predict_proba([list_of_texts])
        except:
            print('prediction error')
            return None

    def get_prediction_message(self, text):
        text_ls = []
        text_ls.append(text)
        text = text_ls
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + "," + self.classes_dict[
            class_prediction] + "," + str(round(prediction_probability * 100, 2))


print("Preparing classifier")
start_time = time.time()
classifier = SentimentClassifier()
print("Classifier is ready")
print(time.time() - start_time, "seconds")


class DemoModel(FlaskForm):
    analis_text = TextAreaField('Текст для анализа тональности', validators=[Length(min=0, max=250)])
    submit = SubmitField('Отправить на обработку')


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def render_main():
    form = DemoModel()
    if request.method == "POST":
        user_text = form.analis_text.data
        #print(user_text)
        predictions = classifier.get_prediction_message(user_text).split(',')
        #print(predictions)
        prediction_message = 'Ваш отзыв классифицирован как ' + predictions[1] + \
                             ' и относится к целевому классу с вероятностью: ' + predictions[2] + r'%'
        return render_template('demo.html', form=form, result=prediction_message)
    else:
        return render_template('demo.html', form=form, result=None)


@app.route('/about/')
def render_about():
    """
    Представление страницы "О сервисе"
    :return: Описание сервиса
    """
    return render_template('about.html')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = sec_key
    app.run()  # for gunicorn server
