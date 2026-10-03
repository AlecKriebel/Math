# Source identity and credited results

Record 30001895 / OWR-11136-027, *Exact Transversals for Families with the
(p,q)-Property*. The approved source snapshot is
[ulamai/UnsolvedMath, revision 37e53eabe540fb458758e198be61634bd02ee008](https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/37e53eabe540fb458758e198be61634bd02ee008).
The source gate checked the full corpus files against the repository's
published manifest: problems, 68,931,837 bytes, SHA-256
`04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`;
reports, 80,334,822 bytes, SHA-256
`8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.
These identify the omitted corpus bodies; this public package does not
contain or newly authenticate them. Dataset curation is attributed to
UnsolvedMath Contributors (2026), under CC BY 4.0; underlying documents
retain their own terms.

The imported statement is:

> For a family of hyperplanes in R^d with the (p,q)-property,
> d+1≤q≤p, must there be a (p−q+1)-transversal; and does the analogous
> statement hold for families of r-element sets with r+1≤q≤p?

This renders the imported TeX without altering the mathematical wording.
The exact imported statement hash is
`b2c9592dc6214e4650ff3d9b969a69b5b639ee643fb8376b9c911568443887d7`;
the repository review hash is
`8204befe62ea6c0bd0191cda6003d590f3af2e8dcfabe643638a39ae19a6047c`.
The source lookup found no matching prior report entry for this code;
the locally saved empty-object fallback is not a prior proof or a user
attempt. The initial repository search found no earlier attempt for this
target. Those are bounded source/prior checks, not global novelty claims.

## Primary formulation and conventions

Dol’nikov's Problem 8 in [OWR 44/2011](https://ems.press/content/serial-article-files/46358),
printed pp. 2540–2541, separately numbers part 2 (hyperplanes) and part 2′
(r-element sets). Its t-transversal is a hitting set of cardinality at
most t, and its (p,q)-property requires a q-member common intersection
inside every p-member choice. It says, “Problem 2′ is a corollary of Problem 2.”
A refutation of part 2 does not settle part 2′. Problem 8's separate
colored Grünbaum part is outside this imported record.

The primary paragraphs do not explicitly require finite families or at
least p members. [Chelnokov–Dol’nikov](https://arxiv.org/abs/1312.4110v1),
Definition 7 and the subsequent conjecture on PDF p. 3, explicitly use
|F|≥p and finite hyperplane families. This package states nonvacuity
explicitly and proves the needed extension from finite r-set families
to arbitrary families. It does not silently call the primary r-set
question finite-only. Sets are nonempty and distinct; common intersection
is stronger than pairwise intersection.

The imported background's 2012 report label and blanket open-status
assessment are historical metadata. The identified report is OWR 44/2011,
and the hyperplane component has a credited counterexample theorem.

## Credited negative hyperplane certificate

Chaya Keller and Shakhar Smorodinsky, *A new lower bound on
Hadwiger–Debrunner numbers in the plane*,
[arXiv:1809.06451v2](https://arxiv.org/abs/1809.06451v2), Theorem 1.1,
PDF p. 3, gives families of actual planar affine lines with

    τ(F) ≥ p^(1+(1−η)/(4q−7)),
    q ≤ 0.01η (ln p/ln ln p)^(1/3), 0<η<1/2, p,q≥3.

No multiplicative constant is suppressed in this displayed theorem.
Its proof uses asymptotic estimates; conservatively take sufficiently
large integer p satisfying the displayed condition. No least p is
claimed. For d=2, q=3, η=1/4, the condition becomes
ln p/ln ln p≥1200³ and the lower bound is p^(23/20)>p−2.
Theorem 1.1 and Proposition 3.1, PDF pp. 8–9, supply finite actual line
families. Nonvacuity follows also from |F|≥τ(F)>p. This directly refutes
the hyperplane claim within its finite, nonvacuous scope.

Publication: *Israel Journal of Mathematics* 244 (2021), 649–680,
[DOI 10.1007/s11856-021-2185-2](https://doi.org/10.1007/s11856-021-2185-2).
The checked constants are those of the cited preprint version.
The q=3 construction has the prior Balogh–Solymosi point-configuration
credit recorded in the paper. No new negative construction is claimed here.

## Credited positive r=2 result and limits

Carlos A. Alfaro, Christian Rubio-Montiel and Adrián Vázquez-Ávila,
*Covering and 2-degree-packing numbers in graphs*, Open Journal of
Discrete Applied Mathematics 7(1) (2024), 1–10,
[publisher PDF](https://pisrt.org/psrpress/j/odam/2024/1/covering-and-2-degree-packing-numbers-in-graphs.pdf),
Proposition 5/Theorem 6, p. 3, proves τ(G)≤ν₂(G)−1 when |E(G)|>ν₂(G).
[DOI 10.30538/psrp-odam2024.0094](https://doi.org/10.30538/psrp-odam2024.0094).
The reductions in TURN1.md extend this to all allowed p,q and arbitrary
nonvacuous rank-at-most-two families. This theorem remains prior credit.

Bollobás' [original set-pair theorem](https://web.vu.lt/mif/s.jukna/EC_Book_2nd/Bollobas.pdf),
Theorem 2, printed p. 452, supplies the critical-edge bound and its
equality case. The uniform equality statement is also explicit in
Gerbner, Lemons, Palmer, Patkós and Szécsi,
[Almost intersecting families of sets](https://www.renyi.hu/~gerbner/papers/glpps2.pdf),
Theorem 2.1, PDF p. 3. They are credited inputs to the structural deductions.

The bounded initial literature check and subsequent audit did not
establish the full r-element theorem or its negation. Linear-family
theorems with extra cardinality thresholds, small-p line results and
independent-vertex versions of hypergraph (p,q) are not substituted for
the requested target. The exact remaining scope and eleven τ=4 pairs
are stated in README.md and the audit. Full-record status remains
unsolved, with five author attempts exhausted.
