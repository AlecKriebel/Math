# Independent CN and connected-invariant audit

Timestamp: 2026-10-24 19:35 UTC. Assigned audit: **100% complete**.
This is not a completion estimate for Kourovka 21.130.

**Verdict:** no substantive flaw found in `RESULTS.md`. Its claims are
partial certificates and exact reformulations, as labeled.

* Independently verified `C_n=(-1)^(n(n-1)/2) kappa_n` by comparing
  permutation-exponent coefficients in `Alt(V(s))=kappa_n V(x)`.
  The exact integer ratio at `(0,1,...,n-1)` is valid; it must be computed
  before reduction modulo the characteristic.
* Independently verified the reflection sign `(-1)^(n-1)`, hence integer
  vanishing for every even `n`, including reduction to characteristic two.
* Independently verified the grid coefficient lemma and its implication
  for all elementary abelian `p`-groups when `p` does not divide `C_n`.
  Actual interpolation denominators remain nonzero when `p<n`.
* Reproduced every alternating-sum value through `n=9`. Ran independent
  direct factor expansion for `n=1,2,6,7`, obtaining `1,0,0,2292864`.
  Together with the existing direct checks, the values through `n=7`
  have independent expansion checks. No direct `n=9` check was attempted.
* Verified the exterior rotation and reversal cancellations in section 4.
* Verified section 5: squarefree color determinant terms may still encode
  disconnected cycle covers; full squarefree vertex extraction from
  `tr(B^n)` forces a Hamiltonian cycle. For `n>2`, each unoriented cycle
  contributes exactly `2n` copies. Over the stated commuting `Q`-algebra,
  color nilpotence removes repetitions and positivity prevents cancellation.
  The precise log identity is `[t^n](-log det(I-tB))=tr(B^n)/n`.

The exact gaps remain those stated: no general odd-`n` nonvanishing proof,
no certificate in the exceptional characteristics or even sizes, and no
automatic extension to non-elementary groups. Nilpotent or Grassmann
rewritings alone do not close these gaps. Ordinary odd Grassmann generators
cannot replace commuting variables without changing the identities; general
ring interpolation requires unit pairwise differences.

Detailed derivations and cautions are in `ADVERSARIAL_VERIFICATION.md`.
No Git or external communication actions were taken.
