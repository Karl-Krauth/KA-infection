# KA-infection
This repository contains a module that has multiple methods to adjust what features each user has for A/B and multivariate testing.

## Running the tests
Run the following commands to install all necessary dependencies:
```
pip install networkx
pip install sortedcontainers
```
Now simply run
```
python run_tests.py
```
You can also import infection\_graph.py and use it as a standalone module.
If you would like to also use the (unfinished) draw functionality you will need
to install matplotlib and pygraphviz.
## Implementation
The library consists of two main parts. 
* infection\_graph.py: Keeps track of the actual coaching relations between users. 
You can query the infection graph for a given user's students and coaches, add new users, relations
and delete relations. The graph is by nature directed.
* components.py: Efficiently keeps track of all connected components in the graph. Note that since
infections travel from students to coaches and vice versa components.py doesn't treat the infection graph
as a directed graph. You can query components.py as to whether two users are indirectly connected, whether
a particular user has a given feature, and get a sorted list of components by size.
The Infection graph is implemented as a standard directed graph using the networkx library (which uses an
implementation similar to an adjacency list).
Components consists of an "inverted" tree where child nodes point to parent nodes. Each component is represented
by an inverted tree. Merging components is done in a way that guarantees operations with logarithmic complexity.
To keep track of component sizes we use a sorted container which has similar guarantees to a balanced binary search
tree.

## Assumptions
We have made a number of assumptions about the problem and Khan academy's data.
* The graph isn't going to be as dense as say facebook's graph. There are going to be
many isolated components of small classrooms. (Don't feel entirely comfortable with this assumption but it seems intuitive
I'd love to hear whether this assumption is correct!) 
* A user having a coach reduces the probability of they themselves being a coach.
* Class sizes are exponentially distributed (not sure how realistic this assumption is)
* There are many isolated nodes from individual students learning on their own.
* We would rather have the wrong number of infections than classes having different versions of the site for the sake of a good user experience.
* We want new coaching relations to update features so that the coach and student have the same features.
* There are on the order of 10 million students with room for growth to the hundreds of millions
http://www.forbes.com/sites/michaelnoer/2012/11/02/one-man-one-computer-10-million-students-how-khan-academy-is-reinventing-education/
* Coaches can remove students from their class:
https://khanacademy.zendesk.com/hc/en-us/articles/202487620-How-can-I-delete-a-class-list-or-remove-a-student-from-a-class-list-
* Coaches can dynamically add students to their class.

## Performance
We let V be the number of vertices of the largest component of the graph and N is the number of components.
C is also the number of users we want to infect with a feature.
We list the worst case time complexity of infection graph's methods. Most methods perform much better in practice.
* *add_user:* O(1)
* *has_feature:* O(log(V))
* *add_coaching_relation:* O(log(V)) 
* *remove_coaching_relation:* O(V)
* *total_infection:* O(log(V))
* *approx_limited_infection:* O(N)
* *exact_limited_infection:* O(NC) 

## Possible improvements
* I didn't have time to implement a good visualization of the infection spread.
* Trade off here between fast infection and fast edge deletion
* Seperating the actual graph of coaching relations from our data structure that determines connected components
means that we can instantly update the deletion view from the user's perspective AND do the slow update on the connected
components seperately if we parallelize. 
* What are we meant to do if a new relation is formed after an infection?
(Probably best to infect the whole new component too)
* Probably won't have time to paralellize the algorithm but it should be easily parallelizable 
in the future. Idea that might work:
Maybe distribute the graph components across multiple machines have a way to lookup where each component
currently lives (simple map from id to location would work). Then edge deletion resolution can happen on its own
seperate machine. 
* What happens if the graph gets updated while we are infecting a subset of users? We would potentially like for those users to be infected too.
Some users might be exposed to two versions of the site temporarily but if we have a seperate graph of relations at least the relation instantly 
updates.
* The fact that I store the entire graph in memory is obviously not scalable. I don't particularly have time to set
up persistent storage beyong simple flat files though.

assumptions:
