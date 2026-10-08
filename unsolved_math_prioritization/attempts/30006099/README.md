# Data-driven maximal time averages: accepted partial progress

Problem **30006099 / OWR-14298803-003**, rank 961. **UNSOLVED, 5/5 approaches.**

The accepted contribution is an explicit non-polynomial, all-finite-degree Chebyshev projection counterexample with an exact-snapshot EDMD realization: approximated derivatives converge uniformly while selected unregularized optimized values are eventually minus infinity. The packet also proves qualified convergence of weighted-error-penalty and spatial-coverage LP alternatives. The complete source program remains unresolved.

Read [the corrected packet's results](accepted/packet/RESULTS.md), [the full independent audit](accepted/audit/AUDIT.md), and [acceptance](accepted/audit/ACCEPTANCE.json). Routes 4 and 5 are dual views of one finite LP with distinct mathematical convergence proofs, not two algorithms. The counterexample does not refute existing strict-feasibility theorems or show that every limit order fails. Positive results require certified global error bounds or regularity and coverage information. No external human peer review or exhaustive novelty certification is claimed.

## Preservation and correction

- `original/` preserves all eight original author files byte-for-byte, including its historical candidate-status lines and incorrect corpus-presence sentence.
- `accepted/` preserves the complete accepted release (23 manifest-listed files plus its manifest), including the full audit and [explicit correction patch](accepted/audit/CORRECTION.patch).
- The only original-to-corrected changes are two corpus-match sentences in `SOURCE_METADATA.json` and the resulting size/hash entry in `MANIFEST.json`. Every mathematical file is unchanged.
- The complete `problems.json` contains one target record. The complete `research_results.json` contains no target record or either identifier. Only public verification metadata is included, not the dataset contents.
- Historical statements about pending review and nonpublication remain frozen provenance; acceptance and this publication wrapper establish the later state.

Pinned SHA-256 anchors:

- Original manifest: `a59fb26e06f8fc99027a248a1feaf80a196a2aa490d62c1ad0c4b7c3b5f9daa5`
- Accepted release manifest: `4bb9b7ddf87bc047bbd3a46c198f47a65b1526fe2d9ed7b93ec54347a3682b39`
- Corrected packet manifest: `19010cb1135f53d157d62882decb37cf9b8ca488a58b637406a5f6a53664f9c2`

## Portable source-free replay

Requires Python 3, NumPy, SciPy and SymPy. The original versions are recorded in `accepted/packet/CHECKS.json`. Obtain the externally pinned public manifest hash from the draft PR or a separately trusted receipt; substituting a hash calculated from untrusted local bytes is not an authenticity check.

    python verify_publication.py --manifest-sha256 TRUSTED_PUBLIC_MANIFEST_SHA256
    python -O verify_publication.py --manifest-sha256 TRUSTED_PUBLIC_MANIFEST_SHA256
    python mutation_tests.py --manifest-sha256 TRUSTED_PUBLIC_MANIFEST_SHA256

The wrapper validates inventory and hashes before invoking frozen code, checks the exact correction diff and unchanged mathematical bytes, and replays the author and independent suites normally and under optimization from a separate working directory. Every recorded check output must reproduce byte-for-byte. Floating diagnostic output is version-sensitive. Mutation controls operate only on temporary copies and test both Python modes.

The author suite has 367 positive checks: 98 symbolic, 200 exact-rational sensitivity comparisons, and 69 floating quadrature/snapshot/LP diagnostics. Six false controls are rejected. The independent suite has 690 requirements, including 210 rational primal/dual witness pairs and 20 integrity-mutation rejections. These finite tests support analytic proofs; floating diagnostics are not exact optimization certificates, and finite checks do not prove infinite-family convergence.

Only authored mathematics, code, audits, acceptance records and public source-verification metadata are included. No source PDFs, extracted scholarly text, dataset contents, private sources, personal data or coordination records are published. Public references and retrieval history are in the corrected packet and audit.
