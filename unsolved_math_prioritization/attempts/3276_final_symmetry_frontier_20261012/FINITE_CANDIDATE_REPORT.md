Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Computational result: full twisted rotational orbits

12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808. Fifth and final pass.

## Result

The first residual fully twisted-transitive minimal-counterexample order from the preceding structural pass, 27, has an exact zero result in a weaker class: full one-step twisted symmetry, distinguished arc 0 to 1 of color 0, no cyclic rainbow triangle, and no monochromatic path to the predecessor. No interval, incidence, primeness, or other-to-other reachability constraint is imposed. Candidate DFS completes this order in 11 nodes and 589 tests; an independent encoder/all-triples/Warshall implementation separately returns zero.

Candidate zero scopes: orders 3,9,15,21,27,45,81. Independent larger zero scopes: 15,21,27,45. Literal complete raw small scopes: 3 and9. These are whole-tournament symmetry scopes, not general finite tournament bounds. The accepted unrestricted finite bound remains ten; periodic controls remain only lengths 3,6,9. This work does not complete periodic twelve or prove an all-size result by computation.

## Exact positive controls

At order nine, among all 1296 full twisted rotational vectors:

- 432 are cyclic-rainbow-free; all nine vertices are sources in every one
- 54 satisfy predecessor nonreachability alone
- zero satisfy both conditions

With the distinguished first arc fixed, the corresponding counts are 216 total,72 rainbow-free,18 predecessor-only,zero both. Both independent literal counting and both DFS implementations match. No normalization by an assumed six-fold orbit is used.

The explicit rainbow-free source model has vector (0,2,2,2), all nine sources, and no one color strongly connected on all vertices. The predecessor-only model (0,1,0,0) has no sources and 18 cyclic rainbow triangles. Full matrices are preserved and freshly checked. Consequently the computation cannot be interpreted as an empty twisted-symmetric class or a color-preserving transitivity theorem.

## Verification

Every full state at n=3 and9 and every erased-orbit partial state is checked with a separately written pairwise encoder and literal graph predicates. The 1302 complete models yield 82992 predicate comparisons,28530 positive-model preservation cases,22050 action checks and12 malformed internal-input rejections. Repeated partial states are counted as model-preservation cases, not distinct graph objects. Fourteen malformed CLI cases are rejected explicitly.

Nine compiled source mutants are rejected with a specific explicit mismatch and exit code2. Accepted detection never means timeout, compilation failure, crash or missing output. The controls cover both prohibitions, path-color mixing, the correct predecessor, complete arc-orbit expansion, the negative-orientation color base, initial-state rejection, actual cyclic rather than transitive triangles, and the final distance variable.

All fresh computations and controls run under normal Python, -O and -OO; substantive receipt fields agree. The C++ compilation mode is -O2. The candidate's counters fail explicitly on overflow. All exceptions are explicit rather than optimization-removable assertions.

## Relationship to structural work

The prior accepted proof establishes that a fully color-permuting-transitive induced-minimal counterexample admits precisely the twisted one-step labeling encoded here, with odd order divisible by nine. The separate fifth-pass structural proof supplies an all-order approach through the three kernel orbits and their monochromatic strong colors. That new structural theorem is not needed to validate this enumeration and is not claimed to follow from its finite tests.

A minimal induced subtournament of an arbitrary symmetric counterexample need not retain the original symmetry. Neither this packet nor its finite interpretation silently transfers symmetry through induced minimization. The unrestricted target remains open in this work; no current-literature-status or novelty claim is made.

## Preservation

Full authored prose, code, examples and receipts are all payloads of the externally pinned manifest. A full-byte rollback archive is actually extracted and verified against that pin. The original prior packets and primary source are unchanged; their identities are recorded. No remote repository or queue writes occur.
