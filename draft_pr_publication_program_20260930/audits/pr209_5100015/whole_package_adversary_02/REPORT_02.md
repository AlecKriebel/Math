# Second new independent whole-publication adversarial review: PR209 / 5100015

**Verdict: PASS for the exact already-published package in its stated domain. No mandatory findings; no optional findings.** Review completion estimate: 100%. This is an automated adversarial audit of an informal mathematical proof and its evidence. It is not human peer review, formal proof verification, or a certification of novelty, firstness, simultaneity, causal independence, or present worldwide openness.

No repair to the scientific package or to the exact inspected Root mathematical note is required by this review. This verdict does not clear the old descending-program operational/recovery helpers, an unreviewed future native overlay, any ref update, or a merge. DOI 10.5281/zenodo.23413614 and the existing tracker row are already published; no staging, publishing, appending or other service mutation occurred here.

## Independent starting point and exact scope

INDEPENDENT_PLAN_02.md and PLAN_SEAL_02.json were written before reading any first-new-review, Root mathematical assessment, or current family report. INITIAL_DERIVATION_02.md and its seal record a complete initial geometric/meromorphic derivation at 25%, before those cross-reviews. Relevant primary source text was treated as evidence, not as reviewer conclusions. All writes are confined to this owned folder. No subagent was spawned, no Git command, install, external outreach, or other-chat message was used. Internal progress reports were sent only to the assigning Root agent.

The frozen publication source is `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint`. The exact seven assigned bindings all match:

| File | Bytes | SHA-256 |
|---|---:|---|
| manuscript.tex | 16085 | 01b7feb398c95ce1a521f379e472e6c856a776408da5b1ccb93db9b0f88a8fe7 |
| manuscript.pdf | 82528 | 8e28a1764160a7f7ef6e9bf4d1a1937062a003ab462ec93ce69c4643a5c36a55 |
| k303b-source-verification.zip | 683157 | 0039aeee870804a149a5ae70f6893335387670e122f833e622d70b42584550f4 |
| metadata.json | 2143 | ea1306176b6d86a921b4783ddb20016eef79815479c35f8b9e6fe1ce0e666f9c |
| deposit.json | 2430 | b5bf1aedcdab7ca6851a776c97170e25ceeeccac88e858cc56078a786d0959ba |
| PACKAGE_MANIFEST.json | 1089 | 4dc82f095c68bd8bc4e7b81718300d40ba1abe79a7290e70e5795df8e0c1d79b |
| historical FINAL_CLEARANCE.json | 10523 | 370cd4bbfb463597680b7b52fd59ba731a762c82296c98ad2571d947f902e065 |

SOURCE_MANIFEST.json is 42,680 bytes, SHA-256 0cad85f8211ae7f401af8b568342bfaf3fffc678c0390a8b80c7fa7e9d36056f. INSPECTED_INPUT_PINS_02.json binds 46 selected read-only sources/receipts, without copying full third-party papers or private journals.

## Exact claim, hidden-assumption attack and proof

I directly read RGK's 2020 v11 Table 4 p.6 and the 2021 published Table 4 p.346, together with the published p.343 signed-area convention. They specify k303,b: signed area of the outer boundary-tangent polygon times signed area of its pedal at O, for N not divisible by four. The theorem uses the strict proper confocal elliptic-caustic domain a>b>0, 0<lambda<b². Hyperbolic, focal and collapsed cases are explicitly excluded. Side lines are the complete boundary tangents; spatial sorting, filled star lobes, clipped feet and original-chord feet are different constructions.

The precise audited locations below refer to manuscript.tex. The current native PROOF.md agrees, using an equivalent reflected-zero proof of the trace lemma.

1. **Lines 36–69, canonical coordinates at 80–98:** Signed shoelace indexing is fixed before derived polygons are formed. Stachel's published Theorem 4.3/(4.9), visually read on p.1614, supplies P(u+2jv), P(z)=(-a sn z,b cn z), modulus k, v=2tauK/N, a=alpha dn(v)/cn(v), b=beta/cn(v), and the admitted primitive windings. This is actual billiard parameterization, not an unjustified equally spaced sample. Strictness gives 0<k<1 and 0<v<K, so cn(v)>0.

