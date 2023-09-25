import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd
AcData = pd.read_excel(r'C:\Users\Erhan\Desktop\CGopt.xlsx',sheet_name='Sayfa1')
SI = pd.read_excel(r'C:\Users\Erhan\Desktop\CGopt.xlsx',sheet_name='Sayfa2')
print(AcData)
nc = len(AcData)
a = []
bagY = int(input("Enter Y class bags"))
bagC = int(input("Enter C class bags"))
TargetIndex = int(input("Enter target Index"))
for  i in SI.Weight:
    a.append(i)
print(a[6])
#model
model = pyo.ConcreteModel()
model.by = pyo.Var(range(nc),within= Integers, bounds=(0,None))
by = model.by
model.bc = pyo.Var(range(nc),within= Integers, bounds=(0,None))
bc = model.bc
model.Cap =pyo.ConstraintList()
for i in range(nc):
    model.Cap.add(expr= by[i]+bc[i] <= AcData.Capacity[i])

by_sum = sum([by[i] for i in range(nc)])
bc_sum = sum ([bc[i] for i in range(nc)])
model.ekonomi = pyo.Constraint(expr = by_sum == bagY)
model.business = pyo.Constraint(expr = bc_sum == bagC)

# obj
balance_sum = sum([by[i]*AcData.Index[i] for i in range(nc)]) + sum([bc[i]*AcData.Index[i] for i in range(nc)])
model.obj = pyo.Objective (expr=balance_sum +a[6] - TargetIndex,sense=minimize)

opt = SolverFactory('gurobi')
results = opt.solve(model)
model.pprint()
print('obj',pyo.value(model.obj))
print('index', pyo.value(balance_sum)+a[6])
for i in range(nc):
    print('by',i, pyo.value(model.by[i]))
print('--------------------------------')
for i in range(nc):
    print('bc',i, pyo.value(model.bc[i]))