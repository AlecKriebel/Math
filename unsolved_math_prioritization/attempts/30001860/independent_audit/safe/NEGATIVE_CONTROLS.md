# Adversarial negative controls

These controls establish sensitivity to specific mistakes. They are not asymptotic proofs.

- Strict versus closed upper endpoint: GL_3(3) changes from 5,265/11,232 = 15/32 to 6,318/11,232 = 9/16 when fixed dimension 2 is incorrectly allowed. Both direct matrix counting and independent partition enumeration detect this.
- Maximum 2-adic layer versus ordinary order parity: GL_2(5) has the correct value 5/16. Collapsing every positive valuation to one color gives the wrong value 3/16. A full order-four stratum cannot be discarded.
- Even-orthogonal sign constraint: at rank 2 and q=3, the exact signed model gives SO^+_4 proportion 9/32, SO^-_4 proportion 3/8, and unconditioned Sp_4 proportion 21/64. Neither conditioned value equals the unconditioned one; their average does. The proof correctly uses an upper factor 2 rather than equality.
- Unitary arithmetic: U_3(3) has torus-model probability 51/128, while GL_3(3) has 15/32. Forgetting the q+1 versus q-1 swap for odd cycles is detected.
- Rank threshold: all independently enumerated SL_2(q) controls, q=3,5,7, have proportion zero, while the corresponding GL_2 proportions are positive. This rejects applying the positive LNP lower bound to Lie rank 1.
- Arbitrary projective lift: diag(1,-1,-1) and its negative in GL_3(3) lie in the same central coset but have fixed dimensions 1 and 2. Exactly one meets the half-open target.
- Deleting the avoidance exponential: without the high-layer factor exp(-log(n/h)/(c h)), the dyadic reciprocal sum over h=2,4,...,2^1000 is 1-2^-1000. It exceeds 32/log(2^1000)+2/sqrt(2^1000). Thus the crucial decay conclusion cannot be obtained by keeping only the bare 1/h marking factor. The actual proof retains the exponential.

Not a claimed counterexample: the fixed-index factors q-1 and q+1 are unbounded as q varies. This shows why the displayed argument does not establish a q-uniform SL/SU result; it does not prove that such a stronger theorem is false.

The fixed-field/rank-growth distinction is also supported by the exact GL_2 formula: the odd prime-power sequences q=3^(2k+1) and q=3^(2^k) yield limits 1/4 and 1/3 at natural dimension 2. This does not contradict the rank-growth theorem.
