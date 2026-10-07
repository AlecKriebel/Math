# Periodic basin-boundary accessibility research packet

Problem 5300048 / AMR-052-0048, rank 954. Frozen author submission,
7 October 2026. **Outcome: unresolved after five mathematical approaches.**
No complete solution, holomorphic-basin counterexample, novelty claim,
independent acceptance, or human peer review is claimed.

The main concrete result is analytic rigidity of the explicit inaccessible
slit-comb domain: every proper holomorphic self-map extending across its
entire closure is affine and therefore has degree one. Thus transporting
z² into this domain by a Riemann map cannot satisfy the required extension
hypothesis. Additional results isolate sufficient access conditions and
specific failures of tempting proof shortcuts.

## Contents

- `PROOF.md`: complete authored mathematics, five approaches, and exact gaps.
- `APPROACH_LEDGER.md`: approach accounting, claim dependencies, and audit targets.
- `SOURCE_NOTES.md`: source interpretation and bounded literature conclusions.
- `SOURCE_METADATA.json`: public citations, locators, recovered PDF/text hashes,
  byte counts, version distinctions, and inspection history. Source files are absent.
- `TARGET_VERIFICATION.json`: exact problem/corpus matching outcomes and hashes,
  with neighboring-problem distinctions. Corpus contents are absent.
- `verify_controls.py`: standard-library exact-arithmetic diagnostics.
- `CONTROL_RESULTS.json`: deterministic results of those diagnostics.
- `AUTHOR_MANIFEST.json`: SHA-256 and byte count of every other packet file.

## Reproduce

From this directory, run:

    python3 verify_controls.py --check-result --check-manifest

The script compares its exact result to `CONTROL_RESULTS.json` and verifies
all manifest entries. It uses no network, third-party package or source
corpus. There are 14 diagnostic groups and 5,963 individual assertions.
These are finite sanity checks; they are not a formal verification of the
analytic proofs or the original question.

The result file covers the hyperbolic coefficient identity, rational degree
deficits, good-time containment constants, monomial inverse-pair distances,
finite mechanical-word discrepancy controls, elementary comb membership,
and low-degree polynomial versions of the slit-rigidity constraints.

## Scope and review status

The original question includes spherical basins at infinity and every
periodic boundary point, not only repelling ones. The catalogue's broader
notation is interpreted using the primary source's attracting self-map
setting. The proof's rational finite-component criterion is expressly a
restricted case. Neutral periodic points are not silently dropped.

The completed author verification rechecked every lemma. In particular,
Corollary 5 now lists all four hypotheses of the imported good-point theorem
and verifies the global pullback component identification, density of good
times, strict containment, shrinking diameter, and basin-side condition.
The sphere and punctured-sphere domain edge cases are explicit. No claim
about an earlier Biswas manuscript version is needed.

No copied source text, PDF, dataset content, private coordination material,
or conversation link is part of this packet. Hashes identify the inspected
inputs without granting redistribution rights. The manuscript is an authored,
unrefereed research note. A fresh independent review remains a separate step.
