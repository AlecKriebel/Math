# Corrections and clarifications

Author packet: `2302019-reconstruction-20261005-v1`  
Author manifest SHA-256: `6584a3d052edae771b709241b7ee909e7684efe318c0045e7ad36118f6008f12`

## Required corrections

None. The frozen mathematical statements and their limitations pass this
fresh audit without modifying the author bytes. No assumption, constant,
equality case, or convergence claim was found to require repair.

## Optional explanatory clarifications

These are nonblocking and are supplied here without changing the freeze.

1. **Type convention, PROOFS.md Section 1.** To make the source-to-definition
   bridge explicit, apply the classical vertical bound at K+epsilon using
   C_epsilon, then let epsilon decrease to zero. The resulting bound at K
   also supplies the fixed global constant needed by the source convention.
   This rules out an apparent circular reading of the current short text.

2. **Poisson quotient, PROOFS.md Sections 3-4.** A harmonic conjugate need
   not be bounded. Only the modulus of its exponential is used, and that
   modulus lies between A and B. The disk maximum argument tolerates the
   exceptional points 0 and infinity because the quotient is bounded.
   Adding these observations can help readers distinguish this argument
   from an unproved formula for log|f|.

3. **Lower-half-plane notation, PROOFS.md Section 4.** For an explicit
   whole-plane formula, set theta=Arg(x+i|y|) in U_step and replace y by
   |y| in D and d. When A>B, use reflection and exchange the caps. The
   existing reflection/conjugation instructions already imply this.

## Limitations that must remain attached

- The nonreal sharp-bound target is not solved by this reconstruction.
- No claimed identification with the exact subharmonic predecessor is made.
- Eremenko's credited extremal result concerns real-axis evaluation.
- The finite arithmetic and floating checks do not establish the theorems.
- Neither author nor audit quadrature is certified by error bounds.
- The 1988 conformal-map formulas were not independently reconstructed;
  OCR, PDF-byte, image, and translation limits remain disclosed.
- No exhaustive 2026 open-status or novelty finding is made.
- A future substantive edit requires a new freeze and review of that edit;
  this acceptance is bound to the digest above.
