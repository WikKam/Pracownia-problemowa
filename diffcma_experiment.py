from __future__ import division, print_function
import cocoex  # experimentation and post-processing modules
from numpy.random import rand  # for randomised restarts

from diffcma import cma_with_diff_evol

def fmin(fun, budget):
    sf = 0.5
    cr = 0.4
    sigma0 = 0.2
    return cma_with_diff_evol(fun, sigma0, sf, cr, budget)

### input
suite_name = "bbob"
output_folder = "diffcma_budget_multiplier=10^5"
budget_multiplier = 10 ** 5  # increase to 10, 100, ...

### prepare
suite = cocoex.Suite(suite_name, "", "")
observer = cocoex.Observer(suite_name, "result_folder: " + output_folder)
minimal_print = cocoex.utilities.MiniPrint()

### go
for problem in suite:  # this loop will take several minutes or longer
    problem.observe_with(observer)  # generates the data for cocopp post-processing
    # apply restarts while neither the problem is solved nor the budget is exhausted
    while (problem.evaluations < budget_multiplier
           and not problem.final_target_hit):
        fmin(problem, budget=budget_multiplier)  # here we assume that `fmin` evaluates the final/returned solution
    minimal_print(problem, final=problem.index == len(suite) - 1)
