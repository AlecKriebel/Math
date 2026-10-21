# Rubel’s bounded-derivative metric: the simply connected component

This is an AI-assisted, unrefereed mathematical draft. Acceptance records one independent internal AI mathematical reconstruction of an identified prior theorem, with explicit local proof repairs. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, sharp-constant, or worldwide-current-openness claim is made.

## Accepted prior theorem with corrected proof

For every nonempty simply connected domain Omega in the complex plane and every p,q in Omega,

    c_0 d_Omega(p,q) <= rho_Omega(p,q) <= d_Omega(p,q),
    c_0 = exp(-8 exp(9/2)/(3 sqrt(2 pi)))/2 > 0.

Here d_Omega is intrinsic Euclidean path distance, and rho_Omega is the supremum of |f(q)-f(p)| over all holomorphic f on Omega with |f'| <= 1 everywhere. The functions themselves need not be bounded. Equal points and the whole plane are included. Proper unbounded domains, infinite inner diameter and arbitrary boundary irregularity are allowed. The constant is exact and independent of the domain and points; its approximate size is 1.28538 × 10^-42.

Credit: Cameron MacMahon, [On Simply Connected Domains Supporting an Unbounded Analytic Function with Bounded Derivative, arXiv:2609.20607v1](https://arxiv.org/abs/2609.20607v1), Theorem 1.2. The source’s printed proof has four local calculation defects. Correcting its Taylor sign, the interval remainder bound, the Gaussian factor of two and the complex-kernel imaginary-part equality leaves the source’s exact constant unchanged. The complete repairs and all missing analytic justifications are retained.

This does not solve the original arbitrary-domain qualitative question of L. A. Rubel, [Hayman–Lingham Problem 7.27](https://arxiv.org/abs/1809.07200v2), PDF page 169 / printed page 168. No universal lower comparison for arbitrary multiply connected domains, exact formula, equality characterization, or optimal constant is claimed.

## Complete contents

- [PROOF.md](PROOF.md): the complete corrected proof, all four local repairs, explicit strip normalization, logarithm and Gaussian bounds, coefficient-area appendix, all domain edge cases and the bounded Theorem 1.1 corollary.
- [AUDIT.md](AUDIT.md): editorial logical checkpoints and acceptance limits for that single reconstruction.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): exact accepted claims and excluded claims.
- [SOURCES.json](SOURCES.json): public bibliography, PDF hashes and sizes, and bounded retrieval/inspection history.
- [VERIFICATION.json](VERIFICATION.json): integrity and finite-check boundaries.
- [MANIFEST.json](MANIFEST.json): all eight filenames and hashes of the other seven. The manifest’s own digest is pinned separately in the proposed draft-PR body.

The additional consequence is only the existence of an unbounded holomorphic function with bounded derivative if and only if the simply connected domain has infinite inner diameter. The uniform-boundedness argument passes to a subsequence where needed. No Theorem 1.3 or 1.4, simultaneous higher-derivative growth, or Rubel(k) assertion is accepted.

Source documents, copied source text or images, datasets, executable code, raw test outputs and private coordination material are excluded. Source inspection and displayed manuscript status are historical observations recorded on 11 October 2026, not claims of journal acceptance or exhaustive current literature coverage.
