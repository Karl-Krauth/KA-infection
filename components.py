import sets

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

  def connect(self, id1, id2):
    node1 = self._get_top(id1)
    node2 = self._get_top(id2)

    if node1.id == node2.id:
      pass
    elif node1.depth < node2.depth:
      self._merge_nodes(node2, node1)
    else:
      self._merge_nodes(node1, node2)

  def add_feature(self, node_id, feature_id):
    node = self._get_top(node_id)
    node.features.add(feature_id)

  def has_feature(self, node_id, feature_id):
    node = self._get_top(node_id)
    return feature_id in node.features

  def component_size(self, id):
    node = self._get_top(id)
    return node.size

  def split_component(self, ids1, ids2):
    if len(ids1) == 0 or len(ids2) == 0:
      return

    node = self._get_top(ids1[0])

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

  def add_id(self, id):
    if self._id_dict.get(id) is not None:
      return

    node = self.Node(id)
    self._id_dict[id] = node

  def _merge_nodes(self, parent, child):
    child.parent = parent
    parent.size += child.size
    if parent.depth == child.depth:
      parent.depth += 1 
    parent.features = parent.features.union(child.features)
    child.features.clear()

  def _get_top(self, id):
    curr_node = self._id_dict.get(id)
    assert curr_node is not None

    while curr_node.parent is not None:
      curr_node = curr_node.parent
    
    return curr_node
