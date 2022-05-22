from __future__ import division, print_function
import cocoex
import numpy as np
from differential_evolution import differential_evolution
pop_size = 20
max_iters = 1000
sf = 0.5
cr = 0.4

### input
suite_name = "bbob"
output_folder = "differential_evolution_budget_multiplier=100"
budget_multiplier = 10 ** 5  # increase to 10, 100, ...

### prepare
suite = cocoex.Suite(suite_name, "", "")
observer = cocoex.Observer(suite_name, "result_folder: " + output_folder)
minimal_print = cocoex.utilities.MiniPrint()

### go
for problem in suite:  # this loop will take several minutes or longer
    problem.observe_with(observer)  # generates the data for cocopp post-processing
    ranges = np.array(list(map(list, zip(problem.lower_bounds, problem.upper_bounds))))
    # apply restarts while neither the problem is solved nor the budget is exhausted
    while (problem.evaluations < budget_multiplier
           and not problem.final_target_hit):
        differential_evolution(ranges, problem, pop_size, max_iters, sf, cr, budget_multiplier)  # here we assume that `fmin` evaluates the final/returned solution
    minimal_print(problem, final=problem.index == len(suite) - 1)
