import random
import time
import infection_graph as ig

# The mean class size on khan academy.
# Model should be fine tunable with actual data.
CLASS_SIZE_MEAN = 0.5 

class Density(object):
  # No coaching relationship.
  none = 1
  # Tries to model a (somewhat) realistic situation 
  # with varying sized classes.
  realistic = 2
  # All users coach every other user
  complete = 3


# InfectionStressTest generates an infection graph
# with user specified properties that can then have
# its methods benchmarked. 
class InfectionStressTest(object):
  def __init__(self, density, num_users):
    self._infection_graph = ig.InfectionGraph()
    self._num_users = num_users
    self._add_nodes(num_users)
    self._connect_nodes(density)

  def _add_nodes(self, num_nodes):
    for i in xrange(0, num_nodes):
      self._infection_graph.add_user(i)

  def _connect_nodes(self, density):
    if density == Density.complete:
      # Connect every single user to every other user.
      for i in xrange(0, self._num_nodes):
        for j in xrange(i + 1, self._num_nodes):
          self._infection_graph.add_coaching_relation(i, j)
          self._infection_graph.add_coaching_relation(j, i)
    elif density == Density.realistic:
      for coach_id in xrange(0, self._num_users):
        # We assume class sizes are exponentially distributed.
        if len(self._infection_graph.get_coaches(coach_id)) == 0:
          class_size = int(random.expovariate(1.0 / CLASS_SIZE_MEAN))
        else:
          class_size = int(random.expovariate(1.0 / 0.001))

        # Add random users to be the current coach's students.
        for i in xrange(0, class_size):
          # Potential for repeated instances of the same student_id.
          # This won't matter for large datasets.
          student_id = random.randint(0, self._num_users - 1)
          if coach_id != student_id:
            self._infection_graph.add_coaching_relation(coach_id, student_id)
    else:
      pass

  def benchmark_total_infection(self):
    return self._benchmark_function(ig.InfectionGraph.total_infection,
                                    random.randint(0, self._num_users - 1), 0)

  def benchmark_approx_limited_infection(self, num_infections):
    return self._benchmark_function(ig.InfectionGraph.approx_limited_infection,
                                    num_infections, 0)

  def benchmark_exact_limited_infection(self, num_infections):
    return self._benchmark_function(ig.InfectionGraph.exact_limited_infection,
                                    num_infections, 0)

  def _benchmark_function(self, foo, *args):
    temp_graph = self._infection_graph
    start = time.time()
    foo(temp_graph, *args)
    end = time.time()
    temp_graph.draw()
    return end - start
