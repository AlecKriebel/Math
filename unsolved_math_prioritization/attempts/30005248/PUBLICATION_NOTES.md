# Publication and clarity notes

Problem 30005248 / OWR-11695855-001. Prepared 3 October 2026, 15:04 UTC.

The ten files under `public/` are preserved byte-for-byte from the frozen author package. The five allowlisted files under `audit/` record a fresh independent AI adversarial audit. The audit accepts the stated partial results; it is not human peer review, a novelty certificate, or a proof of the broad classification. The original problem remains **unsolved, 5/5**.

Completion estimate: the five-approach research deliverable and its scoped audit are complete (100%); no full-resolution claim is made. These additive notes clarify conventions without modifying the audited arguments.

## Sample and grid conventions

- Every fixed-size observation count n or m is a positive integer. The source formula containing log n is used only in its stated large-alphabet regime, with n>1.
- In Attempt 4, assume M>0 and K>=1 is an integer, so delta=M/K>0. For M=0, the functional is constant and no samples or logarithmic amplification expression is needed.
- With k odd, k>=1, and k>=18 log K, the grid estimator uses kn observations and has the stated absolute-error bound 3delta. No independence between different threshold tests is required.
- In Attempt 5, the necessary and sufficient integer sample budgets satisfy

  (nu+delta)/(18delta^2) <= n_min <= ceil(8 log(3)(nu+delta)/delta^2),

  under 0<=nu<nu+delta<=1/2.

## Feasibility of a critical gap

For a fixed n and 0<=nu<1/2, define the restricted critical gap as the infimum over successful delta in (0,1/2-nu], requiring both composite testing errors to be at most 1/3. If this set is empty, its infimum is **+infinity**. Thus sqrt(nu/n)+1/n describes the scale where admissible successful endpoints exist; it does not override the truncation at 1/2. For example, n=1 and nu=.49 admits no successful delta<=.01.

## Safe verification

The author's `public/verify_exact.py` writes `verification.json` beside itself. Run a temporary copy when preserving the frozen artifact hashes. The independent audit runner already creates such a temporary copy and checks input hashes before and afterward.

From this directory, use:

    python audit/audit_controls.py --bundle public --output /tmp/local-complexity-audit.json

The recorded results contain 16,459 author assertions, 20,738 independent assertions, and seven rejected negative controls. These are finite algebraic and probability checks, not proofs of all asymptotic literature or evidence of a complete classification.
