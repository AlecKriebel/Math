# Independent review request: 30004008

All five author turns are frozen. Review the original problem and all scoped claims; do not undertake a sixth author search. Requested verdict: qualified PASS or FAIL for the stated partials, explicitly retaining unsolved5/5 for the original if no defect changes that assessment. No novelty claim is requested.

## Source boundary and external dependency

Read SOURCE_SCOPE.md, SOURCE_MANIFEST.json and PRIOR_GATE.json. The complete original target is Yu Yokoi's OWR50/2018 contribution on printed p3018, PDF page50, including the spanning-root definition and arbitrary parallel arcs. The primary problem statement does not prescribe the output root.

The source PDFs are preserved separately beside the packet in `sources/` and are not part of the public packet:

- OWR_2018_50.pdf, SHA256 a90207e0cadc310ab5a52a228c4b25a16f5e5f617542f006e9909cf90d4c72d2, https://ems.press/content/serial-article-files/46772
- rainbow_2412_15457v2.pdf, SHA256 1295bf402874779e728ca373a571f4be07ad075f0d55fa048cacf2aa609ee23a, https://arxiv.org/pdf/2412.15457v2

The cactus deduction depends on the latter paper's Theorem4.9, with proof in Section5. Printed pp9–10 state the theorem and polynomial matching reconstruction; Section5 occupies pp10–23. The author read the statement, setup, surrounding results and endpoints, and did not independently audit all13 pages of the cycle proof. Theorem4.5 and Corollary4.6 supply the two-multi-root and n≤6 dependencies; those proofs were read. The reported n≤8 computation is credited, not adopted as a new independently checked certificate. The separate cycle preprint was merged into this v2.

## Adversarial targets

1. Turn1: uniqueness of the source SCC, restrictions staying connected, exact forward/backward localization, singleton boundary, root-capacity formula and greedy count
2. Turn2: side-root counting, validity of both tree restrictions at a cut vertex, arbitrary-root gluing, side selection, recursive change of roots, preservation of scaffold blocks when colors are removed, and the precise imported cycle dependency
3. Turn3: Hall's condition for all slot subsets, exact lower quotas, sufficiency of projected-root capacities, repeated attachments, empty/singleton cores, and weighted block-tree centroid argument. Check that its iff is only for the specified construction
4. Turn4: multigraph forest convention, explicit assignment of shared-boundary arcs to one side, component-count identity, boundary indegrees, colored-state compatibility, and the theta example. No all-theta result is claimed
5. Turn5: Laplacian orientation, cycle-zero and tree-one determinants, coefficient inclusion-exclusion, exact upper-half-plane zeros, basis-exchange obstruction, and no inference that one failed algebraic route disproves the conjecture

## Exact replay

Use Python standard library only. From the frozen packet, run `python verify_turn1.py` through `python verify_turn5.py`. Compare stdout bytes to TURN_1_CHECKS.json through TURN_5_CHECKS.json, not just the PASS labels. Scripts2,4,5 import earlier frozen scripts. Check all entries in TURN_1_MANIFEST.json through TURN_4_MANIFEST.json and FINAL_AUTHOR_MANIFEST.json. FINAL_REPLAYS.json records expected counts and hashes.

Finite search neither supplies the all-cactus proof nor certifies current openness or novelty. Preserve all frozen files and identify any needed correction separately. Publication is gated on review; no final queue/PR action is requested by this document itself.
