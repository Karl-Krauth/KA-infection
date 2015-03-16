import networkx as nx
import matplotlib.pyplot as plt
import sets
import components
import Queue

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

  def approx_limited_infection(self, approx_infections, feature_id):
    pass

  def exact_limited_infection(self, num_infections, feature_id):
    pass

  def has_feature(self, user_id, feature_id):
    return self._components.has_feature(user_id, feature_id)

  def draw(self):
    plt.figure(1,figsize=(24,24))
    # layout graphs with positions using graphviz neato
    pos=nx.graphviz_layout(self._graph,prog="neato")
    nx.draw(self._graph, pos, node_size=5, with_labels=False)
    plt.savefig("atlas.png",dpi=75)

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

