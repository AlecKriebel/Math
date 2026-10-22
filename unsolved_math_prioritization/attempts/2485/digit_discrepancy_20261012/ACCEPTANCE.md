# Acceptance and exact mathematical scope

12 October 2026. Verdict: accepted after complete independent AI mathematical review of corrected v2. This is not external human peer review, formal proof-assistant certification, journal acceptance, or a novelty determination.

## Accepted conclusions

For the actual strict-domain minimum

\[
g(k)=\min\{n>k+1:p\nmid\tbinom nk\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k),
\]

and with the prime number theorem as a standard input, the complete proof establishes

\[
\limsup_{k\to\infty}\frac{\log g(k)}k\le\frac67,
\qquad g(k)<\exp(0.86k)<L_k\quad\text{for every sufficiently large integer }k.
\]

The proof retains every relevant local digit restriction and its exact prime-event density. Disjoint mixed-modulus digit cylinders reduce the joint CRT endpoint-error budget, producing a genuine finite initial-interval survivor. No effective numerical onset is supplied.

The review also accepts:

1. The exact mixed-modulus finite CRT/Bonferroni lower bound and strict survivor choice of T.
2. Exact local minimality of the unsigned mod-p/mod-p² cylinder count in the specified cover model.
3. The Taylor remainder sandwich (r/s)e_r(w) <= rho-Q <= e_r(w), for even 2<=r<=s, with the separate r>s exact-polynomial case.
4. The sharp asymptotic threshold kappa for the homogeneous one-third comparison, where 4/5<kappa<5/6.
5. Under the separate hypothesis that all but o(k/log k) primes in (3k/5,3k/4] are omitted, the absolute-error budgets satisfy liminf log(E_split)/k >= 3kappa/20 > 3/25 and liminf log(E_full)/k >= 3kappa/10 > 6/25 whenever the exact odd Bonferroni coefficient is positive.

The last conclusion concerns the explicit unsigned absolute-error certificate TQ-E>0. It is not a lower bound on actual discrepancy, the true first surviving multiplier, g(k), or arbitrary sieve methods. It does not prove subexponential growth impossible. The fixed 3/4-cutoff construction establishing the principal bound does not satisfy that separate omitted-block hypothesis.

## Corrections and complete reasoning

The independent review read the complete corrected proof and confirmed two prose-precision corrections: the full p²-residue representation can require order p² classes but need not do so near p=k; and Q=rho is asserted specifically for r>s, not throughout N<r<=s. No theorem, parameter, bound or proof calculation changed. The exact authored mathematical correction account and complete substantive audit are included.

The proof is distributed byte-identically to the accepted mathematical version. The review and correction history preserve all substantive mathematical reasoning, hypotheses, calculations, exceptions, aggregate diagnostic counts and inspection limits. Editorial changes concern publication metadata and supporting-record references only. All eight theorem sections and all six core audit reasoning sections are present in full.

## Limits and preceding results

No effective onset, all-k strict lcm comparison, subexponential bound, actual successive-ratio conjecture, global optimality, novelty, priority or best-known status is established. The full problem remains unsolved. The earlier 813/875 theorem and its accepted edition remain unchanged; the current 6/7 theorem is a separate stronger continuation.

The classical lcm construction and Brun/Bonferroni input are credited in the proof and source scope. Public-source checks are bounded. Finite diagnostics support arithmetic consistency but do not establish the asymptotic theorem or an effective onset. This is a prose edition, not an executable replay package.

## Distributed text identities

- DIGIT_DISCREPANCY_THEOREM_v2.md: 19,937 bytes; SHA-256 `7fee98a70c5990d1dcc1f0e034adab4ad18e689770d060d2a2d75920ee2e09bd`.
- INDEPENDENT_PROOF_REVIEW.md: 16,919 bytes; SHA-256 `faa69651f67bb19c66e2f4b7e9e3b56d894cd155c3335a247a12077ef32b7269`.
- CORRECTION_HISTORY.md: 1,052 bytes; SHA-256 `877b425e9adae1f7e842952f1bdf7eb6d3aae5693b2117c9f4b93559d28196e9`.

Every identity above refers to an actual distributed member. The public manifest inventories only members of this appendix.
