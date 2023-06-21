import pickle
import random
import numpy as np
import nltk
import json

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam as adam
from keras.callbacks import EarlyStopping

from nltk.stem import WordNetLemmatizer

nltk.download(
    'punkt')  # download for tokenizer (e.g. "running" -> "run", "ran" -> "run")
nltk.download('wordnet')  # download for lemmatization (e.g. "running" -> "run")

lemmatizer = WordNetLemmatizer(
)  # lemmatize words to their root form (e.g. "running" -> "run")

words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

with open("intents.json") as file:
  data = json.load(file)

for intent in data[
    'intents']:  # loop through each sentence in our intents patterns
  for pattern in intent['patterns']:  # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern)  # add to our words list
    words.extend(w)  # add to documents in our corpus (e.g. [[input, class]])
    documents.append(
        (w, intent['tag']
        ))  # add to our classes list (e.g. ["greeting", "goodbye", ...])
    if intent['tag'] not in classes:  # add to our classes list
      classes.append(
          intent['tag']
      )  # lemmatize, lower each word and remove duplicates (e.g. "running", "ran" -> "run")

words = [  # lemmatize and lower each word and remove duplicates
    lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words
]
words = sorted(list(set(words)))  # remove duplicates

classes = sorted(list(set(classes)))  # sort classes

pickle.dump(words, open('words.pkl', 'wb'))  # save words
pickle.dump(classes, open('classes.pkl', 'wb'))  # save classes

# training data

training = []  # create an empty array for our training data
output_empty = [0] * len(classes)  # create an empty array for our output

# add data to training list
for doc in documents:
  bag = []  # bag of words for each sentence
  pattern_words = doc[0]
  pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words] # lemmatize each word - create base word, in attempt to represent related words (e.g. "cats" and "cat")
  for w in words:
    bag.append(1) if w in pattern_words else bag.append(0) # assign 1 if current word is in the vocabulary position, otherwise assign 0

  output_row = list(output_empty)  # initialize our output for this document
  output_row[classes.index(doc[1])] = 1  # set 1 for current tag

  training.append([bag, output_row])  # add this to our training data set

random.shuffle(
    training)  # shuffle our features and turn into np.array to train our model
training = np.array(training,
                    dtype=object)  # create train and test lists (X, Y)

train_x = list(training[:, 0])  # train_x contains the Bag of Words
train_y = list(training[:, 1])  # train_y contains the intents

model = Sequential(
)  # create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
model.add(Dense(128, input_shape=(len(train_x[0]),),
                activation='sigmoid'))  # input layer
model.add(Dropout(0.5))  # prevent overfitting
model.add(Dense(64, activation='sigmoid'))  # hidden layer
model.add(Dropout(0.5))  # prevent overfitting

model.add(Dense(len(train_y[0]), activation='softmax'))  # output layer

optimizer = adam(learning_rate=0.001)  # set learning rate

early_stop = EarlyStopping(
    monitor='val_loss', # quantity to be monitored (loss or accuracy)
    mode='min',  # early stopping will be stopped when the quantity monitored has stopped decreasing (for 'loss', use min; for 'accuracy', use max)
    patience=
    8000,  # set number of epochs with no improvement after which training will be stopped (higher number = more accurate but slower)
    restore_best_weights=
    True  # restore model weights from the epoch with the best value of the monitored metric
)

model.compile(
    loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy']
)  # compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model

history = model.fit( # fit model with training data and validation data
    np.array(train_x),
    np.array(train_y),
    epochs=
    10000,  # set number of epochs to train for (higher number = more accurate but slower)
    batch_size=
    256,  # set number of samples to train on before updating weights (higher number = faster but less accurate)
    validation_split=0.1,  # split data into 90% training and 10% validation data
    callbacks=[early_stop])  # train model with early stopping callback

model.save('chatbot_model_v12.h5', history) # save model to file (e.g. chatbot_model.h5) 

print("model created")