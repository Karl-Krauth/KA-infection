#!/usr/bin/python

import infection_stress_test as stress
import components_test
import infection_graph_test

components_test.test_components()
infection_graph_test.test_infection_graph()

# num_nodes = 1000000
# stress_test_1 = stress.InfectionStressTest(stress.Density.realistic, num_nodes)
# print "total infection for", num_nodes, "nodes ran in", \
#     stress_test_1.benchmark_total_infection(), "seconds"
# print "exact infection for", num_nodes, "nodes ran in", \
#     stress_test_1.benchmark_exact_limited_infection(10000), "seconds"
