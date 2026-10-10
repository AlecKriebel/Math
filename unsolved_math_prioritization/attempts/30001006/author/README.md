# Ricci-flow cones: linked prior work and a PDE realization bridge

Problem 30001006 / OWR-2045-003, rank 817.

**Status: UNSOLVED HERE. One new substantive approach; independent audit pending.**

The algebraic cone is exactly the rank-815 cone after c=2n(n-1)/d^2, and its five ODE approaches are not repeated. The 2008 primary text has an additional literal PDE-necessity issue. The new authored proof uses conformal covariance, analytic local realization, and a quantitative radial gluing argument to claim that ODE preservation and Ricci-flow preservation are equivalent for these closed scalar/Weyl cones.

If accepted, this closes the PDE-to-ODE logical gap for this family. It does not prove the remaining global Weyl-cubic inequality or the proposed threshold n0=12.

Read OVERLAP_AND_SOURCES.md, then APPROACH_1_PDE_REALIZATION.md. PUBLIC_METADATA.json identifies the complete-record review and the prior author/audit archives by SHA-256. The prior archives are external dependencies for the algebraic extrema criterion, not embedded in this packet. The new PDE/ODE bridge proof itself does not require importing their code.

The executable diagnostics are exact algebra and integrity checks, not numerical Ricci-flow simulation or certification of geometric existence. Run python -B math_check.py and compare stdout with results.json. Run python -B verify_package.py --expected-manifest HASH using the external receipt's manifest SHA-256. See VERIFICATION.md for optimized, relocated, and mutation tests.

Only authored proof, code, results, and public verification metadata are included. Source PDFs, extracts, corpus contents, screenshots, and private coordination are excluded. No remote mutation or publication was performed.
