# Phase 0 literature and status audit

Audit date: 2026-07-25  
Scope: standard one-guard-moves eternal domination only  
Working resolution status: **unresolved**

This file records what was directly checked, what was only cross-checked through
citations, and what remains a lead. A negative literature search is not a
mathematical certificate. It is scheduled for weekly refresh during the
campaign.

## 1. Resolution check

No universal proof and no certified graph satisfying

\[
\gamma(G)=\gamma^\infty(G)<\theta(G)
\]

was located in the sources and current searches inspected through
2026-07-25. The recent direct sources found do not supply a universal
resolution:

- Virgélot Virgile's 2024 University of Victoria dissertation states the
  Gamma-Theta Conjecture and reports only the order-at-most-11 computation.
- Dmitrii Taletskii's `arXiv:2412.20120v2` proves the conjecture for planar
  graphs, a proper class, not universally.
- Kimura, Matsumoto, and Sato (Discrete Mathematics Letters 17 (2026),
  45--50) study the stronger maximum-demand question for planar and
  vertex-critical graphs. Their planar theorem covers plane graphs all of
  whose faces have size at least 12; it is not a universal Gamma-Theta
  theorem.

Thus the campaign must continue to distinguish:

- a universal proof or a fully certified counterexample, which would resolve
  the conjecture;
- order-bounded verification and graph-class theorems, which do not.

## 2. Exact model

MacGillivray-Mynhardt-Virgile (MMV) define the relevant game as follows:
the attacker chooses a vertex with no guard, and the defender moves one guard
from a neighboring vertex to the attacked vertex while maintaining a
dominating configuration. Their `gamma-infinity` is therefore the exact
one-guard, one-edge, unoccupied-attack parameter in this campaign.

The papers of Klostermeyer-Mynhardt discuss both this parameter and
`gamma_m-infinity`, the all-guards-move parameter. Their results are usable
only after checking which section and symbol is involved. Eviction, total,
connected, foolproof, directed, distance, and all-guards Cayley results are
outside scope unless independently reproved for the one-guard definition.

## 3. Correct origin and attribution

The historical chain is more subtle than a simple conjecture citation.

1. Klostermeyer and MacGillivray, *Eternal Dominating Sets in Graphs*
   (JCMCC 68, 2009), stated as Theorem 14 that
   `gamma=gamma-infinity` if and only if `gamma=theta`.
2. Klostermeyer and Mynhardt, *Domination, Eternal Domination, and Clique
   Covering* (DMGT 35, 2015), explicitly identified an error in that proof.
   The cliques built from a dominating-set vertex and its external private
   neighbors need not extend to the remaining shared vertices. The same paper
   then asked whether a graph with
   `gamma=gamma-infinity<theta` exists (Question 7.1).
3. Klostermeyer and Mynhardt, *Protecting a Graph with Mobile Guards*
   (2016), restated the counterexample question as a Problem motivated by the
   2009 error. The inspected arXiv source does not call it the Gamma-Theta
   Conjecture.
4. MMV 2022 write: "A question of Klostermeyer and MacGillivray, which was
   later stated as a conjecture by Klostermeyer and Mynhardt," and label it the
   Gamma-Theta Conjecture, citing the 2016 survey and the 2020
   Klostermeyer-Mynhardt chapter. Virgile's 2024 dissertation uses the same
   attribution.

Accordingly, the safe attribution is:

> The assertion appeared, with a flawed proof, in Klostermeyer-MacGillivray
> (2009); Klostermeyer-Mynhardt (2015/2016) reopened it as an explicit
> question/problem; later Klostermeyer-Mynhardt work formulated it as the
> Gamma-Theta Conjecture.

The 2020 chapter itself was not obtained during this compressed checkpoint,
so an assertion about the first literal use of the name remains pending.

## 4. MMV 2022 appendix and computation

### 4.1 Exact catalog

The uncorrupted arXiv TeX source for Table 9 contains:

- 2 connected graphs of order 10;
- 54 connected graphs of order 11;
- 56 graphs total.

The authoritative machine-readable transcription is
`instances/mmv2022_table9.csv`, SHA-256
`801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d`.
It was derived from the TeX source, not PDF extraction. This matters because
PDF text extraction changes Graph6 characters including backtick, tilde,
caret, and backslash.

Both independent campaign evaluators parse all 56 records and agree on every
parameter. Their joint histogram of
`(gamma,i,alpha,gamma-infinity,theta)` is:

| Count | Tuple |
|---:|---|
| 52 | `(2,2,3,3,4)` |
| 2 | `(1,1,3,3,4)` |
| 1 | `(2,3,3,3,4)` |
| 1 | `(2,2,2,3,4)` |

