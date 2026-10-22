## Partial density theorem; both universal targets unresolved

This prose-only edition retains the complete substantive proof and independent
mathematical audit. For n>=5, let F(n) be the maximum of m+p(m) over composites
4<=m<n, with p(m) the least prime divisor. For every fixed real K, the integers
with F(n)-n<=K have natural density zero. Thus F(n)-n tends to infinity in
natural density. Neither eventual positivity for all sufficiently large n
nor pointwise divergence is established. A density-zero set is not proved
finite, and no global last exception is claimed.

The self-contained proof derives Var(S)<=Hv for reduced-residue counts modulo
even squarefree Q directly from CRT joint probabilities, nonnegative divisor
expansion, a triangular-sum bound, and exact Euler-product cancellation.
It neither assumes independence nor requires H<Q. Elementary product bounds
and prime density zero give the composite-witness transfer. The density limit
is taken with H and Q fixed; only afterward is H enlarged.

Also accepted are the two finite inequalities, the exact bounded-prime
obstruction at primorial multiples, endpoint/parity reductions, the correct
square-root upper bound, the exact prime-square identities
F(q^2+1)=q^2+q and G(q^2+1)=q-1, and normalized limsup 1. The primorial
obstruction is a limitation of fixed least-prime-factor cutoffs, not a
counterexample to either original universal target.

The variance estimate is classical: [Montgomery, The combinatorics of moment
calculations (2010)](https://hrj.episciences.org/168/pdf), Section 3, printed
p. 7 / PDF page 6, records the estimate and credits the exact formula to
[Hausman and Shapiro (1973)](https://doi.org/10.1002/cpa.3160260407).
The original 1973 article was not independently inspected. No novelty or
priority for the direct density corollary is claimed.

The original definition was historically checked in
[Erdős (1979), printed p. 73 / PDF page 3](https://users.renyi.hu/~p_erdos/1979-23.pdf)
and [Erdős–Graham (1980), printed p. 74 / PDF page 70](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).
[Tao's 2024 discussion](https://terrytao.wordpress.com/2024/08/19/erdos-problem-385-the-parity-problem-and-siegel-zeroes/)
is credited for contextual obstructions and a conditional semiprime route;
it is not used as an unconditional hypothesis. No current authoritative
problem-status certification or exhaustive literature review is claimed.

“Accepted” means an independent internal AI audit of this partial theorem.
The AI-assisted work is unrefereed; no external human peer review, journal
acceptance, or formal proof-assistant certification is claimed. Only an
inline-math formatting typo was corrected before the original candidate was
sealed. No mathematical correction is required.

Historical independent exact checks covered 16 even squarefree moduli,
9,264 CRT joint counts, 185 moment cases, 55,226 residue values, 33,153
triangular-sum checks, 749 product checks, 69,730 transfer cases, 560 finite
inequality cases, 280 incidence cases, 110,846 obstruction pairs, and 168
prime-square identities. Computation of F through 10^6 independently matched
the original sequence hash. It found exactly 100 zero-gap integers through
1,000,000, with largest value 267680 within that range only. Normal/-O/-OO
outputs were byte-identical. These finite checks supplement the analytic
proof and do not certify any eventual assertion.

The edition contains authored proof, audit, acceptance, public citations and
verification metadata only. Executable code, raw datasets, detailed receipts,
full computational certificates, copied PDFs/source text/images, and private
coordination material are excluded. It is not an executable reproduction
package. Preparation performed byte-integrity and publication-structure checks
without new mathematical tests or scholarly-source retrieval/inspection.
Source metadata distinguishes historical official web inspection from a
second full-file byte acquisition. The original candidate and audit are unchanged.

Exactly eight files are additions under attempts/2087. QUEUE.md and all
unrelated paths are unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,947 bytes; SHA-256 `e0e2da37c30ce4d98138b761e1baf433419eebca1889e55cb905e9ec8e33b808`.
- `ACCEPTANCE.md`: 4,335 bytes; SHA-256 `b19d7119c3439ca071f5df442da451731a2ead73cc847fdf970664dd6130b681`.
- `AUDIT.md`: 16,143 bytes; SHA-256 `1b111e3e2b6732f164b962f857add301644f0d65e96a6abe19fbdd6fd8ea638f`.
- `MANIFEST.json`: 1,686 bytes; SHA-256 `ca2c100d2198f0dfb99d4014e1654c97c4d743e2e8f647322659b6a72cf638c0`.
- `PROOF.md`: 13,148 bytes; SHA-256 `2565d2e1853263acc45c091392deba04d716d9d5d3f1caace2e97cba6f44819e`.
- `README.md`: 4,310 bytes; SHA-256 `c69dfc207aac3af8addd8e4e3f5bd8a2563e4b3f771b2b07c2ef469f6a8f7b33`.
- `SOURCES.json`: 7,377 bytes; SHA-256 `f8d618345121579ce4200ee232995a80c076136fc6f35cf942c55ec6a5e398ad`.
- `VERIFICATION.json`: 3,392 bytes; SHA-256 `6dd2898ab42682a4d8e2efee17384ce5d48b6e98b9b00a44475d4cf2f9f2ce93`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

