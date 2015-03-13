# KA-infection

thoughts:
-The infection problem is actually operating on an undirected graph (despite there being
a directed graph between coaches and students) since students can transmit to coaches and vice-versa
-Trade off here between fast infection and fast edge deletion
-If we have a fast way to lookup components by size we could maybe use dp
to figure out if we can do an infection of an exact size.
-Seperating the actual graph of coaching relations from our data structure that determines connected components
means that we can instantly update the deletion view from the user's perspective AND do the slow update on the connected
components seperately if we parallelize. 
-What are we meant to do if a new relation is formed after an infection?
(Probably best to infect the whole new component too)
-Probably won't have time to paralellize the algorithm but it should be easily parallelizable 
in the future. Idea that might work:
Maybe distribute the graph components across multiple machines have a way to lookup where each component
currently lives (simple map from id to location would work). Then edge deletion resolution can happen on its own
seperate machine. 
-What happens if the graph gets updated while we are infecting a subset of users? We would potentially like for those users to be infected too.
Some users might be exposed to two versions of the site temporarily but if we have a seperate graph of relations at least the relation instantly 
updates.
-The fact that I store the entire graph in memory is obviously not scalable. I don't particularly have time to set
up persistent storage beyong simple flat files though.

assumptions:
-The graph isn't going to be as dense as say facebook's graph. There are going to be
many isolated components of small classrooms. (Don't feel entirely comfortable with this assumption but it seems intuitive
I'd love to hear whether this assumption is correct!) 
-A user having a coach reduces the probability of they themselves being a coach.
-Class sizes are exponentially distributed (not sure how realistic this assumption is)
-Many isolated nodes from individual students learning on their own.
-We would rather have the wrong number of infections than classes having different versions of the site for the sake of a good user experience.
-On the order of 10 million students with room for growth to the hundreds of millions
http://www.forbes.com/sites/michaelnoer/2012/11/02/one-man-one-computer-10-million-students-how-khan-academy-is-reinventing-education/
^Got numbers for 10 million from here (note that the article is two years old, KA has probably grown)
-Coaches can remove students from their class. (No need to update current infections here):
https://khanacademy.zendesk.com/hc/en-us/articles/202487620-How-can-I-delete-a-class-list-or-remove-a-student-from-a-class-list-
-Coaches can dynamically add students to their class (we do need to update infections here)
