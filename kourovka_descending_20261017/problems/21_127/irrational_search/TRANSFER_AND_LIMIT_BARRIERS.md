# Transfer and limit mechanisms considered for a negative solution

2026-10-24 UTC. Research route analysis only; no complete irrational-scl example in a RAAG.

## What a transfer theorem would have to prove

A homomorphism f:H->G always satisfies scl_G(f(w))<=scl_H(w) for w in [H,H]. Consequently an embedding of a known irrational example only gives an ambient upper bound. A retraction, or a defect-preserving extension theorem for an extremal homogeneous quasimorphism together with the inclusion upper bound, would give equality. No such RAAG retraction or extremal extension was constructed here. This is a real issue even for inclusions between free RAAGs: Calegari--Walker, arXiv:1101.4055v1, Examples 2.2 and 2.7 / Proposition 2.9 exhibit strict decreases (in particular for suitable connected surface-boundary words in rank at least three). Their rank-two isometry conjecture must not be mistaken for a theorem about all inclusions. This source is used only to confirm that generic subgroup inclusion cannot be treated as isometric.

A quotient map q:G->H gives the opposite useful inequality scl_G(w)>=scl_H(q(w)). An irrational value downstairs gives only an irrational lower bound. This information cannot force an irrational value upstairs: for every finitely generated group H, choose a free group F_r surjecting onto it. Given h in [H,H], choose a commutator expression and lift its commutator factors to produce w in [F_r,F_r] with q(w)=h. The free-group value scl_F(w) is rational, whether or not scl_H(h) is irrational. Thus even exact eligibility and an explicit quotient do not provide equality.

It is also incorrect to infer equality merely because the quotient kernel is amenable. The exact sequence of a Thompson circle lift has cyclic central kernel. The central unit translation has positive scl upstairs, while its image is the identity downstairs. The bounded-cohomology mapping theorem identifies full bounded cohomology but does not identify the kernels of the comparison maps to ordinary cohomology. A bounded Euler class can become exact only after passing to the central extension. Its primitive rotation quasimorphism then need not descend. The golden-ratio lift is a concrete example: unit translation lies in [G,G], has rotation number one and exact scl 1/2; it maps to the identity of T_tau.

## Rips and Dehn-filling route

A virtually special Rips group surjecting onto an irrational-scl group still offers only the quotient lower bound. Passing to a special finite-index subgroup changes the group and requires a further scl transfer calculation. Embedding that subgroup into an ambient RAAG introduces another possible decrease of scl. None of these steps supplies a matching upper bound or an extremal extension.

The 2026 paper Fournier-Facio, arXiv:2603.12095v1, uses Rips constructions and iterated special quotients to obtain a residually finite *limit* group, with a nontrivial perfect normal subgroup on which scl vanishes. The finite-stage groups are virtually special; this does not assert that their direct limit is special, virtually special, or embeds into a fixed RAAG. In fact any proposed embedding of a group with a nontrivial commutator of zero intrinsic scl into a RAAG would contradict the sharp RAAG 1/2 gap: monotonicity gives ambient scl zero for the same nontrivial commutator. Thus the vanishing-normal-subgroup feature is an obstruction to the desired embedding, not a transfer theorem producing irrationality in a RAAG. No claim about rationality is made in the frozen PDF of this paper.

## Infinite graphs, irrational coefficients, and limits of words

Allowing an infinite defining graph supplies no new elementwise scl values. A finite word uses a finite vertex set S. The induced subgroup A(Gamma[S]) is a retract of A(Gamma), so the two commutator lengths of every power of that word are equal, hence so are scl values. This prevents an irrational supremum from being inserted by infinitely many independent coordinate groups: a RAAG word cannot have infinitely many nontrivial coordinates.

Similarly, irrational coefficients on a real scl chain do not answer the integer-word question. For example sqrt(2) times a free-group chain of scl 1/2 has irrational scl by homogeneity, although every commutator-subgroup element of that free group has rational scl. A sequence of eligible words with rational scl converging to an irrational real number would also be insufficient; the limiting value must occur on one fixed finite word in one fixed eligible group.

## Self-similar word/surface attempt

A possible original negative mechanism would be a fixed RAAG word admitting increasingly efficient surfaces with irrational limiting genus/degree, together with an extremal irrational quasimorphism. Hyperbolic substitutions in a free subgroup do not create such a mechanism by themselves: an ambient group automorphism preserves scl exactly, so growth of word length or an irrational Perron--Frobenius eigenvalue of its letter-substitution matrix need not change the scl value at all. A finite list of rational *linear* surface-gluing constraints has rational optima when its rational objective is finite and attained; proving an irrational optimum would therefore require a genuinely infinite or nonpolyhedral obstruction, not just assigning an irrational eigenvector to finite gluing data. No such surface/gluing lower bound or fixed eligible word was found in this route.

The direct circle-action construction in DYNAMICAL_IRRATIONALITY_FILTER.md succeeds in producing an exactly irrational translation number on an eligible word, but deliberately has rational scl. This isolates the missing extremality/matching-bound step without treating numerical dynamics as a solution.

## Outcome

No explicit finite graph and word with a rigorously irrational scl value has been obtained. The negative route remains unsolved. The useful output consists of checked transplant obstructions, an exact irrational-rotation diagnostic, and precise requirements missing from the quotient, special-limit, and self-similar approaches. No preprint or publication gate is opened by these findings.
