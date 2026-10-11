# Global approximate root selection: two-to-three-chart partial bound

Problem 10800008 / AMR-107-0008, Vassiliev's approximate Problem 2B.

For all six real coefficients in

    x² − y² + a1 x + a2 y + a0 = 0,
    xy + b1 x + b2 y + b0 = 0,

let N(ε) be the least size of an open cover of the entire coefficient space with a continuous selector on each member, everywhere at Euclidean distance strictly less than one fixed ε > 0 from an actual real common root. The accepted partial theorem is

    2 ≤ N(ε) ≤ 3,

and N(ε) has the same value for every positive tolerance. Singular parameters, unbounded coefficients and the zero parameter are included. The exact value 2 versus 3 remains unresolved.

## Complete authored proof and audit

- [PROOF.md](PROOF.md) retains the full candidate argument and its historical pending-audit wording, explicitly superseded by the subsequent partial acceptance. It adds the accepted audit's complete expanded Sections 4–8, including the final cusp mixed-derivative clarification.
- [AUDIT.md](AUDIT.md) gives the complete independently reconstructed mathematical argument: harmonic reduction, properness and degree, Jordan disk, fold/cusp local degrees, the selected exterior covering, phase-chart topology, approximate collars, origin blending, lower obstruction, scaling and precise quantifiers.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json) state the exact accepted and unresolved claims.
- [SOURCES.json](SOURCES.json) records the public scholarly source, its PDF hash and size, and historical inspection limitations.
- [VERIFICATION.json](VERIFICATION.json) distinguishes symbolic checks, byte authentication, and mathematical audit. Both historical inventories are closed; the preparation does not distribute their code or raw outputs.
- [MANIFEST.json](MANIFEST.json) lists exactly eight public files and hashes the other seven. Its own hash is pinned in the draft PR body.

The topology uses the implicit-function theorem, invariance of domain and Jordan separation, planar Brouwer degree, covering-space lifting/triviality, and unbounded real-valued Tietze extension on normal spaces. The proof verifies the singular covering and the relative closedness needed for those applications. The fixed approximation tolerance does not require a uniform geometric collar width or bounded coefficients.

The separate literal exact-section caution establishes no local exact section at the zero parameter. It does not determine the author's intended exact formulation, certify a source correction, or resolve the approximate optimum. The lower approximate obstruction is instead proved independently on a circle of root radius greater than ε.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance applies only to the stated partial theorem; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and symbolic checks described below occurred in the preceding investigation and audit on 11 October 2026. Editorial preparation authenticated retained bytes without a new scholarly-source inspection or mathematical-program rerun.

No novelty, historical priority, exhaustive literature search or present-day resolution claim is made. No copied source PDF, source text, page image, dataset content, checker code, raw output or private coordination material is distributed.