2. **Lines 100–116:** Direct expansion of Jacobi addition gives det(H(z-t),H(z+t))=AB f(t)[dn(z-t)+dn(z+t)], f=sn cn/dn. The edge-polygon identity is area(edges)=2area(P)-(1/2)sum det(P_j,P_(j+2)); cyclic reindexing then gives ab[2f(v)-f(2v)]T(u). This is an identity of indexed sums even when stepping by two separates cycles. No simplicity, convexity, unsigned-area, or nonzero-area assumption enters. f(2v) may vanish or have negative numerator without invalidating the formulas; no division by it occurs.

3. **Lines 118–133:** Both P(z-v) and P(z+v) satisfy the caustic tangent equation. Ellipse polarity gives the outer intersection R_j=diag(a/alpha,b/beta)P(u+(2j+1)v) and area A'=a²b² f(v)T(u+v)/(alpha beta). Parallel boundary tangents would require antipodal endpoints; their center-crossing chord cannot touch the proper inner ellipse. Thus no real infinite outer vertex is suppressed.

4. **Lines 135–176:** Direct orthogonal projection gives Q=n/(n.n), with denominator a²-(a²-b²)sn²(z)>=b²>0 on the real axis. Let w=K-v. Quarter-period identities give cn(w)>0 and dn(w)=b/a. The symmetric endpoint sum and P(z+2K)=-P(z) yield Q=L[P(z+K-v)-P(z+K+v)], L=diag(b/a,1)/(2cn(w)). Its determinant is b/(4a cn²(w)). The global minus sign on an edge vector preserves oriented area in dimension two. Therefore A'_O=b²[2f(v)-f(2v)]T(u+K-v)/(4cn²(w)). This identifies the actual center feet pointwise and fixes the area normalization. Neither polygon area is divided out.

