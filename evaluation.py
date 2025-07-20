# evaluation.py
from sklearn.metrics import accuracy_score, confusion_matrix

def evaluate_model(pred_labels, true_labels):
    acc = accuracy_score(true_labels, pred_labels)
    cm = confusion_matrix(true_labels, pred_labels, labels=["POSITIVE", "NEGATIVE", "NEUTRAL"])
    return acc, cm
