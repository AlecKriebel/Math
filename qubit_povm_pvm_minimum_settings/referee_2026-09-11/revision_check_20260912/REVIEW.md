# Referee assessment of the author's response

Revision reviewed: `53b1570d6424d5d24cabdbdfa3144e318202ba5a`.
Date: 12 September 2026 UTC / 11 September 2026 Pacific.

**Disposition: accept the response to R1–R3. The main equality certification remains valid.** This is a bounded revision review, not a new full-paper referee audit or a newly executed 675-theorem build.

## R1 is resolved

The revised strict residual definition explicitly keeps signature `(1,3)` as a separate hypothesis and restricts the pairwise-positivity/common-cone equivalence to that hypothesis. Orienting the cone to contain `u` is consistent: `u` is the sum of the first two null rays, whose positive pairing makes that sum timelike in their common cone. The scalar inequalities are no longer claimed to imply signature. The only mathematical TeX change is this correction; the main theorem and proof sources are unchanged. The independent [mathematical re-review](math_review.md) checks the correction and downstream uses.

## R2 is resolved as a scope clarification

The coverage document now explicitly lists the auxiliary statements that are specialized, replaced or absent, in agreement with the referee coverage matrix. This resolves the overbroad interpretation of certification; it does **not** supply the missing auxiliary Lean formalizations. The conclusion remains: the principal equality, finite simulation, separation, minimum-setting classification and strengthened attained value are certified, while every mathematical statement in the paper is not.

## R3 is adequately addressed

The certificate now links to its fixed original successful run, distinguishing those receipts from mutable top-level convenience copies. I independently compared current files against both that original run and my fresh referee run: all **88 protected inputs match each snapshot**. I also checked all **123 original command-log hashes**, all **178 original referee artifact hashes**, the **7 recorded current-artifact hashes**, and the **5 response-log hashes**. The received referee report is byte-identical to the original.

The refreshed submission archive contains `main.tex` and `appendices.tex` byte-identical to the corrected working manuscript. The historical proof evidence remains intact. The response accurately says it did not repeat the full 675-theorem audit; unchanged protected inputs preserve the applicability of the prior full verification under the same compiler/cache trust assumptions.

My revision check does not independently repeat PDF rendering, visual inspection or all artifact computations. Their recorded logs and output hashes were verified as evidence; those checks should not be described as newly rerun by this reviewer.

## Minor verifier distinction

The author's `verify_evidence.py` rehashes the protected proof inputs and original command logs, then **regenerates** `evidence/verification.json` with current artifact/log hashes. It does not compare those artifact hashes against the previously saved JSON before rewriting it. This does not invalidate the current response: my independent read-only [verify.py](verify.py) compares the already-recorded hashes to the current files and passes. Use that read-only checker when the purpose is detecting changes to recorded response artifacts, rather than refreshing their receipt.

See [evidence.json](evidence.json) for this review's exact checks. No production manuscript, proof, certificate, or author-response files were changed during this re-review. No further substantive correction is requested for the response to the original referee findings.
