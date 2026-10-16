# Tangent-bundle Seshadri characterization: expanded candidate v2

Problem 30004324 / OWR-17296-007. Prepared 2026-10-05.

**Status: candidate_complete.** Two independent AI geometry audits of the original candidate reported PASS with no essential gap. This expanded derivative awaits an independent final delta audit. It is not externally peer-reviewed, a historical-priority certification, or an accepted resolution.

`candidate_proof.md` gives the full argument for a smooth integral projective variety over an algebraically closed field of arbitrary characteristic, with positive tangent-bundle Seshadri constant at one arbitrary closed point. An absolute pointed degree minimum removes all stable-map boundary; a very free normalization gives surjective proper evaluation; the contracted marking section forces numerical Picard number one; the anticanonical divisor becomes ample, and the established Fano theorem applies.

The revision explicitly supplies four details requested by both reviews:

1. Minimal degree remains minimal over geometric field extensions.
2. The actual inertia-free evaluation fiber is finite over the full projective coarse scheme; no arbitrary closed coarse-space base-change claim is made.
3. The marking supplies a relative degree-one line bundle, so the universal curve is projective.
4. A closed point of the generic evaluation fiber supplies the numerical multisection, including inseparable degree.

## Readiness and integrity history

The original freeze remains unchanged. Its original verifier received **REVISE_REQUIRED (integrity tooling only)**: it ignored extra nested files named MANIFEST.json. The actual original archive had no such extra file and passed strict inventory checks. Both geometry verdicts were PASS.

The v2 root `verify_manifest.py` is the authoritative strict replacement, copied byte-for-byte from the first independent audit. The vulnerable code is retained only as `historical/v1_verify_manifest.py`, explicitly for the regression demonstration. Do not use it to validate this package.

The complete original audit reports and source-verification metadata are preserved under `review/`. Their verdicts bind the original proof, not a yet-unperformed v2 delta audit. `REVIEW_HISTORY.md` and `status.json` distinguish these stages.

## Reproduce

Python 3 standard library only. Run the complete portable replay:

    python3 replay.py

Or run the component checks:

    python3 checks.py
    python3 verify_manifest.py
    python3 test_integrity.py
    python3 test_nested_manifest_regression.py

Optionally bind the root manifest externally:

    python3 verify_manifest.py . EXPECTED_MANIFEST_SHA256

The original 909,136 finite mathematical controls are unchanged. The strict verifier's fixture suite accepts a clean packet and rejects 14 mutations. The dedicated regression demonstrates historical v1 acceptance of a nested manifest and v2 rejection. These programs do not prove the geometry.

No source PDFs, source extracts, page images, raw catalog data, private sources, or private coordination records are included. No remote write or publication is performed by this revision. No additional substantive approach was used: the count remains two, with a five-approach budget. A queue label `claimed_solved, 2/5` is proposed only after the final delta audit; no queue is changed here.
