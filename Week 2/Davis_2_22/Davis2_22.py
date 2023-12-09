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


# All demand must be met during that month. Each sneaker is made by
# workers and requires 20 minutes per pair.  [v]
# 
# Each worker works 200 hours
# per month and can work up to 40 hours of overtime per month. Workers
# are paid a salary of $3000 per month, plus $75 per hour of overtime. [v]

# Prior to each month’s production, Fitness Sneaker can either hire
# additional workers or lay off some of its current workers. Due to
# administrative and other expenses, it costs $2000 to hire a worker and
# $3000 to fire a worker.  [v]
# 
# Currently, at most 3000 pairs of sneakers can be
# stored in inventory, and this number is calculated at the end of the month
# (after all production). [v]
# 
# Each stored pair costs $5 per month in storage fees. [v]

# If there are 15 workers and 1000 pairs of sneakers in storage at the
# beginning of month 1, determine how Fitness Sneaker can minimize its
# cost of meeting the demand. [v]

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