The four exceptions to the dominant tuple are:

| Graph6 | `(gamma,i,alpha,gamma-infinity,theta)` |
|---|---|
| `JQyurj]yt\|?` | `(2,2,2,3,4)` |
| `JEhbtj{rv}?` | `(2,3,3,3,4)` |
| `JEhbtj{rv~_` | `(1,1,3,3,4)` |
| `JEhbtnN~F~_` | `(1,1,3,3,4)` |

Consequently exactly 55 satisfy
`alpha=gamma-infinity=3<theta=4`, as MMV report. Of those 55, two have
`gamma=1` and 53 have `gamma=2`; none has `gamma=3`. The graph
`JEhbtj{rv}?` is particularly instructive: it has `i=alpha=3` and hence is
well-covered, but still has `gamma=2`. It is a concrete warning that
well-coveredness does not imply `gamma=alpha`.

### 4.2 Reconciliation of the dissertation's 54/53 figures

Virgile's 2024 dissertation says in the prose after Table 3.7 that there are
54 graphs with `gamma-infinity<theta`, 53 of which also have
`alpha=gamma-infinity<theta`. This is not a corrected total.

Appendix Table 5.2 in the same dissertation lists the same two order-10
strings and 54 order-11 strings as MMV. Moreover:

- the 54 order-11 graphs alone are exactly the dissertation's first number;
- among those 54, all except `JQyurj]yt|?` have
  `alpha=gamma-infinity`, giving exactly 53.

The dissertation's 54/53 sentence therefore counts only the order-11 portion
while its wording and appendix concern orders 10 and 11. The combined correct
figures are 56/55.

### 4.3 What is and is not publicly reproducible

MMV describe a Python/NetworkX implementation of a colored
configuration-digraph deletion algorithm. They used NAUTY 2.7001,
PLANTRI 5.2, PuLP, and MIP, and report approximately 85 CPU days for the
through-order-11 Gamma-Theta table.

The inspected arXiv source archive contains only the TeX source and one image.
The journal page exposes the article PDF. No source-code archive, raw case
manifest, solver log, or proof certificate was found in this checkpoint.
Therefore:

- the 56 listed graphs and their parameter values can be and have been
  independently checked on the laptop;
- the claim that no omitted graph of order at most 11 is a counterexample is
  a published exhaustive-computation result, but the original run is not
  packaged to the campaign's stronger certificate standard;
- reproducing the billion-graph order-11 enumeration is neither required nor
  appropriate on this laptop.

## 5. Positive class theorem ledger

“Maximum-demand” means the stronger equality
`gamma-infinity(G)=theta(G)`.

| Class | Exact result | Source status | Consequence for a counterexample |
|---|---|---|---|
| Perfect graphs | Every perfect graph is maximum-demand. | Original Burger et al. 2004 theorem consistently restated in inspected 2015, 2016, 2022, and 2024 sources; original text not yet archived. | It is imperfect. |
| Circular-arc graphs | Every circular-arc graph is maximum-demand. | Attributed to Regan's 2007 Bonn thesis by inspected primary sources; thesis not yet obtained. | It is not circular-arc. |
| `K4`-minor-free graphs | Every `K4`-minor-free graph is maximum-demand. | Anderson et al. 2007, cross-checked in 2016 and 2024; original text not yet obtained. | It has a `K4` minor. |
| Series-parallel graphs | Covered by the exact `K4`-minor-free statement under the standard definition. | Same source. | It is not series-parallel. |
| Outerplanar graphs | Maximum-demand, also a consequence of being `K4`-minor-free. | Same source. | It is not outerplanar. |
| Subcubic graphs | If `Delta<=3` and `gamma=gamma-infinity`, then `gamma-infinity=theta`. | Klostermeyer-Mynhardt 2015, Theorem 6.3, directly inspected. | `Delta>=4`. |
| `C3`-free / triangle-free graphs | If triangle-free and `gamma=gamma-infinity`, then `gamma-infinity=theta`. | Klostermeyer-Mynhardt 2015, Theorem 6.6, directly inspected. | It contains a triangle. |
| `C4`-free graphs | Taletskii states that the conjecture holds for `C4`-free graphs, citing Klostermeyer-Krop-MacGillivray, unpublished manuscript (2018). In Taletskii's terminology, `H`-free means no `H` subgraph, not merely no induced `H`. | Underlying manuscript not located. | The claimed 4-cycle restriction remains provisional and must not yet be a hard coverage filter. |
| Planar graphs | For every planar `G`, `gamma=gamma-infinity` implies `gamma-infinity=theta`. | Taletskii, `arXiv:2412.20120v2`, exact theorem inspected; long proof not yet adversarially audited by this campaign. | It is nonplanar, subject to proof audit. |

