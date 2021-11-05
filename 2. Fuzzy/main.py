# Author: Damian Eggert s19766
# Author: Adrian Paczewski s14973

"""
==========================================
Fuzzy Control Systems: The Tipping Problem
==========================================
To run program install
pip install scikit-fuzzy
pip install matplotlib

The 'tipping problem' is commonly used to illustrate the power of fuzzy logic
principles to generate complex behavior from a compact, intuitive set of
expert rules.

If you're new to the world of fuzzy control systems, you might want
to check out the `Fuzzy Control Primer
<../userguide/fuzzy_control_primer.html>`_
before reading through this worked example.

The Tipping Problem
-------------------

Let's create a fuzzy control system which models how you might choose to tip
at a restaurant.  When tipping, you consider the service and food quality,
rated between 0 and 10.  You use this to leave a tip of between 0 and 25%.

We would formulate this problem as:

* Antecednets (Inputs)
   - `service`
      * Universe (ie, crisp value range): How good was the service of the wait
        staff, on a scale of 0 to 10?
      * Fuzzy set (ie, fuzzy value range): poor, acceptable, amazing
   - `food quality`
      * Universe: How tasty was the food, on a scale of 0 to 10?
      * Fuzzy set: bad, decent, great
* Consequents (Outputs)
   - `tip`
      * Universe: How much should we tip, on a scale of 0% to 25%
      * Fuzzy set: low, medium, high
* Rules
   - IF the *service* was good  *or* the *food quality* was good,
     THEN the tip will be high.
   - IF the *service* was average, THEN the tip will be medium.
   - IF the *service* was poor *and* the *food quality* was poor
     THEN the tip will be low.
* Usage
   - If I tell this controller that I rated:
      * the service as 9.8, and
      * the quality as 6.5,
   - it would recommend I leave:
      * a 20.2% tip.


Creating the Tipping Controller Using the skfuzzy control API
-------------------------------------------------------------

We can use the `skfuzzy` control system API to model this.  First, let's
define fuzzy variables
"""
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

mileage = ctrl.Antecedent(np.arange(10000, 500000, 5000), 'mileage')
year = ctrl.Antecedent(np.arange(1997, 2019, 1), 'year')
body = ctrl.Antecedent(np.arange(1, 4, 1), 'body')
value = ctrl.Consequent(np.arange(7500, 75000, 1500), 'value')

mileage.automf(5)
year.automf(5)
names = ['hatchback', 'sedan', 'estate wagon']
body.automf(names=names)

value['lowest'] = fuzz.trimf(value.universe, [7500, 7500, 10000])
value['lower'] = fuzz.trimf(value.universe, [10000, 15000, 20000])
value['low'] = fuzz.trimf(value.universe, [20000, 30000, 40000])
value['average'] = fuzz.trimf(value.universe, [30000, 40000, 50000])
value['high'] = fuzz.trimf(value.universe, [40000, 50000, 60000])
value['higher'] = fuzz.trimf(value.universe, [60000, 65000, 70000])
value['highest'] = fuzz.trimf(value.universe, [70000, 75000, 75000])

rule1 = ctrl.Rule(antecedent=((mileage['good'] & year['poor'] & body['hatchback']) |
                              (mileage['decent'] & year['poor'] & body['hatchback'])),
                  consequent=value['lowest'])

rule2 = ctrl.Rule(antecedent=((mileage['good'] & year['mediocre'] & body['hatchback']) |
                              (mileage['decent'] & year['mediocre'] & body['hatchback']) |
                              (mileage['average'] & year['poor'] & body['hatchback']) |
                              (mileage['good'] & year['poor'] & body['sedan']) |
                              (mileage['good'] & year['poor'] & body['estate wagon'])),
                  consequent=value['lower'])

rule3 = ctrl.Rule(antecedent=((mileage['good'] & year['average'] & body['hatchback']) |
                              (mileage['good'] & year['decent'] & body['hatchback']) |
                              (mileage['decent'] & year['average'] & body['hatchback']) |
                              (mileage['mediocre'] & year['poor'] & body['hatchback']) |
                              (mileage['poor'] & year['mediocre'] & body['hatchback']) |
                              (mileage['decent'] & year['mediocre'] & body['sedan']) |
                              (mileage['average'] & year['mediocre'] & body['sedan']) |
                              (mileage['good'] & year['mediocre'] & body['sedan']) |
                              (mileage['decent'] & year['poor'] & body['sedan']) |
                              (mileage['good'] & year['average'] & body['sedan']) |
                              (mileage['average'] & year['poor'] & body['sedan']) |
                              (mileage['decent'] & year['mediocre'] & body['estate wagon']) |
                              (mileage['good'] & year['mediocre'] & body['estate wagon']) |
                              (mileage['decent'] & year['poor'] & body['estate wagon']) |
                              (mileage['average'] & year['poor'] & body['estate wagon'])),
                  consequent=value['low'])

