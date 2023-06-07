import pandas as pd

input_name = input_name_sb
output_name = output_name_sb

df = pd.read_csv('desc_data/' + input_name)
# print(df)

formula = ['formula']
# print([i for i in df.columns if 'AN_' in i])

df_an      = df.loc[:,formula + [i for i in df.columns if 'AN_' in i]]
df_ar      = df.loc[:,formula + [i for i in df.columns if 'AR_' in i]]
df_aw      = df.loc[:,formula + [i for i in df.columns if 'AW_' in i]]
df_cor     = df.loc[:,formula + [i for i in df.columns if 'CoR_' in i]]
df_crr     = df.loc[:,formula + [i for i in df.columns if 'CrR_' in i]]
df_en      = df.loc[:,formula + [i for i in df.columns if 'EN_' in i]]
df_ir      = df.loc[:,formula + [i for i in df.columns if 'IR_' in i]]
df_mn      = df.loc[:,formula + [i for i in df.columns if 'MN_' in i]]
df_mp      = df.loc[:,formula + [i for i in df.columns if 'MP_' in i]]
df_pg      = df.loc[:,formula + [i for i in df.columns if 'PG_' in i]]
df_pgmt    = df.loc[:,formula + [i for i in df.columns if 'PGmatrix_' in i]]
df_pn      = df.loc[:,formula + [i for i in df.columns if 'PN_' in i]]
df_pnmt    = df.loc[:,formula + [i for i in df.columns if 'PNmatrix_' in i]]
df_spdfmat = df.loc[:,formula + [i for i in df.columns if 'SPDFmatrix_' in i]]
df_spdf    = df.loc[:,formula + [i for i in df.columns if 'spdf_' in i]]

df_list = [df_an, df_ar, df_aw, df_cor, df_crr, df_en, df_ir, df_mn, df_mp, df_pg, df_pgmt, df_pn, df_pnmt, df_spdfmat, df_spdf]
for num, desc in enumerate(df_list):
    if num == 0: df_new = desc
    else: 
        df_new = pd.merge(df_new, desc, on='formula')
        # print(df_new)
print(df_new)
df_new.to_csv('desc_data/' + output_name,index=False)


# print(df_an)
