# Author: Damian Eggert s19766
# Author: Adrian Paczewski s14973

"""
To run program install:
pip install pandas
pip install matplotlib
pip install seaborn
pip install sklearn

Research: Attack range of a player playing in the Polish volleyball league

Data {x}:
- height [cm]
- weight [kg]
- age [years]
- training internship [years]

Data reference {x}:
* http://statystyki.pzps.pl/pl/
* wikipedia (to check internship)
* https://www.plusliga.pl/

Data {y}:
- attack range [cm]
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import svm


# parsing csv file data
args_x = ['Height', 'Weight', 'Age', 'Training internship']

data = pd.read_csv('dane.csv', delimiter=',', names=['Height', 'Weight', 'Age', 'Training internship', 'Jump'])
data.head()

sns.pairplot(data, x_vars=args_x, y_vars=['Jump'], kind="reg")

plt.show()
print('Data correlation')
print(data.corr())

X = data[args_x]
y = data['Jump']

# Fit the SVM model with different kernel types
svc_linear = svm.SVC(kernel="linear").fit(X.values, y)
svc_poly = svm.SVC(kernel="poly").fit(X.values, y)
svc_rbf = svm.SVC(kernel="rbf").fit(X.values, y)
svc_sigmoid = svm.SVC(kernel="sigmoid").fit(X.values, y)

height = 199
weight = 90
age = 18
training_internship = 1

print(
    f"Attack range of a player with height {height}, weight {weight}, age {age} and training internship "
    f"{training_internship} is equal : ")
print(f"Linear kernel type: ", svc_linear.predict([[height, weight, age, training_internship]]), "cm")
print(f"Poly kernel type: ", svc_poly.predict([[height, weight, age, training_internship]]), "cm")
print(f"Rbf kernel type: ", svc_rbf.predict([[height, weight, age, training_internship]]), "cm")
print(f"Sigmoid kernel type: ", svc_sigmoid.predict([[height, weight, age, training_internship]]), "cm")
