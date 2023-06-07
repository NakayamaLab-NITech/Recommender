#!/usr/bin/env python
import pickle
import os
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,KFold
from sklearn.metrics import mean_squared_error,mean_absolute_error
def rmse(y_true,y_pred):
    rmse = np.sqrt(mean_squared_error(y_true,y_pred))
    return rmse
import warnings
warnings.filterwarnings('ignore')

list_name =["RandomForest"]#"PLS","optunaLGBM","Ridge","RandomForest","ElasticNet","LinearSVR","KernelSVR","LightGBM","Lasso"]

name_atom="LiO"
filename = "predict_file_desc.csv"

loaded_model_d ={}
for model_name in list_name:
    output_name = model_name+'_model.pickle'
    with open(output_name,mode='rb') as fp:
        loaded_model = pickle.load(fp)
        loaded_model_d[filename + model_name ] = loaded_model
    print('Loaded  file')#name:',output_name)


df_new = pd.read_csv(filename)
df=df_new.drop(['formula'],axis=1)

df_pred=df_new[['formula']]
#print(df_pred.columns)
#df = df_new.drop('Unnamed: 1995',axis=1)
#print(df_new.columns)
def prediction(model,model_name,new_X):
    pred_y = model.predict(new_X)
    pred_proba=model.predict_proba(new_X)
    return pred_y,pred_proba
"""
    if best_param_for_each_model_d[model_name]['Is_scaler']:
        scaler = StandardScaler()
        scaler.fit(X)
        new_X_sc = scaler.transform(new_X)
        pred_y = model.predict(new_X_sc)
    else:
"""

pred_y_d = {}
for model_name,loaded_model in zip(loaded_model_d.keys(),loaded_model_d.values()):
    pred_y,pred_proba = prediction(loaded_model,model_name,df)

    print(pred_proba)
    pred_y_d[model_name] = pred_y
for model_name, pred_y in zip(pred_y_d.keys(),pred_y_d.values()):
    print('Add prediction ({})'.format(model_name))

    #df_pred['predict'] = pred_y
    print(pred_y)
    #    pred_num=int(pred_y)
    percent=[]
    what=[]
    for u in range(len(pred_y)):
        k=int(pred_y[u])
        if k == 0:
            Great='stable'
        elif k == 1:
            Great='meta-stable'
        else:
            Great='un-stable'
        what.append(Great)


        perc=pred_proba[u,k]
        percent.append(perc)
    df_pred['this_Stability_percent'] = percent
    df_pred['predict_number'] = pred_y
    df_pred['Stability'] = what
    df_1=pd.DataFrame(pred_proba,columns = ['probability class 0 (0-0.01 eV / atom)','probability class 1 (0.01-0.1 eV / atom)','probability class 2 (0.1- eV / atom)'])
    df_pred1=pd.concat([df_pred,df_1],axis=1)

print('\n\n'+'-'*40 + 'We use e_above_hull as a metric to predict stability.'+'-'*40+'\n\n')
print(df_pred1)

print('\n\n_____________all_predict_finish_____________\n')
print('if you need predict_file.\nyou should go to after_predict_box!\n')
print('Have a Nice Day!\n\n')


os.chdir('/data/Search_meta-stable/after_predict_box')
os.system('mv * ../make_desc/Unnecessary_box/.')

df_pred1.to_csv('pred_y_{}.csv'.format(name_atom),index=False)
