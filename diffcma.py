import numpy as np
from differential_evolution import generate_population, differential_evolution
from cma.evolution_strategy import CMAEvolutionStrategy

def cma_with_diff_evol(problem, sigma0, sf, cr):
    es = CMAEvolutionStrategy(problem.initial_solution, sigma0, {'verbose': -9, 'ftarget': 1e-8})
    iters = 0
    use_cma = False
    current_population = np.array(es.ask())
    es.tell(current_population, [problem(s) for s in current_population])
    ranges = np.array(list(map(list, zip(problem.lower_bounds, problem.upper_bounds))))
    best = None

    while(not es.stop()):
        if use_cma:
            #es.disp_annotation()
            #es.disp()
            es.inject(current_population)
            #es.disp()
            X = es.ask()
            es.tell(X, [problem(x) for x in X])
            #es.disp()
            current_population =  np.array(es.ask())
            best = es.best.f
            use_cma = False
        else:
            population, best_from_pop = differential_evolution(ranges, problem, len(current_population), 1, sf, cr, current_population)
            current_population = population
            best = best_from_pop
            use_cma = True

    return current_population, best