Two additional useful results are:

- graphs with `theta<=3` are maximum-demand;
- if `alpha=gamma-infinity=2`, then `theta=2`.
- every plane graph all of whose faces have size at least 12 is
  maximum-demand (Kimura--Matsumoto--Sato 2026, Theorem 1.2).

Goddard--Hedetniemi--Hedetniemi (2005, Theorem 3, attributing the result to
Burger et al.) also record the exact one-guard values
`gamma-infinity(C_n)=(n+1)/2` and
`gamma-infinity(complement(C_n))=3` for odd `n`.  In particular,
`gamma-infinity(C_7)=4`; this classical value is now used in the structural
lane to eliminate an induced `complement(C_7)` in the complement of any
parameter-three counterexample.

Together with the independently proved equality collapse, the
`alpha=gamma-infinity=2` item gives the minimum counterexample parameter
`k>=3`.

## 6. Related constructions and near misses

These constructions concern `gamma-infinity<theta` or
`alpha=gamma-infinity<theta`; none is a Gamma-Theta counterexample unless
`gamma=alpha` is also proved.

1. Klostermeyer-MacGillivray (2005), as exactly restated in the 2016 survey:
   for every pair of integers `k>=a>=3`, there is a connected graph with
   `alpha=gamma-infinity=a` and `theta=k`. The explicit construction and its
   domination number still need extraction before it becomes a synthesis
   template.
2. Complements of Mycielski graphs have
   `alpha=2`, `gamma-infinity=3`, and arbitrarily large `theta`. These are
   infinite claw-free gap examples, not equality hosts.
3. MMV's bow-tie construction turns a suitable triangle-free seed with
   `gamma-infinity<theta=ceil(n/2)` into an infinite triangle-free gap family.
   Their related circulant identity gives an infinite circulant gap family.
   Neither statement supplies `gamma=alpha`.
4. MMV Table 9 supplies the 55 closest published finite hosts through order
   11. The parameter audit above gives the exact reason each fails.

## 7. Well-covered structure and generation

One directly recovered structural theorem is Ravindra's characterization:
a bipartite graph without isolated vertices is well-covered if and only if it
has a perfect matching `M` such that
`G[N(x) union N(M(x))]` is complete bipartite for every matched pair.
This is constructive for bipartite regression cases, but a counterexample
must contain a triangle and so cannot be bipartite.

The requested general generation audit is not complete. No canonical
generator or complete catalog for connected well-covered graphs of orders
12-16 with fixed `alpha=k` and `gamma=k` was verified in this checkpoint.
Recognition results do not by themselves prove generation coverage. Before
any negative finite claim based on well-covered generation, the campaign must
still obtain and audit:

- a constructive generator or a proved complete canonical-augmentation
  scheme;
- its exact treatment of isolated vertices, connectedness, and fixed
  independence number;
- coverage counts or hashes for the intended orders;
- the additional `gamma=alpha` test, since well-coveredness alone is
  insufficient.

## 8. Variant exclusion ledger

| Notation/model | Movement and attacks | Campaign use |
|---|---|---|
| `gamma-infinity` in MMV and the relevant KM theorems | One guard traverses one edge to an unoccupied attacked vertex; every maintained position dominates. | In scope. |
| `gamma_m-infinity` / `gamma_all-infinity` | Multiple or all guards may move after an attack. | Out of scope. Tree and Cayley theorems in this model cannot be imported. |
| Eviction `e-infinity` | Attacks and forced departures differ from standard eternal domination. | Out of scope. |
| Total, connected, foolproof, directed, distance, fractional, vertex-cover variants | Alter domination, legal configurations, attacks, or movement. | Out of scope unless reproved from the campaign definition. |

## 9. Immediate literature follow-ups

1. Obtain and inspect the Klostermeyer-Krop-MacGillivray 2018 `C4`-free
   manuscript. Until then, “a counterexample contains a 4-cycle” is a
   literature lead, not an audited hard filter.
2. Obtain the 2020 Klostermeyer-Mynhardt chapter to pin down the first literal
   use and exact statement of the name Gamma-Theta Conjecture.
3. Audit Taletskii's publication status and adversarially review its planar
   proof. The Kimura--Matsumoto--Sato 2026 full text and exact stated results
   have now been checked.
4. Locate general constructive well-covered generators/catalogs suitable for
   orders 12-16.
5. Repeat the direct-resolution and citation search weekly. Do not contact
   authors or other researchers.
