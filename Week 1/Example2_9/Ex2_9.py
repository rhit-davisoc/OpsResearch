#
# Example 2.1 - Allen Holder
#
# I confirm that al code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Example 2.1"

# Sets
M.DoorType = Set()
M.MachineType = Set()
M.MarketDoorType1 = Set(within=M.DoorType)
M.MarketDoorType2 = Set(within=M.DoorType)

# Parameters
M.Hours = Param(M.DoorType, M.MachineType, within=NonNegativeReals)
M.Labor = Param(M.DoorType, M.MachineType, within=NonNegativeReals)
M.Profit = Param(M.DoorType, within=NonNegativeReals)
M.MachineLimit = Param(M.MachineType, within=NonNegativeReals)
M.LaborLimit = Param(within=NonNegativeReals)

# Variables
M.NumDoors = Var(M.DoorType, within=NonNegativeIntegers)

# Objective
def CalcProfit(M):
   return sum (M.NumDoors[d]*M.Profit[d] for d in M.DoorType)
M.TotProf = Objective(rule=CalcProfit, sense=maximize)
# Constraints
def EnsureMachineLimit(M,m):
   return sum (M.NumDoors[d]*M.Hours[d,m] for d in M.DoorType) \
          <= M.MachineLimit[m]
M.MachineUpBound = Constraint(M.MachineType, rule=EnsureMachineLimit)

def EnsureLaborLimit(M):
   return sum (M.NumDoors[d]*M.Labor[d,m] \
               for d in M.DoorType for m in M.MachineType) \
          <= M.LaborLimit
M.LaborUpBound = Constraint(rule=EnsureLaborLimit)

def EnsureMarketRatio(M):
   return sum (M.NumDoors[d] for d in M.MarketDoorType1) \
          <= sum (M.NumDoors[d] for d in M.MarketDoorType2)
M.MarketRatio = Constraint(rule=EnsureMarketRatio)

# Create a problem instance
instance = M.create_instance("Ex2_1.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)