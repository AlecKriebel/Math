# Sharp triangle modular threshold: credited coverage

Problem 30001248 / OWR-3473-009.

Review and distribution status: AI-assisted and unrefereed. Acceptance means an
internal AI mathematical audit, not external human peer review or formal
proof-assistant certification. This is a prose edition, not a computational
reproduction package. No new LLT, first-resolution, or priority claim is made.

## Exact result and prior credit

For fixed p in (0,1), let T count ordinary unlabeled triangles in G(n,p).
For every sequence of positive integers q_n,

    max_a |q_n P(T = a mod q_n) - 1| -> 0  iff  q_n = o(n^2).

This is a credited consequence of Sah–Sawhney's quantitative LLT,
arXiv:2006.11369v1, Theorem 1.1. Scott–Tateno's 2009 contribution had
already stated a triangle LLT and modular uniformity for q=o(n^2/log n).
The present reduction uses concentration and finite central-window summation
for sufficiency and an independently derived CLT/Fourier obstruction for
necessity. It makes no new LLT or bibliographic-priority claim.

The exact variance is binom(n,3)p^3(1-p^3)+12binom(n,4)p^5(1-p),
asymptotic to p^5(1-p)n^4/2. Sigma is its square root. The count has span
one; labeled embeddings instead give 6T. All modulus edge cases are covered,
including q=1, bounded or composite q, oscillating sequences and moduli
arbitrarily slowly below, at, or above the standard-deviation scale.

## Complete reports and overlap

PROOF.md retains the full corrected coverage proof. AUDIT.md combines the
full independent derivation and the full cross-audit. The n>=3 concentration
boundary, explicit L1 assumption, true sigma, Gaussian-cell comparison,
concentration/window argument and varying-frequency justification all remain.

The complete reconstruction of Sah–Sawhney's ordinary-unlabeled 2K2 Gaussian
LLT obstruction is also retained. Its atom bound is of order n^(-5/2), while
its standard deviation is of order n^3. This overlaps the adjacent general
subgraph problem 30001249 / OWR-3473-010 and is not counted as a separate
discovery. No complete classification of disconnected modular ranges is claimed.

The essential source theorem was historically inspected in the required
count and standard-deviation conventions. Its deep Fourier/decoupling proof
is imported, not fully reconstructed. The independent audit checks the core
triangle and 2K2 mathematics, not every peripheral literature-table assertion.
Berkowitz normalization defects are limited to the identified displays in
the recorded PDF, without extrapolating to every version.

## Recovery and distribution limits

Recovery scope: all three complete authored mathematical reports were recovered
byte-for-byte and match the previously recorded SHA-256 hashes. The earlier
full evidence packages and their external seals are unavailable in this edition.
Statements below about earlier source inspection and finite checks describe
historical work recorded in those exact reports; they are not claims that the
old supporting packages were recovered or that the checks were newly rerun.

Only the eight authored prose/metadata files in MANIFEST.json are public.
No copied source documents, dataset contents, code, raw enumeration outputs,
private sources or private coordination material are distributed. Exact report
hashes establish byte identity, not truth, novelty or formal verification.
ACCEPTANCE.json binds the original and edited reports; SOURCES.json records
historical source metadata and its limits; VERIFICATION.json separates fresh
recovery checks from unavailable earlier evidence packages.
