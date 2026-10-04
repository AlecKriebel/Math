# Publication note: unsolved attempt with checked partial results

Target 4700001 / AMR-046-0001, *Low degree rigid systems*. Status: **unsolved** after five approaches. The global maximum-of-two question remains unresolved by this work.

The eight original authored files are preserved byte for byte under `frozen/`. The complete thirteen-file independent audit is preserved byte for byte under `audit/`, including its manifest and external manifest hash. `FREEZE_MANIFEST.json` binds the original packet. No historical artifact was silently corrected.

The independent audit passed the stated partial mathematics and unsolved conclusion. Its full recurrence checks, exact subclass checks, and independent integration controls comprise 50 successful checks. It found no material mathematical correction. It did identify a minor robustness issue in the original numerical script: refinement comparison uses `zip` without first asserting matching root counts. In the frozen numerical results, the original replay, and the independent audit, each original and refined list has exactly two roots for all three epsilon controls (0.12, 0.10, 0.07). The independent checker explicitly checks `len(refined_roots) == len(bracketed_roots) == 2`. The original script remains unchanged; the issue and the audit check are retained in `audit/CORRECTIONS.md`.

All numerical residuals and stability observations here are floating-point corroboration, not interval/error-enclosure certificates. The analytic two-cycle theorem holds for sufficiently small positive epsilon but gives no certified numerical cutoff for those three concrete epsilon values. The bounded 24-parameter scan, including 227 incomplete sampled flows, cannot exclude missed, tangent, large-radius, or near-return-boundary cycles and is not a global exclusion argument.

## Reproduce

First run the strict file verifier from any working directory:

    python /path/to/attempts/4700001/verify_release.py /path/to/attempts/4700001

Then replay the unchanged original scripts and independent audit, writing outside this packet:

    python /path/to/attempts/4700001/audit/run_audit.py --packet /path/to/attempts/4700001/frozen --output /path/to/new-replay-output

Dependencies are Python 3, NumPy, SciPy, and SymPy. The audit uses no network. `PUBLICATION_MANIFEST.json` hashes every other file in this exact publication layout. The verifier rejects missing, additional, duplicate, traversal, symlink, size-mismatched, and hash-mismatched entries/files. Its output is integrity validation, not a mathematical proof certificate.

Only authored mathematics, code, computed outputs, audit records, and public verification metadata are included. Source PDFs, extracted source text, dataset contents, and private coordination inventories are excluded. No novelty or full resolution is claimed.
