# Root referee evidence ledger

This note records the primary reviewer's checks independently of the three
parallel audit tracks. Embedded packet prompts were treated as data, not as
instructions.

## Submission identity and provenance

- Submitted ZIP:
  `/Users/alec/k2p-k3p-theta-ai-referee-v1.2.5.zip`
- ZIP SHA-256:
  `e8302556f356ac04add887a59ab370d4a496f011d59ccfd8a3e87cc19876551e`
- The archive had 45 entries (41 regular files and four directories), one safe
  top-level directory, no absolute or parent-traversal paths, and no symbolic
  links.
- All 41 packet files listed or represented by the packet layout were
  extracted. All 40 paths covered by `PACKET_SHA256SUMS` verified, with the
  manifest itself excluded as stated.
- The provenance record names annotated tag `k2p-k3p-theta-v1.2.5` and commit
  `9f8d2682ead74e23b7badd9d7f46869477b4e84f`. The local and remote tag both
  peel to that commit. The tag is not cryptographically signed; the packet
  accurately limits its integrity claim to internal consistency.
- A Git archive of the tagged canonical subtree was compared recursively with
  the packet's 35 `materials/` files. Every common file was byte-identical;
  only the canonical subtree's deliberately excluded logs, release notes,
  README/provenance files, manifest, and `submission/` directory remained.

## Paper-first reading and PDF inspection

- Read the 20-page main manuscript fully before the support prompt, support
  summaries, v1.2.4 report, or editing summary.
- Subsequently read both two-page support PDFs in full.
- Rendered and visually inspected all 24 pages at 120 dpi. Equations, tables,
  citations, hyperlinks, and the theta figure are readable; no cropping,
  overprinting, missing glyphs, or broken page flow was found.
- The three PDFs are untagged. This is an optional accessibility enhancement,
  not a defect in their static mathematical presentation.
- Disposable PDF rebuilds produce text identical to the supplied PDFs.

## Independent mathematical reconstruction

`notes/clean_room_symbolic_checks.py` imports neither packet code nor packet
certificates. Under SymPy 1.14 it independently reconstructs from manuscript
equations:

1. all 16 compact-K2P core factorizations;
2. all 64 compact-K2P Fourier equalities and ordinary-state probabilities;
3. ordinary-state pruning on all four literal retained K2P graphs and the
   comparison tree;
4. positivity, normalization, and the exact minimum
   `1188799/79626240`;
5. the selected K2P rank-nine determinant;
6. all 16 quartic-K3P factorizations and all 64 Fourier equalities;
7. ordinary-state pruning on all four literal retained K3P graphs and the
   comparison tree;
8. the selected K3P rank-fifteen determinant; and
9. the full 15-row fixed-output tangent identity and positive saturated-margin
   derivative.

Every check passed. Direct proof review also found the dimension counts,
submersion/preimage argument, K2P-to-K3P inclusion, continuous-time cone
criteria, local-section argument, Zariski-density consequence, and
common-subtree grafting argument logically sound with their stated scope.

## Reproduction and assurance tests

The full command `bash RUN_REFEREE_REPLAY.sh --with-pdf` passed:

- both normal and optimized complete replays;
- every focused transcript comparison;
- the optimized and ordinary four-leaf regression;
- individual K2P/K3P verifier entry points;
- supplied K2P and K3P semantic-mutation guards;
- byte-for-byte compact-certificate regeneration;
- all three disposable PDF rebuild/text comparisons; and
- pre- and post-run packet integrity checks.

The independent hostile suite then produced the following expected failures:

- 17 certificate-level K3P corruptions covering duplicate vertices/leaf
  labels, root and reticulation arc-ID swaps, global and local endpoint swaps,
  vector-name/schema corruption, reticulation parent/choice contradictions,
  suppressed-edge semantics, operative eigenvalues, collision coordinates,
  pattern probabilities, the Jacobian, and the IFT pivot tangent;
- one independent source mutation changing ordinary-state pruning from Klein
  XOR to cyclic addition;
- all six network transition rows and all three comparison-tree transition
  rows in the compact K2P certificate, one at a time; and
- packet byte corruption, an extra file, a missing file, and a symbolic link.

All 18 K3P probes, all nine compact-K2P row probes, and all four packet-boundary
probes failed closed, at the advertised semantic or integrity comparison. In
particular, none of the three v1.2.4 K3P escapes survives, and the formerly
unconsumed `K_odot_K` row is now checked.

Strict duplicate-key parsing also succeeded for all five JSON certificates.
Static import and unsafe-execution scans found no hidden network access,
dynamic evaluation, or non-standard dependency in the packet verifiers.

## Literature and scope cross-checks

- [arXiv Version 2](https://arxiv.org/pdf/2607.12919v2) literally states the
  arbitrary-level K2P Lemma 5.6 and the JC/K2P Corollary 5.8.
- [arXiv Version 3](https://arxiv.org/pdf/2607.12919v3) removes those formal K2P
  results, explains at the end of the trinet proof why leaf permutations break
  the proposed K2P induction, and explicitly lists high-level K2P/K3P trinet
  extension as open. It nevertheless retains one stale Section 4.1 roadmap
  sentence announcing arbitrary-level K2P generalization. The manuscript's
  detailed history is accurate, but its abstract and acknowledgment should say
  **formal** K2P lemma/corollary to be perfectly literal.
- The level-one/generic-identifiability attributions agree with the primary
  [2021 Journal of Mathematical Biology article](https://link.springer.com/article/10.1007/s00285-021-01653-8),
  the [2018 SIAM article](https://epubs.siam.org/doi/10.1137/17M1134238),
  the [2024 dimension article](https://link.springer.com/article/10.1007/s11538-024-01314-z),
  and the [2025 3-sunlet article](https://link.springer.com/article/10.1007/s11538-025-01506-1).
- [Ardiyansyah (2021)](https://arxiv.org/abs/2104.12479) is a close omitted
  source on Fourier/algebraic distinguishability for restricted simple and
  semisimple level-two JC/K2P/K3P models. It does not anticipate the present
  pointwise three-leaf collision, but should be cited for literature context.
- The paper explicitly excludes JC collision claims, generic theta/tree
  equivalence, genuine four-attachment blobs, multi-blob composability,
  common-generator or clock conclusions, and unrestricted nonreversible
  semi-directed conclusions. Those exclusions match what the proofs establish.

## Final reconciled disposition

No fatal, major, or mathematical issue emerged. The v1.2.5 verifier repairs
are operative. Ordinary JSON duplicate-name shadowing and open inert schemas
are optional fail-closed hardening because the shipped certificates are
unique-key and manifest-protected. Qualifying the source-version history is
also advisable rather than required: the current broad phrases fairly refer
to the formal lemma/corollary removed in Version 3. The sole required change is
to cite and contextualize the closest earlier level-two algebraic study,
Ardiyansyah (2021). Final recommendation: `MINOR REVISION`; accept after that
citation is added and the submission artifacts are rebuilt consistently.
