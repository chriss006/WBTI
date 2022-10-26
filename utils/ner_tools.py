from transformers import AutoTokenizer, AutoModel
from transformers import TFBertModel
import numpy as np
import torch
import tensorflow as tf
from collections import defaultdict
import pandas as pd
train = pd.read_csv("/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/models/ner/ner_train.csv")
tokenizer = AutoTokenizer.from_pretrained("skt/kobert-base-v1", use_fast=False)


def ner_inference(test_sentence, nr_model):
    label = train['tar'].unique().tolist()
    label_dic = {word: i for i, word in enumerate(label)}  # enumerate: 인덱스와 값을 함께 반환
    label_dic.update({"[PAD]": len(label_dic)})  # label_dic에 [PAD] 추가
    index_to_ner = {i: j for j, i in label_dic.items()}

    temp_d = defaultdict(list)
    result = defaultdict(str)
    tokenized_sentence = np.array([tokenizer.encode(test_sentence, max_length=36, truncation=True, padding='max_length')])
    tokenized_mask = np.array([[int(x != 1) for x in tokenized_sentence[0].tolist()]])
    ans = nr_model.predict([tokenized_sentence, tokenized_mask])
    ans = np.argmax(ans, axis=2)

    tokens = tokenizer.convert_ids_to_tokens(tokenized_sentence[0])

    for token, label_idx in zip(tokens, ans[0]):
        if (token.startswith("##")):
            temp_d[index_to_ner[label_idx]].append(token[2:])
        elif (token == '[CLS]'):
            pass
        elif (token == '[SEP]'):
            pass
        elif (token == '[PAD]'):
            pass
        elif (token != '[CLS]' or token != '[SEP]'):
            temp_d[index_to_ner[label_idx]].append(token)

        for key in temp_d.keys():
            result[key] = ''.join(temp_d[key])

    return dict(result)
