import re
import os
import numpy as np
import argparse
import math
import subprocess as sp
from subprocess import check_output
import pandas as pd
import shutil
import make_hist_in_ver5
import glob

df = pd.read_csv(csv_name_sb)#ここでファイル名を変更する
output_name = output_name_sb
formula = columns_name_sb

print ("number of samples",len(df))
df.head()

path=os.getcwd()
d_list=[]
str_list=[]
drop_formula=[]
list_formula=[]
dic={'formula':[]}
for i in range(len(df)):
    
    composition=df[formula][i]#ここで組成式が入っているラベルを指定

    parser = argparse.ArgumentParser(
    usage='python make_hist.py structure -sigma= -kh='
        'composition         : enter a composition name (e.g. LiCoO2)'
        '-sigma=T          : not apply broadening (Def. F)'
        '-kh=T             : output histgram descriptors considering two elements (Def. F)'
        'Histogram format  : 1:Prop (eg. AN, EN)  2: 3  3: prop_min  4: prop_max  5: bin_num  6: gaussian_sigma')

    parser.add_argument('composition',type=str)
    parser.add_argument('-sigma')
    parser.add_argument('-kh')


    args = parser.parse_args(args=[composition,'-kh=F','-sigma=F'])#ここでオプションを設定する。
    reference = args.composition
    aparam2=args.sigma
    aparam3=args.kh
    reference = reference.split()
    list_formula.append(reference)
    if aparam2 is None:
        aparam2 = ''
    
    if aparam3 is None:
        aparam3 = ''
    df_columns=[]
    df_data=[]
    r = reference
    mk_hist=make_hist_in_ver5.compdescript(aparam2,aparam3,reference)
    comp_hist=mk_hist[6]
    comp_list=[]
    comp_list1=[]
    comp_list2=[]
    # print(r[0])
    if not mk_hist=='owari':
        if aparam3=='T':
            for comp in comp_hist:
                comp_list.append(mk_hist[3][comp])
                comp_list1.append(mk_hist[4][comp])
                comp_list2.append(mk_hist[5][comp])
        else:
            for comp in comp_hist:
                comp_list.append(mk_hist[3][comp])
    else:
        df.drop(i,inplace=True)
        drop_formula.append(reference[0])
        continue
    dic['formula'].append(r[0])
    if aparam3=='T':
        df_last1=pd.concat(comp_list, axis=1)
        df_last2=pd.concat(comp_list1, axis=1)
        df_last3=pd.concat(comp_list2, axis=1)
        df_h = pd.concat([df_last1,df_last2,df_last3,mk_hist[0],mk_hist[1],mk_hist[2]], axis=1)
    else:
        df_last4=pd.concat(comp_list,axis=1)
        df_h=pd.concat([df_last4,mk_hist[0],mk_hist[1],mk_hist[2]],axis=1)
    d_list.append(df_h)
    str_list.append(reference[0])
f_frame=pd.DataFrame(dic)
df2=pd.concat(d_list,axis=0,ignore_index=True)
df3=pd.concat([f_frame, df2], axis=1)
# print(drop_formula)

df3.to_csv('desc_data/' + output_name,index=False)
