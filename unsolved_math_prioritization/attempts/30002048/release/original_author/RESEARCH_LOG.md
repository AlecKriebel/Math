# Research log

All timestamps UTC on 2026-10-04. Percentages estimate progress toward the full all-degree discovery, not confidence or elapsed task completion. They are deliberately conservative.

- 13:05–13:08: Checked exact catalogue identity, the primary report's web-rendered statement, and Stewart's papers. Corrected author attribution. Established the nonzero hypothesis and the distinction between exact algebraic degree, monic polynomial degree, and bounded coefficient tables. Full-target estimate: 0%.
- 13:08–13:09: Route 1 established the exact root-of-unity prefix formula and strict degree bound. Route 2 established finite-field order obstructions and isolated the nonunit and unbounded-height loopholes. Full-target estimate: 3%.
- 13:09–13:12: Route 3 reduced low-degree targets to 576 rational CRT tuples, then 24 integral residues. Derived exact degrees 7, 8, and 9, with exhaustive one-variable quartics for degree nine. Full-target estimate: 8%; no extrapolation from finite degrees.
- 13:12–13:14: Built an exact standard-library verifier with rational Gaussian elimination, Bareiss determinants, exhaustive rational-root tests, and modular Frobenius irreducibility certificates. Independently compared exploratory SymPy computations. Route 5 tested degree amplification by substitution and proved its exact resultant identity. Full-target estimate: 8%.
- 13:14–13:17: Route 4 checked the archimedean growth route and identified the missing uniform near-unit-circle product estimate. Wrote the scoped proof and explicit gaps. Full-target estimate: 8%; mathematically substantial partials, no full resolution.
- 13:19: Finalized author packet for fresh independent adversarial review. All-degree status remains unsolved. No merge, release, DOI, or external outreach is part of this work.

- 13:19: The second implementation passed 116 exact symbolic quartic/resultant checks and 225 root-of-unity resultant controls (orders 2–80). A signed-resultant cross-check discrepancy was traced to argument ordering; the second implementation now explicitly applies the mathematical swap sign. Unit decisions and all asserted bounds were unchanged. Full-target estimate: 8%.
