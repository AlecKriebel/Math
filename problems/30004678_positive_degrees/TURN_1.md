# Turn 1: necessary finite-fiber algebra and the five-element bottleneck

AI-assisted proof attempt. The source-corrected first question remains unresolved. The parity phenomenon is credited to Stephan (2001); the following elementary derivation and finite classification do not supply a new realized cardinality.

Fix a truth-table degree d. Let P(d) be its positive degrees, ordered by positive reducibility. Positive functionals are total monotone truth tables on all oracles.

## 1. Intrinsic operations

For representatives X,Y in d, X⊕Y is in d and its positive degree is their least upper bound: even and odd projections give the two reductions, and two positive reductions into Z combine into a positive reduction of the join. Thus P(d) is a join-semilattice.

Complement induces an order-preserving involution c. If a truth table F is monotone, its dual G(s)=1−F(1−s) is also monotone, so X≤pY implies complement(X)≤p complement(Y). Applying twice proves well-definedness and order equivalence.

There is a greatest element t=[X⊕complement(X)]p, independent of X in d. Every truth-table reduction to X can be rewritten as a disjunction of conjunctions of literals; each literal is supplied positively by one of the two columns. Hence every Y in d is positive reducible to this join. Its complement simply swaps the two columns up to a computable permutation, so c(t)=t. For every a, a∨c(a)=t.

If a=c(a), the preceding identity forces a=t. If a≤c(a), applying c gives the reverse inequality, hence a=t. Thus all non-top elements form incomparable conjugate pairs. A finite fiber therefore has odd size, with exactly one fixed point. A nontrivial finite fiber has no least element: a least element is fixed by every order automorphism and would equal t. These assertions apply to abstract fibers and do not by themselves prove nonrecursive fibers are nontrivial; the latter lower bound is the credited Jockusch result recorded by the primary source.

## 2. Exact classification if the fiber has five elements

Write its non-top elements a,a*,b,b*, where * denotes c. There are precisely two possible isomorphism types consistent with the operations above:

(i) four mutually incomparable elements below t;
(ii) two disjoint two-element chains a<b and a*<b*, capped by t.

Proof. No element is comparable with its conjugate. Any comparison must cross the two conjugate pairs. Relabeling and, if necessary, interchanging names within a pair gives a<b, and conjugation gives a*<b*. No further comparison is possible: reverse edges contradict antisymmetry; a<b* would imply a*<b, giving b as a common upper bound of a,a*, contrary to a∨a*=t; similarly a*<b is excluded. Edges b<a* and b*<a would produce a directed cycle together with the existing paired comparisons. This exhausts all cross-pair edges. If there is no initial edge, (i) holds. Both displayed structures really are join-semilattices with the required conjugation, and their joins are uniquely determined by the order.

This is a necessary two-case reduction, not an exclusion or a realization of cardinality five. In particular, the source's known examples cannot be used to decide either case.

## 3. Why these axioms cannot answer the cardinality question

For every k≥1, take 2k incomparable atoms a1,a1*,...,ak,ak* and one greatest element t. Distinct atoms have join t; each atom joins itself to itself; t absorbs. Swap the paired atoms and fix t. The operation is associative, commutative and idempotent; the involution preserves joins, has only t fixed, and a∨a*=t for every element. This abstract model has exactly 2k+1 elements.

Consequently parity, the complemented join identity, the unique fixed point, and the absence of a least element allow every odd number ≥3. Any exclusion of further finite cardinalities requires additional computability-specific information. Conversely these abstract models are not claimed to be fibers of positive degrees.

## Verification and next direction

The standard-library checker exhausts all labelled partial orders on the four non-top elements, tests the fixed conjugation, joins and conjugate-join condition, and obtains five labelled structures in exactly the two types above. It also checks the explicit star models for k=1,...,20 and finite Boolean duality. These controls verify finite algebra only; they do not construct nonrecursive sets or decide infinite reducibility. Further work will test concrete oracle encodings and identify when an embedding can or cannot control the entire truth-table fiber.
