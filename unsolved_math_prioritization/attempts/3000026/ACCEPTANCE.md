# Acceptance report: complete-host soccer scores

Problem 3000026 / AMR-029-0026. Edition dated 2026-10-11.

**ACCEPTED as scoped partial results and a narrow published-theorem correction. The unrestricted recognition-complexity target is not solved.**

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. Novelty and priority are unestablished; no exhaustive current-openness claim is made.

## Accepted mathematical scope

- Fixed-draw graph integral-flow and subset criterion.
- Decisive-match accounting and incidence-budget kernel with at most 2m retained teams.
- Sharpness for the stated restricted deletion model.
- Exact 2^{O(m log(m+1))} recognition and witness lifting.
- Complete m=0,1,2 deviation patterns.
- Convex-hull holes in labeled score-coordinate space.
- Refutation of printed 2017 Theorem 9 sufficiency for a prescribed oriented-graph vertex.
- Stronger forced-loss counterexample for the prescribed full vector.
- Correct loss-parity identity and necessary transmitter condition.

The independent mathematical audit required no correction to the candidate proofs. PROOF.md preserves the complete mathematical report and correction note; AUDIT.md preserves the full independent mathematical review. Editorial changes remove internal handling details, disclose review status, and make the already-audited labeled-coordinate interpretation explicit.

## Exact correction boundary

The published source is Pirzada, Samee and Naikoo, Tournaments, oriented graphs and football sequences, Acta Universitatis Sapientiae, Mathematica 9(1) (2017), 213–223, DOI https://doi.org/10.1515/ausm-2017-0014. Theorem 9 on printed p. 220 incorrectly makes the parity condition sufficient for a vertex of a given oriented graph to be a transmitter. Its proof on pp. 220–221 starts by assuming a transmitter and supports the valid necessary direction.

The six outcomes in PROOF.md produce (3,2,5,5), with the 3-point team losing twice. The full all-realizations contradiction rules out an undefeated 3-point team even after changing the realization of that entire score vector. This does not contradict the different, valid scalar-existence statement on scores n−1,n+1,...,3(n−1), or reject the paper as a whole. The correct identity is l_i congruent to n−1−f_i modulo 2.

## Limits and evidence

No all-input polynomial-time recognition algorithm or complete-host hardness reduction is provided. Arbitrary-host and elimination hardness are different targets. The convexity result concerns labeled coordinates and continuous linear feasibility/projection; sorting, other nonlinear preprocessing, integer auxiliaries and arbitrary Boolean combinations are outside that claim.

The historical independent audit reran the creator's finite mathematical checks and performed its own enumeration under normal, -O and -OO Python. It reviewed all 6,998 sorted in-range vectors through five teams, 10,360 labeled inputs through four teams, 3,194 fixed-host quota cases, sparse six-team cases, and actual semantic corruptions. These finite checks support the prose proofs and do not settle the general problem. This edition preparer only rechecks byte integrity and publication packaging; it does not rerun mathematical programs.

Historical source inspection and the journal contribution's publication status are recorded in SOURCES.json. The 272-page issue was retrieved, but not read in full. The separate 11-page EMIS article was inspected at the decisive statement and proof; byte identity across hosts is not claimed. Standard score identities, flow arguments and the 2012 draw-pairing example retain prior credit. Novelty, priority, worldwide current openness and paper-wide correctness are not certified.

This eight-file prose edition excludes programs, raw scans, datasets, copied source documents, images and private coordination material. The compact six-game schedule is mathematical proof content. Source bytes, original mathematical reports, closed inventories, and distributed prose have distinct recorded identities.
