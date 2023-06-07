import os
import sys
import pandas as pd
#import pickle
#import subprocess

"""
Created on 2021 Sun Des 13 1:15
@author : Hamaie Masato

""python version == 3.9 or 3.10  can't use 3.11""
This program make a prediction for chemical compound stablity 
 using histgram format comositinal descriptors.
"""
"""
Usage:
 $python recommender.py Li Li2O MgCo2O4 Li1.2AlS0.2Cl3.8
 # you can put some compositions in ref[1:] 
 # 
"""

pwd = os.path.abspath(".")
listdirname = 'list.dirname'
make_dir = 'histgram_desc'
needs = 'need_files'
predict_file = 'predict_file_desc.csv'
hist_d_file = 'histgram_desc.py'
mix_file = 'mix_desc.py'

try:
    comp_l = sys.argv[1:]
except:
    print("Usage:\n $python recommender.py Li Li2O MgCo2O4 Li1.2AlS0.2Cl3.8\n # you can put some compositions in ref[1:]")

tablelist = ''
os.chdir(pwd + '/predict')
with open(listdirname,'w') as w: 
    for comp in comp_l:
        tablelist += comp + '_'
        w.write(comp + '\n')
        print(comp)
    comp_all = tablelist.rstrip('_')
    tablelist += 'tablelist'
os.chdir(pwd)

def make_compdesc_in_python(comp_all = comp_all,comp_l = comp_l):
    os.chdir(pwd + '/histgram_desc')
    os.system(f'cp ../need_files/{hist_d_file} .')
    df_sample = pd.DataFrame(columns = ['index','formula'])
    df_sample['formula'] = comp_l
    df_sample.to_csv('sample_dataset.csv')

    with open(hist_d_file)as v:
        s = v.read()
    s = s.replace("csv_name_sb","'sample_dataset.csv'")
    s = s.replace("output_name_sb",'"merge.table_{}_schema.csv"'.format(comp_all))
    s = s.replace("columns_name_sb","'formula'")
    with open(hist_d_file,'w')as v:
        v.write(s)
    os.system('python {}'.format(hist_d_file))

    os.system(f'cp ../need_files/{mix_file} .')
    with open(mix_file)as v:
        s = v.read()
    s = s.replace("input_name_sb",'"merge.table_{}_schema.csv"'.format(comp_all))
    s = s.replace("output_name_sb",'"merge.table_{}_schema.csv"'.format(comp_all))
    with open(mix_file,'w')as v:
        v.write(s)
    os.system('python {}'.format(mix_file))
    os.chdir(pwd)


def change_inp(comp_all=comp_all):
    os.chdir(pwd)
    os.chdir(pwd+'/predict')
    os.system('cp {}/{}/model_fit.py .'.format(pwd,needs))
    os.system('cp ../{}/desc_data/merge.table_{}_schema.csv {}'.format(make_dir,comp_all,predict_file))
    with open ('model_fit.py','r') as y:
        u = y.read()
    u = u.replace("kokowokaeru","{}".format(predict_file))
    u = u.replace("namae_atom",'{}'.format(comp_all))
    with open ('model_fit.py','w') as v:
        v.write(u)
    print("I'm thinking...")
    os.system('python model_fit.py -n4')

if __name__ == '__main__':
    if len(comp_l) != 0:
        make_compdesc_in_python()
        change_inp()
    else:
        print("++++++++++you should input at least ref1++++++++++")
        print("Usage:\n $python recommender.py Li Li2O MgCo2O4 Li1.2AlS0.2Cl3.8\n # you can put some compositions in ref[1:]")
