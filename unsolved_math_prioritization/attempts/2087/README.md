# EP-385 / problem 2087: composite overshoot in natural density

**Partial density theorem only. Eventual positivity and pointwise divergence remain unresolved by this work.**

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the partial density theorem, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. Only an inline-math formatting typo was corrected before the original candidate was sealed; no mathematical correction is required. Eventual positivity and pointwise divergence remain unresolved by this work. The variance estimate is classical, recorded by Montgomery (2010) and attributed there to Hausman and Shapiro (1973); no novelty or priority of the density corollary is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

For n>=5, let F(n) be the maximum of m+p(m) over composites 4<=m<n, where p(m) is the least prime divisor. For every fixed real K, the integers with F(n)-n<=K have natural density zero. The full CRT second-moment derivation and elementary transfer argument are included. The order of limits is essential: first take density with the interval and modulus fixed, then enlarge the interval. A density-zero exceptional set is not shown finite.

The supplementary finite inequalities, primorial bounded-prime obstruction, endpoint/parity reductions, correct square-root upper bound, and exact prime-square values are preserved. Neither a pointwise lower bound nor a global last exception is established. Historical computation found exactly 100 zero-gap integers through 1,000,000; 267680 is the largest only within that tested range.

## Files and verification

PROOF.md retains the complete substantive proof. AUDIT.md retains the independent mathematical audit and historical check results. ACCEPTANCE.md and ACCEPTANCE.json record the accepted scope and bind the edition proof/audit identities. SOURCES.json retains public citations, PDF hashes and sizes, historical retrieval/inspection records, and their limits. VERIFICATION.json contains historical check counts, hashes, and scope. MANIFEST.json lists all eight members and hashes the other seven; its own digest is independently pinned in the publication description.

The independent exact checks included 16 even squarefree moduli, 9,264 CRT joint-count cases, 185 moment cases, 55,226 residue values, 33,153 triangular-sum checks, 749 product checks, 69,730 transfer cases, 560 finite-inequality cases, 280 incidence cases, 110,846 obstruction pairs, and 168 prime-square cases. Independent F(n) computation through 10^6 matched the original sequence hash. Normal/-O/-OO outputs were byte-identical. These historical finite checks do not replace the analytic proof and were not rerun for this edition.

## Prior work and source limits

[Montgomery, The combinatorics of moment calculations (2010)](https://hrj.episciences.org/168/pdf), printed p. 7 / PDF page 6, records the classical variance estimate and credits [Hausman and Shapiro (1973)](https://doi.org/10.1002/cpa.3160260407) for the exact formula. The original 1973 paper was not independently inspected. The density corollary has no verified novelty or priority claim.

The original formulation was checked in [Erdős (1979), printed p. 73 / PDF page 3](https://users.renyi.hu/~p_erdos/1979-23.pdf) and [Erdős–Graham (1980), printed p. 74 / PDF page 70](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf). [Tao's 2024 discussion](https://terrytao.wordpress.com/2024/08/19/erdos-problem-385-the-parity-problem-and-siegel-zeroes/) supplies contextual attribution for the short-window obstruction and conditional semiprime route. No current authoritative problem-status certification or exhaustive literature review is claimed. Independent official web inspection is distinguished from a second full-file byte acquisition.
