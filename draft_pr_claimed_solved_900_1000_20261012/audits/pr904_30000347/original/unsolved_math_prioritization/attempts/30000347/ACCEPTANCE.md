# Acceptance report

Date: 7 October 2026. Problem: 30000347 / OWR-1111-001.

## Accepted mathematical claim

For finite simple undirected graphs with unit traversal lengths and three distinct originally connected terminals, finding an edge set that increases every terminal-pair distance by at least one is NP-complete in its decision form. This holds even when every deletion cost is 1 and all three original distances are 3; exact optimization is NP-hard. Disconnection counts as infinite distance, as permitted by the historical source. The proof also establishes the positive binary-encoded rational-cost decision classification and an optional construction retaining finite terminal distances, indeed exactly 4 after the selected deletions.

The frozen manuscript gives a complete polynomial many-one reduction from Vertex Cover. Replacing each source edge by a path of length 3 gives a supplied tripartite graph H with tau(H) = m + tau(Q). Terminal spokes give an exact blocker optimum tau(H), including arbitrary deletion of middle edges. Budget B = m + k, graph size, edgeless and zero-budget cases, binary encoding, and NP membership are all addressed.

## Reviews and identity

Both independent full-proof reviews accepted the same unchanged manuscript. Required mathematical corrections: none. Each auditor reports not reading the other audit. They independently checked the source model and reconstructed both reduction directions, then supplied separate finite controls. The second auditor's controls were written and first run before inspecting the author's implementation.

Accepted PROOF.md: 11,661 bytes; SHA-256 f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7.
Frozen manifest SHA-256: b13c9cee3e806a263ba0e24b2838599692727ea48d26977d4fca714e1e30d273.
Original archive SHA-256: f05e41d5a419c2faffc584e495da799bc43b306850ccd50c4f1f8824ab224996.
Audit A report SHA-256: 827f4cd5449672fef203232eb559f214fc4dedd68c61c0cca36ef7feaf45f2da.
Audit B report SHA-256: ea3f75a2827fa0d75af07a32e4f985690dc6d791b47cbcc97e30ff40dd0d4b68.

All historical deterministic computation counts are replayed by the portable publication verifier, which uses only included authored files. These tests are supplementary to the written universal reduction. Mutation controls check rejected alterations, missing files, and malformed manifests, including optimized Python mode.

## Scope and status

Disposition: claimed_solved, 1/5 completed substantive proof-attempt turns. One complete author reduction was frozen within the budget; source triage, independent auditing and packaging did not extend an unfinished proof search. No novelty or priority claim is made. The current-literature search was bounded and cannot establish that no prior result exists. The cited historical report explicitly already treats directed-triangle hardness; this work concerns the undirected model.

No planar, bounded-degree, weighted-traversal-length, unique-geodesic, or globally connected residual-graph theorem is asserted. Independent AI-assisted mathematical acceptance is not human peer review, journal acceptance, or formal proof-assistant certification. Original authored reports and manifests remain intact, including their historical status language. Only public citations and source verification metadata accompany the authored work; copied third-party sources and dataset contents are excluded.
