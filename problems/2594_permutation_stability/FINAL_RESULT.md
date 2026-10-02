# KOU-21.85: five-turn partial research result

**Problem 2594, rank 366. Original implication remains unsolved after five substantive author turns.** This is an unreviewed final author packet awaiting independent review of the scoped claims. It does not propose a new theorem resolving the Kourovka question or certify historical novelty.

## Exact target

For a finitely generated group G, every pointwise asymptotically multiplicative sequence f_n:G→Sym(n) is assumed repairable by genuine actions on m_n≥n points, with m_n−n=o(n) and o(n) disagreement on the original points for each fixed g. Must every such sequence be repairable by genuine actions on exactly n points?

The current primary source is Kourovka 21st edition, arXiv:1401.0300v47 (30 September 2026), Problems 21.83–21.85, printed p. 189. The target is not uniform-in-g stability, weak/sofic-only stability, local stability, or operator-norm stability. The existing amenable implication is credited to Ioana; no later complete permutation-theoretic answer was verified in the source gate.

## Strongest proved reduction

Let R be the finite residual of a flexibly stable G, and Q=G/R. The packet proves that Q is flexibly stable and residually finite, every challenge of G asymptotically kills R, and G is strictly stable if and only if Q is strictly stable. Thus a counterexample, if one exists, can be chosen finitely generated, residually finite and nonamenable. Flexible groups with amenable Q satisfy the implication by the known amenable theorem plus the proved descent.

Within the flexible class, strict stability is equivalent to the vanishing small-deletion repair modulus for genuine finite actions. It suffices to test transitive actions. If D tests all actions and T tests transitive actions, the packet proves

    D(δ) ≤ T(η)+δ/η  for every η>0.

The location of the deleted set may be chosen favorably without changing vanishing at zero: transported compressions differ at at most three times the number of exchanged retained points. Equivalently, one seeks small equivariance defect of an **integral injection** from a slightly smaller exact action into a transitive finite action. The injection objective and the fixed-puncture repair objective differ by at most 2k/n in one direction and k/n in the other.

This isolates the central remaining assertion; it does not establish it for general flexibly stable groups.

## Positive conditional estimates

- First-return compression after deleting k points has multiplicativity defect at most 2k/n, with the constant sharp.
- Flexible repairs with tight orbit-size distributions can be converted to strict repairs.
- More generally, any sufficiently small invariant reservoir can be discarded and its labels transported, whether or not it contains the deleted points. The error is bounded by the reservoir size plus k, divided by n; an overlap-sensitive version is proved.
- A manufactured fixed-point reservoir gives strict repair if its cardinality dominates added points plus total generator repair disagreements. Flexible stability alone supplies no such relative rate.

## Failed mechanisms proved or preserved

- Reapplying flexible stability to a compressed exact action can simply restore the deleted points.
- Retaining only untouched orbits can lose the entire action even in an easily repairable cyclic case.
- The known uniform-instability examples for Z do not refute pointwise permutation stability.
- Replication alone does not produce invariant blocks permitting de-amplification to the original dimension.
- The classical spectral obstruction needs a gap for the diagonal action with every candidate repair. Expansion of the given orbit alone is insufficient. A self-contained four-permutation expander construction shows this with a fixed free group, while explicitly crediting Becker–Lubotzky's earlier warning and projection argument.
- The basic fractional matching relaxation has zero cost in every instance. A family with exact integral cost 1 uses varying prime-cyclic domain groups, so it is not a fixed-group asymptotic counterexample.

## Author turn ledger

1. Compression, exact deletion modulus, tight-orbit criterion, and uniform/pointwise diagnostic
2. Finite-residual descent and fixed-point reservoir conversion with its relative-rate gap
3. Arbitrary invariant-reservoir balancing and reduction to transitive finite actions
4. Credited joint spectral obstruction and a self-contained expander diagnostic
5. Deletion-location transport, integral matching formulation, fractional obstruction, and finite-presentation certificate scope

Source retrieval, review, checkpoint packaging and publication are not author proof turns. Earlier top-level state/log files are historical snapshots bound by checkpoint manifests; `CURRENT_STATUS.json` and this final result give the current author disposition.

## Exact gap and disposition

No proof that every flexibly stable finitely generated group has the required vanishing transitive integral matching defect has been obtained. No single fixed group is proved both globally flexibly stable and non-P-stable. The original implication therefore remains **unsolved, 5/5**.

The five finite receipts replay byte-exactly: 1,633,648 total assertions across five programs, including deliberately overlapping algebra controls. These are not 1,633,648 independent mathematical theorems or an exhaustive search over groups. Infinite assertions and all quantifier transfers have written proofs. Historical source and proof hashes remain bound. Raw source PDFs, rendered pages and imported records are not part of the public packet.
