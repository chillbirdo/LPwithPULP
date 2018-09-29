import pandas as pd
import pulp

# PARAMETERS
generatorsParam = pd.read_csv('generators_variables_1.csv', sep=';', index_col=['Generators'])
demandParam = pd.read_csv('demand_variables_1.csv', sep=';', index_col=['Month'])

# print(len(generatorsParam.index));

# print(generatorsParam.loc['L','Max'])

# DECISION VARIABLES
p = []
for gen in generatorsParam.index:
    for month in demandParam.index:
        # DECISION VARIABLE: p(i,t), generator Output per generator and month
        p.append( gen + "_" + str(month))

i = []
for month in demandParam.index:
    i.append(str(month))

# print(genOnOffVarNames);
# print(genOutVarNames);
genOutLpVar = pulp.LpVariable.dicts("prod", p, cat='Continuous')
importLpVar = pulp.LpVariable.dicts("import", i, cat='Continuous')

#MODEL OBJECTIVE
toSum = []
for gen in generatorsParam.index:
    for month in demandParam.index:
        idxP = gen + "_" + str(month)
        idxI = str(month)
        toSum.append(genOutLpVar[idxP] * float(generatorsParam.loc[gen, 'VCost'])
                                            + float(generatorsParam.loc[gen, 'VCost'])
                                            + genOutLpVar[idxP] * float(generatorsParam.loc[gen, 'Emission']) * 20
                                            + importLpVar[idxI] * float(demandParam.loc[month, 'ImportCost']));

model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)
model += pulp.lpSum(toSum), "Output*Costs for each generator and each month"

# MODEL CONSTRAINTS
for month in demandParam.index:
    generatorsSum = []
    idxI = str(month)
    for gen in generatorsParam.index:
        idxP = gen + "_" + str(month)
        generatorsSum.append(genOutLpVar[idxP])
    model += pulp.lpSum(generatorsSum) + importLpVar[idxI] - demandParam.loc[month] == 0, "Meet demand for month " + str(month)

print(model);

# model.solve()
# print(pulp.LpStatus[model.status])

