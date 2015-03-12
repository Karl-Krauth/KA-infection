import networkx as nx
import matplotlib.pyplot as plt

class InfectionGraph(object):
  def __init__(self):
    self._graph = nx.DiGraph()

  def add_user(self, user_id):
    self._graph.add_node(user_id)

  def remove_user(self, user_id):
    self._graph.remove_node(user_id)

  def add_coaching_relation(self, coach_id, student_id):
    self._graph.add_edge(coach_id, student_id)

  def remove_coaching_relation(self, coach_id, student_id):
    self._graph.remove_edge(coach_id, student_id)

  def get_students(self, coach_id):
    return self._graph.successors(coach_id)

  def get_coaches(self, student_id):
    return self._graph.predecessors(student_id)

  def total_infection(self, user_id, feature_id):
    pass

  def approx_limited_infection(self, approx_infections, feature_id):
    pass

  def exact_limited_infection(self, num_infections, feature_id):
    pass

  def has_feature(self, user_id, feature_id):
    pass

  def draw(self):
    plt.figure(1,figsize=(24,24))
    # layout graphs with positions using graphviz neato
    pos=nx.graphviz_layout(self._graph,prog="neato")
    nx.draw(self._graph, pos, node_size=5, with_labels=False)
    plt.savefig("atlas.png",dpi=75)
