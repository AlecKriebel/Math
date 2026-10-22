# Corrections and summary guardrails

## Mandatory mathematical corrections

None found. The frozen submission was not modified.

## Optional editorial clarifications

1. When summarizing Proposition 1, retain the word **uniform**. Sharpness is over all centers for a fixed (A,B), not a claim that every center has exactly the same largest radius.
2. When summarizing Proposition 3, call R a **guaranteed domain-of-starlikeness radius**. No sharpness assertion for this spatial radius has been proved.
3. `FULL_PROOF.md` is a complete proof of the stated partial deductions, not a proof of the original full target. Its opening status already states this clearly; avoid dropping that qualifier in links or descriptions.
4. The 15-file manifest counts payload files and excludes itself. The frozen directory contains 16 files total; this is consistent with the supplied receipt and verifier.
5. Running verify.py and capturing stdout adds an extra final newline compared with CONTROL_RESULTS.json because the script prints an already newline-terminated string. The parsed JSON is identical; no correction is required.

## Claims that must remain restricted

- Keep the target status `unsolved`, turns `5/5`, and the exact missing strict singular-value inequality.
- Keep starlikeness distinct from local univalence, global univalence, and close-to-convexity.
- Boundary equality at the extremal point is not an interior failure of the closed coefficient ball.
- No finite search or floating-point evaluation is a proof, exhaustive measure search, or certified counterexample.
- The Herglotz parametrization is complete at B=-1 only; the b<1 construction is used as a subclass.
- The subdisk conclusion relies on the known theorem as recorded in Hayman–Lingham; the original 1989 proof was not independently obtained.
- Fournier 2020 full text remains unavailable in this review. No comprehensive current still-open, already-solved, or novelty certificate is justified.
- Frozen source metadata may be published with the original audit deductions, but source PDFs, corpora, extracted text, screenshots, and private response bodies must stay excluded.

The frozen `STATUS.json` intentionally retains its pre-audit value `independent_audit: pending`. The separate audit status records completion without changing the reviewed bytes.
