# PR #9 adversarial mathematical review

## 2026-09-29T21:23:43-07:00 — checkpoint 1

Review target: validate the exposed-point irreducibility theorem, generic purely nonlinear equality, source scope, edge cases, and reproducible evidence at PR head `a29887ed0e341851d02fa992c26500d4089267be`. A result passes only if every general proof step is supported and the stated source target is covered. Numeric checks are corroboration, not a proof.

Snapshot archived without switching from main. Existing unrelated working-tree changes are left untouched. Approach families will independently audit analytic/convex structure, generic-position approximation, and exact algebra/source correspondence.

Estimated review completion: **10%**. No conclusion yet.

## 2026-09-29T21:29:30-07:00 — checkpoint 2

Independent preliminary analytic/convex and generic-face audits identify no proof defect. Root verified the exact OWR exposed-point formulation and obtained matching hashes for both published primary PDFs. Candidate, reviewed candidate, and proof PDF hashes agree with their records; mathematical Sections 2–6 are unchanged from the prior review. Three approach-family reviews remain active, including exact-algebra reproduction.

Potential nonmathematical finding under investigation: the PR edits generated QUEUE.md without changing state.json or the maintained turn history, so rank regeneration may silently lose the claimed result and consumed turn. No queue files have been modified by this review.

Estimated review completion: **55%**. This estimates task progress, not correctness probability. Primary downloaded PDFs/text and render scratch files remain locally available and excluded from publication; their provenance manifest is retained.

## 2026-09-29T21:43:09-07:00 — checkpoint 3

All three independent mathematical audits pass: the exact convex/analytic Theorem 1, generic face Theorem 4 and real generic scope, and exact algebra/reproduction. The source script rerun matches the recorded JSON under SymPy 1.14.0; 154 math blocks agree between Markdown and LaTeX. Root inspected all five proof PDF pages and the complete original source pages for definitions, conventions, and conjectures.

Correction to checkpoint 2: actual isolated regeneration does lose the manually recorded status/turn, but the base repository log explicitly documents manual queue maintenance because the older generator is incompatible. The adversarial follow-up therefore refutes classification as a new PR-specific P2 issue. The provisional finding is withdrawn, with reproduction and counterevidence retained. This is an inherited conditional repository risk and has no effect on mathematical correctness.

The full review has been saved and sent for a final synthesis check. Reviewed PR head remains a29887ed0e341851d02fa992c26500d4089267be. The earlier immutable-snapshot checkpoint was published on main as 60292bed09f59236aa192cb17aa138f7b4750e1a.

Estimated review completion: **95%**. Remaining: synthesis verification, final links/provenance checks, and publication of the finished review. Historical priority remains unresolved and is not part of this progress estimate.

## 2026-09-29T21:45:59-07:00 — final review checkpoint

Final synthesis verification passed without correction. Both complete mathematical theorems and the claimed generic source scope remain accepted. The final queue challenge additionally established that the base already had fourteen manual active/claimed/published rows, the original catalog was already queued/zero/eligible, and the PR preserves a committed local turn ledger. The prior broader phrase implying absence of any durable history is rejected; there is no new P2 finding and no demonstrated live data loss. Reproduction output and final report now state these limits explicitly.

All sixteen archived artifact hashes were revalidated, local report links resolve, and exact original check output remains identical to the rerun. Final reports, independent checks, source provenance, and verdict are ready for publication on main. Downloaded third-party source PDFs and scratch/environment files are excluded. Existing unrelated working-tree changes were preserved. No mathematical edit to the PR or shared queue was made; no approval, merge, release, DOI, or external outreach was initiated.

Estimated review completion: **100% of the requested adversarial audit**. Strongest verified result: the complete stated E-irreducibility theorem and generic S=E theorem. Exact remaining mathematical gap: none identified. Historical priority and human peer review remain unestablished and are separate from review completion.
