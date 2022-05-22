import numpy as np

### My differential evolution algorithm
def generate_population(range, pop_size: int):
    return range[:, 0] + (np.random.rand(pop_size, len(range)) * (range[:, 1] - range[:, 0]))

def choose_candidates(skip_index, pop):
    candidates_to_choose_indexes = [index for index in range(len(pop)) if index != skip_index]
    chosen = np.random.choice(candidates_to_choose_indexes, 3, replace=False)
    return pop[chosen] 

def adjust_number(number: int, min: int, max: int):
    if number > max:
        return max
    if number < min:
        return min
    return number

def fix_mutation(mutation, ranges):
    return np.array([adjust_number(x, *ranges[i]) for i, x in enumerate(mutation)])

def crossover(mutated, target, dims, cr):
    p = np.random.rand(dims)
    trial = [mutated[i] if p[i] < cr else target[i] for i in range(dims)]
    return np.array(trial)

def differential_evolution(vector_range, problem, pop_size: int, max_iters: int, scale_factor: float, cr: float, starting_population=None, budget: int=None):
    population = generate_population(vector_range, pop_size) if starting_population is None else starting_population 
    obj_evals = [problem(x) for x in population]
    best_candidate_index = np.argmin(obj_evals)
    best_current_index = best_candidate_index
    best_candidate = population[best_candidate_index]
    best_obj_value = obj_evals[best_candidate_index]
    for iter in range(max_iters):
        if budget is not None and problem.evaluations < budget and not problem.final_target_hit: break
        for parent_index in range(pop_size):
            target, rand_1, rand_2 = choose_candidates(parent_index, population)
            mutation = target + scale_factor * (rand_2 - rand_1)
            mutation = fix_mutation(mutation, vector_range)
            trial = crossover(mutation, population[parent_index], len(mutation), cr)
            obj_trial = problem(trial)
            obj_current = problem(population[parent_index])
            if obj_trial < obj_current:
                population[parent_index] = trial
                obj_evals[parent_index] = obj_trial
                best_current_index = np.argmin(obj_evals)
        if obj_evals[best_current_index] < best_obj_value:
            best_candidate = population[best_current_index]
            best_obj_value = obj_evals[best_current_index]
        #print('Iteration: %d f([%s]) = %.5f' % (iter + 1, np.around(best_candidate, decimals=5), best_obj_value))
    return population, best_candidate

