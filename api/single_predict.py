from transformers import BertForSequenceClassification, BertTokenizer
import torch
import logging
import time


def predict_single(seq):

    threshold = 0.5

    start = time.process_time()
    model = BertForSequenceClassification.from_pretrained(
        "./models/AmBERT")
    elapsed = time.process_time() - start
    logging.warn(msg="Model loaded in "+str(elapsed)+" seconds")

    start = time.process_time()
    tokenizer = BertTokenizer.from_pretrained("./models/tokenizer/")
    elapsed = time.process_time() - start
    logging.warn(msg="Tokenizer loaded in "+str(elapsed)+" seconds")


    start = time.process_time()
    inputs = tokenizer(" ".join(seq), return_tensors="pt")
    elapsed = time.process_time() - start
    logging.warn(msg="Sequence tokenized in "+str(elapsed)+" seconds")

    start = time.process_time()
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.softmax(logits, axis=-1).detach().numpy()
    seq_dict = {
        "sequence": seq,
        "prediction": str(prediction[0][1])
    }
    elapsed = time.process_time() - start
    logging.warn(msg="Prediction processed in "+str(elapsed)+" seconds")
    
    if prediction[0][1] > threshold:

        return ("Positive", seq_dict)
    else:

        return ("Negative", seq_dict)
