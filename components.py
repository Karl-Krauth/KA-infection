'''This module contains a data structure to efficiently keep track of 
what components are connected to each other and what component-wide features
are active.'''

import sets
import sortedcontainers

class Components(object):
  class Node(object):
    def __init__(self, id):
      self.id = id
      self.parent = None
      self.size = 1
      self.depth = 0
      self.features = sets.Set()

  def __init__(self):
    self._id_dict = {}
    self._component_sizes = sortedcontainers.SortedList()

  def connect(self, id1, id2):
    '''Connect two components together.'''
    node1 = self._get_top(id1)
    node2 = self._get_top(id2)

    if node1.id == node2.id:
      return

    self._component_sizes.remove((node1.size, node1.id))
    self._component_sizes.remove((node2.size, node2.id))
    if node1.depth < node2.depth:
      self._merge_nodes(node2, node1)
      self._component_sizes.add((node2.size, node2.id))
    else:
      self._merge_nodes(node1, node2)
      self._component_sizes.add((node1.size, node1.id))

  def add_feature(self, node_id, feature_id):
    '''Add a feature to the component the node_id belongs to.'''
    node = self._get_top(node_id)
    node.features.add(feature_id)

  def has_feature(self, node_id, feature_id):
    '''Check if the component the node belongs to has the given feature.'''
    node = self._get_top(node_id)
    return feature_id in node.features

  def component_size(self, id):
    '''Get the size of the component the node belongs to'''
    node = self._get_top(id)
    return node.size

  def split_component(self, ids1, ids2):
    '''Split a component into two parts.

    ids1 and ids2 are disjoint list of ids that represent the two new
    desired components.
    '''
    if len(ids1) == 0 or len(ids2) == 0:
      return

    node = self._get_top(ids1[0])
    self._component_sizes.remove((node.size, node.id))

    parent_node1 = self.Node(ids1[0])
    parent_node1.features = node.features.copy()
    self._id_dict[ids1[0]] = parent_node1
    parent_node2 = self.Node(ids2[0])
    parent_node2.features = node.features.copy()
    self._id_dict[ids2[0]] = parent_node2

    for id in ids1[1:]:
      parent_node1.depth = 1
      node = self.Node(id)
      self._merge_nodes(parent_node1, node)
      self._id_dict[id] = node

    for id in ids2[1:]:
      parent_node2.depth = 1
      node = self.Node(id)
      self._merge_nodes(parent_node2, node)
      self._id_dict[id] = node

    self._component_sizes.add((parent_node1.size, parent_node1.id))
    self._component_sizes.add((parent_node2.size, parent_node2.id))

  def add_id(self, id):
    '''Add a single node component with the given id.'''
    if self._id_dict.get(id) is not None:
      return

    node = self.Node(id)
    self._id_dict[id] = node
    self._component_sizes.add((node.size, node.id))

  def get_sorted_sizes(self):
    '''Gets a list sorted by size of all components.
    
    The return list consists of tuples where the first element is the size
    of the component and the second element is an id of a node belonging to
    the component.
    '''
  
    return self._component_sizes.as_list()

  def _merge_nodes(self, parent, child):
    '''Merge two components together and combine their features'''
    child.parent = parent
    parent.size += child.size
    if parent.depth == child.depth:
      parent.depth += 1 
    parent.features = parent.features.union(child.features)
    child.features.clear()
    

  def _get_top(self, id):
    '''Get the top level node of a component'''
    curr_node = self._id_dict.get(id)
    assert curr_node is not None

    while curr_node.parent is not None:
      curr_node = curr_node.parent
    
    return curr_node
