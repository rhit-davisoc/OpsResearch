#
# Exercise 2.16 - Olivia Davis
#
# I confirm that all code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Davis Exercise 2.16"

# Sets
M.StoreType = Set()
M.StoreGroup = Set()

# Parameters
M.MinSpace = Param(M.StoreType, within=NonNegativeReals)
M.MaxSpace = Param(M.StoreType, within=NonNegativeReals)
M.Cost = Param(M.StoreType, within=NonNegativeReals)
M.Profit = Param(M.StoreType, within=NonNegativeReals)
M.Budget = Param(within=NonNegativeReals)
M.RetailSpace = Param(within=NonNegativeReals)
M.IsInGroup = Param(M.StoreType, M.StoreGroup, within=NonNegativeIntegers)
M.MinPercent = Param(M.StoreGroup)
M.MaxPercent = Param(M.StoreGroup)

# Variables
M.StoreSpace = Var(M.StoreType, within=NonNegativeReals)
M.TotStoreSpace = Var(within=NonNegativeReals)

# Objective
def CalcProfit(M):
   return sum(M.Profit[s]*M.StoreSpace[s] for s in M.StoreType)
M.TotalProfit = Objective(rule=CalcProfit, sense=maximize)

# Constraints
def BalanceSpace(M):
   return sum(M.StoreSpace[s] for s in M.StoreType) == M.TotStoreSpace
M.BalanceStoreSpace = Constraint(rule=BalanceSpace)

def EnsureCostLimit(M):
   return sum(M.Cost[s]*M.StoreSpace[s] for s in M.StoreType) <= M.Budget
M.TotalCost = Constraint(rule=EnsureCostLimit)

def EnsureRetailSpaceLimit(M):
   return sum(M.StoreSpace[s] for s in M.StoreType) <= M.RetailSpace
M.RetailSpaceLimit = Constraint(rule=EnsureRetailSpaceLimit)

def EnsureLowerSpaceLimit(M,s):
   return M.StoreSpace[s] >= M.MinSpace[s]
M.LowerSpaceLimit = Constraint(M.StoreType,rule=EnsureLowerSpaceLimit)

def EnsureUpperSpaceLimit(M,s):
   return M.StoreSpace[s] <= M.MaxSpace[s]
M.UpperSpaceLimit = Constraint(M.StoreType,rule=EnsureUpperSpaceLimit)

def EnsureLowerPercentLimit(M,g):
   return sum(M.StoreSpace[s]*M.IsInGroup[s,g] for s in M.StoreType) >= M.MinPercent[g]*M.TotStoreSpace
M.LowerPercentLimit = Constraint(M.StoreGroup,rule=EnsureLowerPercentLimit)

def EnsureUpperPercentLimit(M,g):
   return sum(M.StoreSpace[s]*M.IsInGroup[s,g] for s in M.StoreType) <= M.MaxPercent[g]*M.TotStoreSpace
M.UpperPercentLimit = Constraint(M.StoreGroup,rule=EnsureUpperPercentLimit)


# Create a problem instance
instance = M.create_instance("Davis2_16.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)