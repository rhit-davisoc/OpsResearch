#
# Exercise 2.3 - Olivia Davis
#
# I confirm that all code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Davis Exercise 2.3"

# Sets
M.Thickness = Set()
M.MachineType = Set()

# Parameters
M.Minutes = Param(M.Thickness, M.MachineType, within=NonNegativeReals)
M.Revenue = Param(M.Thickness, within=NonNegativeReals)
M.Cost = Param(M.Thickness,within=NonNegativeReals)
M.MaxDemand = Param(M.Thickness,within=NonNegativeReals)
M.MachineLimit = Param(M.MachineType, within=NonNegativeReals)
M.MachineCost = Param(M.MachineType, within=NonNegativeReals)

# Variables
M.NumThickness = Var(M.Thickness, within=NonNegativeReals)

# Objective
def CalcTotalThicknessProfit(M):
   return sum (M.NumThickness[t]*(M.Revenue[t]-M.Cost[t]) for t in M.Thickness)

def CalcTotalMachineCost(M):
   return sum(M.NumThickness[t]*M.MachineCost[m]*(M.Minutes[t,m])/60 for t in M.Thickness for m in M.MachineType)

def CalcProfit(M):
   return CalcTotalThicknessProfit(M) - CalcTotalMachineCost(M)
M.TotProf = Objective(rule=CalcProfit, sense=maximize)

# Constraints
def EnsureMachineLimit(M,m):
   return sum (M.NumThickness[t]*(M.Minutes[t,m]/60) for t in M.Thickness) \
          <= M.MachineLimit[m]
M.MachineUpBound = Constraint(M.MachineType, rule=EnsureMachineLimit)

def EnsureDemandLimit(M,t):
   return (M.NumThickness[t] <= M.MaxDemand[t])
M.DemandUpBound = Constraint(M.Thickness, rule=EnsureDemandLimit)

# Create a problem instance
instance = M.create_instance("Davis2_3.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)