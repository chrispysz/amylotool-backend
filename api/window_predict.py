from csv import reader
from transformers import BertForSequenceClassification, BertTokenizer
import torch
import numpy as np
import tensorflow as tf
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score, roc_curve, auc, average_precision_score


def run(seq):

    seq_cutoff = 39

    threshold = 0.5

    model = BertForSequenceClassification.from_pretrained(
        "./models/AmBERT")
    tokenizer = BertTokenizer.from_pretrained("./models/tokenizer/")

    current_label = 0


    predictions = []
    positive_sequences = []
    spec_preds = []

    seq_proper = ''
    for aa in seq:
        seq_proper += aa+' '

    if len(seq) > seq_cutoff:
        splits = len(seq)-seq_cutoff
        for i in range(splits):
            subseq = seq[i:seq_cutoff+i+1]
            inputs = tokenizer(" ".join(subseq), return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits
            prediction = torch.softmax(logits, axis=-1).detach().numpy()
            if prediction[0][1] > threshold:
                print(subseq)
                predictions.append('1')
            else:

                predictions.append('0')

            spec_preds.append(prediction[0][1])

    if '1' in predictions:
        return "Positive"

    else:
        return "Negative"


