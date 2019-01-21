"""
    .. autoclass:: RocAucScore(one_hot_labels=True, one_hot_offset=0, one_hot_classes=10)
"""

from torchbearer import metrics


@metrics.default_for_key('roc_auc')
@metrics.default_for_key('roc_auc_score')
@metrics.to_dict
class RocAucScore(metrics.EpochLambda):
    """Area Under ROC curve metric. Default for keys: 'roc_auc', 'roc_auc_score'.

    .. note::

        Requires :mod:`sklearn.metrics`.

    Args:
        one_hot_labels (bool): If True, convert the labels to a one hot encoding. Required if they are not already.
        one_hot_offset (int): Subtracted from class labels, use if not already zero based.
        one_hot_classes (int): Number of classes for the one hot encoding.
    """

    def __init__(self, one_hot_labels=True, one_hot_offset=0, one_hot_classes=10):
        import sklearn.metrics
        import numpy as np

        def to_categorical(y):
            return np.eye(one_hot_classes, dtype='uint8')[y - one_hot_offset]

        if one_hot_labels:
            process = to_categorical
        else:
            process = lambda y: y

        super().__init__('roc_auc_score', lambda y_pred, y_true: sklearn.metrics.roc_auc_score(process(y_true.cpu().numpy()), y_pred.cpu().detach().numpy()))
