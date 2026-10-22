# Publication scope addendum

2026-10-04. Disposition: **unsolved, 5/5**.

The frozen author packet in `submission/` and the complete separate audit in
`audit/` are preserved byte-for-byte. The audit accepted the partial results
with no mandatory mathematical correction. These clarifications govern reuse:

1. `chart_count` is an **affine** routine. For B+zG it does not inspect the
   projective infinity point G. A full-pencil caller must check that point once
   when det G=0 and add its rank/chart contribution. The audit supplies and
   tests such a wrapper; the function name alone is not an API guarantee.
2. The executable exact-arithmetic routines assume **rational coefficients**.
   The sign theorem works over real coefficients, but Q[z]/(r) and this rational
   implementation are not an interface for arbitrary real or floating input.
   An independent pencil and a rank-seven design are caller preconditions.
3. Four zero Bougnoux quartics, or any zero sign query, are **unclassified** by
   that chart. Zero positive-chart count does not mean camera impossibility
   when unclassified roots remain. The explicit critical example admits a
   positive common-focal continuum; a separate zero-quartic example does not.
4. The equal-determinant/opposite-sign construction disproves a determinant-
   only decision rule for the supplied pencils. It is not a complete solution
   of real-camera feasibility, cheirality, or the broad primary AIM question.
5. Positive calibration of a matrix, cheirality of all its proposed matches,
   noisy estimation, pre-candidate analysis and post-candidate RFC are distinct
   requirements. No practical speedup, full primary-question resolution or
   new-discovery claim is made.

The author verifier reports 240 exact assertions. The separate audit reports
676 additional assertions, including author-byte binding and replay checks.
Both outputs reproduce byte-for-byte in this final directory layout. This
separate AI-assisted audit is not peer review.

## Reproduce

From this directory, using Python 3 and SymPy 1.14.0:

- `python submission/verify.py` reproduces submission/CONTROL_RESULTS.json
- `python audit/audit_verify.py` reproduces audit/AUDIT_RESULTS.json
- `python submission/verify_manifest.py` checks the frozen author file set
- `python audit/verify_audit_manifest.py` binds and checks both frozen packets
- `python verify_publication.py` checks the complete publication file set

The publication includes no source PDFs, source full text, dataset contents,
credentials or private coordination inventory. The proposed queue change is
limited to this target's Status, Turns and its previously blank Findings cell.
Historical source-gate and status files remain unchanged as historical records;
the current audit disposition and publication clarifications are given here.
