from utils.intent_tools import intent_predict
from transformers import BertForSequenceClassification
import torch
from utils.ner_tools import ner_inference
from transformers import AutoTokenizer
from keras.models import load_model


tokenizer = AutoTokenizer.from_pretrained("skt/kobert-base-v1", use_fast=False)
# 질문 의도 추출
def get_intent(query):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    intent_model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased")
    intent_model.load_state_dict(
        torch.load('/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/models/intent/intent_model_state_dict.pt',
                   map_location=device))
    intent = intent_predict(query, intent_model)
    return intent

#와인특성 개체명 인식
def get_ner(query):
    ner_model = load_model('/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/models/ner/save_model')
    ner = ner_inference(query, ner_model)
    bold, acidic, tannic, sweet, winetype = '', '', '', '', ''
    for tag in ner.keys():
        if 'bold' in tag:
            bold = ner[tag].strip('▁')
        elif 'acidic' in tag:
            acidic = ner[tag].strip('▁')
        elif 'tannic' in tag:
            tannic = ner[tag].strip('▁')
        elif 'sweet' in tag:
            sweet = ner[tag].strip('▁')
        elif 'category' in tag:
            winetype = ner[tag].strip('▁')

    for i in [bold, acidic, tannic, sweet, winetype]:
        if i =='':
            i = '_'

    return [bold, acidic, tannic, sweet, winetype]

# 부족한 개채명 확인
# def find_missing_ner(ner):
