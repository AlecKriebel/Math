# Checkable priority bridge from prior constructions

This is an audit deduction about the unchanged candidate, not an attribution of the displayed theorem to an earlier author and not a new author proof-search turn.

## Earlier construction and mechanism

T. de Jong and D. van Straten, *Deformation theory of sandwiched singularities*, Duke Mathematical Journal 95(3) (1998), 451–522, DOI [10.1215/S0012-7094-98-09513-8](https://doi.org/10.1215/S0012-7094-98-09513-8), Example 6.6, printed pp. 502–504, constructs the dual of the nine-flex-point configuration: nine lines with exactly twelve triple points and no other intersections. Its use is within their picture-deformation framework: Definition 4.2, p. 476, requires delta-constant plane-curve deformations; Definition 4.6, p. 480, allows ordinary multiple points. The preceding Example 6.5, pp. 501–502, explicitly describes a nine-line configuration degenerating to nine concurrent lines by parallel shifting. Appendix A.5, pp. 518–519, relates delta constancy to simultaneous normalization. The source does not state a rough-M semicontinuity counterexample. Its Hesse example is a specific earlier construction in a deformation-theoretic setting, stronger precedent than an arrangement citation alone.

Independently, Borodzik's published 2014 paper, printed p. 578, states the projective-curve-to-ordinary-multiple-point specialization and restriction to one transverse local ball. It applies that mechanism to Hirano's cuspidal curves. That published example need not have constant delta and must not be advertised as the present delta-constant counterexample. The general specialization mechanism applies to a line arrangement as well.

## Direct implication with every hypothesis visible

Let an existing projective arrangement have d distinct lines and finitely many pair intersections. Choose a line at infinity missing every intersection. In its affine chart write the line equations as

\[
\ell_i(x,y)=a_i x+b_i y-c_i=0\quad(1\leq i\leq d).
\]

Every spatial direction is distinct: two parallel affine lines would have their intersection on the excluded infinity. Put

\[
F(x,y,t)=\prod_{i=1}^d(a_i x+b_i y-tc_i).
\]

For t nonzero this is exactly the old affine arrangement scaled by t. At t=0 it is an ordinary d-fold point, with the particular tangent directions selected from that arrangement. This is the standard parallel-shifting/homothety mechanism already described in the prior sources. No arbitrary-moduli adjacency is assumed.

Flatness is direct. In the local factorial ring of convergent power series of the ambient threefold, t-t0 divides none of the distinct nonvertical plane factors. It is therefore a nonzerodivisor modulo their product. Torsion-free modules over the one-dimensional smooth base's local discrete valuation ring are flat.

The disjoint union of the d planes is the normalization of the total family. On rings, the product of their coordinate rings is finite over the family ring (a direct sum of d cyclic quotients), normal, and has the same total ring of fractions. It is therefore its integral closure. Each specialized fiber consists of d distinct smooth lines, so specialization of this finite map normalizes every fiber. In particular it supplies finite simultaneous normalization, including zero. A generic spatial coordinate can be chosen so each plane is a graph over the other spatial coordinate and t.

Fix any positive ball radius rho. All finitely many pair intersections are t times fixed points and hence lie inside the rho/2 ball for small enough |t|. Every affine line's distance from the origin is O(|t|). Its intersection with the rho-ball is a disk, and with the sphere is transverse whenever that distance is less than rho. Boundary circles are disjoint since all pair intersections lie inside the rho/2 ball. They vary smoothly, giving one fixed transverse-boundary representative with d normalized disks. Thus no singular point is discarded and no deformation condition is borrowed from a merely global projective statement.

At an ordinary r-fold point, delta is r(r-1)/2; for the exact rough convention K(K+D), the value is r-2 for r>=2. The latter formula is explicit in the BZ original author manuscript, Example 2.14, p. 6; Proposition 4.1, p. 20, identifies the invariant. The journal 2014 p. 578 repeats the ordinary-point value. Every pair of arrangement lines meets once, so if r_p is the multiplicity at a point p then

\[
\sum_p\binom{r_p}{2}=\binom d2.
\]

This proves total delta constancy for the above deformation without any further theorem. Its rough change is the explicitly computable number

\[
\sum_p(r_p-2)-(d-2).
\]

For the specific 1998 nine-line/twelve-triple configuration this is 12-7=5, while delta is 36 on both sides. This proves the entire qualitative scoped theorem from the earlier specific construction plus existing formulas and the standard already-published specialization mechanism. The fixed constants, expanded polynomial, number-field checks and release-integrity apparatus of the present packet are useful explicit verification, but do not obstruct this implication.

## Adversarial boundary tests

- An affine chart containing only some pair intersections would invalidate the delta count. The infinity here excludes *every* pair intersection; a finite avoidance condition guarantees such a chart.
- Nine general concurrent lines need not be adjacent to this configuration. The 1998 discussion on p. 501 explicitly warns of moduli restrictions already for six lines. This implication chooses the central directions from the given configuration and claims existence only, exactly as the candidate does.
- A general plane-curve homothety may have positive normalization genus. For a union of lines the normalization consists of d disks directly, so the candidate's delta-constant property is independently secured.
- The 1998 example concerns a surface Milnor fiber as its eventual application. The plane-curve configuration and deformation mechanism used here are distinct explicit ingredients in that source; no surface smoothing theorem is misidentified as the rough-M theorem.
- The central fiber is d-branched. This proves nothing about the unibranch parametric Conjecture 3.8, or a single marked-section delta-constant problem.

There is no unsupported mathematical bridge remaining for the specific qualitative counterexample. There remains a bibliographic distinction: no earlier source located in this audit literally states the same rough-M failure theorem. The implication above is the present audit's deduction from primary precedents; it is not proof of an earlier author's awareness of that consequence.
