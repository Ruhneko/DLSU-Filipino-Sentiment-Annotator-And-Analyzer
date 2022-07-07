import demoji
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # Load vocabulary
import seaborn as sns
import tensorflow as tf
import tensorflow.keras.layers as tfl
import tensorflow.keras.models as tfm
import tensorflow.keras.utils as tfu
from gensim.models import KeyedVectors
from scikeras.wrappers import KerasClassifier, KerasRegressor
from sklearn.metrics import (ConfusionMatrixDisplay, classification_report,
                             confusion_matrix)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from tensorflow.keras.metrics import *


class Classifier:
 
    # default constructor
    def __init__(self, datadir='data'):
        tf.random.set_seed(1)
        vocab = pd.read_csv(datadir + '/vocab.csv').rename(columns={'Unnamed: 0': 'token'})
        vocab = set(vocab['token'].tolist())
        vocab = list(vocab)
        max_len = 60
        self.vectorizer = tfl.TextVectorization(
            output_mode='int',
            output_sequence_length=max_len,
            standardize=None,
            vocabulary=vocab
        )

        model_ug_sg = KeyedVectors.load(datadir + '/w2v/w2v_model_ug_sg.word2vec')
        embeddings_index = {}
        for w in model_ug_sg.wv.key_to_index:
            embeddings_index[w] = model_ug_sg.wv[w]

        voc = self.vectorizer.get_vocabulary()
        word_index = dict(zip(voc, range(len(voc))))
        embedding_matrix = np.zeros((len(voc), 200))

        for word, i in word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        self.model = tf.keras.models.load_model(datadir + '/lr0001_b16')
        self.model.layers[1].set_weights([embedding_matrix])
        met = [BinaryAccuracy(), Precision(), Recall()]
        adam = tf.keras.optimizers.Adam(learning_rate=0.0001)
        self.model.compile(optimizer=adam, loss='binary_crossentropy', metrics=met)

    def strip_emoji(string):
        string = demoji.replace(string, '')
        return string

    def strip_all_tweets(self, X):
        X_copy = np.copy(X)
        for i in range(len(X_copy)):
            X_copy[i] = self.strip_emoji(X_copy[i])
        return X_copy

    def pred_report(self, X_test, y_test, strip=False):
        if strip:
            X_test = self.strip_all_tweets(X_test)
        y_pred = self.model.predict(self.vectorizer(X_test))
        y_classes = np.round(y_pred).astype(int)
        report = classification_report(y_test, y_classes, output_dict=True)
        print(classification_report(y_test, y_classes))
        
        cm = confusion_matrix(y_test, y_classes, labels=[0,1])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0,1])
        disp.plot()
        plt.show()
    
        return report

    def predict(self, X_test, strip=False):
        if strip:
            X_test = self.strip_all_tweets(X_test)
        y_pred = self.model.predict(self.vectorizer(X_test))
        y_classes = np.round(y_pred).astype(int)
        return y_classes