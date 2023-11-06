import numpy as np
from scipy.stats import multivariate_normal as mvn


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.naivebay = dict()
        self.priors = dict()

    def fit(self, X, Y):
        """Fit Naive Bayes classifier according to X, y."""
        labels = set(Y)

        for c in labels:
            current_x = X[Y == c]

            self.naivebay = {
                "mean": current_x.mean(axis=0),
                "var": current_x.var(axis=0) + self.alpha,
            }
            self.priors = float(len(Y[Y == c])) / len(Y)

    def predict(self, X):
        N, D = X.shape
        lenn = len(self.naivebay)
        P = np.zeros((N, lenn))
        for i, j in self.naivebay.iteritems():
            mean, var = j["mean"], j["var"]
            P[:, i] = mvn.logpdf(X, mean=mean, cov=var) + np.log(self.priors)
        return np.argmax(P, axis=1)

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        pred = self.predict(X_test)
        return np.mean(pred == y_test)
