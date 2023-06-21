import os
from numpy import array
from pickle import load as pickle_load

os.environ[
    'TF_CPP_MIN_LOG_LEVEL'] = '1'  
import tensorflow as tf

tf.get_logger().setLevel(
    'ERROR')  # or any {'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL', 'ALL'}

from json import load as json_load

from tensorflow import keras
from keras.models import load_model

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from cppyy import gbl, include

include("/static/include/cpplib.hpp")
random_choice = gbl.random_choice


def ensure_nltk_data_downloaded():
  from nltk import download, data
  try:
    data.find('tokenizers/punkt')
  except LookupError:
    download('punkt')
  try:
    data.find('corpora/wordnet')
  except LookupError:
    download('wordnet')


ensure_nltk_data_downloaded()

lemmatizer = WordNetLemmatizer()

with open("intents.json") as file:
  data = json_load(file)

words = pickle_load(open('words.pkl', 'rb'))
classes = pickle_load(open('classes.pkl', 'rb'))
model = load_model('model_v12.h5')

responses_if_no_intent = [
    "Sorry, I don't understand.",
    "I'm not sure what you mean.",
    "I don't understand.",
    "I'm not sure I understand.",
]


# lemmatize and lower each word and remove duplicates
def clean_up_sentence(sentence):
  sentence_words = word_tokenize(
      sentence)  # tokenize the pattern - split words into array
  sentence_words = [
      lemmatizer.lemmatize(word.lower()) for word in
      sentence_words  # lemmatize - create base word, in attempt to represent related words
  ]
  return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words):
  sentence_words = clean_up_sentence(sentence)  # tokenize the pattern
  bag = [0] * len(words)  # initialize bag of words array
  for s in sentence_words:
    for i, w in enumerate(
        words):  # assign 1 if current word is in the vocabulary position
      if w == s:
        bag[i] = 1
  return (array(bag))  # return bag of words array


# predict the class of the sentence using the model and return the probability of each class
def predict_class(sentence, model):
  p = bow(sentence, words)  # filter below a threshold (e.g. 0.25)
  res = model.predict(array(
      [p]))[0]  # get the highest probability from the predictions
  ERROR_THRESHOLD = 0.25
  results = [
      [i, r]
      for i, r in enumerate(res)
      if r > ERROR_THRESHOLD  # sort by strength of probability (highest first)
  ]  # filter out predictions below a threshold (e.g. 0.25)
  results.sort(key=lambda x: x[1],
               reverse=True)  # sort by strength of probability (highest first)
  return_list = []  # create a list of tuples (class, probability)
  for r in results:  # return tuple of intent and probability (e.g. ("greeting", 0.999))
    return_list.append({
        "intent": classes[r[0]],
        "probability": str(r[1])
    })  #   return tuple of intent and probability (e.g. ("greeting", 0.999))
  return return_list


# get a random response from the intents file for the tag that was predicted
def get_response(ints, intents_json):
  if not ints:  # if there is no matching tag
    return random_choice(responses_if_no_intent)
  tag = ints[0]["intent"]  # get the tag of the first prediction
  list_of_intents = intents_json["intents"]  # find the matching intent tag
  for i in list_of_intents:
    if i["tag"] == tag:  # set a random response from the intent
      result = random_choice(i["responses"])
      break
  return result


def chatbot_response(msg):
  ints = predict_class(msg, model)
  res = get_response(ints, data)
  return res