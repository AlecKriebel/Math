# Acceptance report: EP-385 / problem 2087

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the partial density theorem, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. Only an inline-math formatting typo was corrected before the original candidate was sealed; no mathematical correction is required. Eventual positivity and pointwise divergence remain unresolved by this work. The variance estimate is classical, recorded by Montgomery (2010) and attributed there to Hausman and Shapiro (1973); no novelty or priority of the density corollary is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

## Decision and exact scope

ACCEPT_PARTIAL: for every fixed real K, the set of integers n>=5 with F(n)-n<=K has natural density zero. Here F(n) maximizes m+p(m) over composite integers 4<=m<n, and p(m) is the least prime divisor. The nontrivial theorem is for K>=0; negative K is immediate from F(n)>=n.

The complete self-contained argument proves Var(S)<=Hv for reduced-residue counts modulo an even squarefree Q. It expands the exact CRT pair probability, bounds a nonnegative triangular sum by an integral, and cancels a finite Euler product. No independence assumption or H<Q restriction is used. Elementary product bounds and prime density zero then transfer a surviving rough integer to a composite witness, except on finitely many shifted-prime sets of density zero. H and Q remain fixed while the upper density is taken; only afterward does H tend to infinity.

Also accepted are both finite two-parameter inequalities, the exact bounded-prime obstruction at primorial multiples, endpoint and parity reductions, the upper square-root bound, the prime-square identities F(q^2+1)=q^2+q and G(q^2+1)=q-1, and normalized limsup 1. None supplies pointwise control of all sufficiently large integers.

The original independent checks used exact arithmetic and explicit failure gates. Their normal/-O/-OO outputs were byte-identical. Counts and hashes are retained in VERIFICATION.json; finite tests supplement the written proof. The check found exactly 100 zero-gap integers through 1,000,000, with largest value 267680 within that range. This is not a global last-exception claim.

## Attribution and unresolved questions

The variance estimate is classical: [Montgomery, The combinatorics of moment calculations (2010)](https://hrj.episciences.org/168/pdf), Section 3, printed p. 7 / PDF page 6, records it and credits the exact formula to [Hausman and Shapiro (1973)](https://doi.org/10.1002/cpa.3160260407). The 1973 original was not independently inspected. This edition retains a self-contained proof and makes no novelty or priority claim for the direct density corollary.

Both original universal targets remain unresolved by this work: F(n)>n for all sufficiently large n, and F(n)-n tending to infinity pointwise. A density-zero exceptional set need not be finite. No largest exceptional n is proved to exist. Primorial multiples obstruct a fixed least-prime-factor cutoff, but are not thereby counterexamples to either universal assertion. Tao's contextual semiprime route is conditional and is not used as an unconditional hypothesis.

Only a preseal inline-math formatting typo in the v_y definition was corrected. No mathematical correction is required, and no new mathematical work was performed for this edition.

## Exact edition identities

- PROOF.md: 13,148 bytes; SHA-256 2565d2e1853263acc45c091392deba04d716d9d5d3f1caace2e97cba6f44819e.
- AUDIT.md: 16,143 bytes; SHA-256 1b111e3e2b6732f164b962f857add301644f0d65e96a6abe19fbdd6fd8ea638f.

The original candidate and audit are unchanged. Tracked editorial changes clarify review and distribution status and describe omitted verification historically. All substantive mathematics and original acceptance qualifications are preserved.
