# Local erratum and mandatory scope

## E1: second-moment cap treated as equality

Location: frozen PROOF_RECONSTRUCTION.md, line 90, in section 6.

The equality E(X-Y)^2=2(R-1) is not justified from EX^2<=R. The correct chain is E(X-Y)^2=2(EX^2-1)<=2(R-1), using independence and EX=EY=1. A deterministic unit variable with R>1 already refutes the displayed equality under those assumptions. Replacing equality by this chain preserves the preceding minimum bound, the subsequent rho bound, and the right-end asymptotic. The corresponding external canonical proof uses its actual second moment R_p before bounding it and has no such defect.

Severity: minor, locally corrected in this audit; no failure of the spectral theorem. The frozen file is deliberately unmodified. Any derivative presentation should incorporate this correction or carry this erratum beside it.

## Required qualifiers

- Credited external mathematical characterization, not a newly discovered theorem or priority claim.
- Expectation exponent for independent hierarchical edge replacement, with p denoting series probability.
- Interior theorem p in (1/2,1); critical identity relies here on published near-critical information plus monotonicity.
- Exact implicit spectral/variational formula; no elementary scalar formula or full global-shape theorem.
- No uniqueness or convergence of all normalized laws is proved.
- Almost-sure limits are outside this candidate theorem; see the separate current-source update before making any broader openness claim.
- Original author PDF 404 and exact catalogue 403 remain; original PDF bytes and full current catalogue statement are not certified.
- One source-verification route, 1/5, with no five-route exhaustion.
