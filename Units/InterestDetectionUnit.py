import numpy as np
from sklearn.naive_bayes import MultinomialNB
from keras.models import Sequential
from keras.layers import SimpleRNN


class InterestDetectionUnit:
    def __init__(self, search_history, reaction_history):
        self.search_history = search_history
        self.reaction_history = reaction_history
        self.interests = []
        self.model = None

    def detect_interest(self):
        # Analyze user's search history and reactions
        tau = self.analyze_history_and_reactions()

        # Use Naive Bayes to classify documents
        classifier = MultinomialNB()
        t_tau = classifier.fit_transform(tau)

        # Perform majority voting on t_tau to find the user's main interest
        self.interests.append(np.argmax(np.bincount(t_tau)))

    def train_model(self):
        # Train a many-to-one vanilla RNN model on the user's prior search interests
        self.model = Sequential()
        self.model.add(SimpleRNN(units=64, input_shape=(None, len(self.interests))))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.fit(np.array(self.interests), epochs=10)

    def predict_interest(self):
        # Predict the user's search interest
        return self.model.predict(np.array(self.interests))

    def analyze_history_and_reactions(self):
        # This is a simple implementation that just returns the search history.
        # You might want to replace this with your own implementation.
        return self.search_history
