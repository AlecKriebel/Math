# A counterexample to the disk tour bound 8

## Scope

This note gives a negative answer to the Hamiltonian-cycle subquestion in Oleg Musin's contribution to the Open Problems Session, Oberwolfach Report 40/2012, printed page 2488, DOI https://doi.org/10.4171/OWR/2012/40. It does not settle the separate perfect-matching bound 4 or the general question about other convex figures. No novelty or historical-priority claim is made.

The ambient space is the Euclidean plane. For a finite set P, the cost of a Hamiltonian cycle is the sum of the squared Euclidean lengths of its edges, including its closing edge. Each point is visited exactly once. Crossings are permitted; therefore a lower bound for every such cycle also applies if crossings are forbidden. The points need only lie in the disk; they need not all be vertices of a convex polygon. There are no Steiner vertices, repeated vertices, asymptotic normalization, or maximum-edge objective.

## 1. Three-point obstruction

Let u=(1,0), v=(-1/2,sqrt(3)/2), and w=(-1/2,-sqrt(3)/2). These are unit vectors and every pair has squared distance 3. Every Hamiltonian cycle through the three points uses all three unordered pairs, so its cost is exactly 9, greater than 8. If the disk is interpreted as open, replace the three points by r times themselves, where sqrt(8/9)<r<1. The cycle cost is 9r^2>8.

This already refutes the unrestricted finite-set statement. The following independent rational certificate removes any concern about odd cardinality, boundary points, or a three-vertex convention.

## 2. Six distinct rational points strictly inside the disk

Take the six points, in the order indicated,

p0=(95,0)/100, p1=(96,0)/100,
p2=(-50,83)/100, p3=(-51,83)/100,
p4=(-50,-83)/100, p5=(-51,-83)/100.

They are pairwise distinct. Their squared distances to the origin, multiplied by 10000, are

9025, 9216, 9389, 9490, 9389, 9490.

All are strictly less than 10000, so all six points lie in the open unit disk.

Partition the set into A={p0,p1}, B={p2,p3}, and C={p4,p5}. Every edge between B and C has vertical coordinate difference 166/100; hence its squared length is at least 27556/10000. Every edge between A and B, or between A and C, has horizontal difference at least 145/100 and vertical difference 83/100; hence its squared length is at least (145^2+83^2)/10000=27914/10000. Consequently every intercluster edge has squared length at least

27556/10000 = 6889/2500.

In any Hamiltonian cycle, each of the three clusters has a positive even number of edges crossing its cut. To see evenness, sum degree 2 over the vertices in that cluster: each internal edge is counted twice, and each crossing edge once. Positivity follows from connectedness and the fact that the cluster is a proper nonempty subset of the vertices. Thus each cut has at least two edges. Summing over the three clusters counts each intercluster edge twice, so the cycle has at least three intercluster edges.

All squared edge costs are nonnegative. Every Hamiltonian cycle therefore has cost at least

3*(6889/2500) = 20667/2500 = 8.2668 > 8.

This proves a counterexample with even cardinality and strict disk containment. No numerical approximation, search, or optimality computation is required for the proof.

## 3. Exact finite optimality certificate (optional strengthening)

There are (6-1)!/2=60 undirected Hamiltonian cycles on six labeled vertices. Fixing p0 as the first vertex removes rotations. Keeping only permutations whose second label is smaller than their last label removes reversal exactly once, because these labels are distinct. The retained cycles therefore exhaust every undirected Hamiltonian cycle.

The accompanying verifier computes every cost with integers, in units of 1/10000. Their minimum is 83678/10000=41839/5000=8.3678. The cycle (0,1,2,3,5,4,0) attains it: its six edge numerators are 1, 28205, 1, 27556, 1, and 27914, summing to 83678. Enumeration provides the matching lower bound over all 60 cycles. This is an exact finite certificate for this six-point configuration, not a theorem bounding arbitrary point sets.

## 4. Any universal disk tour constant is at least 9

The obstruction persists at every fixed cardinality n>=3. Fix epsilon in (0,1), and use the three equilateral unit directions u,v,w from section 1. Distribute n distinct points among three nonempty clusters on their three radial segments: each point has form r*u, r*v, or r*w, with 1-epsilon<r<1 and distinct radii within each cluster. This can be done for any finite n.

For different directions and radii r,s, the squared distance is r^2+s^2+rs > 3*(1-epsilon)^2, since the dot product of the unit directions is -1/2. The same cut argument forces at least three intercluster edges. Thus every tour has cost greater than 9*(1-epsilon)^2. If a uniform constant K<9 bounded all tours of that cardinality, choose epsilon small enough that 9*(1-epsilon)^2>K, a contradiction. In particular this works for every even n>=4.

This proves only that a possible universal constant must be at least 9. It does not prove that 9 is sufficient, nor identify the best constant.

## 5. Why this does not refute matching

For the six-point example, matching each of the three displayed pairs gives squared cost 3/10000, far below 4. A Hamiltonian cycle on an even number of vertices splits into two perfect matchings by alternating its edges, so a tour bound K would imply existence of a matching with cost at most K/2. The reverse implication is not asserted. Failure of the cycle bound 8 consequently provides no disproof of the matching bound 4.

Indeed, for this example every edge has squared length at least 1/10000, and a perfect matching has exactly three edges. The three-pair matching is therefore optimal with cost 3/10000. This also gives a complete analytic matching computation for the example alone.
