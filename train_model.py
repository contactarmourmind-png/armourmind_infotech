import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

with open("ai/intents.json") as file:
    data = json.load(file)

words=[]
classes=[]
documents=[]
ignore=["?","!"]

for intent in data["intents"]:
    for pattern in intent["patterns"]:

        tokens=nltk.word_tokenize(pattern)
        words.extend(tokens)
        documents.append((tokens,intent["tag"]))

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words=[lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore]
words=sorted(set(words))
classes=sorted(set(classes))

training=[]
output_empty=[0]*len(classes)

for doc in documents:

    bag=[]
    pattern_words=[lemmatizer.lemmatize(w.lower()) for w in doc[0]]

    for w in words:
        bag.append(1 if w in pattern_words else 0)

    output_row=list(output_empty)
    output_row[classes.index(doc[1])]=1

    training.append([bag,output_row])

random.shuffle(training)
training=np.array(training,dtype=object)

train_x=list(training[:,0])
train_y=list(training[:,1])

model=Sequential()

model.add(Dense(128,input_shape=(len(train_x[0]),),activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64,activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation="softmax"))

sgd=SGD(learning_rate=0.01,momentum=0.9)

model.compile(loss="categorical_crossentropy",optimizer=sgd,metrics=["accuracy"])

model.fit(np.array(train_x),np.array(train_y),epochs=200,batch_size=5)

model.save("chatbot_model.h5")

print("Model trained successfully")