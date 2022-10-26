import pandas as pd
import re
from utils.query_tools import  get_ner, get_intent
from utils.Preprocess import trans_prop
from utils.find_best_wine import find_best_wine
red= pd.read_csv('/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/data/data_red_wine.csv')
white = pd.read_csv('/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/data/data_whitewine.csv')


def sim_wine_recommend(query):
    wine_name = re.sub(r'[ㄱ-ㅣ가-힣-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]+', '', query)
    if '레드와인' in query:
        try:
            wine = red[red['name'] == wine_name]
        except:
            return f'해당 {wine_name} 와인이 와인db에 없습니다. 다시 입력해주세요.'

        wine_info = wine[['bold', 'acidic', 'tannic', 'sweet', 'winetype']].values.tolist()
        df = red
    else:
        try:
            wine = white[white['name'] == wine_name]
        except:
            return f'해당 {wine_name} 와인이 와인 db에 없습니다. 다시 입력해주세요.'
        wine_info = wine[['bold', 'acidic', 'tannic', 'sweet', 'winetype']].values.tolist()
        df = white
    inputs = trans_prop(wine_info)
    return find_best_wine(inputs, df)


def reg_recommend(inputs):
    # bold, acidic, tannic, sweet, winetype
    inputs = trans_prop(inputs)

    if inputs[-1] == 0:
        df = red
    else:
        df = white
    return find_best_wine(inputs, df)


