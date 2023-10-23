import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import re
from src import cleaning
sharks = pd.read_csv('data/attacks.csv', encoding='latin1')

cleaning.clean_dataframe (sharks)