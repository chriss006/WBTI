import tensorflow as tf
import pandas as pd
import numpy as np
from keras.utils import pad_sequences
from sklearn.model_selection import train_test_split
from transformers import TFBertModel
import pickle
train = pd.read_csv("ner_train.csv")

label = train['tar'].unique().tolist()
label_dic = {word: i for i, word in enumerate(label)} # enumerate: 인덱스와 값을 함께 반환
label_dic.update({"[PAD]" : len(label_dic)}) # label_dic에 [PAD] 추가
index_to_ner = {i:j for j, i in label_dic.items()}

with open("attention_masks.pickle","rb") as fr:
    attention_masks = pickle.load(fr)
with open("input_id.pickle","rb") as fr:
    input_ids = pickle.load(fr)
with open("tags.pickle","rb") as fr:
    tags = pickle.load(fr)

tr_inputs, val_inputs, tr_tags, val_tags = train_test_split(input_ids, tags, random_state=2022, test_size=0.1)
tr_masks, val_masks, _, _ = train_test_split(attention_masks, input_ids, random_state=2022, test_size=0.1)


def create_model():
  model = TFBertModel.from_pretrained("skt/kobert-base-v1", from_pt=True, num_labels=len(label_dic),
                                      output_attentions=False,
                                      output_hidden_states=False)

  token_inputs = tf.keras.layers.Input((36,), dtype=tf.int32, name='input_word_ids')  # 토큰 인풋
  mask_inputs = tf.keras.layers.Input((36,), dtype=tf.int32, name='input_masks')  # 마스크 인풋

  bert_outputs = model.bert(token_inputs, mask_inputs)[0]
  nr = tf.keras.layers.Dense(30, activation='softmax')(bert_outputs)  # shape : (Batch_size, max_len, 30)

  nr_model = tf.keras.Model([token_inputs, mask_inputs], nr)

  nr_model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.00002),
                   loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                   metrics=['sparse_categorical_accuracy'])

  return nr_model

nr_model = create_model()
nr_model.fit([tr_inputs, tr_masks], tr_tags, validation_data=([val_inputs, val_masks], val_tags), epochs=1, shuffle=False, batch_size=32)
nr_model.save('save_model')
