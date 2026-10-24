# Exact row-path product construction

Recorded 2026-10-24T19:40:00Z. Best-guess overall discovery completion: **20%**; the arbitrary-subset conjecture remains unresolved. The following is a checked elementary construction. Its novelty has **not** been established; it must not be promoted as a new literature result without the separate priority audit.

## General fiber lemma

Let G and H be additive abelian groups with no nonzero element killed by 2. Let R={h_1,...,h_r}, r>2, have a cyclic ordering with pairwise distinct sums h_i+h_(i+1). For each h in R, let B_h be a finite subset of G of size greater than two, with a rainbow cyclic ordering that contains the **same undirected edge {u,v}**, u≠v. Write c=u+v. Then

A = union over h in R of (B_h x {h})

has a rainbow cyclic ordering.

**Proof.** Delete the edge {u,v} from each fiber cycle and orient the remaining Hamilton path from u to v. Concatenate these paths in the stated cyclic order of R. This enumerates every element of A exactly once. Every internal edge in row h has second color coordinate 2h, so internal colors from different rows cannot coincide. Within each row the colors are distinct, and their first coordinate avoids c because the deleted edge was the unique edge of that color. Every joining edge goes from (v,h_i) to (u,h_(i+1)), with color (c,h_i+h_(i+1)). Join colors are pairwise distinct by the hypothesis on R, and cannot equal any internal color because their first coordinate is c. This proves the claim.

**Cartesian-product corollary.** If B⊆G and R⊆H each have rainbow cyclic orderings and both have size greater than two, then B x R does too: use B_h=B and choose any edge of its cycle. This is a preservation result, not a proof that an arbitrary subset admits such an ordering.

**Boundary.** This proof needs each nonempty fiber to support a rainbow cycle sharing the prescribed edge. That condition cannot be silently assumed. For example, in C5 the subset {0,1,2,4} has no rainbow Hamilton cycle containing edge {0,1}: the two orders up to reversal that contain this edge are (0,1,2,4) and (0,1,4,2), and each repeats color 1. Thus an attempted universal fiber proof that merely assumes prescribed-edge existence is blocked.

## Punctured-fiber corollary

Suppose finite odd-order G has rainbow cycles on G and G\{0} that share edge {u,v}. For any odd-order abelian H and **any** D⊆H, the subset

A = (G x H) \ ({0} x D)

has a rainbow cycle. Use B_h=G\{0} for h∈D and B_h=G otherwise, then the fiber lemma with R=H. H admits a rainbow full-group cycle by the mixed-radix construction below. If |H|=1, the conclusion is simply the assumed full or punctured G cycle and does not need the fiber lemma's r>2 condition.

There are explicit bases:

- G=C5: full cycle (0,1,2,3,4), punctured cycle (1,2,4,3), common edge {1,2}. Cut paths u=1→v=2 are (1,0,4,3,2) and (1,3,4,2).
- G=C3 x C3, encoded a+3b: full cycle (0,1,2,3,4,5,6,7,8), punctured cycle (2,5,4,6,1,7,8,3), common edge {4,5}. Cut paths u=4→v=5 are (4,3,2,1,0,8,7,6,5) and (4,6,1,7,8,3,2,5).

Each listed cycle and path can be checked directly by modular addition; `product_constructions.py` constructs explicit larger instances and the standalone `verify.py` checks the resulting cycles without relying on this proof.

For F5^d, every complement contained in an affine hyperplane is carried by an affine automorphism into {0} x F5^(d-1). The C5 corollary therefore covers it. For F3^d, d≥2, every complement contained in an affine subspace of codimension at least two is carried into {0} x F3^(d-2), using G=F3². In particular, every complement of size at most three in F5³ and F3⁴ satisfies the stated rank bounds. This explains the exact product rescues of the dense finite samples; it does not settle larger complements of full affine rank.

## Full-group mixed-radix construction

For G=C_(m_1) x ... x C_(m_d), every m_j odd, enumerate elements by the integers 0,...,q-1 in mixed radix, the first coordinate least significant. This natural cyclic listing has all q adjacent sums distinct. To verify, write an index's coordinates x_j and the carry into coordinate j in incrementing the index as e_j, with e_1=1. Its adjacent-sum coordinate is 2x_j+e_j modulo m_j. Since 2 is invertible modulo m_j, the sum's first coordinate determines x_1; that determines the carry e_2, hence the next sum coordinate determines x_2, and so forth. Thus the sum determines the edge's starting index uniquely, including the wraparound edge, proving bijectivity.

## Exact gap

The general claim includes arbitrary A⊆G, which need not be a Cartesian product or a family of fibers whose cycles share one edge. The finite searches establish only their enumerated domains. The product construction establishes the specified structured family. Neither replaces the missing general argument or an exact counterexample.
