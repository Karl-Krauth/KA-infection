#!/usr/bin/python

import infection_stress_test as stress

stress_test_1 = stress.InfectionStressTest(stress.Density.realistic, 10000)
print stress_test_1.benchmark_total_infection()
