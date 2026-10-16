# First independent historical conclusion, before candidate release

Frozen before any candidate/inherited/root/sibling reading. This conclusion was reached by independently following the source's factorization and lattice terminology into primary literature.

## Primary result found

Thomas Kahle and Seth Sullivant, *Lattice supported distributions and graphical models*, arXiv:2411.03139v1, first submitted 2024-11-05 14:31:16 UTC according to the primary arXiv submission-history page https://arxiv.org/abs/2411.03139 ; full text https://arxiv.org/pdf/2411.03139v1 . The PDF gives a manuscript date of 6 November 2024; these are different metadata and no attempt is made to silently reconcile them.

Example 6.5 on PDF p.13 explicitly gives a globally four-cycle-Markov lattice-support nonfactorization example. Its support, in subset notation, is L={∅,12,3,4,34,123,124,1234}; equivalently x1=x2. Equation (9) gives the obstructing quartic p∅p34p124p123−p4p3p12p1234. The concluding mass assignment has an overlapping-domain typo: it sets p∅=1/2 and also says pS=1/14 for S∈L. The normalized reading gives the second assignment to the seven nonempty states. Even without that editorial reading, the example explicitly treats every support-L distribution violating (9), and the exact probability law below is in this prior family.

**First priority conclusion:** Conjecture 3 was explicitly refuted by Example 6.5. The example's normalized mass choice also refutes Conjecture 2 through the independently verified MTP2 specialization below. The old paper need not call the law MTP2 for its explicitly specified family and mass choice to supply a qualifying prior witness. Its abstract's natural-lattice positive theorem is narrower and must not be mistaken for a proof of the original general conjecture.

## Independent exact specialization to the authenticated source

Let G have edges 12,23,34,14 on V={1,2,3,4}, and define integer weights

- w0000=7;
- wx=1 for x1=x2 and x≠0000;
- wx=0 for x1≠x2.

Set p=w/14. There are eight support states: 0000,0001,0010,0011,1100,1101,1110,1111; the normalizer is 7+7=14. Thus p0000=1/2, each other supported mass=1/14, and all eight excluded masses vanish.

**Lattice.** Equality x1=x2 is preserved by both coordinatewise min and max. Hence L is a Boolean sublattice, containing bottom and top. Its three atoms are the blocks {1,2},{3},{4}; it is not a natural sublattice in Definition 2.4 because the rank of {1,2} is one but its cardinality is two. Thus the natural-lattice hypothesis of the paper's Theorem 6.1 is genuinely absent.

**Global Markov.** The only nontrivial C4 separations, up to interchange of A and B, are 1 separated from 3 by {2,4}, and 2 separated from 4 by {1,3}. Removing fewer than two vertices leaves a connected graph, and with two removed only singletons remain. For the first CI, X1 is determined by the conditioned X2; for the second, X2 is determined by the conditioned X1. A random variable constant at a given positive-mass conditioning value is independent of any other variable there. Conditioning values of zero probability are vacuous. Therefore the law is globally G-Markov exactly in the source's sense. The independent verifier also enumerates all disjoint A,B,C plus unused-coordinate assignments and checks every 2×2 conditional-marginal determinant; all four ordered nontrivial separations pass.

**MTP2.** If x or y is outside L then p(x)p(y)=0. If both lie in L, meet and join lie there. If one is bottom or if the pair is comparable, meet/join are x,y and equality holds. Otherwise neither input is bottom and p(x)p(y)=1/14²; the meet is either bottom, giving left side 7/14², or nonbottom, giving 1/14². The join cannot be bottom. Thus all MTP2 inequalities hold. The exact integer verifier tests all 16²=256 ordered pairs and records zero failures, with no floating-point arithmetic.

**No finite real clique factorization.** Every C4 clique is an edge, singleton or empty; smaller-clique factors can be absorbed into edges. Define U=(0000,0011,1101,1110) and W=(0001,0010,1100,1111). For every edge the multiset of edge configurations in U equals that in W. For 12 the two sides each contain two 00's and two 11's. For each of 23,34,14 the two sides each contain exactly one 00,01,10,11. Substitution into any finite-real edge-factorization gives ∏u∈U p(u)=∏v∈W p(v), independent of signs and zeros. On this law the products equal 7/14⁴ and 1/14⁴, with difference 6/14⁴=3/19208. They are unequal. Hence no finite real clique factorization exists. Because this polynomial identity is continuous, the law is not even in the pointwise closure M_E(G).

These are complete deductions for the qualifying prior family/law; they do not depend on candidate proof/code, the completeness of any previously known toric generating set, or a numerical solver.

## Controls and exact remaining gap

The independently checked standard old C4 tables in Geiger–Meek–Sturmfels (2006), Examples7 and8, are both globally Markov but are not MTP2 in the displayed coordinate order: the exact verifier records respectively 12 and10 ordered-pair failures. They therefore cannot by themselves be cited as already solving the MTP2 conjecture without a further valid transformation or different law. A known invariant is not the same priority object as the qualifying Kahle–Sullivant law.

The strongest result at this checkpoint is a complete qualifying prior refutation of both source Conjectures2 and3, first public preprint date no later than 2024-11-05. The audit does **not** yet compare any candidate, establish the earliest possible occurrence, or assess any claimed extension. Exact remaining work: receive explicit candidate release, compare its witness/theorem and any extensions, inspect older cited primary sources and broader citation chains, finish ledger/read-scope/manifest, and submit a sealed report. Completion estimate: 55% for the assigned audit (main historical match independently established; candidate and breadth work pending).
