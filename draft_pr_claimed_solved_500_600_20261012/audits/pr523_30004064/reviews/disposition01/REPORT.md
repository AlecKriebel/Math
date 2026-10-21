# Fresh adversarial review of the PR523 disposition

Target frozen head: `2d771da7629db2dc9751c96f96af21149e6d45e5`. Completed 2026-10-13 UTC. This review writes only within `reviews/disposition01`; it makes no commits, pushes, branch changes, remote mutations, or communications with individuals. It is an audit, not a manuscript.

**Recommendation: the proposed closure without merger or a new claimed-resolution paper survives adversarial review. The frozen exact theorem is mathematically correct and fully answers a defensible literal source interpretation. Its acceptance as a novel resolution fails the positive prior-work gate.** These are different conclusions and must remain separate in any public disposition.

There is no mathematical defect requiring repair in the frozen exact proof, and no defect found in the current root repair certificate. The reasonable stronger repair is checkable, but its central theorem and concrete witnesses are already public. An attributed replication or explanatory note would be possible; it would not meet the specified novel original-resolution acceptance criterion.

## Independence and the strongest case for acceptance

I first read the frozen authored material, independently derived its optimizer inequality and checked the row/column construction, and saved `INDEPENDENT_PREASSESSMENT.md`. I then freshly retrieved and inspected the primary papers before reading the new root draft or sibling reports. The historical audit shipped by the candidate is part of the authored input, not independent evidence for this review. The present sibling source report was read only after my own certificate code passed.

For every real matrix A and y=As with s in the unit cube,

\[
F_y(u)-F_y(0)=\tfrac12\|u\|^2+
\sum_j\bigl(|(A^Tu)_j|-s_j(A^Tu)_j\bigr)
\geq\tfrac12\|u\|^2.
\]

Thus zero is the unique unprojected minimizer, including rank-deficient matrices. For P=AA-dagger, box feasibility gives Py=y and the same expansion with the quadratic `||Pu||^2/2`; the complete projected minimizer set is ker(A^T). The displayed full-row-rank 3x3 data really have precisely two checkerboard completions and five common coordinates. The all-size extension, undersampling limit, and unique-image counterexample are valid.

