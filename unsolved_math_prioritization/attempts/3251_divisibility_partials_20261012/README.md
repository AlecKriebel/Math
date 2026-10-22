# Odd-hole-free 2-divisibility: accepted partial results

Problem 3251 · Open Problem Garden 56230 · queue row 1753 · 12 October 2026

**Status: unsolved.** This initial authored edition records the second confirmed substantive pass: one earlier screen and the present structural/hypergraph continuation. The lifetime attempt count is unknown. The two complementary lanes and their independent audits belong to this one continuation; they are not extra rounds. No subsequent research round is included.

The exact target is: every finite simple graph with at least one edge and no induced odd cycle of length at least five has a vertex partition whose two induced clique numbers are each strictly smaller than the original clique number. Equivalently, no maximum-cardinality clique is monochromatic. Because odd-hole-freeness is hereditary, proving this for the class would prove hereditary 2-divisibility. Edgeless induced subgraphs are exempt.

This is different from perfect divisibility, which requires a perfect part and a clique-lowering complementary part without requiring the perfect part's clique number to decrease. The five-cycle demonstrates why the notions cannot be interchanged: it is perfectly divisible but has no division into two stable sets.

## Complete arguments and audits

- [Structural proofs](STRUCTURAL_PROOFS.md): color grouping; minimal-obstruction order, degree, clique-pair, matching, core, complement and module reductions; clique-precolor extension; exact separator compatibility; and its numerical consequences.
- [Structural audit](STRUCTURAL_AUDIT.md): complete substantive independent mathematical audit, exact finite checks, corrected pre-freeze assertion defect, and explicitly vacuous critical-separator test coverage.
- [Hypergraph proofs](HYPERGRAPH_PROOFS.md): exact shadow realizability; Fano obstruction; an all-size chordal family whose maximum-clique shadow contains an odd hole; the incidence-two Euler construction; and the Hall representative criterion.
- [Hypergraph audit](HYPERGRAPH_AUDIT.md): complete substantive independent audit, including parity cases, exact case-set coverage, nonuniform/repeated-edge tests and hostile controls.
- [Small authored witnesses](SMALL_WITNESSES.md), [verification scope](VERIFICATION_SCOPE.md), [source ledger](SOURCES.md), and [acceptance boundaries](ACCEPTANCE_AND_SCOPE.md).

## What has and has not advanced

A smallest counterexample has clique number k at least four, at least 3k−2 vertices, chromatic number at least 2k−1, minimum degree at least 2k−2, no nontrivial module, a 2-connected maximum-clique edge core, and connected complement. Every vertex has the proved paired-neighborhood obstruction. A clique separator imposes exact intersection constraints on feasible boundary colorings; for k=4 a two-vertex clique separator forces at least eighteen vertices. This does not rule out clique separators in general.

The hypergraph results give all-size sufficient incidence conditions and identify why arbitrary non-two-colorable hypergraphs and edge-deletion reductions do not immediately yield graph counterexamples. In particular, deleting edges outside maximum cliques can create odd holes even from chordal graphs.

The cases omega=2 and omega=3 are known: the former is elementary bipartiteness, and the latter follows from the Chudnovsky–Robertson–Seymour–Thomas four-color theorem by grouping four proper colors into two pairs. This edition credits that external theorem; it does not prove its full decomposition argument. The unrestricted clique-number-at-least-four target remains unresolved. General clique-cutset exclusion remains conjectural in the inspected literature.

## Distribution and claim boundaries

The complete proof arguments and substantive audits are retained, with reversible editorial removal of original omitted artifact identities and operational references. This is a prose-only authored edition, supplemented by public-source verification metadata and a manifest of the files actually distributed. It includes no executable certificate bundle, raw corpus, copied scholarly source document, source extraction, or private coordination file. The original computations cannot be rerun from these files alone.

There is no full-solution, novelty, exhaustive literature-coverage, human-peer-review, or machine-checked formalization claim. Independent audits here mean independent AI mathematical and finite-computation review. Local preparation is not integration, publication, or a queue update.


## Prior-credit update

The separately checked Hu–Xu–Zhuang preprint arXiv:2603.01967v2 already states directly overlapping minimal-non-2-divisibility necessary conditions: the minimum-degree bound, full clique number on cutset pieces, incompatible boundary traces, and maximum-clique blocking at minimum-disagreement traces. The complete arguments retained here are independent derivations without a novelty claim. See the [complete prior-credit audit](PRIOR_CREDIT_AUDIT.md) and [source ledger supplement](SOURCES.md). That source does not prove unrestricted clique-cutset exclusion or the target conjecture. Its distinct MNPD questions are kept separate from the later, explicitly conditional [status caveat](RELATED_STATUS_CAVEAT.md).
