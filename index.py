# Librerías para el tratamiento de los datos
import numpy as np 
import pandas as pd

# Librerías para entrenamiento y modelado
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Librerías para visualización
import matplotlib.pyplot as plt
import seaborn as sns

salary_data = pd.read_csv('./Salary.csv')

salary_data.sample(10)
salary_data.shape
salary_data.info()
salary_data.describe()