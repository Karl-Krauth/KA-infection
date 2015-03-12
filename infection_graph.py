import networkx as nx

class InfectionGraph(object):
    def __init__(self):
        self._graph = nx.DiGraph()

    def add_user(self, user_id):
        self._graph.add_node(user_id)

    def remove_user(self, user_id):
        pass

    def add_coaching_relation(self, coach_id, student_id):
        pass

    def remove_coaching_relation(self, coach_id, student_id):
        pass

    def get_students(self, coach_id):
        pass

    def get_coaches(self, student_id):
        pass

    def total_infection(self, user_id, feature_id):
        pass

    def approx_limited_infection(self, approx_infections, feature_id):
        pass

    def exact_limited_infection(self, num_infections, feature_id):
        pass

    def has_feature(self, user_id, feature_id):
        pass
