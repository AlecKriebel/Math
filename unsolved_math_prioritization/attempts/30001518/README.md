# Perfect billiard retroreflectors: accepted scoped partial results

Problem **30001518 / OWR-4412-008**, queue rank **976**. Disposition: **unsolved, 5/5 approaches**. The general existence problem for a bounded piecewise-smooth specular body reversing almost every incident ray remains unresolved. No novelty, exhaustive current-status certification, human peer review, or full-solution claim is made.

## What is accepted

- Exact resistance-defect and angular-error identities, with an exposed planar boundary-length lower bound under the stated normalization and hull assumptions.
- A regular support-point obstruction, excluding globally C1 planar bodies and finite simple polygonal planar bodies. These are proper subclass exclusions, not a reduction of the full target.
- Local rigidity of regular open two-bounce planar retroreflecting branches into perpendicular straight mirror arcs.
- The local symplectic scattering constraint X=A(p)-x and a path-length identity. Symplecticity alone is not a contradiction.
- A conditional finite-itinerary continuity result and an exact sawtooth counterexample to inferring scattering convergence in measure from Hausdorff convergence alone.

Read the [source normalization and literature limits](packet/SOURCE_SCOPE.md), the [five full proofs](packet/README.md), the [complete independent audit](audit_frozen/AUDIT_REPORT.md), and its [scoped acceptance](audit_frozen/ACCEPTANCE.json). No mathematical correction was required. The independent review is a separate AI mathematical/computational audit, not human peer review. Finite tests support the explicit computations but do not formally verify the analytic proofs.

## Frozen evidence and historical statements

The 16-file author packet, 10-file audit packet, and both original ZIP archives are byte-preserved. Their historical statements such as “independent review not performed by this author” or “remote changes: false” describe those freezes; they do not override the subsequent independent acceptance or this publication. Original full source/corpus validation results are retained as historical evidence. They are not asserted to be newly rerun by a source-free replay.

- Author manifest SHA-256: `802e09153108d1ca826841748adfe751aec2fb2c1fe6718bca1083b0e56eb610`
- Author ZIP SHA-256: `164e5736afdf41580386741079a6ee5b05ea5041b56036def48f379970f3042b`
- Audit manifest SHA-256: `8e5005761c5f9c0fddd8b0bcc5c4dfb9a599cbc92c011d541d06b7da2e097e46`
- Audit ZIP SHA-256: `9d2a975d347fe8f54301b7d31d70a365b9fa28503082cf4d52760f07a46a475c`

Public source titles, URLs, hashes, byte counts and bounded inspection history are included. Downloaded source documents, extracted text, page renders, dataset contents, private sources, and private coordination material are excluded.

## Portable source-free reproduction

Python 3.10+ with its standard library is sufficient; no downloads, copied papers, datasets, or third-party packages are required. Obtain the exact PUBLIC_MANIFEST.json SHA-256 from the PR description or another trusted external receipt. Do not compute a new expected hash from an untrusted copy and treat that as authentication.

From any working directory:

```sh
python /path/to/30001518/verify_publication.py --expected-manifest-sha256 TRUSTED_EXTERNAL_HASH
python -O /path/to/30001518/verify_publication.py --expected-manifest-sha256 TRUSTED_EXTERNAL_HASH
python -OO /path/to/30001518/verify_publication.py --expected-manifest-sha256 TRUSTED_EXTERNAL_HASH
python /path/to/30001518/mutation_tests.py --expected-manifest-sha256 TRUSTED_EXTERNAL_HASH
```

The wrapper checks its own anchored exact file and directory inventory, original manifest pins, individual frozen file bytes, and exact ZIP member contents. It launches a genuine optimization-level-0 child for the author replay. The frozen author scripts intentionally reject -O/-OO; those rejections are negative controls, never passed optimized author replays. The independent verifier actually runs at optimization levels 0, 1 and 2, with 77,613 exact checks per mode (including 9,450 sawtooth trajectories and 756 predicted singular cases). The author normal replay has 9,280 exact checks. The audit also rejects 12 mathematical faults, 40 anchored packet/archive corruptions, and four optimized author-script executions.

The publication corruption suite uses a trusted verifier against temporary copies. It exercises each valid/corrupt case under all three actual wrapper modes. A self-consistently rewritten packet or manifest is rejected by the externally fixed pin. This protects integrity, not the truth of arbitrary prose or a compromised external trust anchor.

Source PDFs and corpora explicitly report `NOT_RUN` in source-free replay; the optional source-PDF corruption test is likewise not rerun. To repeat those additional byte checks, separately obtain the public files described in the frozen metadata and use the audit's documented optional input paths. Byte matching is not a fresh semantic literature review. Historical searches were bounded; no exhaustive later-literature or priority conclusion follows.