rule4 = ctrl.Rule(antecedent=((mileage['good'] & year['good'] & body['hatchback']) |
                              (mileage['poor'] & year['poor'] & body['hatchback']) |
                              (mileage['decent'] & year['decent'] & body['hatchback']) |
                              (mileage['mediocre'] & year['mediocre'] & body['hatchback']) |
                              (mileage['average'] & year['average'] & body['hatchback']) |
                              (mileage['decent'] & year['good'] & body['hatchback']) |
                              (mileage['average'] & year['decent'] & body['hatchback']) |
                              (mileage['mediocre'] & year['average'] & body['hatchback']) |
                              (mileage['poor'] & year['average'] & body['hatchback']) |
                              (mileage['good'] & year['good'] & body['sedan']) |
                              (mileage['poor'] & year['poor'] & body['sedan']) |
                              (mileage['decent'] & year['decent'] & body['sedan']) |
                              (mileage['mediocre'] & year['mediocre'] & body['sedan']) |
                              (mileage['average'] & year['average'] & body['sedan']) |
                              (mileage['good'] & year['decent'] & body['sedan']) |
                              (mileage['decent'] & year['good'] & body['sedan']) |
                              (mileage['mediocre'] & year['poor'] & body['sedan']) |
                              (mileage['poor'] & year['mediocre'] & body['sedan']) |
                              (mileage['average'] & year['decent'] & body['sedan']) |
                              (mileage['decent'] & year['average'] & body['sedan']) |
                              (mileage['mediocre'] & year['average'] & body['sedan']) |
                              (mileage['average'] & year['mediocre'] & body['sedan']) |
                              (mileage['good'] & year['good'] & body['estate wagon']) |
                              (mileage['poor'] & year['poor'] & body['estate wagon']) |
                              (mileage['decent'] & year['decent'] & body['estate wagon']) |
                              (mileage['mediocre'] & year['mediocre'] & body['estate wagon']) |
                              (mileage['average'] & year['average'] & body['estate wagon']) |
                              (mileage['good'] & year['average'] & body['estate wagon']) |
                              (mileage['good'] & year['decent'] & body['estate wagon']) |
                              (mileage['decent'] & year['average'] & body['estate wagon']) |
                              (mileage['average'] & year['mediocre'] & body['estate wagon']) |
                              (mileage['mediocre'] & year['poor'] & body['estate wagon'])),
                  consequent=value['average'])

rule5 = ctrl.Rule(antecedent=((mileage['average'] & year['good'] & body['hatchback']) |
                              (mileage['mediocre'] & year['decent'] & body['hatchback']) |
                              (mileage['mediocre'] & year['good'] & body['hatchback']) |
                              (mileage['poor'] & year['decent'] & body['hatchback']) |
                              (mileage['mediocre'] & year['decent'] & body['sedan']) |
                              (mileage['poor'] & year['decent'] & body['sedan']) |
                              (mileage['mediocre'] & year['good'] & body['sedan']) |
                              (mileage['average'] & year['good'] & body['sedan']) |
                              (mileage['poor'] & year['average'] & body['sedan']) |
                              (mileage['decent'] & year['good'] & body['estate wagon']) |
                              (mileage['average'] & year['decent'] & body['estate wagon']) |
                              (mileage['average'] & year['good'] & body['estate wagon']) |
                              (mileage['mediocre'] & year['average'] & body['estate wagon']) |
                              (mileage['mediocre'] & year['decent'] & body['estate wagon']) |
                              (mileage['poor'] & year['mediocre'] & body['estate wagon']) |
                              (mileage['poor'] & year['average'] & body['estate wagon'])),
                  consequent=value['high'])

rule6 = ctrl.Rule(antecedent=((mileage['poor'] & year['good'] & body['hatchback']) |
                              (mileage['good'] & year['good'] & body['sedan']) |
                              (mileage['mediocre'] & year['good'] & body['estate wagon']) |
                              (mileage['poor'] & year['decent'] & body['estate wagon'])),
                  consequent=value['higher'])

rule7 = ctrl.Rule(antecedent=(mileage['poor'] & year['good'] & body['estate wagon']),
                  consequent=value['highest'])


value_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])

valuation = ctrl.ControlSystemSimulation(value_ctrl)

valuation.input['mileage'] = 300000
valuation.input['year'] = 2010
valuation.input['body'] = 3

valuation.compute()

print(valuation.output['value'])
value.view(sim=valuation)

plt.show()
