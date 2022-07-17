import pandas as pd
import numpy as np
from joblib import dump, load


def run_to_serialize():

    df = pd.read_csv('./model.csv', parse_dates=['date'])
    df.set_index('date', inplace=True)

    pivot_date = df.index.min()
    max_id = df['state'].unique().max()
    states = df['state'].unique().tolist()

    count_reg_models = list(range(max_id+1))
    for state in states:
        df_ = df[df['state'] == state]
        reg_poly_coeffs = np.polyfit(df_["date_id"], df_["count"], 2)
        reg_poly = np.poly1d(reg_poly_coeffs)
        count_reg_models[state] = reg_poly

    amount_reg_models = list(range(max_id+1))

    for state in states:
        df_ = df[df['state'] == state]
        reg_poly_coeffs = np.polyfit(df_["date_id"], df_["amount"], 2)
        reg_poly = np.poly1d(reg_poly_coeffs)
        amount_reg_models[state] = reg_poly

    registration_reg_models = list(range(max_id+1))

    for state in states:
        df_ = df[df['state'] == state]
        reg_poly_coeffs = np.polyfit(df_["date_id"], df_["registeredUsers"], 1)
        reg_poly = np.poly1d(reg_poly_coeffs)
        registration_reg_models[state] = reg_poly

    kinds = {
        1: count_reg_models,
        2: amount_reg_models,
        3: registration_reg_models
    }
    return {'kinds': kinds, 'variables': [pivot_date, states]}


kinds, pivot_date = [None]*2
try:
    data = load('model.joblib')
    kinds = data['kinds']
    pivot_date, states = data["variables"]
except:
    print("Model dump loading failed!")
    print("Refitting Model!")
    data = run_to_serialize()
    kinds = data['kinds']
    pivot_date, states = data["variables"]
    print('Dumping Model!')
    dump(data, 'model.joblib')


predict_df = pd.DataFrame()
predict_df['state'] = states


def predict(kind, date):
    date_id = (pd.to_datetime(date)-pivot_date).days
    predict_df = {
        "value": [],
        "state_code": []
    }
    for state in states:
        value = kinds[kind][state](date_id)
        predict_df['state_code'].append(state)
        predict_df['value'].append(value)
    return pd.DataFrame(predict_df)