5. **Lines 178–218:** KLS v1 Appendix A Eq.86 (v2 Eq.85) is precisely V=C_q U_q for an odd real subgroup. C_q is finite and positive because each factor cs(2Kj/q) has argument strictly between 0 and K; q=1 has empty product one. Multiplication by the K translate and dn(z)dn(z+K)=k' gives U_q(z)U_q(z+K)=(k')^q/C_q² meromorphically. The included independent residue reproof is also complete: dn has real period 2K, imaginary antiperiod 2iK', and simple poles; shifted poles are distinct modulo 2K. At iK', pairing h and -h cancels the signs in (-i)^(q-1)prod cs(h), leaving C_q. The same residue ratio reaches every pole by subgroup translation and antiperiodicity, including the other imaginary pole row. V-C_qU_q is entire elliptic, hence constant; its antiperiodicity forces zero. Complex denominator zeros are handled as meromorphic identities and removable singularities, not asserted absent. The native reflected-zero proof likewise excludes K from odd H before evaluating U(K+iK'), then removes every possible pole of the product. There is no transferred unsupported central claim.

6. **Lines 220–240:** Modulo dn's real period 2K, 2jv exhausts the subgroup of order q=N/gcd(N,2), with r=gcd(N,2) repetitions. q is odd exactly for the eligible primitive periods. T's 2v period aligns the area traces at u+v and u+v+K, giving the displayed explicit constant. This arithmetic covers every admitted coprime star without reordering. Reversal negates each area and preserves their product. A d-fold listed traversal multiplies each sum by d and the product by d²; if dN is not divisible by four, neither is N.

7. **Lines 242–252:** The invariant has length-four units. Genuine one/two-bounce orbits cannot touch the strictly interior centered elliptic caustic. The circular limit is separately justified by rigid rotation of fixed-step regular stars. The omitted parity is essential: on x²/4+y²=1, the diamond and normal-bisected rectangle share lambda=4/5 and satisfy the reflection law, but their products are 32 and 50. No excluded endpoint or parity is silently promoted.

The strongest verified result is the complete informal analytic proof of that exact signed invariant in this domain. The written identities, not finite samples, establish its universal quantifiers.

## Owned checks, exactness and failure disclosure

`independent_geometry_02.py` was written in this folder without importing inherited scientific code. The final full execution under Python 3.11.8 `-E -S -B -P`, installed SymPy 1.14.0 and mpmath 1.3.0 passed:

- 80 primitive families and 240 phases, including all reduced windings in N=3,5,6,7,9,10,11,14 at k=0.02,0.4,0.91,0.999;
- 23,596 numerical assertions at 70 decimal digits, direct boundary/reflection/common-caustic checks, tangent intersections, normal feet, pointwise edge map, both area formulas, explicit constant, reversal, repeated lists and length-four scaling;
- 54 complex trace cases for q=1,3,5,7,11,17, including points approaching the imaginary pole row; maximum scaled residual approximately 1.00022e-60;
- 36 exact SymPy assertions checking the two period-four examples, including boundary, common caustic, normalized forward reflection, actual areas and products 32/50.

These numerical checks are not interval certificates or a proof by sampling. The initial passing exact fixture included ordinary Python zero coordinates that could introduce floating-point zero. The final source sympifies every exact coordinate before any geometry arithmetic, and the complete program was rerun successfully; the earlier source/result is preserved. Own package-check attempts also failed due to incorrect assumptions about a receipt key and tracker column layout, plus an ancillary relative-parent path typo. Corrected source copies and OWNED_CHECK_CORRECTION_02.json disclose each error. These were errors in the owned checker, not findings against the package, and failed attempts were not promoted as evidence.

`independent_package_checks_02.py` passed all seven assigned freeze pins, 210 source rows, 149 verification rows, 48 prepared current-packet rows, 211 actual ZIP members, 77 native attempt bodies, 23 original-history identities, and 112 selected V3 public allowlist files. SUPPLEMENTAL_PACKAGE_RESULTS_02.json adds the 53-row revised native current manifest, exact equality of all four tracker cells to the native release receipt, regular non-symlink ZIP modes and lossless failed-output decompression. The source/ZIP member sets match exactly, every member equals its frozen source, and there are no duplicate names, traversal paths, CRC failures, third-party paper PDFs, caches, private directories or bundled environments.

## Harness, reproduction and correction history

I read all eight frozen scientific programs, run_checks.py, integrity.py and harness_failure_controls.py. The actual programs contain meaningful algebraic, Cartesian/reflection, subgroup, divisor and classical-bridge controls, and label finite/non-interval evidence correctly. The author six-period witnesses are credited through PR148, rather than presented as independent parameter discoveries. The physical programs check actual geometry rather than accepting fitted Jacobi traces alone.

The portable harness runs unchanged copies in new output folders outside the entire archive, rejects optimization, compares actual scientific output with explicit timestamp-only omissions, and checks frozen inputs before and after. Raw binary partial timeout streams, launch errors and nonzero exits lead to per-suite failure receipts and aggregate completion with the after-input check. Writable storage remains an explicit limitation. Synthetic success fixtures are labelled orchestration evidence and do not count as scientific reproduction.

The old first-review mandatory M1 concerned lost timeout/launch evidence on different, 679,151-byte ZIP bytes. ROOT_REVIEW01_RESOLUTION.json identifies the repair, current code contains it, and the subsequent historical review binds the actual 683,157-byte package. The prior finding is not silently converted into a pass on its old bytes. The failed physical triangle derivation, negative-control threshold and nondiscriminating wrong-construction samples, historical -B omissions, timestamp/report corrections and recovery limits remain disclosed. I decompressed the preserved bad physical output: 72,751 bytes, SHA-256 b74725bfa1ff239c31f73443898644c6fcf29cc044de4f30edc32c2c75333dbb, exactly the pre-compaction binding. This proves byte recovery while preserving the fact of intervening compaction.

I inspected Root's actual aggregate at parent `root_reproduction_01/isolated_replay/REPRODUCTION.json`, 5,711 bytes, SHA-256 d9edfce796d4fcc73f268ce6ef9409507cae3264a0463821cd217538662f8cb1. All eight suites passed, copied program pins match the frozen sources, all scientific fields agree, and 149 files verified before/after. That is Root execution evidence; I did not execute those eight inherited scientific suites. My independent 23,596 numerical/36 exact checks are separate owned evidence.

## Primary sources, attribution and chronology limits

Relevant actual primary passages were read directly, not inferred solely from source maps:

- RGK 2020 v11 Table4 p6 and 2021 Table4 p346/Section3.4, with the p343 signed shoelace convention, establish the exact target and side-line object.
- Stachel's published Theorem4.3/(4.9), p1614, gives canonical coverage and modulus conventions. Standard polarity and [DLMF 22.4](https://dlmf.nist.gov/22.4), [22.8](https://dlmf.nist.gov/22.8) support the period/pole and addition formulas; both official DLMF pages were also freshly opened read-only in this audit.
- KLS v1 Eq86, visually read in its complete Appendix A page, and the v1/v2 adjacent discussion give the precise old all-phase product-to-sum identity and prior meromorphic mechanism. The [official KLS record](https://arxiv.org/abs/math-ph/0207019) was freshly opened. KS2003 preprint Eqs13–15 includes the argument scale and normalization. The 2004 publisher PDF access limitation does not block the proof: the exact KLS result and the manuscript's residue reproof suffice independently.
- AST Theorem4 proof supplies the reflected unit-velocity relation; Lemma3.1/Remark3.2 names the skew hodograph and credits Veselov. BT Theorem4.1 studies the actual same boundary-tangent feet, with centroid/squared-distance conclusions. These mechanisms are credited, not represented as a wholly new map or theorem. Chavez-Caliz Theorem6 concerns original/outer areas, a different pair; the supplement's auxiliary 2q-family bridge is a valid deduction, not an attribution of the explicit target statement to that paper.
- Ferudun v1.1, DOI10.5281/zenodo.23088516, Theorem2 and complete Section6, is the exact full contemporary theorem: same strict domain, actual center feet, signed stars and all eligible repeated lengths. Its odd self-paired removable vertex is explicitly handled. I also read v1.0's actual opening theorem: its primitive 2mod4 arbitrary-point result implies the centered even subset, not the whole later centered result. The manuscript, metadata, current native proof and target tracker notes make this distinction explicitly.

The manuscript's 05:35:19 GitHub server receipt and the two Zenodo creation times are bounded chronology observations. Root's preserved fresh provider record observations agree with the 16:56:14/18:12:36 times. Neither chronology nor missing archive captures proves historical public visibility, absence of earlier website posting, historical independent non-derivation, or firstness. The package expressly leaves ordering, independence and novelty undetermined; that is the correct conclusion. No exhaustive new global priority search is claimed here.

After sealing the initial derivation, I read the first new whole-package report and Root's exact 10,740-byte mathematical/priority note, SHA-256 518b673911f18d65af765dd70f887cf4b1e4500e3e09fc54159c8bdb954de0b3. Their mathematical conclusions and scope agree with this reconstruction. No required edit to that Root note was found.

## PDF, native custody, metadata and actual provider evidence

I rendered the exact frozen PDF afresh with Poppler at 85 dpi and visually read all five pages. The theorem, indices, formulas, symbols, references and disclosures are legible and agree with TeX; no clipping, overlap, unresolved reference or missing glyph was found. PDF_QA_02.json binds the render inputs and intermediate PNGs.

The 23 captured originals match the immutable copies in the revised native history, prepared native history and verification/original_submission. The current scientific PROOF is preserved separately from the old historical binding. Current native status/disposition explains dated pending-review text; original claimed_solved and author turn1/5 remain preserved. No historical proof is silently overwritten to manufacture better prior attribution.

I read the complete selected public V3 custody verifier, checked all 112 allowlist bindings and its executable AST equivalence with V2, then personally executed it read-only under Python3.11 `-E -S -B -P`. Exit0, zero stderr: all 77 attempt bodies, seven native commit bodies, 17 authenticated trees, two complete target deltas and original23 history identities verify. The only verifier source change from V2 is its docstring command filename. Root's own actual V3 acceptance is also retained. The enormous foreign first-parent delta is privately retained custody evidence, not exported by this review or newly recomputed here. This target-custody result does not authorize selecting the old prepared root or performing a native operation.

Metadata.json and deposit metadata match the public record's title, description, author/ORCID, date, preprint/license type, version, keywords and qualified claims, with the API's standard nested representation accounted for. Both public file MD5 values match local exact bytes. Root's actual top-level kit inspection and public-download SHA receipts bind the exact published PDF/ZIP, DOI resolution HTTP200 and no metadata normalization. The read-only GWS receipt has the DOI exactly once, in row121; all four cells equal the native release receipt, including blank B and the fully qualified D notes. Those provider actions are Root evidence inspected and byte-checked here, not actions performed by this reviewer. No provider mutation or duplicate publication/append is proposed.

## Disposition

Mandatory findings: **none**. Optional findings: **none**. No scientific or attribution repair, republication, or tracker edit is required by this review. The exact qualified research note is fit for Root's adoption as a checked informal result. The broader goal, operational helpers, actual future minimal native overlay and any merge require their own separately bounded decisions; this clean publication verdict does not clear them.
