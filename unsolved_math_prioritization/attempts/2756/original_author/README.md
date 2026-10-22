# Kirby 2.8: planar and spherical stabilizer intersections

Problem ID: 2756. Assessment date: 2026-10-06.

**Outcome: partial, not a solution of the arbitrary-bridge-number problem.**

The accompanying proof supplies the missing planar-to-spherical transfer. For an n-bridge unknot splitting, n >= 2, its planar wicket-stabilizer intersection K sits in

\[
1\longrightarrow F_{2n-1}\times\mathbb Z\longrightarrow K
\longrightarrow G\longrightarrow1,
\]

where G is the side-preserving spherical bridge Goeritz group. Finite generation and finite presentation of K are respectively equivalent to those of G. The verified literature therefore gives finite presentation for n = 2 and n = 3. For n = 2 the kernel has index four. No general finite generating set or presentation is established here.

These are standard-theory deductions and a formulation audit; no novelty is claimed. In particular, the finite spherical group in the 2-bridge case must not be identified with the infinite planar braid subgroup.

- `PROOF.md`: definitions, complete transfer argument, finiteness transfer, and a counterexample to an invalid abstract intersection argument.
- `REPORT.md`: primary-source formulation and literature audit, with the exact unresolved scope.
- `APPROACH_LOG.md`: three bounded approaches and their stopping conditions.
- `STATUS.json`: machine-readable result and proposed queue cells.
- `VERIFICATION_METADATA.json`: hashes, byte counts, public sources, and inspection metadata only.

The package contains authored analysis and verification metadata. It contains no copied source PDFs, source extracts, or dataset records. There is no computational mathematical certificate. An independent mathematical audit is still required before publication.
