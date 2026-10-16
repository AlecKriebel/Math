# Independent adversarial source/quantifier audit: PR200 / k115

## Finding

**The submitted PROOF.md passes this audit for its explicit theorem:** a>b>0, strictly nested nondegenerate confocal elliptical caustic, least period N divisible by four, every admissible primitive star turning number, and ordinary focal distances from consecutive outer-tangent intersections. No unresolved mathematical gap was found in that theorem. Literal primary-source inspection and my own derivation/checks support this result; favorable reviews were not used.

Two material scope/source findings remain:

1. **Least period is essential.** The original definition/table does not explicitly state the primitive convention. A repeated primitive six-orbit interpreted as a 12-orbit has a nonconstant 12-factor product. DERIVATIONS.md proves this exactly for every 0<k<1; check_results.json illustrates it numerically. The candidate explicitly imposes least period and correctly limits its repetition remark. This is a source-interpretation caveat, not a flaw in its stated theorem. Downstream claims must retain this quantifier.
2. **The Stachel dn-shift typo occurs in both editions.** Preprint p.10 and published p.1613 incorrectly attach (-1)^r to dn(u+2rK). The candidate uses the correct DLMF identity, so no proof conclusion depends on the error. A source note should name both affected editions.

This is mathematical/source review only. No publisher, human-review, historical-priority, novelty or publication clearance is given.

## Literal target and dependencies

The supplied arXiv v11 hash was verified before candidate inspection. Table 2 p.5 k115 is the correct outer-vertex one-focus product; its Introduction explicitly uses confocal ellipses. The complete journal *Fifty New Invariants* (2021), DOI10.1007/s40598-021-00174-y, was independently obtained and its table p.345 visually checked: k115 retains the formula/parity/status, although nearby labels change. SOURCE_LEDGER.md distinguishes the editions and hashes rather than conflating the Eighty/Fifty titles or 2020/2021 dates.

Stachel's published Theorem 4.3/(4.9) and preprint Theorem 2/(4.10) literally support arbitrary phase, modulus c/alpha, step 2v, axes relations and coprime star turns. Hyperbolic caustics are outside the literal target definition and the cited canonical theorem. DLMF periods, poles, zeros, quarter shifts, addition identities and derivatives were checked directly.

## Adversarial challenges and dispositions

| Challenge | Evidence/mechanism | Disposition |
|---|---|---|
| Wrong prime/derived polygon | Actual source table/figure and direct tangent equations | Closed: adjacent outer tangent intersections |
| Simple or tau=1 restriction | Literal arbitrary-phase/coprime-turn Stachel theorem; complete tangent lines | Closed for all primitive stars |
| Covered periods acquire parity | Exact orbit-coset divisor obstruction; repeated 6 gives nominal 12 | Broad traversal-length reading falsified; retain least period |
| Elliptic vs hyperbolic | Exact primary definition and canonical theorem | Closed in elliptical scope; extension excluded/unproved |
| Real denominator or focal zero | Positive sn(v),cn(v),dn(u),D0; nonzero tangent determinant; Q exterior to E | Closed including symmetry phases |
| Modulus/parameter confusion | k is modulus; code passes k^2 | Closed |
| 4K geometry vs 2K meromorphic lattice | Correct DLMF shifts and translation order N/2 | Closed |
| Factorization error | Own coefficient derivation and exact polynomial expansion | Closed |
| Divisor multiplicity/hidden pole | Degree-two J, full divisors and orbit coefficients | Closed |
| Exceptional primitive 4 | Separate degree drop at delta=K | Closed |
| Complex square-root branch | Positive ordinary focal factors and antipodal pairing | Closed |
| Prior work silently assumed | Only literal canonical/Jacobi inputs; method citations only credited | Closed for mathematics; priority unassessed |

No route was called blocked/reopened; the nonprimitive extension is falsified, not transferred to an unsupported lemma.

## Strongest verified result and exact remaining gaps

Within the stated noncircular confocal-ellipse scope, the candidate's theorem holds for every primitive N=0 mod4 and every admissible turn. My orbit-coset calculation also proves that for primitive even N>=4 the outer focal product is constant **if and only if** N is divisible by four. This establishes the exact repeated-six obstruction without relying on numerical disagreement. This audit deduction makes no novelty claim.

The circle has a separate immediate fixed-radius argument. Hyperbolic/degenerate/focal caustics, coincident conics and singular limits are not established. Signed areas and interior/exterior angle conventions play no role. The source's least-period convention is the remaining interpretive issue; the broader traversal-length assertion is false, so it cannot be supplied by extra proof work. Present-day novelty and publication questions remain independently unassessed.

## Checkable artifacts and validation limits

DERIVATIONS.md contains direct tangent geometry, all denominator/positivity checks, the coefficient identity, divisors, parity classification and exact cover counterexample. Independently authored check_quantifiers.py constructs the original tangent intersections; it imports/runs no submitted verifier. Its 65-decimal run checks 51 primitive families, three phases each, every coprime turn for N=4,8,12,16,20,24 and k=.05,.65,.98. Product spread, focal equality, caustic tangency, reflection and Q-formula residuals are below 1e-62. Exact polynomial expansion and finite rational-orbit controls through N=100 also pass.

For k=.65, alpha=2, nominal 12-cover products at phases 0 and .37K are approximately 25632.34717 and 25600.35347 (relative change -0.00124818). The exact analytic divisor argument proves variation; these decimals are diagnostic rather than interval certificates. Finite tests do not replace the all-N proof. Standard cited Jacobi and complex-analysis results remain explicit mathematical inputs.

## Integrity and completion

SOURCE_FIRST_FREEZE.md was written with UTC before candidate/favorable-report inspection. After the independent derivation, reading source_record.json for its statement unexpectedly displayed old literature triage in trailing research_summary; that field is not evidence here. No independent_review/prior_imported_report file, root math or other family's authored file was read. Only shared thirdparty runtime packages were imported at root direction. No local Git action, ref/PR mutation, outreach or publication action was performed.

This bounded source/quantifier/math audit is complete (100%). Its mathematical pass applies exactly to the explicit candidate theorem, subject to the source interpretation and excluded extensions above. No priority/publication clearance is implied.
