import infection_graph as ig

def test_infection_graph():
  base_test()
  total_infection_test()

def base_test():
  graph = ig.InfectionGraph()
  graph.add_user(0) 
  graph.add_user(1)
  graph.add_user(2)
  graph.add_user(3)
  graph.add_user(4)

  assert graph.get_students(0) == []
  assert graph.get_coaches(1) == []
  
  graph.add_coaching_relation(0, 4) 
  graph.add_coaching_relation(1, 3)
  graph.add_coaching_relation(1, 4)
  assert len(graph.get_students(1)) == 2
  assert len(graph.get_students(0)) == 1
  assert graph.get_students(0)[0] == 4
  assert len(graph.get_coaches(4)) == 2
  assert len(graph.get_coaches(3)) == 1
  assert graph.get_coaches(3)[0] == 1
  assert graph.get_coaches(2) == []
  assert graph.get_students(2) == []  

  graph.add_coaching_relation(3, 1)
  graph.add_coaching_relation(4, 1)
  assert len(graph.get_coaches(4)) == 2
  assert len(graph.get_coaches(3)) == 1
  assert graph.get_coaches(3)[0] == 1
  assert len(graph.get_students(4)) == 1
  assert len(graph.get_students(3)) == 1
  assert len(graph.get_coaches(1)) == 2
  assert graph.get_coaches(2) == []
  assert graph.get_students(2) == []  

  graph.remove_coaching_relation(0, 4)
  assert len(graph.get_students(0)) == 0
  assert len(graph.get_coaches(0)) == 0
  
  graph.remove_coaching_relation(1, 4)
  assert len(graph.get_coaches(4)) == 0

def total_infection_test():
  graph = ig.InfectionGraph()
  graph.add_user(0) 
  graph.add_user(1)
  graph.add_user(2)
  graph.add_user(3)
  graph.add_user(4)
  graph.add_user(5) 
  graph.add_user(6)
  graph.add_user(7)
  graph.add_user(8)

  graph.add_coaching_relation(0, 1)
  graph.add_coaching_relation(1, 2)
  graph.add_coaching_relation(1, 3)
  graph.add_coaching_relation(1, 4)
  graph.add_coaching_relation(4, 2)
  graph.add_coaching_relation(3, 0)
  graph.add_coaching_relation(5, 8)
  graph.add_coaching_relation(7, 8)

  graph.total_infection(6, 10)
  assert graph.has_feature(6, 10) 
  assert not graph.has_feature(0, 10)
  assert not graph.has_feature(8, 10)

  graph.total_infection(8, 11)
  assert graph.has_feature(8, 11)
  assert graph.has_feature(5, 11)
  
  graph.total_infection(5, 12)
  assert graph.has_feature(8, 12)
  assert graph.has_feature(7, 12)

  graph.remove_coaching_relation(7, 8)
  assert graph.has_feature(7, 11)
  assert graph.has_feature(5, 12)
  assert graph.has_feature(7, 12)

  graph.total_infection(2, 13)
  graph.total_infection(0, 14)
  assert graph.has_feature(4, 13)
  assert graph.has_feature(3, 14)
  assert graph.has_feature(1, 14)

  graph.remove_coaching_relation(0, 1)
  graph.remove_coaching_relation(3, 0)
  assert graph.has_feature(0, 13)
  assert graph.has_feature(1, 14)
  assert graph.has_feature(3, 14)
  assert graph.has_feature(4, 14)
  assert graph.has_feature(0, 14)

  graph.total_infection(0, 15)
  graph.total_infection(3, 16)
  assert not graph.has_feature(3, 15)
  assert not graph.has_feature(0, 16)
  assert not graph.has_feature(4, 15)
  assert graph.has_feature(4, 16)

test_infection_graph()
