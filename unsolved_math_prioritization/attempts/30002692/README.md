# Known construction with one hyperbolic conformal boundary

Problem 30002692 / OWR-13347-011, rank 720. Disposition: **already_solved, 1/5 substantive approaches**, only for the **dimension-unrestricted existential statement printed in Woolgar (2014), page 2550**. The exact current aggregator page returned HTTP 403 and raw AI-problem corpora were unavailable; their statement equivalence remains unverified.

## Accepted result and attribution

The cosh-warped metric on R x S, modulo the product of end reflection and a free orientation-reversing isometric involution of a closed hyperbolic genus-two surface S, gives a complete orientable hyperbolic three-manifold with Ric(g) = -2g. Its smooth compact conformal closure has exactly one boundary component, isometric to S for the chosen compactification. The boundary is S, not the nonorientable central quotient S/tau. An exact smooth even geodesic expansion establishes the unobstructed regularity required in the primary context.

This prior construction is explicit in [Xi Yin (2008), section 6, equation (6.1)](https://arxiv.org/abs/0710.2129v2), and [Skenderis and van Rees (2010), section 4.2, equations (44)-(46)](https://arxiv.org/abs/0912.2090v2). No novelty, first-discovery or new-theorem claim is made. The three-dimensional existential example is not an assertion for every prescribed higher dimension, filling topology, or boundary metric. The primary question is in [Woolgar's 2014 contribution](https://doi.org/10.4171/OWR/2014/45).

Read [release/PROOF.md](release/PROOF.md), the complete [independent audit](audit_release/AUDIT.md), and [current publication assessment](PUBLICATION_STATUS.json). The geometric proof establishes global completeness, smoothness and boundary topology; the computations are supplementary diagnostics, not a formal proof assistant or human peer review.

## Preserved artifacts

Both original ZIPs and all 21 extracted files remain byte-for-byte unchanged. The original pending-review, pending-acceptance and no-remote-write fields describe their historical freeze times. The accepted independent audit and current publication assessment record subsequent progress separately. No source PDFs, extracts, images, raw corpus/catalog records or private coordination files are included.

## Portable offline verification

Python 3.10+ and SymPy are required for the full replay (tested with Python 3.12 and SymPy 1.14.0). The original author diagnostics use only the standard library. No network or private source files are needed. From any working directory, run:

    python3 -B /path/to/30002692/verify_publication.py /path/to/30002692 EXPECTED_MANIFEST_SHA256 --replay
    python3 -O -B /path/to/30002692/verify_publication.py /path/to/30002692 EXPECTED_MANIFEST_SHA256 --replay
    python3 -B /path/to/30002692/test_publication_integrity.py

Obtain EXPECTED_MANIFEST_SHA256 from the draft PR or a separately trusted receipt. The outer manifest excludes only itself. The verifier checks exact files and directories, bytes, SHA-256, original archive/member equality, fixed inner manifest/archive anchors, and claim scope. It runs the frozen assertion-based scripts with optimization explicitly disabled, even when the wrapper is invoked with -O or PYTHONOPTIMIZE. The wrapper's own checks use explicit exceptions and remain active under optimization. The original scripts should not be used directly under -O as integrity verifiers.

Full replay covers 32 author diagnostics and seven author integrity mutations; 31 independent positive groups (81 Riemann and nine Ricci components), ten mathematical negatives, ten author-input integrity mutations, and ten audit-integrity mutations. Publication tests separately corrupt disposable files, manifests, paths, archives, and claim fields and require rejection. The tests supplement the written geometric argument and source-scope assessment.

Only this problem's queue Status, Turns and previously blank Findings are changed. Chat, DOI, all other rows and the existing embedded header remain byte-for-byte unchanged. No queue regeneration, merge, scholarly release, DOI, or outreach is part of this draft. GitHub CI status is checked separately; zero checks is not a CI pass.
