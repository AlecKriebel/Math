# Independent delta audit: the exact P4 chain certificate

Completed October 24, 2026 UTC; the exact time and reviewed input hashes are in `DELTA_EXACT_CHAIN_RECEIPT.json`. Review completion: **100% of this certificate's stated scope**. This is an AI mathematical audit, not independent human peer review, formal verification, or a new originality assessment.

**Verdict: pass, with no substantive objections.** In the P4 RAAG,

    C = [ab,d] + [d,a]
    scl_G(C) = 1.

Both summands are commutators, so C is a null-homologous homogeneous chain. The statement is an exact value for this chain, not for arbitrary elements or chains in a RAAG.

## Upper bound: topology and degree

The earlier audit independently verified the actual four-holed-sphere construction and its four oriented boundary labels. Its two retained inner loops are freely homotopic to b and b^-1. Their inverses are therefore freely homotopic, which is exactly the condition for attaching a mapped annulus between them using orientation-reversing boundary identifications. In this particular construction the inner loops can be chosen as the standard positive and negative b loops in the middle torus; alternatively, homotopy collars first put them in that form. No nonzero winding is filled by a disk.

The annulus has Euler characteristic zero, and the attaching circles have Euler characteristic zero. Gluing its two ends to distinct boundary components of the same connected four-holed sphere preserves chi=-2, preserves connectedness, and leaves two boundary components. The resulting orientable surface has genus one. The other two boundaries still map with degree +1 over the respective prescribed loops `[ab,d]` and `[d,a]`.

For a chain with two prescribed terms, the degree in the chain surface formula is the **common degree per prescribed loop**, which here is 1. It is not the sum 2 of the two boundary degrees. Thus this surface gives `-chi/(2n)=2/(2*1)=1`. Since the connected surface has negative Euler characteristic, chi-minus equals its ordinary Euler characteristic. This proves the upper bound. As an independent check, two disjoint once-punctured tori, one bounding each displayed commutator, also have total chi-minus -2 and common degree 1, giving the same upper bound.

## Lower bound: genuine homomorphism and homogeneous chain class

Sending `a→x`, `b→x^-2`, `c→1`, `d→y` respects all three defining relations: the first images are powers of x, and both remaining relators contain the identity. It therefore defines an actual homomorphism to the free group on x,y, rather than just an assignment on the boundary words.

Let `h=[x,y]`. The first chain term maps to `[x^-1,y]`. Expanding and freely reducing `x^-1 h^-1 x` gives exactly this word. The second maps to `[y,x]=h^-1`. In homogeneous chain space, conjugate group elements represent the same class. Consequently the image of C is the class `2 h^-1`. Conjugacy invariance, inversion symmetry, and positive homogeneity of chain scl give

    scl(2 h^-1) = 2 scl(h) = 1.

Here `scl(h)=1/2` is the established free-commutator value, already checked against Heuer Section 2.2 in the earlier audit. Chain monotonicity under the displayed homomorphism forces `scl_G(C)≥1`. Combining the two bounds proves equality. No inference from an element gap alone to an arbitrary chain gap is used.

## Reproduction, scope, and limits

Run `python3 independent_exact_chain_check.py`. The author checker is copied and executed within `exact_chain_reproduction/`, and its output JSON is required to equal the frozen original JSON. A separate letter-inversion implementation independently checks the defining relations, both chain images, and the expanded actual outer boundary words. Exact integer and rational bookkeeping checks the annulus attachment, genus, chain degree, and the independent two-punctured-torus upper construction. All checks passed; details are in `independent_exact_chain_results.json`.

The previously audited matching formula gives persistent loss 2 for the specified eight-vertex piece graph, in agreement with the retained surface chi=-2. The exact chain value strengthens the earlier lower bound 1/2 to 1. It does not turn that fixed-graph optimization into an absolute-scl algorithm, bound the graph types for arbitrary words, or settle Kourovka 21.127. No external priority claim is made.
