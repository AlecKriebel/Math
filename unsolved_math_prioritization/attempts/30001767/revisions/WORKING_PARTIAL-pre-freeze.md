# Fixed-point lemma for the p-subgroup subclass

Provisional checkpoint, not yet independently reviewed. The full Ellers–Murray conjecture remains unresolved. No novelty claim.

Let k be any field of characteristic p, A a finite-dimensional unital k-algebra, and P a finite p-group acting by k-algebra automorphisms. Every central idempotent of the fixed-point algebra A^P belongs to Z(A).

Indeed, any nonzero finite-dimensional kP-module M has a nonzero fixed vector. This follows inductively on |P|: choose a central element z of order p; the kernel of z−1 on M is nonzero since (z−1)^p=0, is P-stable, and carries an action of P/<z>. For e a central idempotent of A^P, the spaces eA(1−e) and (1−e)Ae are P-stable. A nonzero fixed vector in either space belongs to A^P but cannot commute with e. Therefore both spaces vanish, proving that e is central in A. Conversely, every P-invariant central idempotent of A is central in A^P.

Consequently the block idempotents of A^P are the sums over P-orbits of block idempotents of A. If P acts by inner automorphisms, each central element of A is fixed, so the block idempotents of A^P and A are identical.

Apply this to A=kS_n and P=S_2 in characteristic two. The group algebra kS_2 has just one block idempotent, namely1. Thus every block idempotent of (kS_n)^{S_2} is exactly e·1 for a block idempotent e of kS_n, for every n≥2. No normality of S_2 in S_n is used.

The proof relies on nonzero fixed vectors, not division by |P| or averaging. It does not prove equality of full centers, nor assert that arbitrary primitive idempotents of A^P are central in A.

The centralizer question for arbitrary S_l is not covered: a general S_l-module in characteristic p can have no fixed vectors. A small diagnostic is the sign representation of S_3 in characteristic3. More concretely, let S_3 act on V=k⊕sgn and hence by conjugation on A=End(V)=M_2(k). Its fixed algebra is the diagonal k×k, so it has two block idempotents while A has one. This is an abstract interior-algebra control, not a counterexample with A=kS_n. In particular, this V is not a projective kS_3-module, whereas restrictions of defect-zero symmetric-group modules would be projective.

## Source checkpoint

The full original OWR2011/21, printed1183–1184, states the exact unrestricted block conjecture and already credits the cases n−l≤3. Its coefficients belong to a sufficiently large p-modular system, residue characteristic p, and S_l fixes the letters larger than l. The stronger full-center-generation conjecture is separate.

The complete Fayers–Putignano author manuscript, accepted and published as Journal of Algebra685 (2026),271–312, retains the full assertion as Conjecture2.5 and proves generalized ribbon/belt cases with no repeated p-content. Full source: https://webspace.maths.qmul.ac.uk/m.fayers/papers/ribbonblocks.pdf, DOI10.1016/j.jalgebra.2025.07.042. Do not promote those special cases to the unrestricted statement.

The complete Danz–Ellers–Murray2013 paper supplies an arbitrary-subgroup counterexample G=S6,H=A4,p5, which is outside the natural symmetric-subgroup target, and a normal-p-subgroup positive proposition. The elementary argument above does not use normality; this is recorded without any priority claim or criticism of the source. The same paper reports computations of the stronger center assertion for natural S_l≤S_n with n≤8, so repeating those computations is not a new result.

Sources are retained outside the repository in the problem source cache. One proof family has been investigated so far. Work pauses at this checkpoint for an assigned independent review of another problem.
