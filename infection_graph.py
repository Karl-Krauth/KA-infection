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
    '''Add a new user to the graph'''
    self._graph.add_node(user_id)
    self._components.add_id(user_id)

  def remove_user(self, user_id):
    '''Remove a user from the graph'''
    self._graph.remove_node(user_id)
    assert False, "Method not implemented"

  def add_coaching_relation(self, coach_id, student_id):
    '''Set a given user as the coach of another user'''
    self._graph.add_edge(coach_id, student_id)
    self._components.connect(coach_id, student_id)

  def remove_coaching_relation(self, coach_id, student_id):
    '''Remove the given user from the list of the coach's students.'''
    self._graph.remove_edge(coach_id, student_id)
    nodes1 = self._get_connected(coach_id, student_id)
    if nodes1 == None:
      return
    nodes2 = self._get_connected(student_id, coach_id)
    self._components.split_component(list(nodes1), list(nodes2))

  def get_students(self, coach_id):
    '''Get all the students of a given coach'''
    return self._graph.successors(coach_id)

  def get_coaches(self, student_id):
    '''Get all the coaches of a given student'''
    return self._graph.predecessors(student_id)

  def total_infection(self, user_id, feature_id):
    '''Give all the users that are connected to the given user the given feature.

    Note that the transferal of features is transitive and operates in both directions.
    A student can infect their coach and vice versa.
    '''
    self._components.add_feature(user_id, feature_id)

  def approx_limited_infection(self, feature_id, approx_infections):
    '''Give around approx_infections users the given feature.

    Note that this function assumes that there will be a decent amount 
    of single nodes or small components to work optimally.
    '''
    sizes = self._components.get_sorted_sizes()
    num_infected = 0
    infected = []

    for i in reversed(xrange(len(sizes))):
      # We have reached exactly the number of infections
      if num_infected + sizes[i][0] == approx_infections:
        infected.append(sizes[i][1])
        num_infected += sizes[i][0]
        break
      # Adding the current component won't exceded our number of infections
      elif num_infected + sizes[i][0] < approx_infections:
        infected.append(sizes[i][1])
        num_infected += sizes[i][0]

    # Infect all the components we added to our list.
    for user_id in infected:
      self.total_infection(user_id, feature_id)
    return num_infected

  def exact_limited_infection(self, feature_id, num_infections):
    '''Try to infect exactly num_infections users with the given feature.

    If we can't infect the given number return false. Otherwise return true and
    infect them.
    '''

    # We can always infect 0 users.
    if num_infections == 0:
      return True

    sizes = self._components.get_sorted_sizes()
    if len(sizes) == 0:
      return False

    # Create a len(sizes) x num_infections memoization array.
    dp = [array.array('i', (-1,) * (num_infections + 1)) for i in xrange(len(sizes))]

    if not self._rec_exact_infection(sizes, len(sizes) - 1, num_infections, dp):
      return False

    infected = []
    subset_end = len(sizes) - 1
    num_to_infect = num_infections
    # Trace through the dp array to build the list
    # of components to infect.
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
   
    # infect all the appropriate components.
    for user_id in infected:
      self.total_infection(user_id, feature_id)
    return True  

  def has_feature(self, user_id, feature_id):
    return self._components.has_feature(user_id, feature_id)

  def draw(self, dest):
    plt.figure(1,figsize=(24,24))
    # layout graphs with positions using graphviz neato
    pos=nx.graphviz_layout(self._graph,prog="neato")
    nx.draw(self._graph, pos, node_size=5, with_labels=False)
    plt.savefig(dest, dpi=75)

  def _rec_exact_infection(self, sizes, subset_end, num_infect, dp):
    '''Check if it's possible to infect num_infect users given the component sizes.
   
    subset_end determines the largest component we can use in our sizes array
    when infecting users.
    '''
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

