import pandas as pd
import numpy as np

df = pd.read_csv('apy.csv')
dess = df.describe()
print(dess)