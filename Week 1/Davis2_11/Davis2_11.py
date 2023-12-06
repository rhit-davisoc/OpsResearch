#
# Exercise 2.11 - Olivia Davis
#
# I confirm that al code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Davis Exercise 2.11"

# Sets
M.CandyType = Set()
M.BagType = Set()

# Parameters
M.LowerPercentage = Param(M.CandyType, M.BagType, within=NonNegativeReals)
M.UpperPercentage = Param(M.CandyType, M.BagType, within=NonNegativeReals)
M.MinPerBag = Param(M.BagType, within=NonNegativeReals)
M.MaxPerBag = Param(M.BagType, within=NonNegativeReals)
M.MaxCandyType = Param(M.CandyType, within=NonNegativeReals)
M.Revenue = Param(M.BagType, within=NonNegativeReals)
M.CandyCost = Param(M.CandyType, within=NonNegativeReals)

# Variables
M.x = Var(M.CandyType, M.BagType, within=NonNegativeIntegers)
M.q = Var(M.CandyType, within=NonNegativeIntegers)
M.z = Var(M.BagType, within=NonNegativeIntegers)

# Objective
def CalcProfit(M):
   return sum(M.Revenue[j]*M.z[j] for j in M.BagType) \
          - sum(M.CandyCost[i]*M.q[i] for i in M.CandyType)
M.Profit = Objective(rule=CalcProfit, sense=maximize)

# Constraints
def BalanceCandy(M,i):
   return sum (M.x[i,j] for j in M.BagType) == M.q[i]
M.BalanceCandyProduction = Constraint(M.CandyType, rule=BalanceCandy)

def BalanceBag(M,j):
   return sum (M.x[i,j] for i in M.CandyType) == M.z[j]
M.BalanceBagProduction = Constraint(M.BagType, rule=BalanceBag)

def EnsureCandyTypeLimit(M,i,j):
   return M.x[i,j] <= M.MaxCandyType[i]
M.LimitCandyPerBag = Constraint(M.CandyType, M.BagType, rule=EnsureCandyTypeLimit)

def EnsureLowerCandyLimit(M,j):
   return M.z[j] >= M.MinPerBag[j]
M.LowBagBound = Constraint(M.BagType, rule=EnsureLowerCandyLimit)

def EnsureUpperCandyLimit(M,j):
   return M.z[j] <= M.MaxPerBag[j]
M.UpBagBound = Constraint(M.BagType, rule=EnsureUpperCandyLimit)

def EnsureLowerPercentCandyLimit(M,i,j):
   return M.x[i,j] >= M.LowerPercentage[i,j]*M.z[j]
M.LowPercentBound = Constraint(M.CandyType, M.BagType, rule=EnsureLowerPercentCandyLimit)

def EnsureUpperPercentCandyLimit(M,i,j):
   return  M.x[i,j] <= M.UpperPercentage[i,j]*M.z[j]
M.UpPercentBound = Constraint(M.CandyType, M.BagType, rule=EnsureUpperPercentCandyLimit)

# Create a problem instance
instance = M.create_instance("Davis2_11.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)