The primary [OWR report](https://content.ems.press/assets/public/full-texts/serials/owr/16/1/16766/online/10.4171-owr-2019-4.pdf), printed p258/PDF page50, explicitly displays the exact optimal-multiplier recovery rule. I visually inspected this page and read the complete contribution, pp256-259. Consequently an exact-rule reading is textually defensible. It would be too strong to claim that *no* original-source interpretation is fully resolved by the candidate. The correct objection is that this defensible interpretation supplies no new resolution after the positive prior theorem match.

The experimental conjecture also speaks of the broader dual approach. The [Kadu/van Leeuwen v3 manuscript](https://arxiv.org/pdf/1807.09196v3), associated with [IEEE DOI10.1109/TCI.2019.2898333](https://doi.org/10.1109/TCI.2019.2898333), already distinguishes exact scalar zero optima from approximate signs. Its equations10-11 give zero for noiseless scalar endpoints; SectionII-C discusses smoothing; Algorithm2 returns an auxiliary variable's sign. I visually inspected v3 p3 and read the relevant SectionsII-III and numerical discussion. The frozen theorem cannot by itself decide those different outputs. The scalar fact alone would not justify dismissing a general theorem's novelty; the following positive match does.

## Independently validated prior theorem and chronology

I freshly downloaded the canonical [Ferudun PDF](https://eulersolve.org/papers/owr-16766-004/paper.pdf), independently extracted it, and visually inspected p3. **Lemma2.1 contains a complete valid proof of the overlapping general result.** Set w=Pmu; the projector identities give A^Tmu=A^Tw and Py=y. For y=Az with ||z||_infinity<=1, Holder's inequality gives `||A^Tw||_1>=z^TA^Tw=y^Tw`. Therefore the projected objective is at least `||w||^2/2+||y||^2/2`, with equality exactly at w=0. This establishes the full projected optimizer set and the unique-zero full-row-rank case, without solver behavior or other claims from that preprint.

The prior paper's setting uses tomography incidence matrices, but the lemma's proof needs only an arbitrary real matrix, an orthogonal range projector, and box feasibility. The candidate's arbitrary-real-matrix phrasing adds no new mechanism. Its unprojected uniqueness without rank is also an immediate consequence of prior Proposition2.2(b)'s zero-optimum characterization and the objective's strict convexity. The candidate's exact common-recovery failure follows immediately from these facts.

The freshly retrieved [DataCite DOI record](https://api.datacite.org/dois/10.5281/zenodo.23110494) gives `findable`, version1.0, issued2026-10-02, and created/registered/updated **2026-10-02T20:09:16.000Z**. Its unchanged registered abstract describes both the zero optimum and the 5x5 fractional competitor. The publisher's [machine-readable metadata](https://eulersolve.org/papers/owr-16766-004/metadata.json) gives the same version, first public release date, DOI, and canonical PDF SHA-256, matching my fresh bytes:

`b374bbc76792418e60fa96a329a5ae6b6f5e596b12b5572b69466d6467bab43b`.

The candidate's authored source gate and attempt log are dated October4. This is positive, independently corroborated public chronology, not a negative literature-search inference or a website summary accepted as mathematical evidence. The direct Zenodo record and deposited-file requests from this review returned403, so I did not personally retrieve archived bytes. After this report was drafted, root supplied `root_reproduction/prior_public_deposit_check.json`; I inspected it. Root independently fetched record23110494 (created2026-10-02T20:09:15.753594+00:00, modified2026-10-02T20:09:16.081292+00:00) and its deposited `OWR-16766-004-paper.pdf`, whose SHA-256 equals my fresh publisher PDF. This adds a separate independent dated deposit check; my personally reproduced evidence remains the publisher PDF, publisher hash/version binding, and DOI chronology.

## Repair and its precise overlap

I inspected the current root `verify_repair_overlap.py` and replayed it. Its output is byte-identical to `repair_overlap_results.json`. The exact baseline subtraction correctly uses Fraction. The 6250 enumeration count, kernel/support checks, exposing potential, restricted rank, segment endpoint bounds, and positive-epsilon control all hold. Its disabled-assertion guard prevents optimized Python from silently bypassing checks.

My independently authored `verify_disposition.py` constructs line families separately, enumerates binary row choices, checks the exposing table's row-space membership by augmented rational rank rather than importing the supplied potential coefficients, and computes the segment interval by intersecting all cube bounds. It confirms the prior Theorem4.2 image has one binary solution, a 19x25 measurement matrix of rank16, exactly11 movable and14 fixed pixels, and the precise box fiber `s+lambda*c`, `0<=lambda<=1`.

The nonzero c satisfies Ac=0 and c_j*s_j<0 on its support. If sign(A^Tmu)=s for any real mu, all11 nonzero summands in `c^TA^Tmu` would be negative, contradicting `mu^TAc=0`. Thus **no exact back-projected multiplier, optimal or approximate, has the complete image's correct sign**. Removing redundant rows preserves the row space. Smoothing cannot overcome this sign-separation obstruction if its reported output remains sign(A^Tmu). Thresholding small entries to zero cannot produce a successful complete binary image either, since success would still require every sign to be correct and nonzero.

This is an independently derived direct corollary of the prior example's checkable certificate; it should not be misrepresented as a verbatim theorem statement from the note. It makes the repair rigorous without importing any solver claim, but its central obstruction and explicit construction already have prior coverage. Turning that known certificate into this immediate sign argument does not establish new discovery priority for the original conjecture.

I also independently checked the prior Theorem4.6 explicit 4x4 example: 576 row-conditioned candidates give exactly four binary solutions with four common pixels, and the rational fractional witness moves two common pixels. The same orthogonality argument rules out the *unthresholded exact* common sign pattern. It does not prove failure for every finite threshold, since prethreshold nonzero entries at variable pixels could compensate the inner product. No such unsupported stronger threshold conclusion is used here.

For the frozen 3x3 row/column example, the multiplier `epsilon*(1,0,0,1,0)` has the correct common pattern for every epsilon>0 and exact objective gap epsilon^2. Its limit is zero. This is a concrete reason that the frozen exact-zero obstruction does not already establish failure of the useful approximate-sign interpretation in that example.

## Why only the checked prior claims may be credited

I did not validate the prior note's full image census, all real-solver runs, MATLAB/CVX behavior, or general central-path rates. Moreover its Corollary3.3 is overbroad as written: it says the nonfixed pixels also survive the positive threshold for tau>=tau2.

Take A=((1,0,0),(0,1,1)), y=(1,0). Then Q={(1,t,-t): -1<=t<=1}, so the second and third pixels are nonfixed. In the logarithmic box barrier, strict convexity and symmetry force z2=z3=0 for every tau>0, hence their back-projections are always zero and never survive any positive threshold. At tau=3/8 the exact stationary point is z=(1/2,0,0), mu=(1/2,0), and A^Tmu=(1/2,0,0); my checker confirms stationarity with rational arithmetic. This counterexample concerns an assertion outside Lemma2.1 and the exact 5x5/4x4 certificates. It does not weaken those independently verified results or reverse the priority rejection.

The root draft already limits its reliance appropriately. No required root correction follows. An optional clarity improvement is to say explicitly that the exact reading is defensible and completely answered, while the checked prior lemma and certificates defeat novelty. Do not describe the prior preprint as independently validated in its entirety.

## Final disposition and surviving gap

Preserve the valid frozen proof and all audit evidence. Subject to the root's final live exact-eligibility check, close the claimed-resolution PR without merger, a new preprint, release, or acceptance DOI. Record the positive prior theorem and the exact/numerical interpretation boundary in the disposition.

**No mathematical gap remains in the frozen literal result. The surviving acceptance gap is the absence of a verified novel contribution resolving the complete original research claim.** Reasonable local repairs either restate a valid but prior exact theorem, or use prior original-scope witnesses. A materially new theorem about an independently specified auxiliary-variable selection or numerical algorithm would need its own formulation, evidence, and priority assessment; it is not supplied by this candidate and is not a local editorial repair.

Audit completion estimate:100%. Completion toward a verified novel original-resolution publication from this frozen candidate:0%. Normal and optimized executions of my verifier produce byte-identical output, with all checks active. Downloaded source papers, metadata bodies, text, and page images stay in ignored `sources/`; authored provenance, code, results, and review are suitable for the root's later evidence commit.
