import pandas as pd
import numpy as 

header_df = pd.read_csv("ECBDL14_IR2_simplified.header")

columns = header_df.columns

print(columns)

columns_list = [' PSSM_central_2_N',' PSSM_r1_0_G',' PSSM_r1_0_T',' PSSM_r1_1_R',' PSSM_r2_-2_V',' PSSM_r2_4_I']

columns_list_indexes = []

for i in columns_list:
    columns_list_indexes.append(columns.get_loc(i))

print("Índices: ")
print(columns_list_indexes)