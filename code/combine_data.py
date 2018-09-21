import pickle
from master_data import data_path


with open(data_path + 'umg_data.p', 'rb') as F:
    umg_data = pickle.load(F)

with open(data_path + 'unfolded_data.p', 'rb') as F:
    unfolded_data = pickle.load(F)

d = umg_data
d = unfolded_data

for key in d.keys():
    print(key)
