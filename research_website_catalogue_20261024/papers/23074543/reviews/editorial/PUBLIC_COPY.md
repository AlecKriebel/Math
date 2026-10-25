# Irreducibility of exposed-point varieties of discotopes

A connected analytic support parametrization proves general exposed-point irreducibility and, separately, equality with the purely nonlinear part under a generic-position condition.

[Alec Kriebel](https://orcid.org/0009-0001-9320-500X) · Independent researcher · 30 September 2026 · Version 1.0 · Unrefereed preprint

[Read the paper](https://zenodo.org/api/records/23074543/files/paper.pdf/content) · [Complete source and verification archive](https://zenodo.org/api/records/23074543/files/source-and-verification.zip/content) · [DOI](https://doi.org/10.5281/zenodo.23074543)

## Abstract

We prove that the complex Zariski closure of the exposed points of any finite Minkowski sum of ellipsoidal discs of dimension at least two is irreducible. No genericity or full-dimensionality assumption is needed. This proves the exposed-point irreducibility conjecture stated by Meroni in the 2023 Oberwolfach report. Under an explicit generic condition on the summand spans, we also prove that this closure equals the purely nonlinear part defined by Gesmundo and Meroni, thereby proving their 2022 irreducibility conjecture. The proof uses a connected real-analytic support-point parametrization. A nongeneric example shows why the two varieties must be distinguished.

## The general exposed-point theorem

A disc here is a centered ellipsoidal ball in its own linear span: a linear image of a closed Euclidean unit ball. A discotope is a finite Minkowski sum

\[
D=D_1+\cdots+D_N\subset\mathbb R^d,\qquad N\ge1.
\]

A point is exposed when it uniquely maximizes a nonzero real linear functional. Write \(E(D)\) for the complex Zariski closure of these exposed points. If every summand has dimension at least two, then \(E(D)\) is irreducible over \(\mathbb C\).

This theorem requires neither genericity nor full dimensionality of the sum. It allows repeated discs, coincident summand spans, dependent quadratic radicals and noninjective support parametrizations. The target is the closure of the actual exposed points.

## A separate equality of varieties

Gesmundo and Meroni define the purely nonlinear part using relative summand boundaries:

\[
S(D)=\overline{\left(\sum_i\partial_{L_i}D_i\right)\cap\partial D}^{\mathrm{Zar},\mathbb C},
\qquad L_i=\operatorname{span}D_i.
\]

The second theorem assumes that \(D\) is full-dimensional and that, for every subset \(J\) of summands,

\[
\dim\!\left(\sum_{i\in J}L_i\right)
=\min\!\left(d,\sum_{i\in J}\dim L_i\right).
\tag{GP}
\]

Under this explicit condition, \(S(D)=E(D)\), so \(S(D)\) is irreducible as well. The condition holds on a nonempty real Zariski-open set of the prescribed full-rank matrix parameters. As in the earlier discotope work, a smaller total ambient span may be used as the ambient space.

The distinction matters outside generic position. For two identical unit discs in the \(xy\)-plane and one in the \(xz\)-plane, the point \(e_3\) lies in the set generating \(S(D)\), while a polynomial vanishing on all exposed points has value \(16\) at \(e_3\). Thus \(S(D)\) can strictly contain \(E(D)\). The general exposed-point theorem alone would not establish the earlier conjecture about \(S(D)\); the separate equality theorem supplies that bridge.

## The proof mechanism

Represent each disc as \(D_i=A_i(B^{m_i})\) with \(A_i\) injective and \(m_i\ge2\). A normal \(u\) exposes one summand point exactly when \(A_i^Tu\ne0\), in which case that point is

\[
p_i(u)=\frac{A_iA_i^Tu}{\|A_i^Tu\|}.
\]

The face of a Minkowski sum is the sum of its summand faces. Its exposed-point set is therefore exactly the image of

\[
F(u)=\sum_i p_i(u),\qquad
U=\mathbb R^d\setminus\bigcup_i\ker A_i^T.
\]

Every excluded kernel has codimension at least two, making \(U\) connected. The positive real denominators make \(F\) real analytic on that domain. If a product of two complex polynomials vanishes on its image, analytic uniqueness forces one factor to vanish throughout the image. The vanishing ideal is prime, proving complex irreducibility without choosing global complex square-root branches.

For the equality theorem, (GP) makes the summands killed by a supporting normal independent inside its perpendicular hyperplane. A single small normal perturbation can then realize all their prescribed relative-boundary points simultaneously. Every point generating \(S(D)\) is a limit of exposed points, giving the reverse inclusion into \(E(D)\).

## Scope and predecessor credit

Meroni's 2023 Oberwolfach contribution states the generic exposed-point irreducibility conjecture. The first theorem covers that formulation with genericity removed. Gesmundo–Meroni's 2022 Conjecture 8.2 concerns \(S(D)\), and is addressed by combining the two theorems under the stated genericity convention.

Gesmundo and Meroni already proved irreducibility for generic discotopes when \(\sum_i(\dim D_i-1)\le d-1\), for generic sums of two-dimensional discs, and for the case in which every summand is full-dimensional. Their Section 5 already uses the support-gradient parametrization. Kucharz and Kurdyka explicitly record the real-Zariski version of the connected analytic-image principle in the proof of Proposition 4.3. The present manuscript includes the complex-coefficient argument and applies this mechanism to the general discotope theorem and the generic identification.

Rank-one summands are outside the theorem. An interval has two exposed points, while a planar disc plus a nonzero segment has an exposed-point closure consisting of two distinct conics. No result about degrees, birationality or irreducibility of the entire complex critical locus is claimed. Historical first priority is not asserted.

## Research status and substantive contributions

This is an unrefereed preprint. Generative AI tools were used extensively in proof development, writing, literature work and symbolic checking. Internal AI checking is not human peer review or formal proof certification. The complete source and verification archive accompanies the paper; its finite symbolic controls support formulas and examples, while the written argument proves the universal statements.

Substantive proof checks, counterexamples and precise source comparisons are welcome. Authorship and acknowledgments follow actual contributions. The cited researchers receive credit for their prior work; citations do not imply participation or endorsement.

## References

1. F. Gesmundo and C. Meroni, [*The Geometry of Discotopes*](https://doi.org/10.4418/2022.77.1.8), Le Matematiche **77**(1) (2022), 143–171; [arXiv:2111.01241v2](https://arxiv.org/abs/2111.01241v2). See Definition 3.3, Theorems 4.3 and 6.1, Remark 3.4, Section 5 and Conjecture 8.2.
2. W. Kucharz and K. Kurdyka, [*Rationality of semialgebraic functions*](https://doi.org/10.18778/8088-922-4.14), in *Analytic and Algebraic Geometry 2*, Łódź University Press, 2017, 85–96; proof of Proposition 4.3, p.95.
3. C. Meroni, [*Two convex conjectures for different flavours*](https://doi.org/10.4171/OWR/2023/15), in *New Directions in Real Algebraic Geometry*, Oberwolfach Reports **20** (2023), Report 15/2023, 829–832; Conjecture 1, p.830.
