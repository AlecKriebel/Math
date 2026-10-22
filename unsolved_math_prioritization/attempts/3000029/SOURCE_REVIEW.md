# Source review and exact claim boundary

Problem 3000029 / AMR-029-0029. Recorded proof-review and independent-audit
observations, 10 October 2026. This is an AI-assisted, unrefereed partial result.

## Original question and prior credit

The original [EGRES question](https://oldlemon.cs.elte.hu/egres/open/Destroying_rigidity)
and its [discussion](https://oldlemon.cs.elte.hu/egres/open/Talk:Destroying_rigidity)
ask for minimum edge deletion destroying generic local rigidity in the plane,
equivalently a minimum cocircuit of the restricted planar rigidity matroid.
The abstract input graph need not be topologically planar. The vertex set is
fixed; neither global rigidity, vertex deletion nor clique pinning is the task.

[Bérczi, Bernáth, Király and Pap, Blocking optimal structures](https://egres.elte.hu/tr/egres-17-07.pdf),
2017, printed page 3 / PDF page 4, distinguishes this question from its polynomial
results for unions of graphic/hypergraphic matroids. Transversal minimum-circuit
hardness does not imply rigidity minimum-cocircuit hardness.

The rigid-component description is classical. [Servatius, Planar Rigidity](https://users.wpi.edu/~bservat/phddissertation.pdf),
1987 dissertation in a 2005 typeset conversion, Chapter 4 Theorem 2, printed
pages 32-33 / PDF pages 52-53, provides the historical cocircuit treatment.
The report proves its needed budgeted-cover identity directly in the Laman
matroid. [Cruickshank, Jackson, Jordán and Tanigawa's 2025 survey](https://arxiv.org/abs/2508.11636),
Theorem 3.1 and equation (2), pages 10-11, records the classical rank-cover
formula and credits Lovász and Yemini. The [1982 publication record](https://doi.org/10.1137/0603009)
was checked, but the original article was not obtained or read in full.

The source caveat is deliberately narrow. Servatius's displayed even-subfamily
condition combines a strict inequality with an additive two. Two triangles
sharing one vertex give equality at five in that display, although adding
one cross-edge makes a seven-edge Laman graph on five vertices. The report
uses none of that printed condition. No source-author intent or replacement
theorem is inferred; no correction of the source's full theorem is claimed.

The degree bound rho <= delta-1 is prior work: [Yu and Anderson, Agent and Link
Redundancy for Autonomous Formations](https://skoge.folk.ntnu.no/prost/proceedings/ifac2008/data/papers/0554.pdf),
Lemma 3, printed page 6586 / PDF page 3. Their small-graph convention is not
imported: the report treats K2 separately with rho=1, and a one-vertex input
outside its domain has no feasible deletion.

The deterministic rank oracle is credited to [Lee and Streinu, Pebble Game
Algorithms and Sparse Graphs](https://arxiv.org/abs/math/0702129),
[Discrete Mathematics 308 (2008), 1425-1437](https://doi.org/10.1016/j.disc.2007.07.104).
The audit checks the basic (2,3) algorithm and its O(nm) bound; no faster
implementation is needed. [Jordán's extremal redundancy paper](https://egres.elte.hu/tr/egres-20-21.pdf),
[2021 published version](https://doi.org/10.1007/s00373-021-02327-4), concerns
extremal sizes and particular families, without providing arbitrary-input
optimization for this objective.

## Accepted partial mathematics

The exact budgeted clique-cover identity and closure proof retain all vertex
and rank boundary cases. Deleting at most min(delta-1, nullity+1) edges gives
exact class-wise polynomial / XP algorithms. This includes topologically
planar simple rigid graphs, where delta <= 5 permits testing at most four
edges, but it is not a uniform polynomial algorithm for arbitrary inputs
and is not an FPT claim.

K6 with its K3,3 basis disproves the one-fixed-basis shortcut: every fundamental
cocircuit has size seven, while the optimum is four. The clique-inflated K2,q
family has a unique cut of size t, unbounded residual rigid-component count
as q grows, and unbounded degree/ordinary-connectivity gap as s grows. Its
residual is 2-vertex-connected. These are structural counterexamples, not
hardness reductions. All proofs appear in full in [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md).

The general complexity question remains unresolved by this work. Neither a
uniform deterministic polynomial algorithm nor a valid hardness reduction
is supplied. No novelty, priority, or worldwide-current-openness claim is made.

## Recorded inspection and supporting evidence

[SOURCE_METADATA.json](SOURCE_METADATA.json) preserves eight recorded source
sizes and SHA-256 hashes, available retrieval times, public URLs, and inspection
locators. Their identities matched during independent audit. Complete retained
EGRES text was inspected; direct live opening failed during that audit, so
it is not described as successful fresh retrieval. The earlier proof review's
live-search recheck is a separate historical observation. The survey, Servatius,
Yu-Anderson and Lee-Streinu pages identified above were visually inspected
during review or audit as recorded; these are not new edition-preparation claims.

The audit records 33,866 finite graphs, 8,128 rigid inputs, 75,139 optimal
residuals and 56,564 independent family deletion checks, with normal/optimized
agreement after excluding elapsed time. Author checks include sampled larger
families, whose component counts come from the theorem rather than exhaustive
component enumeration. The infinite-family result rests on the analytic proof.
Only aggregate supporting results are distributed. The proof needs no omitted
program, generated certificate, raw output or source body.

Edition preparation performed no new scholarly-source retrieval, source-file
rehash, source inspection, literature search or mathematical test rerun.
The separate mathematical audit is not external human peer review, journal
acceptance or formal proof-assistant certification. Bounded source checks
do not certify novelty or current global openness.
