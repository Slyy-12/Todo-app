import matplotlib.pyplot as plt 
import pandas as pd 
import sys

file = pd.read_excel('Results_6u_c16gd.xlsx') 

x_axis = file['Current (A)'] 
y_axis = file['Time'] 

plt.bar(x_axis, y_axis, width=5) 
plt.xlabel() 
plt.ylabel() 
plt.show() 