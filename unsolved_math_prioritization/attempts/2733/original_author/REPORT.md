# Connected sum ropelength assessment

## Finding

**Partial formulation audit, stalled on the intended problem.** The literal
unrestricted part (a) fails with an unknot summand. The intended claim for
nontrivial summands and the positive-universal-saving existence question
in part (b) remain unresolved in this investigation. There is no novelty
claim for the elementary deductions, and no claim that bounded searches
prove the absence of earlier or later work.

## Statement and source reconciliation

The inspected K3 author-preliminary PDF has 436 pages. Printed pages 69–70
contain Problem 1.74; page 67 identifies thickness with reach and the
normal-tube radius. Page 69 states the two inequalities with constants
4π−4 and an unspecified c>0. Neither the local statement nor the chapter
convention on page 11 excludes the unknot. The chapter uses smooth knot
types unless otherwise specified. Ropelength is minimized over rectifiable
representatives; finite ropelength imposes C^{1,1} regularity [CKS02].

The occurrence of “infimal” in K3's informal reach description on page 67
is inconsistent with the standard definition. We use the standard
supremal unique-nearest-point radius in [CKS02], Lemma 2, which agrees
with K3's normal-tube description and its Hopf-link normalization. No
mathematical conclusion here uses the erroneous infimal wording.

The exact UnsolvedMath URL could not be read live: web retrieval returned
an internal error, and a direct request to the www host returned HTTP 403.
The exact-ID inherited record was inspected and hash-matched instead.
The separate AIM workshop-summary link is not treated as the K3 text.
The K3 PDF and its extracts are retained only as inspection inputs and
are excluded from this package.

## Why the intended problem is not refuted

Cantarella–LaPointe–Rawdon's primary computational study [CLR12] builds
composites from prime summands (pages 3–4) and discusses the conjectured
saving in Section 3.2 (pages 9–11). It is evidence for the intended
nontrivial-summand reading, rather than for extending the conjecture to
an identity summand. K3's stronger literal wording therefore warrants a
scope note. It does not justify announcing that the intended conjecture
has been solved or disproved.

The 1997 Nature article [KOP97] was identified by DOI and its author
abstract was inspected via PubMed. The full original article was not
obtained: the Nature page retrieval failed. No claim is made about an
exact implicit qualifier in that full text. The conclusion about intended
scope is an inference from the inspected primary composite-knot study.

For links, merely saying “nontrivial links” is insufficient. The selected
components matter. `PROOF.md` gives exact cancellation of split spectator
blocks; a selected split unknot contributes exactly 2π saving even when
the whole link contains a nontrivial knotted spectator.

## Prior results and bounded literature check

[CKS02] proves regularity and existence, and supplies exact tight simple
chains of Hopf links. Its Figure 1 gives R(C_m)=(4π+4)m−8 for an m-ring
simple chain, m≥2. An end-component sum C_m#C_n=C_{m+n−1} consequently
has saving 4π−4 by direct subtraction. This is a prior special family,
not a new proof for arbitrary knots or links.

[CLR12] provides numerical evidence and carefully constructed upper
bounds. It explicitly discusses the possibility of local minima. An
upper-bound comparison for the two summands and the composite does not
by itself prove an inequality between their three infima. Likewise,
[Diao24] proves a lower bound for alternating knots; a relation between
lower bounds does not furnish the upper bound on the connected sum
required here.

The March 2026 preprint [Klotz26] was checked for current context. Its
abstract and introduction concern bounds and constructions for T(Q,Q)
torus links, not a verified universal connected-sum-saving theorem.
No universal proof for the intended problem was verified in this bounded
check. That sentence is a statement about this review's evidence only.

## Exact remaining gap and stopping decision

The second approach examined a thickness-controlled splice. The precise
rescaling bound is proved in `PROOF.md`. To turn it into a uniform saving
requires a geometric construction with simultaneous topology, tangent,
curvature, nonlocal separation, and length guarantees. Neither minimizer
existence, exposed points of a convex hull, nor numerical retightening
alone supplies that construction. No such certificate was established.

Work stops after two approaches with partial deductions and a named gap.
It does not consume the remaining three approach slots with equivalent
reformulations or unguided computation. The executable only checks package
integrity and exact arithmetic identities; it cannot validate the missing
geometric construction and does not purport to do so.

## Public references

- [K3] R. İnanç Baykur, Robion C. Kirby, Daniel Ruberman, K3: A New Problem
  List in Low-Dimensional Topology, author-preliminary version, Problem 1.74.
  https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [CKS02] Cantarella, Kusner, Sullivan, On the Minimum Ropelength of Knots
  and Links. https://arxiv.org/abs/math/0103224
- [CLR12] Cantarella, LaPointe, Rawdon, The Shapes of Tight Composite Knots,
  J. Phys. A 45 (2012), 225202. https://arxiv.org/abs/1110.3262
  Author PDF: https://jasoncantarella.com/downloads/tightcompositeknots.pdf
- [KOP97] Katritch, Olson, Pieranski, Dubochet, Stasiak, Properties of Ideal
  Composite Knots, Nature 388 (1997), 148–151.
  https://doi.org/10.1038/40582
  Author abstract: https://pubmed.ncbi.nlm.nih.gov/9217153/
- [Diao24] Yuanan Diao, The Ropelength Conjecture of Alternating Knots,
  Mathematical Proceedings of the Cambridge Philosophical Society 177
  (2024), 367–369. https://doi.org/10.1017/S0305004124000288
  https://arxiv.org/abs/2208.00123
- [Klotz26] Alexander R. Klotz, Tight Bounds for Tight Links: Ropelength of
  T(Q,Q) Torus Links, arXiv:2603.02416v1, 2 March 2026.
  https://arxiv.org/html/2603.02416v1
