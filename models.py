import pickle
import spacy
import numpy as np

#nlp = spacy.load('en_core_web_lg')
#with open('nlp_en.pkl', 'rb') as f:
#    nlp = pickle.load(f)

class SentimentClassifier(object):
    """
    Модель анализа текста на содержание спама (на английском языке)
    """
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

    def get_prediction_message(self, text):
        text_ls = []
        text_ls.append(text)
        text = text_ls
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + "," + self.classes_dict[
            class_prediction] + "," + str(round(prediction_probability * 100, 2))


class ToneSentimentClassifier(object):
    def __init__(self):
        with open('model_text_tone.pkl', 'rb') as f:
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
            return self.model.predict(np.array([nlp(text).vector]))[0], \
                   self.model.predict_proba(np.array([nlp(text).vector]))[0][1]
        except:
            print("prediction error")
            return -1, 0.8

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + "," + self.classes_dict[
            class_prediction] + "," + str(round(prediction_probability * 100, 2))


class PhoneReviewsToneSentimentClassifier(object):
    """
    Модель для анализа тональности отзывов о сотовых телефонах (на русском языке)
    """
    def __init__(self):
        with open('model_phone_review.pkl', 'rb') as f:
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

    def get_prediction_message(self, text):
        text_ls = []
        text_ls.append(text)
        text = text_ls
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + "," + self.classes_dict[
            class_prediction] + "," + str(round(prediction_probability * 100, 2))
