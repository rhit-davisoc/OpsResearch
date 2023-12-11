#
# Exercise 2.22 - Olivia Davis
#
# I confirm that all code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Davis Exercise 2.22"

# Sets
M.NumMonths = Param(within=NonNegativeIntegers)
M.Month = RangeSet(1,M.NumMonths)

# Parameters
M.Demand = Param(M.Month, within=NonNegativeIntegers)
M.Labor = Param(within=NonNegativeReals)
M.HoursPerMonth = Param(within=NonNegativeReals)
M.OvertimePerMonth = Param(within=NonNegativeReals)
M.Salary = Param(within=NonNegativeReals)
M.Overtime = Param(within=NonNegativeReals)
M.HireCost = Param(within=NonNegativeReals)
M.FireCost = Param(within=NonNegativeReals)
M.MaxInventory = Param(within=NonNegativeReals)
M.StorageCost = Param(within=NonNegativeReals)
M.InitWorkers = Param(within=NonNegativeIntegers)
M.InitSneakers = Param(within=NonNegativeIntegers)

# Variables
M.SneakerProd = Var(M.Month, within=NonNegativeIntegers)
M.Inventory = Var(M.Month, within=NonNegativeIntegers)
M.Workers = Var(M.Month, within=NonNegativeIntegers)
M.Fired = Var(M.Month, within=NonNegativeIntegers)
M.Hired = Var(M.Month, within=NonNegativeIntegers)
M.OvertimeHours = Var(M.Month, within=NonNegativeReals)
M.RegularHours = Var(M.Month, within=NonNegativeReals)

# Objective
def CalcWorkerCostMonth(M,t):
   work_cost = M.Workers[t]*M.Salary + M.OvertimeHours[t]*M.Overtime
   return work_cost + M.Fired[t]*M.FireCost + M.Hired[t]*M.HireCost

def CalcCost(M):
   return sum(CalcWorkerCostMonth(M,t) for t in M.Month) + sum(M.Inventory[t]*M.StorageCost for t in M.Month)
M.TotalCost = Objective(rule=CalcCost, sense=minimize)

# Constraints
def EnsureBalance(M,t):
   if t != 1:
      return M.Inventory[t] == M.Inventory[t-1] + M.SneakerProd[t] \
                                - M.Demand[t]
   else:
      return M.Inventory[t] == M.InitSneakers + M.SneakerProd[t] \
                                - M.Demand[t]
M.InventoryBalance = Constraint(M.Month, rule=EnsureBalance)

def BalanceWorkers(M,t):
   if t != 1:
      return M.Workers[t] == M.Workers[t-1] + M.Hired[t] \
                                - M.Fired[t]
   else:
      return M.Workers[t] == M.InitWorkers + M.Hired[t] \
                                - M.Fired[t]
M.WorkerBalance = Constraint(M.Month, rule=BalanceWorkers)

def EnsureLaborLimit(M,t):
   return M.SneakerProd[t]*M.Labor/60 == M.RegularHours[t] + M.OvertimeHours[t]
M.LimitLabor = Constraint(M.Month, rule=EnsureLaborLimit)

def EnsureOvertimeLimit(M,t):
   return M.OvertimeHours[t] <= M.Workers[t]*M.OvertimePerMonth
M.LimitOvertime = Constraint(M.Month, rule=EnsureOvertimeLimit)

def EnsureHoursLimit(M,t):
   return M.RegularHours[t] <= M.Workers[t]*M.HoursPerMonth
M.LimitHours = Constraint(M.Month,rule=EnsureHoursLimit)

def EnsureInventoryLimit(M,t):
   return M.Inventory[t] <= M.MaxInventory
M.InventoryLimit = Constraint(M.Month, rule=EnsureInventoryLimit)

# Create a problem instance
instance = M.create_instance("Davis2_22.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)