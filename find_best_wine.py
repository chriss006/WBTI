import pandas as pd
import numpy as np
red= pd.read_csv('/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/data/data_red_wine.csv')
white = pd.read_csv('/Users/chrissl/WBTI Dropbox/Pycharm_files/wbti/data/data_whitewine.csv')


def find_best_wine(input_vec, df):
    white_id = white.loc[:, ['wine_id', 'bold', 'sweet', 'acidic']]
    red_id = red.loc[:, ['wine_id', 'bold', 'sweet', 'acidic', 'tannic']]

    best_match, best_match_id, best_match_vector = 10, -1, []

    if input_vec[-1] == 0:
        for i in red_id['wine_id']:
            if input_vec[0] != i:
                tmp_prop = np.array(red_id.loc[i, ['acidic', 'bold', 'sweet', 'tannic']])
                dist = np.sum(np.square(input_vec[2:] - tmp_prop))
                if dist < best_match:
                    best_match = dist
                    best_match_id = i
                    best_match_vector = tmp_prop
    else:
        for i in white_id['wine_id']:
            if input_vec[0] != i:
                tmp_prop = np.array(white_id.loc[i, ['acidic', 'bold', 'sweet']])
                dist = np.sum(np.square(input_vec[2:-1] - tmp_prop))
                if dist < best_match:
                    best_match = dist
                    best_match_id = i
                    best_match_vector = tmp_prop

    result = df[df.loc[:,'wine_id']== best_match_id].values.tolist()
    return best_match_id