from __future__ import division, print_function
import cocoex  # experimentation and post-processing modules
from numpy.random import rand  # for randomised restarts

import cma

def fmin(fun, x0):
    return cma.fmin(fun, x0, 2, {'verbose':-9, 'ftarget': 1e-8})

### input
suite_name = "bbob"
output_folder = "cma.fmin_budget_multiplier=10^5"
budget_multiplier = 10 ** 5  # increase to 10, 100, ...

### prepare
suite = cocoex.Suite(suite_name, "", "")
observer = cocoex.Observer(suite_name, "result_folder: " + output_folder)
minimal_print = cocoex.utilities.MiniPrint()

## TODO: KRZYZYK PRZY 5!!!

### go
for problem in suite:  # this loop will take several minutes or longer
    problem.observe_with(observer)  # generates the data for cocopp post-processing
    x0 = problem.initial_solution
    # apply restarts while neither the problem is solved nor the budget is exhausted
    while (problem.evaluations < budget_multiplier
           and not problem.final_target_hit):
        fmin(problem, x0)  # here we assume that `fmin` evaluates the final/returned solution
        x0 = problem.lower_bounds + ((rand(problem.dimension) + rand(problem.dimension)) *
                    (problem.upper_bounds - problem.lower_bounds) / 2)
    minimal_print(problem, final=problem.index == len(suite) - 1)
