# Exact transversals: five-turn outcome for record 30001895

Date: 2026-10-03 UTC. Source code: OWR-11136-027. Original queue rank: 433.
**Full original record remains unsolved after five substantive author responses.**
No complete candidate proof or counterexample for the r-element component
has been produced. Partial deductions and finite certificates below await
a fresh, uninvolved mathematical/computational audit. Novelty is not claimed.

## Original scope

The imported record asks separately whether the bound τ≤p−q+1 holds for
hyperplane families in R^d when d+1≤q≤p, and for families of r-element sets
when r+1≤q≤p. In both questions the (p,q)-property means that every p distinct
members contain q with a common point. A transversal consists of points
meeting every member. We use the nonvacuous convention |F|≥p explicitly.

The primary source is Dol’nikov's Problem 8, parts 2 and 2′, in
[OWR 44/2011](https://ems.press/content/serial-article-files/46358), printed
pp. 2540–2541. The source does not explicitly restrict the r-set family to
be finite. Part 2′ is a separately numbered question, even though the source
also describes it as a consequence of the proposed hyperplane assertion.
Negating the latter does not resolve the former.

## Credited resolution of the hyperplane component

Keller and Smorodinsky, *A new lower bound on Hadwiger–Debrunner numbers in
the plane*, [arXiv:1809.06451v2](https://arxiv.org/abs/1809.06451v2), Theorem
1.1, gives finite families of actual affine lines in R² with the
(p,q)-property and

    τ ≥ p^(1+(1−η)/(4q−7)),
    q ≤ 0.01η (ln p / ln ln p)^(1/3),  0<η<1/2.

Set d=2, q=3, η=1/4 and choose sufficiently large integer p satisfying
ln p/ln ln p≥1200³. Then τ≥p^(23/20)>p−2, contradicting the proposed bound.
There is no multiplicative constant omitted from this displayed theorem.
The construction is finite and nonvacuous; this is not a lower bound merely
for arbitrary convex bodies. The journal publication is Israel J. Math.
244 (2021), 649–680, [DOI](https://doi.org/10.1007/s11856-021-2185-2).
This is credited prior literature, not a new result or an author attempt.

## The separately requested r-element component

For a finite hypergraph H, ν_s(H) denotes the maximum number of distinct
edges in a subfamily whose vertex degrees are at most s. The full finite
r-set question is equivalent to

    ν_r(H) ≥ min(|H|, τ(H)+r−1),                    (C_r)

for every family of distinct nonempty sets of rank at most r. Equivalently,
when Δ(H)>r it asks for τ(H)≤ν_r(H)−r+1.

TURN1.md proves the exact reduction, including the fact that q=r+1 suffices
for all larger q because ν_(s+1)≥min(|H|,ν_s+1). Private padding proves the
equivalence of exactly-r and rank-at-most-r formulations. A finite-witness
induction proves that a positive theorem for finite nonvacuous families
extends to arbitrary families. These reductions do not themselves prove C_r.

Prior literature now covers r=2: Alfaro, Rubio-Montiel and Vázquez-Ávila,
*Covering and 2-degree-packing numbers in graphs*, Open J. Discrete Applied
Mathematics 7(1) (2024), 1–10, Proposition 5/Theorem 6,
[DOI](https://doi.org/10.30538/psrp-odam2024.0094). The theorem matches C₂
when Δ>2. The reductions extend this credited result to every allowed p,q
and to arbitrary nonvacuous families of rank at most two. Distinct singleton
families have no nonvacuous (p,q) instance with q≥2.

## Strongest candidate partial results from this attempt

1. **General elementary structure.** Any maximal r-packing gives a cover
   of size at most the packing size, hence τ≤ν_r. A minimal counterexample
   to C_r must be connected, τ-critical, satisfy τ=ν_r−r+2, and preserve
   ν_r after every edge deletion. The more ambitious saturation-surplus
   shortcut fails on an explicit Fano-plane extension, even across all
   maximum packings. See TURN2.md.

2. **Rank-three, τ≥3 packing bound.** Subject to the stated finite encoding
   and checker correctness, τ(H)≥3 implies ν₃(H)≥min(|H|,5). The proof uses
   Bollobás' credited critical-edge bound and 15 complete finite search
   trees, checked independently in Python. Consequently the original bound
   holds for r=3 and p=q+1, q≥4. The p=q boundary holds for every r by the
   elementary rank-r Helly argument. See TURN3.md.

3. **Extremal critical degrees.** The credited equality case of Bollobás'
   set-pair theorem forces a τ-critical r-uniform family attaining degree
   binom(r+τ−2,r−1) to be complete on r+τ−1 vertices. Such a family has an
   explicit cyclic r-packing and satisfies the target. Thus a minimal
   counterexample satisfies strict versions of both the critical-degree
   and critical-edge bounds. See TURN4.md.

4. **The next rank-three obstruction is narrower but remains.** For τ=4,
   graph-link certificates and explicit six-edge packings exclude degrees
   nine and eight, in addition to the extremal degree-ten case. Exact
   counting leaves twenty (|H|,Δ) pairs, and nine complete additional
   search trees exclude nine of those. Eleven pairs remain unresolved.
   See TURN4.md and TURN5.md.

None of these items is a resolution of the entire r-element component.
The computational claims are finite statements with explicit reductions;
they are not inferences from failure to find a counterexample.

## Precisely unresolved

At rank three and τ=4, an edge-minimal counterexample would still be allowed
by the current work at these pairs (edge count, maximum degree):

    (11,5);
    (11,6),(12,6),(13,6),(14,6);
    (12,7),(13,7),(14,7),(15,7),(16,7),(17,7).

It must also satisfy ν₃=5, simplicity, uniformity, connectedness,
τ-criticality and deletion-stability as stated above. The attempted finite
search on these pairs stopped at explicit node/time limits. This provides
no infeasibility proof and no claim that the computation is intrinsically
infeasible. Larger τ at rank three and general r≥4 remain unresolved too.

## Reproducible evidence and review entry points

- TURN1.md: reductions and exact small labelled uniform-family computation.
- TURN2.md: saturation obstruction and critical-counterexample deduction.
- TURN3.md: full incidence encoding and finite/infinite implications.
- TURN4.md: equality-case theorem application and degree-nine link proof.
- TURN5.md: degree-eight links, external-vertex handling, counting bounds,
  partial τ=4 search, and the corrected pilot-array error.
- `python3 verify_tau3_certificate.py`: checks all 15 rank-three τ=3 trees.
- `python3 verify_link_certificate.py`: checks the nine-edge link exclusion.
- `python3 verify_degree8_certificate.py`: checks eight-edge links and traces.
- `python3 verify_tau4_certificate.py`: checks the nine finished τ=4 trees
  and explicitly reports the eleven unresolved parameter pairs.
- `python3 reproduce_turn3.py` and `python3 reproduce_turn5.py`: reproduce
  the corresponding completed certificates. The latter does not resume
  unfinished cases. Python assertions must be enabled.

Per-turn manifests bind each immutable checkpoint. FINAL_AUDIT_MANIFEST.json
binds the complete final package and identifies every proof, certificate,
checker and result file. The source PDFs and private coordination are not
part of the public package. The required next step is independent review
of the frozen results and their applicability, followed by a disposition
that preserves the full original record as unresolved unless further
authorized work actually closes every requested component.
