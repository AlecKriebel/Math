# Hall coefficient-sign question: accepted partial results

Record 2307034 / AMR-022-7034, R. Hall's Problem 7.34 in Hayman and Lingham's [Research Problems in Function Theory (New Edition), arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed page 170 / PDF page 171.

**UNRESOLVED; approach 1 of 5.** The accepted results concern the real/half-plane, at-most-two-parameter, and rational-exponent subcases. The unrestricted complex-parameter problem with arbitrary positive irrational exponents remains unresolved by this work. No novelty or exhaustive current-literature claim is made.

## Accepted results

For positive real exponents beta_j, set B=sum beta_j and use the local product f(z)=product (1-zeta_j z)^(beta_j), normalized by f(0)=1, with real Taylor coefficients a_k.

- Some a_k is nonpositive by index ceil(B)+n if all parameters are real, or if every nonreal parameter is in the closed left half-plane. Positive real, repeated, and zero parameters are allowed.
- The same bound holds for every admissible complex configuration when n<=2. For the exponent tuple (3/5,3/5), the sharp universal bound is N=4.
- For rational exponents and any common positive denominator q, the uniform bound is N<=qB+1.
- An exact two-real-parameter example refutes the proposed bound 1+sum ceil(beta_j).
- An exact four-complex-parameter example, all exponents 21/10, has a_1,...,a_13>0 and a_14<0. It refutes the proposed unrestricted bound ceil(B)+n=13. It proves only the lower bound 14 for that exponent tuple; the established rational upper bound is 85. Sharpness at 14 is not claimed.

The conclusion is nonpositive, not necessarily negative. These counterexamples refute proposed bounds, not Hall's existence statement.

## Reading guide

- [PROOF.md](PROOF.md): complete derivations, both exact examples, full 14-entry rational table, and the unresolved compactness/degree-drop discussion.
- [AUDIT.md](AUDIT.md): full mathematical independent review, with the exact coefficient table and all qualifications.
- [ACCEPTANCE.json](ACCEPTANCE.json): scoped acceptance, original identities, edition identities, and the distinction between them.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): primary citation, public PDF identity, inspection history, and literature limits.
- [PROVENANCE.md](PROVENANCE.md): precise editorial scope and the Section 8 clarification.
- [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): unresolved status, accounting, and the complete edition manifest.

Section 8 now distinguishes a positive real denominator zero/logarithmic-derivative pole from a branch singularity, which requires a nonintegral merged exponent. No theorem is altered. The mathematical work and review are AI-assisted and unrefereed; no formal proof-assistant certification or human peer-review acceptance is asserted.
