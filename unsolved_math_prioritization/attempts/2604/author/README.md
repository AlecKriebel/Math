# Kourovka 21.95: rigorous exclusions, still unresolved

Problem ID 2604; rank 771 in the inspected repository queue. Author: N. V. Maslova. Governing source: the October 2026 update of the 21st Kourovka Notebook, printed page 191.

> Is there an almost simple but not simple group which is recognizable by the isomorphism type of its Gruenberg–Kegel graph?

The comparison class is all finite groups and the graph is unlabelled. The preceding problem defines this convention. The accompanying note cites Cameron–Maslova's implication that such recognisability forces almost simplicity. The October source has no solved or unconfirmed-AI marker on 21.95. Its question is also stated in Chen–Maslova–Zinov’eva's 2025 preprint, Problem 2.

## Result

**Not solved.** Five substantive approaches give rigorous family exclusions and exact finite certificates, with no claimed new recognisable group and no claimed impossibility theorem.

- Every S_n, n ≥ 5, has infinitely many affine groups with the same labelled prime graph.
- Every group between a characteristic-two symplectic group and its field-semilinear extension has infinitely many such affine competitors. This includes nonsimple PSL_2(2^f) field extensions.
- All 183 PGL_2(q) candidates with odd prime-power q, 5 ≤ q ≤ 1,000, have explicit unlabelled graph collisions with other PGL_2(r), r ≤ 10,000.
- General universal-vertex and unchanged-socle obstructions rule out additional candidates. Selected sporadic extensions are excluded using precisely bounded literature statements.

Theorems and proofs are in PROOFS.md. Literature provenance and boundaries are in LITERATURE.md and SOURCE_VERIFICATION.json. The five approaches and their stopping points are in RESEARCH_LOG.md.

## Replay

Run `python3 verify_manifest.py` and `python3 verify_math.py` from this directory. Only the Python standard library is needed. The latter independently regenerates the exact finite results and compares them to CHECK_RESULTS.json; it does not access the network or require source PDFs, source datasets, GAP, or Sage. Normal replay does not rewrite any file.

The code checks all elements of the affine examples, projective matrix examples, the finite collision list, and deliberately unsuccessful module constructions and vertex maps. Those checks support the proved partial results, not an overall solution. The structural proofs cover infinite families independently of the finite checks.

## Status and scope

Authored research packet; independent audit pending at author freeze. No novelty or priority assertion. Imported recognition/classification theorems are credited and were not independently reproved. No remote write, external communication, or journal submission was performed in this investigation. The payload contains authored exposition/code/results and public verification metadata only.
