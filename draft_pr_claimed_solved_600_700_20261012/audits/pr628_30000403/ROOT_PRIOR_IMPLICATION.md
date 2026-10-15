# Prior implication candidate for independent falsification

Prepared 2026-10-15 UTC. This is an authored derivation, not a claim that an earlier paper explicitly states the Hurwitz theorem. Mathematical gate: passed. Priority disposition: pending independent falsification.

## Exact target

At immutable PR628 head `677673860f9e67dffc610f52384f0bd60e65e363`, the target is the minimum extension degree admitting an **ordinary coarse** inner Hurwitz point above a rational reduced point, in characteristic zero, with at least three distinct branch points. The asserted universal upper bound is two, sharp for six-branch C2 covers; geometric cover-point stabilizer V4 has bound one. This is not descent of an actual marked cover object or pointwise optimality for each fixed datum.

## Dated primary theory

Giulio Bresciani, *The field of moduli of a divisor on a rational curve*, arXiv:2211.03438v1, 7 November 2022, section 1 and Proposition 2 (pp.3–4): https://arxiv.org/pdf/2211.03438v1 . Proposition 2 is about arbitrary finite étale gerbes, not only divisors. If a nonsplit genus-zero curve P admits a rational map to such a gerbe with geometrically irreducible genus-zero fibers, its geometric band is cyclic. The source constructs the compression and its rational map in section 1. Published version: Journal of Algebra647(2024),72–98, DOI https://doi.org/10.1016/j.jalgebra.2024.02.021 ; theorem numbering must not be mixed with the preprint.

Giulio Bresciani, *The field of moduli of varieties with a structure*, arXiv:2303.01409v2, 28 November 2023, sections2.1–2.2, Theorem2, Definition5 and Lemma6 (pp.2–5): https://arxiv.org/pdf/2303.01409v2 . Lemma6 identifies a finite gerbe with a universal family and faithful inertia action as an algebraic structure. Theorem2 identifies general structures with twisted quotient/compression data. The text explicitly separates descent to a twist from descent to the specified split variety (Definition15 and Theorem16 later in the paper). The following bridge therefore needs proof, not a substitution of the weaker conclusion.

## Complete coarse-point bridge

Let H=PGL2/k and let F be the reduced geometric orbit, descended to k, in the ordinary coarse Hurwitz fiber above x. Equivalently take the geometrically homogeneous reduced orbit itself if the scheme fiber carries extra structure. The orbit is Galois invariant because x is rational; it is an H-homogeneous space with finite geometric stabilizer E. Finiteness follows from the faithful action on the r≥3 distinct branch points. E is the stabilizer of the coarse cover point, and can be smaller than the stabilizer of the branch divisor.

Form the finite étale gerbe G=[F/H]. Its base change to the algebraic closure is BE. Form the associated family U=[(F×P1)/H]→G, with diagonal H-action; it is a P1-bundle over G and geometrically equals [P1/E]. The inertia action on P1 is faithful. Thus it satisfies the general-structure framework, independently of any invisible center in the actual cover stack: only the coarse scheme F and E⊂PGL2 are being used.

The coarse space Y of U is a smooth projective genus-zero curve over k, since geometrically it is P1/E≅P1. The free-action locus of E on P1 is nonempty and has finite complement. Over its image, U has trivial inertia; its coarse map is an isomorphism onto a nonempty open Y°⊂Y. Consequently Y⇢G is a rational map with geometrically irreducible genus-zero fibers (the geometric atlas of BE pulls it back to the open E-cover in P1).

For an extension K/k, a point y∈Y°(K) gives an object of U(K): an H-torsor T together with an equivariant map T→F×P1. The P1 component gives a K-point of the associated Brauer–Severi curve T×^H P1. A conic with a rational point is split, and H1(K,PGL2) classifies these conics, so T is trivial. A trivialization then gives a point of F(K). This proves the required split-target **coarse Hurwitz** lift, rather than just neutrality of G or existence of a cover over a twisted base.

Every nonempty open of a genus-zero curve over an infinite characteristic-zero field has a point of degree at most two: for a nonsplit conic, intersect with a k-line avoiding the finitely many excluded points and tangent lines; for a split conic choose a rational point in the open. Hence F(K) is nonempty for some [K:k]≤2, for every E, without a subgroup case analysis.

If E is noncyclic, Proposition2 forces Y(k)≠∅. Then Y≅P1 and, since k is infinite, Y°(k)≠∅; the same bridge gives F(k)≠∅. This includes V4, and actually all noncyclic strata. An equivalent elementary explanation is that the characteristic-zero quotient P1→P1/E for noncyclic E has exactly three branch values; their Galois-invariant degree-three divisor descends to Y, so the conic has odd index and splits. E=V4 is not a cyclic exception.

## Sharpness and priority consequence to test

The sharpness mechanism is the classical nonsplit-conic/point-divisor obstruction: six generic points defined on an anisotropic conic, with trivial geometric stabilizer, yield a reduced C2 class but no coarse lift on the split line. The PR supplies a useful explicit exact example, checked independently, not evidence that the general bound remains new. Earlier sources include Marinatto2013 and Cadoret2008 Remark3.14; the original packet already credits an earlier quadratic obstruction in cyclic strata. The explicit coordinates may be different and must not be called copied or historically dependent without evidence.

If the bridge above survives falsification, the full claimed upper bound and its V4 improvement are short consequences of dated prior general descent theory, while necessity of two was already known. The new elliptic realization proof and executable arithmetic example remain valid artifacts, but cannot support a claim to newly resolve an unsolved universal bound. Relabeling the result as expository would change the requested research contribution. No PR disposition should be executed until this exact implication and any viable mathematical repair have been independently challenged.
