# Complete credited negative answer, review pending

For problem 30005767 / OWR-14298158-012, the proper pattern class Av(2341,2413,3142) has ordinary generating function

C(z) = (1 − 2z + 2z² − √P(z)) / (2z(1 − z + z²)),

where P(z) = 1 − 8z + 20z² − 24z³ + 16z⁴ − 4z⁵ and √P has constant term 1.

This exact enumeration is already Callan, Mansour and Shattuck, *Wilf classification of triples of 4-letter patterns II*, DMTCS 19:1 (2017), article 6, Theorem 11. [Primary paper](https://dmtcs.episciences.org/3219/pdf).

The full proof in TURN_1.md reconstructs the enumeration through unique first direct/skew components and proves that Q(z,C)=Q(z,√P) is not contained in the exact field Q(z,√(1−4z),√(1−6z+5z²)) from the 2024 source. Four square classes are ruled out by odd valuations, and the radical coefficient is explicitly nonzero. Including or excluding the empty permutation has no effect on the conclusion.

This answers the printed Question 5 negatively. No novelty or priority claim is made for the enumeration or its field consequence. Recommended final disposition after independent approval: already_solved, 1/5 substantive turns. The first turn derived the grammar and field obstruction before the matching published enumeration was identified. The packet is frozen pending review; the recommendation is not yet a review verdict.

The checker passes 143,023 exact controls: all 46,234 permutations through length 8, canonical grammar checks, 6,262 bounded factor pairs, and formal coefficients through degree 80. Finite checks support the written all-length proof. Python 3 standard library only. This result does not address separate rationality/structural questions in the report.
