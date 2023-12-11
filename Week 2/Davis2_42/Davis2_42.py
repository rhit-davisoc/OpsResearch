#
# Exercise 2.42 - Olivia Davis
#
# I confirm that all code is my own and is submitted according to the integrity policy of MA444
#

from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Instantiate and name the model
M = AbstractModel()
M.name = "Davis Exercise 2.42"

# Sets
M.NumNodes = Param(within=NonNegativeIntegers)
M.Node = RangeSet(1,M.NumNodes)

# Parameters
M.Arc = Set(within=M.Node*M.Node)
M.StartNode = Param(within=M.Node)

# Parameters
M.Weight = Param(M.Arc, within=NonNegativeIntegers)

# Variables
M.Flow = Var(M.Arc, within=NonNegativeIntegers)
M.TotalDistanceFromStart = Var(M.Node, within=NonNegativeIntegers)

# Objective
# def CalcLength(M):
#    return sum(M.Flow[i,j]*M.Weight[i,j] for (i,j) in M.Arc)
# M.TotalLength = Objective(rule=CalcLength, sense=minimize)

def CalcTotalLength(M):
   return sum(M.TotalDistanceFromStart[i] for i in M.Node)
M.TotalLengthOfPaths = Objective(rule=CalcTotalLength, sense=minimize)

# Constraints
# def EnsureBalance(M,k):
#    if(k == M.StartNode):
#         return sum(M.Flow[k,i] for i in M.Node if (k,i) in M.Arc) >= M.NumNodes - 1
#    else:
#         return sum(M.Flow[i,k] for i in M.Node if (i,k) in M.Arc) - sum(M.Flow[k,j] for j in M.Node if (k,j) in M.Arc) >= 1
# M.FlowBalance = Constraint(M.Node, rule=EnsureBalance)

def EnsureBalance(M,k):
   if(k == M.StartNode):
      return Constraint.Feasible
   else:
      return sum(M.Flow[i,k] for i in M.Node if (i,k) in M.Arc) == 1 # Each non-start node should have one path leading into it
M.FlowBalance = Constraint(M.Node, rule=EnsureBalance)

def BalanceTotalDistance(M,k):
    if(k == M.StartNode):
        return M.TotalDistanceFromStart[k] == 0 # Total distance of the start node to start node is 0.
    else:
        return sum(M.Flow[i,k]*(M.TotalDistanceFromStart[i] + M.Weight[i,k]) for i in M.Node if (i,k) in M.Arc) \
               == M.TotalDistanceFromStart[k]
M.TotalDistanceBalance = Constraint(M.Node, rule=BalanceTotalDistance)

# Create a problem instance
instance = M.create_instance("Davis2_42.dat")

# Indicate which solver to use
Opt = SolverFactory("gurobi")

# Generate a solution
Soln = Opt.solve(instance)
instance.solutions.load_from(Soln)

# Print the output
print("Termination Condition was "+str(Soln.Solver.Termination_condition))
display(instance)