import numpy as np
import pandas as pd

df = pd.read_csv('data_moods.csv')

moods = list(set(df['mood']))

happy = []
sad = []
neutral = []
surprised = []
