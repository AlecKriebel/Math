# Independent exact reproduction plan

Frozen 2026-10-15 09:17 UTC, before reading CANDIDATE or submitted verifier.

Target hypothesis: the alpha=16 construction supplies a valid incoming center and at least five distinct admissible outgoing centers for the same six boundary vertices, contrary to a maximum-three claim. All geometric interpretation remains conditional on independent definition review by the parent audit.

1. Read the construction source and derive the one-dimensional outgoing and incoming residuals. Identify denominators, radicands, branch choices, algebraic boundary constants, strict nondegeneracy conditions, and the cancellation risk at large parameters.
2. Build a separate Python-standard-library verifier from those equations using Fraction arithmetic and outward closed rational intervals. Root bounds must be proved by integer power comparisons, with explicit endpoint handling, strict sign checks, and no binary floating arithmetic in proof computations.
3. Establish boundary-root isolation and admissibility, six alternating outgoing endpoint signs, incoming endpoint signs, distinct/disjoint parameter intervals, and geometric nondegeneracy. Treat reuse of an algebraic interval as a dependency enclosure, never as an independent exact value.
4. Include deliberate false root bounds and reversed/forged sign controls that must fail; test interval operations against exact rational examples and exercise large-parameter cancellation.
5. Only after the independent checker exists, inspect all submitted verifier source as data, copy it byte-identically into the owned folder, and replay it with owned output paths. Inspect invoked local modules as needed. No execution from the source folder, no network, package installs, subprocesses, credentials, or writes outside this audit.
6. Compare original machine certificates as data after independent results exist. Record exact meanings of counts, reproducible commands, SHA-256 hashes, and the strongest checked result and gaps. Set deliverable files read-only at completion; do not mutate Git refs, index, or original/shared artifacts.

Success criterion: independent exact inequalities establish the five IVT brackets and incoming existence with all stated algebraic and nondegeneracy conditions, and the submitted verifier reproduces its claimed result under source inspection. A failed obligation is a finding, not a reason to weaken it.

Checkpoint estimate: 5% toward completing this mathematical reproduction audit.
