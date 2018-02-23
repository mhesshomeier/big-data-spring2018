import pandas
import numpy
import pandas as pd
import numpy as np
new_list = []
df = pd.DataFrame()
print(df)
df['nam']=['bilbo', 'frodo', 'samwise']
df.assign(height = [0.5, 0.4, 0.6])
import os
os.chdir('week-03')
df = pd.read_csv('data/skyhook_2017-07.csv', sep=',')
