import numpy as np
from differential_evolution import generate_population, differential_evolution
from cma.evolution_strategy import CMAEvolutionStrategy

def cma_with_diff_evol(problem, sigma0, sf, cr, budget):
    es = CMAEvolutionStrategy(problem.initial_solution, sigma0, {'verbose': -9, 'ftarget': 1e-8})
    use_cma = False
    ranges = np.array(list(map(list, zip(problem.lower_bounds, problem.upper_bounds))))

    current_cma_population = np.array([])
    current_diff_population = generate_population(ranges, 4 * problem.dimension)

    best_de = None
    best_cma = None
    #TODO: niezalene populacje
    # DE Populacja 4*wymiary

    while(not es.stop() and problem.evaluations < budget
           and not problem.final_target_hit):
        if use_cma:
            current_cma_population = es.ask()
            es.tell(current_cma_population, [problem(x) for x in current_cma_population])
            best_cma = es.best.f
            use_cma = False
        else:
            population, best_from_pop = differential_evolution(ranges, problem, len(current_diff_population), 1, sf, cr, current_diff_population, budget)
            current_diff_population = population
            best_de = best_from_pop
            use_cma = True

    return best_de, best_cma


