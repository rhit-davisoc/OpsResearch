#
# Exercise 2.9 - Olivia Davis
#
# I confirm that all code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Davis Exercise 2.9"

# Sets
M.Stage = Set()
M.Conversion = Set()

# Parameters
M.ConversionRate = Param(M.Conversion, M.Stage, within=Reals)
M.Cost = Param(M.Conversion, within=NonNegativeReals)
M.Labor = Param(M.Conversion, within=NonNegativeReals)
M.Revenue = Param(M.Conversion, within=NonNegativeReals)
M.Max = Param(M.Conversion, within=NonNegativeIntegers)
M.LaborBound = Param(within=NonNegativeReals)

# Variables
M.Convert = Var(M.Conversion, within=NonNegativeIntegers)
# M.Convert = Var(M.Conversion, within=NonNegativeReals)

# Objective
def CalcCost(M):
   return sum(M.Convert[c]*M.Cost[c] for c in M.Conversion)

def CalcRevenue(M):
   return sum(M.Convert[c]*M.Revenue[c] for c in M.Conversion)

def CalcProfit(M):
   return CalcRevenue(M) - CalcCost(M)
M.TotalProfit = Objective(rule=CalcProfit, sense=maximize)

# Constraints
def EnsureBalance(M,s):
   return sum(M.ConversionRate[c,s]*M.Convert[c] for c in M.Conversion) == 0
M.MaterialBalance = Constraint(M.Stage, rule=EnsureBalance)

def EnsureLaborLimit(M):
   return sum(M.Labor[c]*M.Convert[c] for c in M.Conversion) <= M.LaborBound
M.LimitLabor = Constraint(rule=EnsureLaborLimit)

def EnsureDemand(M,c):
   if(M.Max[c] != 0):
      return M.Convert[c] <= M.Max[c]
   else: return Constraint.Feasible
M.SatisfyDemand = Constraint(M.Conversion, rule=EnsureDemand)

# Create a problem instance
instance = M.create_instance("Davis2_9.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)