#!/usr/bin/python

import infection_stress_test as stress
import components_test
import infection_graph_test

components_test.test_components()
infection_graph_test.test_infection_graph()

# stress_test_1 = stress.InfectionStressTest(stress.Density.realistic, 1000000)
# print stress_test_1.benchmark_total_infection()
# print stress_test_1.benchmark_exact_limited_infection(100000)
