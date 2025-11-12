from seqeval.metrics import precision_score, recall_score, f1_score, classification_report

def evaluate(true_labels, pred_labels):
    print("Precision:", precision_score(true_labels, pred_labels))
    print("Recall:", recall_score(true_labels, pred_labels))
    print("F1 Score:", f1_score(true_labels, pred_labels))
    print(classification_report(true_labels, pred_labels))
import numpy as np
from sklearn.utils import resample
from seqeval.metrics import precision_score, recall_score, f1_score

def bootstrap_metrics(true_labels, pred_labels, n_iterations=1000, alpha=0.05):
    precisions, recalls, f1s = [], [], []
    data = list(zip(true_labels, pred_labels))

    for _ in range(n_iterations):
        sample = resample(data, replace=True, n_samples=len(data))
        y_true_sample, y_pred_sample = zip(*sample)
        precisions.append(precision_score(y_true_sample, y_pred_sample))
        recalls.append(recall_score(y_true_sample, y_pred_sample))
        f1s.append(f1_score(y_true_sample, y_pred_sample))

    def ci(metric_list):
        lower = np.percentile(metric_list, 100 * alpha / 2)
        upper = np.percentile(metric_list, 100 * (1 - alpha / 2))
        return round(lower, 3), round(upper, 3)

    return {
        "Precision CI": ci(precisions),
        "Recall CI": ci(recalls),
        "F1 CI": ci(f1s),
    }
def bonferroni_threshold(alpha=0.05, comparisons=4):
    return alpha / comparisons 
