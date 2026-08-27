# Independent mathematical spot checks

## Scope and method

This folder contains fresh derivations and small symbolic/numeric checks made
from the article formulas and literal parameter maps.  Packaged certificates
are treated only as later comparison targets.  The checks actively search for
counterexamples and record what they do *not* prove.

## Checkpoints

- 2026-08-26T17:42:12-07:00 — Started independent spot-check program.  Read
  the referee instructions and the article's model and three-leaf geometry
  sections.  Exact target: independently test the physical domains,
  tree--sunlet separator, triangle hypersurface, bridge fibre/gluing,
  representative four-port and restoration/probe claims, Krawczyk claims,
  and cherry inverse.  Completion estimate: 5%.
- 2026-08-26T17:55:00-07:00 — Completed exact three-leaf, physical-domain,
  bridge-fibre, capped-gluing, and representative four-port scripts.  Found
  no counterexample within the stated strict domains.  Found expected boundary
  failures at an identity/zero-inheritance sunlet and the genuine unmarked
  degree-two bridge stabilizer, confirming that the stated exclusions are
  essential.  Completion estimate: 65%.
- 2026-08-26T17:58:00-07:00 — Completed self-contained exact-rational
  Krawczyk replay from literal DAG maps and streamed every restoration/probe
  ledger and exact transport.  Krawczyk inclusion, contraction, rank, and
  physical-margin checks all passed.  Ledger roots, counts, references, and
  literal transport maps all passed.  Recorded that ledger validation is not
  producer regeneration.  Completion estimate: 90%.
- 2026-08-26T18:03:21-07:00 — Final clean rerun of all five scripts and
  `py_compile` passed.  Consolidated severity-ranked findings, exact values,
  scope limits, article file:line references, and artifact hashes.  No
  critical or major defect found; bridge topology exclusion and four-port
  global enumeration remain outside this subreview's independent coverage.
  Completion estimate: 100%.
- 2026-08-26T18:22:37-07:00 — Follow-up semantic probe audit.  Reconstructed
  five representative rows (isomorphism, ordinary triangle, quartet,
  tree--sunlet, and two-port parent restriction) from literal profiles without
  importing the producer/atlas; exact graph hashes, incidence/labels,
  arrowheads, restrictions, displayed splits, and K3P circuits all passed.
  Confirmed a major verifier-assurance gap: the actual standalone
  `validate_transport` accepts a coherently self-hashed record whose target
  edge is not induced by its vertex map and contains an unmapped vertex.
  `validate_restriction` is similarly structural-only.  This is not a
  mathematical counterexample, and five samples do not establish the semantic
  completeness of all 574,535 probe rows.  Completion estimate: 100%.
