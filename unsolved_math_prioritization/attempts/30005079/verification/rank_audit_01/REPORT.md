# Rank/arithmetic adversarial report: PR888 / PID30005079

Candidate head: a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7. Candidate PROOF.md SHA256: 657f458cf3eece42eef9c8dfd46a7c20aaaf363e3a6744f396af3c7389fa43a3.
Original research effort remains 1/5. This report validates an existing claimed solution; it starts no new central search.

## Disposition

**ACCEPT this independent arithmetic/rank family’s obligations.** The exact a,b in the candidate have irrational ratio, and the specified valuation on the function field has value group aZ+bZ of rational rank2. It is therefore nondivisorial in the required sense c·ord_F with any real c>0 excluded. This conclusion is proved mathematically for all rational slopes; numerical brackets are auxiliary.

This family does **not** independently certify global H-minimization, the special degeneration’s complete geometric construction, or publication readiness. Its exact remaining dependency is that the candidate’s filtration is the canonical first H-minimizing degeneration with the claimed central variety, as audited by the separate geometry and global-minimizer families. Under those identifications there is no remaining arithmetic/rank gap. No fatal arithmetic flaw was found.

## Mechanism, evidence, and limits

| Obligation | Mechanism and checkable evidence | Status / exact gap |
|---|---|---|
| Exact moment weights | Polynomial antiderivative recurrence, rational moments, rational Taylor remainder certificates in exact_rank_checks.py and EXACT_RANK_RESULTS.json | Verified; no floating-point proof |
| Unique positive roots | Strictly negative derivative, positive moment at0, exponentially dominant negative interval | Verified for original integrals; t=0 is a spurious zero of rewritten exponential polynomials |
| Full toric vector | Slice width y+2, mean x=y/2, positive covariance Hessian | Verified; no inference from minimizing only one selected line |
| Primary first-factor normalization | Actual MWv2 pp.11–12 including rendered p.12: s=k/m−1 and stated density/sign | Verified |
| Transcendental coordinate | Hermite–Lindemann applied only to nonzero algebraic2b; B’s denominator cannot vanish | Verified; theorem statement checked in actual primary research paper Delayguev2 TheoremA |
| Irrational ratio | Candidate’s transported-field infinity-place proof; independent resultant leading term r^(6q)3^(3p) | Verified for all p,q>0; no transcendence conjecture |
| Function-field rank | h,w have values a,b; Gauss formula gives reverse inclusion | Value group exactly aZ+bZ, rational rank2 |
| Residue / Abhyankar | Distinct leading exponent pairs cannot tie; residues form C(E)(z) | Residue trdeg3 and 2+3=dimX=5; ordered rank is1, not2 |
| Nondivisoriality | A real-scaled prime divisor has value group cZ and rational rank1 | Verified directly; irrational rescaling alone is not used |
| Canonical shift | ak+b(j+m)−m(a+b)=a(k−m)+bj | Verified for the fixed local/section conventions |
| Canonical/global identification | Requires special real degeneration and weighted central semistability | Outside this family; not inferred from separate factor minimization |

The independent universal resultant derivation and the complete rank/residue argument are in ANALYTIC_FREEZE.md. Five actual exact Sylvester determinants check the resultant’s general leading-term formula. These controls have no universality claim separate from the proof. The checks also validate all21 original source byte/SHA pins, including old-report files as immutable bytes.

## Sign convention and a reasonable optional clarification

The actual WZ Lemma2.2 has exp(+c·y), while the MW/HL filtration convention has exp(−ξ·α). They are compatible under the inverse action on sections. HLopt Example2.13 explicitly gives point action Z1↦tZ1 but section weight−1; Equation44 gives the negative discrepancy shift used here. With section/valuation weights j for w^j, the grading’s point action is w↦t^(−1)w, so the WZ analytic coefficient is c_w=−b. MW’s chosen divisor degeneration similarly gives point action u↦t^(−1)u. Thus the total signs agree. An explicit sentence stating this conversion would improve readability; it is not an arithmetic repair required for validity.

## Independence and historical-report disclosure

TARGET_FREEZE.md was saved after the native target and actual OWR report but before candidate/older audit inspection. ANALYTIC_FREEZE.md was saved and sent to the parent before source/audits was opened. Only then were the two old acceptance reports and reviewerB’s script read. Their arithmetic conclusions agree with this independent result; they are not treated as evidence or authority for the disposition. The independent resultant certificate and derivative-recurrence implementation were produced before that disclosure. No other-family findings, other PR, other shard, individual, or chat were consulted. Only the parent received messages.

PRIMARY_SOURCE_PINS.json records actual external sources and hashes, including the failed403 attempt to inspect Lindemann’s original1882 paper. I do not claim to have read that inaccessible paper or reproved Hermite–Lindemann. The primary modern paper’s exact theorem statement suffices to check its application. No full historical priority search was undertaken.

## Reproducibility and boundaries

Run `python3 -B exact_rank_checks.py` from any directory, retaining the sibling parent source receipt/layout. This requires only Python’s standard library and produces EXACT_RANK_RESULTS.json. Python3.14.6 actually ran the final exact controls successfully. The candidate’s SymPy scripts were read but not executed by this family; original-script replay belongs to the artifact family. No candidate or original-source file was edited. No Git, external publication, remote, release, Zenodo, or account mutation was performed.

Final family completion estimate:100% of assigned arithmetic/rank audit; overall mathematical solution readiness is not assigned a percentage by this family. Safe payload inventory, byte lengths, hashes, explicit exclusions, and privacy checks are in SAFE_PAYLOAD_MANIFEST.json; the manifest excludes itself to avoid a circular hash.
