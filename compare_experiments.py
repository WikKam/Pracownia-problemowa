import os, webbrowser  # to show post-processed results in the browser
import cocopp  # experimentation and post-processing modules

cwd = os.getcwd()

cocopp.main("./exdata/differential_evolution_budget_multiplier=100 ./exdata/cma.fmin_budget_multiplier=10^5 ./exdata/diffcma_budget_multiplier=10^5-001")  # re-run folders look like "...-001" etc
webbrowser.open("file://" + os.getcwd() + "/ppdata/index.html")