import networkx as nx
import matplotlib.pyplot as plt
import sets
import components
import Queue
import array

class InfectionGraph(object):
  def __init__(self):
    self._graph = nx.DiGraph()
    self._components = components.Components()

  def add_user(self, user_id):
    self._graph.add_node(user_id)
    self._components.add_id(user_id)

  def remove_user(self, user_id):
    self._graph.remove_node(user_id)
    assert False, "Method not implemented"

  def add_coaching_relation(self, coach_id, student_id):
    self._graph.add_edge(coach_id, student_id)
    self._components.connect(coach_id, student_id)

  def remove_coaching_relation(self, coach_id, student_id):
    self._graph.remove_edge(coach_id, student_id)
    nodes1 = self._get_connected(coach_id, student_id)
    if nodes1 == None:
      return
    nodes2 = self._get_connected(student_id, coach_id)
    self._components.split_component(list(nodes1), list(nodes2))

  def get_students(self, coach_id):
    return self._graph.successors(coach_id)

  def get_coaches(self, student_id):
    return self._graph.predecessors(student_id)

  def total_infection(self, user_id, feature_id):
    self._components.add_feature(user_id, feature_id)

  def approx_limited_infection(self, feature_id, approx_infections):
    sizes = self._components.get_sorted_sizes()
    num_infected = 0
    infected = []

    for i in reversed(xrange(len(sizes))):
      if num_infected + sizes[i][0] == approx_infections:
        infected.append(sizes[i][1])
        num_infected += sizes[i][0]
        break
      elif num_infected + sizes[i][0] < approx_infections:
        infected.append(sizes[i][1])
        num_infected += sizes[i][0]

    for user_id in infected:
      self.total_infection(user_id, feature_id)
    return num_infected

  def exact_limited_infection(self, feature_id, num_infections):
    if num_infections == 0:
      return True

    sizes = self._components.get_sorted_sizes()
    if len(sizes) == 0:
      return False

    dp = [array.array('i', (-1,) * (num_infections + 1)) for i in xrange(len(sizes))]

    if not self._rec_exact_infection(sizes, len(sizes) - 1, num_infections, dp):
      return False

    infected = []
    subset_end = len(sizes) - 1
    num_to_infect = num_infections
    while num_to_infect != 0:
      if sizes[subset_end][0] == num_to_infect:
        infected.append(sizes[subset_end][1])
        num_to_infect = 0
      elif dp[subset_end - 1][num_to_infect]:
        subset_end -= 1
      else:
        infected.append(sizes[subset_end][1])
        num_to_infect -= sizes[subset_end][0]
        subset_end -= 1
   
    for user_id in infected:
      self.total_infection(user_id, feature_id)
    return True  

  def _rec_exact_infection(self, sizes, subset_end, num_infect, dp):
    if dp[subset_end][num_infect] != -1:
      return dp[subset_end][num_infect]

    if subset_end == 0:
      if sizes[0][0] == num_infect:
        dp[subset_end][num_infect] = 1
      else:
        dp[subset_end][num_infect] = 0
    else:
      dp[subset_end][num_infect] = \
          self._rec_exact_infection(sizes, subset_end - 1, num_infect, dp) or \
          self._rec_exact_infection(sizes, subset_end - 1, num_infect - sizes[subset_end][0], dp) or \
          (sizes[subset_end][0] == num_infect)
    return dp[subset_end][num_infect]

  def has_feature(self, user_id, feature_id):
    return self._components.has_feature(user_id, feature_id)

  def draw(self, dest):
    plt.figure(1,figsize=(24,24))
    # layout graphs with positions using graphviz neato
    pos=nx.graphviz_layout(self._graph,prog="neato")
    nx.draw(self._graph, pos, node_size=5, with_labels=False)
    plt.savefig(dest, dpi=75)

  def _get_connected(self, source, connected_node):
    visited = sets.Set()
    to_visit = Queue.Queue()
    to_visit.put(source)   
    visited.add(source)   
 
    while not to_visit.empty():
      curr_id = to_visit.get()
      neighbors = self._get_neighbors(curr_id)
      for neighbor in neighbors:
        if not neighbor in visited:
          if neighbor == connected_node:
            return None
          to_visit.put(neighbor)
          visited.add(neighbor)
    
    return visited

  def _get_neighbors(self, user_id):
    return self.get_coaches(user_id) + self.get_students(user_id)

