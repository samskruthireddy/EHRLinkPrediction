import pandas as pd
import numpy as np
import re

def diag_icd(y):
    x=y[4]
    if(x[0] == 'E'):
        if(len(x) == 4):
            return x
        else:
            return x[0:4]+'.'+x[4:]
    else:
        if(len(x) == 3):
            return x
        else:
            return x[0:3]+'.'+x[3:]




def proc_icd(y):
    x=y[4]
    x = str(x)
    if(x[0] == 'E'):
        if(len(x) == 4):
            return x
        else:
            return x[0:4]+'.'+x[4:]
    elif(x[0] == 'V'):
        if(len(x) == 3):
            return x
        else:
            return x[0:3]+'.'+x[3:]
    else:
        if(len(x) == 2):
            x='0'+x
        return x[0:2]+'.'+x[2:]


#MIMIC
d_icd_diagnoses=pd.read_csv('/mnt/data/sams/mimic/D_ICD_DIAGNOSES.csv',dtype=str)
diagnoses_icd=pd.read_csv('/mnt/data/sams/mimic/DIAGNOSES_ICD.csv',dtype=str)
diagnosis_merged=diagnoses_icd.merge(d_icd_diagnoses,on='ICD9_CODE')
diagnosis_merged['entity1']=diagnosis_merged.apply(lambda x: x[1]+'_'+x[2],axis=1)
diagnosis_merged['Rela']='hasIcdDiagnosis'
#diagnosis_merged['entity2']=diagnosis_merged.apply(lambda x: x[4]+'_'+(x[6].replace(' ','_')),axis=1)
diagnosis_merged['entity2']=diagnosis_merged.apply(diag_icd,axis=1)
diagnosis_graph=diagnosis_merged[['entity1','Rela','entity2']]



#import pandas as pd
procedures_icd=pd.read_csv('/mnt/data/sams/mimic/PROCEDURES_ICD.csv',dtype=str)
d_icd_procedures=pd.read_csv('/mnt/data/sams/mimic/D_ICD_PROCEDURES.csv',dtype=str)
procedures_merged=procedures_icd.merge(d_icd_procedures,on='ICD9_CODE')
procedures_merged['entity1']=procedures_merged.apply(lambda x: x[1]+'_'+x[2],axis=1)
procedures_merged['Rela']='hasIcdProcedures'
#procedures_merged['entity2']=procedures_merged.apply(lambda x: x[4]+'_'+(x[6].replace(' ','_')),axis=1)
procedures_merged['entity2']=procedures_merged.apply(proc_icd,axis=1)
procedures_graph=procedures_merged[['entity1','Rela','entity2']]
#procedures_graph=procedures_graph.rename(index=str, columns={'ICD9_CODE':'object'})

withicd9[(withicd9.iloc[:,0].isin(d_icd_diagnoses['ICD9_CODE'].apply(diag_icd).unique().tolist())) & \
(withicd9.iloc[:,3].isin(d_icd_diagnoses['ICD9_CODE'].apply(diag_icd).unique().tolist()))]



#import pandas as pd
prescriptions=pd.read_csv('/mnt/data/sams/mimic/PRESCRIPTIONS.csv',dtype=str)
prescriptions['entity1']=prescriptions.apply(lambda x: x[1]+'_'+x[2],axis=1)
prescriptions['Rela']='hasPrescriptions'
prescriptions['entity2']=prescriptions.apply(lambda x: x[7].replace(' ','_'),axis=1)
prescriptions_graph=prescriptions[['entity1','Rela','entity2']]




#UMLS


withicd9=pd.read_table('withicd9.txt',header=None,delimiter='\t')
#withicd9['code1']=withicd9.apply(lambda x: re.sub('[^0-9a-zA-Z]+', '',x[0]),axis=1)
#withicd9['code2']=withicd9.apply(lambda x: re.sub('[^0-9a-zA-Z]+', '',x[3]),axis=1)
#withicd9['entity1']=withicd9.apply(lambda x: x[5]+'_'+(x[1].replace(' ','_')),axis=1)
#withicd9['entity2']=withicd9.apply(lambda x: x[6]+'_'+(x[4].replace(' ','_')),axis=1)
withicd9['entity1']=withicd9.iloc[:,0]
withicd9['entity2']=withicd9.iloc[:,3]
withicd9['Rela']=withicd9.iloc[:,2]
withicd9_graph=withicd9[['entity1','Rela','entity2']]


#ignore withouticd9 for now
"""
withouticd9=pd.read_table('withouticd9.txt',header=None,delimiter='\t')
withouticd9['code1']=withouticd9.apply(lambda x: re.sub('[^0-9a-zA-Z]+', '',x[0]),axis=1)
withouticd9['entity1']=withouticd9.apply(lambda x: x[4]+'_'+(x[1].replace(' ','_')),axis=1)
withouticd9['entity2']=withouticd9.apply(lambda x: x[3].replace(' ','_'),axis=1)
withouticd9['Rela']=withouticd9.iloc[:,2]
withouticd9_graph=withouticd9[['entity1','Rela','entity2']]
"""

result_withoutumls=pd.concat([diagnosis_graph,procedures_graph,prescriptions_graph])
result_withoutumls=result_withoutumls.drop_duplicates()


#split
split=np.random.permutation(len(result_withoutumls['entity1'].unique()))
split_train=split[:((len(result_withoutumls['entity1'].unique()))*9)//10]
split_test=split[((len(result_withoutumls['entity1'].unique()))*9)//10:]
train_ids=result_withoutumls['entity1'].unique()[split_train]
test_ids=result_withoutumls['entity1'].unique()[split_test]

#train without umls and test
result_withoutumls_train=result_withoutumls[result_withoutumls['entity1'].isin(train_ids)]
result_test=result_withoutumls[result_withoutumls['entity1'].isin(test_ids)]

#UMLS
result_withumls_train=pd.concat([result_withoutumls_train,withicd9_graph])
result_withumls_train=result_withumls_train.drop_duplicates()


result_withoutumls_train.to_csv('/mnt/data/sams/rdfs/mimic_train_without_umls_dot.tsv',sep='\t',index=False,header=False)
result_withumls_train.to_csv('/mnt/data/sams/rdfs/mimic_train_with_umls_dot.tsv',sep='\t',index=False,header=False)
result_test.to_csv('/mnt/data/sams/rdfs/mimic_test_dot.tsv',sep='\t',index=False,header=False)

