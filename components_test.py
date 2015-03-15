import components

def test_components():
  print "Running base tests"
  component_base_test()  
  print "Base tests passed"

  print "Running feature tests"
  component_feature_test()
  print "Feature tests passed"

  print "Running split tests"
  component_split_test()
  print "Split tests passed"

  print "Running sizes tests"
  component_sizes_test()
  print "Sizes tests passed"

# Tests adding nodes, merging components and getting component size  
def component_base_test():
  comps = components.Components()

  comps.add_id(1)
  comps.add_id(2)
  assert comps.component_size(1) == 1
  assert comps.component_size(2) == 1
  
  comps.connect(1, 2)
  assert comps.component_size(1) == 2
  assert comps.component_size(2) == 2

  comps.add_id(3)
  assert comps.component_size(3) == 1
  comps.connect(1, 3)
  assert comps.component_size(1) == 3
  assert comps.component_size(2) == 3
  assert comps.component_size(3) == 3

  comps.add_id(4)
  comps.add_id(5)
  comps.connect(4, 5)
  assert comps.component_size(4) == 2
  assert comps.component_size(5) == 2

  comps.connect(5, 2)
  assert comps.component_size(1) == 5
  assert comps.component_size(4) == 5

  comps.connect(5, 5)
  assert comps.component_size(5) == 5

  comps.connect(1, 4)
  assert comps.component_size(1) == 5
  assert comps.component_size(3) == 5

def component_feature_test():
  comps = components.Components()
  
  comps.add_id(1)
  comps.add_feature(1, 11)
  assert comps.has_feature(1, 11)

  comps.add_id(2)
  comps.add_feature(2, 12)
  assert not comps.has_feature(1, 12)
  assert comps.has_feature(2, 12)
  comps.connect(1, 2)
  assert comps.has_feature(1, 12)
  assert comps.has_feature(2, 11)

  comps.add_id(3)
  comps.add_id(4)
  comps.add_id(5)
  comps.connect(3, 4)
  comps.connect(4, 5)
  comps.add_feature(5, 13)
  assert comps.has_feature(3, 13)
  assert comps.has_feature(4, 13)
  assert comps.has_feature(5, 13)
  assert not comps.has_feature(3, 11)

  comps.connect(5, 1)
  assert comps.has_feature(3, 11)
  assert comps.has_feature(4, 12)
  assert comps.has_feature(2, 13)

  comps.add_id(6)
  comps.add_feature(6, 14)
  comps.add_feature(6, 15)
  comps.add_feature(6, 16)
  assert not comps.has_feature(2, 14)
  assert not comps.has_feature(3, 15)
  assert not comps.has_feature(1, 16)
  comps.connect(3, 6)
  assert comps.has_feature(2, 14)
  assert comps.has_feature(3, 15)
  assert comps.has_feature(1, 16)

def component_split_test():
  comps = components.Components()
  
  comps.add_id(1)
  comps.add_id(2)
  comps.add_id(3)
  comps.add_id(4)
  comps.add_id(5)
  comps.add_id(6)

  comps.connect(6, 5)
  comps.connect(5, 4)
  comps.connect(4, 3)
  comps.connect(3, 2)
  comps.connect(2, 1)

  comps.add_feature(3, 11)
  assert comps.has_feature(1, 11)
  assert comps.has_feature(4, 11)
  assert comps.component_size(3) == 6

  comps.split_component([1, 3, 6], [2, 4, 5])
  assert comps.component_size(3) == 3
  assert comps.component_size(4) == 3
  assert comps.has_feature(1, 11)
  assert comps.has_feature(2, 11)
  assert comps.has_feature(3, 11)
  assert comps.has_feature(4, 11)
  assert comps.has_feature(5, 11)
  assert comps.has_feature(6, 11)

  comps.add_feature(5, 12)
  assert comps.has_feature(4, 12)
  assert not comps.has_feature(1, 12)
  assert not comps.has_feature(3, 12)

  comps.connect(3, 5)
  assert comps.has_feature(1, 12)
  assert comps.has_feature(3, 12)

  comps.add_id(7)
  comps.add_feature(7, 13)
  comps.add_feature(7, 14)
  comps.add_feature(7, 15)
  assert not comps.has_feature(1, 13)
  assert not comps.has_feature(2, 14)
  assert not comps.has_feature(3, 15)
  assert not comps.has_feature(7, 12)
  assert not comps.has_feature(7, 11)

  comps.connect(7, 5)
  comps.split_component([1, 2, 3, 4, 5, 6], [7])

  assert comps.has_feature(1, 13)
  assert comps.has_feature(2, 14)
  assert comps.has_feature(3, 15)
  assert comps.has_feature(7, 12)
  assert comps.has_feature(7, 11)

def component_sizes_test():
  comps = components.Components()

  assert len(comps.get_sorted_sizes()) == 0

  comps.add_id(1)
  comps.add_id(2)
  comps.add_id(3)
  comps.add_id(4)
  comps.add_id(5)
  comps.add_id(6)
  comps.add_id(7)

  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 7
  assert sizes[0][0] == 1
  assert sizes[1][0] == 1
  assert sizes[6][0] == 1

  comps.connect(1, 5)
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 6
  assert sizes[0][0] == 1
  assert sizes[5][0] == 2

  comps.connect(2, 7)
  comps.connect(5, 3)
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 4
  assert sizes[0][0] == 1
  assert sizes[3][0] == 3
  assert sizes[2][0] == 2

  comps.connect(7, 3)
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 3
  assert sizes[0][0] == 1
  assert sizes[2][0] == 5

  comps.connect(4, 6)
  comps.connect(6, 7)
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 1
  assert sizes[0][0] == 7

  comps.split_component([1, 2, 3, 4, 5, 6], [7])
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 2
  assert sizes[0][0] == 1
  assert sizes[0][1] == 7
  assert sizes[1][0] == 6

  comps.split_component([1, 3, 5], [2, 4, 6])
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 3
  assert sizes[0][0] == 1
  assert sizes[1][0] == 3
  assert sizes[2][0] == 3

  comps.split_component([1], [3, 5])
  comps.split_component([3], [5])
  comps.split_component([2], [4, 6])
  comps.split_component([4], [6])
  sizes = comps.get_sorted_sizes()
  assert len(sizes) == 7
  assert sizes[0][0] == 1
  assert sizes[1][0] == 1
  assert sizes[6][0] == 1
  

test_components()
