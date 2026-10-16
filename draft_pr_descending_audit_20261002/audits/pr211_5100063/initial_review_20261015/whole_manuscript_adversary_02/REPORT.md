# Review 02: independent whole-manuscript and publication-package adversary

PR211 / 5100063 / AMR-050-0063 / k904,a. Review date: 15 October 2026 UTC. Reviewer: internal independent AI subagent `pr211_whole_manuscript_adversary_02_20261015`.

**Final result: the final frozen review02 packet has no unresolved mathematical, source-scope, metadata, provenance, presentation or package findings in this review. Mandatory findings: none. Optional findings: none.** Review01 M1 and elected O1 have been resolved globally in these frozen bytes. The acknowledged historical-priority and source-access limitations remain material and accurately disclosed. This report is a version-bound research review, not publication authorization or human peer review. Parent retains integration and every release decision.

## Frozen scope, independence and success criteria

Sole publication scope: `preprint/history/review02_frozen/` within the PR211 case. Exact pins:

| File | SHA256 |
|---|---|
| manuscript.tex | 58d3bc3388e586ec64cb391b2c6324e2585794a5919715d010701a1855a6f784 |
| manuscript.pdf | 82b2710dd69f706dc2018f8d7ee6de4e8d894688f8dc15c3e8006219e974ab06 |
| k904a-source-verification.zip | 25bc0a99297b0a8ecfb9a70a7542cdfb82d1e2c2063b8630155f3b81f262d49b |
| SOURCE_MANIFEST.json | 35ac30bb627398486a0210a6326f92b295a3a8e542216c301d8cfcf2a77b061e |
| PACKAGE_MANIFEST.json | 778efe2f6d79a5f2bb69ae8bb033e34bae1a4b76bc9bf082d92d8d8c4c912ad0 |
| metadata.json | 7e53e8d7ca6c70248c48bc3f1d4652a9dc82670424048de852cabd8660005784 |

I read the entire manuscript source before any inherited reviewer report or checker. At 11:23:28 UTC I froze `INDEPENDENT_ATTACK_MAP.md`, which reconstructs the target, proof mechanism and attacks. My new controls were written without importing inherited checkers. Review01 and root resolution records were inspected only after that reconstruction and the initial independent mathematics. The supplied task identified documentary history as an attack surface; I did not treat supplied verdicts as evidence of mathematical truth.

The exact hypothesis is strict nondegenerate nested confocal elliptical caustics in a noncircular billiard ellipse, odd least period N>=3, every admitted coprime star winding, original billiard foci, OUTER consecutive tangent intersections, unit vertex inversion, and signed straight-segment shoelace areas. A fixed repeated traversal and reversal are included with their stated area factors. Circle and geometric/inversion-radius scaling claims are separately checked. No equivalence with original-vertex inversion, outer-locus-own-focus inversion, inverse arcs or filled-face area was presumed.

Success required a checkable all-period proof, exact source-domain match, no hidden critical/degenerate case in that domain, honest priority/access qualification, and consistent reproducible bindings. No finite numerical sweep was accepted as a substitute for the universal argument.

## Independent mathematical verification

### Physical coordinates, finiteness and exact edge normalization

The actual primary Stachel Theorem4.3/(4.9), printed p1614, supplies the canonical elliptic-caustic parameter with modulus equal to caustic eccentricity, the shift `2v=4K tau/N`, and all coprime turning numbers. Reversal permits `0<tau<N/2`, hence `0<v<K`. This is not uniform spacing in eccentric anomaly. Numerical programs use parameter m=k².

The tangent coefficients are `(-sn(z)/a,cn(z)/b)`. The stated Q satisfies both tangent equations. Their determinant has nonzero magnitude `2 sn(v)cn(v)dn(u)/(ab(1-k²sn²(u)sn²(v)))` on the real axis. Consequently all outer intersections are finite, even for stars. Since both axis ratios Ao/a and Bo/b exceed one, every real Q has original-ellipse quadratic form strictly greater than one. Both original foci are strictly inside that ellipse, so neither real inversion is undefined. The proof correctly allows Ao<Bo; it never silently replaces original focus c with the eccentricity of the outer locus.

I reconstructed the focal bilinear distance quadratic and reduced it in the algebraic quotient with `cn²=1-sn²`, `dn²=1-k²sn²`, and corresponding v relations. The two linear factors are exactly `(1+k sn u)(U+kV sn u)` with normalization alpha²/q². The translated determinant divided by two is `alpha Bo h d dn(u)(d+kC sn u)/(C D)`. Dividing by TWO focal distances supplies `(q²/alpha²)²`, giving exactly `C0=Bo h d q⁴/(alpha³ C)`. The q⁴ factor and dimensional scaling are correct.

The new exact controls prove zero residuals for the distance, determinant, both product factors, mixed coefficient, dn/cn triple numerators, strict branch-factor gap and outer nonconfocal obstruction. These are polynomial quotient identities, not fitted high-precision equalities. Triple-angle divisions are legal: `C,d>0`, `W>0`, and `Z=W²(1-k²t sn²(2v))>0` for each strict family. No division by V or by an area is used.

The identities `L0=Z dn(3v)`, `L1=Z cn(3v)`, `L0²-k²L1²=k'² Z²>0` imply `L0>k|L1|`; likewise `d>kC`. Every denominator factor of e is positive for real u, as are dn(u), D and C0. Thus e>0 genuinely proves nonvanishing, without assuming product constancy. `L1=0` would require `3v=K` in the permitted interval, giving `N=6tau`, impossible for odd N.

### Branch-fiber and valuation audit

I audited poles using the full Jacobi torus `Y=C/(4K Z+4iK' Z)`, where every function and e is single valued. Translation by `2iK'` fixes sn and changes the signs of cn,dn and e. Pole locations and orders therefore descend to the smaller sn torus `T=C/(4K Z+2iK' Z)` even though e itself is anti-invariant there. This avoids mistakenly treating an anti-period as a period of e. The manuscript explicitly doubles the imaginary period when using compactness for F, so it commits no such mistake.

On T, sn has degree two and derivative square `(1-sn²)(1-k²sn²)`, giving branch values ±1,±1/k. The quarter shift gives `sn(K+iK'+z)=dn(z)/(k cn(z))`, so the first linear factor has roots `r0±v`, value `-d/(kC)`. Its absolute value exceeds 1/k, so both roots are simple, distinct and exhaustive. Squaring permits order two.

For the second factor the roots are `r0±3v`. When cn(3v) is nonzero, its fiber value is `-dn(3v)/(k cn(3v))`. Its squared excess above 1/k² is `k'² sn²(3v)/(k² cn²(3v))`. Thus the only critical fiber in `0<3v<3K` occurs at `3v=2K`, and coincidence of the displayed roots independently gives the same condition. Primitivity forces exactly N=3,tau=1.

In this critical triangle, the factor is `Z(1-k sn u)`, with a double zero at K+iK'. At that point cn²=1-1/k² is nonzero, and `dn'=-k²sn cn` is nonzero. dn has one zero order, cancelling one of the two denominator orders. Also `D=1-t=q>0`, and the first factor is nonzero there. The resulting edge pole is simple, not an overlooked double pole. Our complex controls independently detect a nonzero simple residue for two moduli.

The two denominator fibers are disjoint: equality would force 2v or 4v to be a multiple of 4K, excluded by `0<v<K`. At a common Jacobi pole, sn and dn each have order one, numerator `dn(1-k²t sn²)` has order three, and the denominator has order three with nonzero leading coefficient because k,C,L1 are nonzero. Those points are removable. At any other dn zero the numerator cannot create a pole. The list is exhaustive; no branch point, Jacobi pole or triple-angle division adds a hidden pole.

### Every translated quadratic part, exact divisor and second focus

Jacobi parity and periods give `sn(2r0-u)=sn(u)`, `dn(2r0-u)=-dn(u)`, hence odd reflection of e. If a double Laurent coefficient at r0+v is a, the reflected coefficient at r0-v is -a: squaring the local coordinate preserves its sign while odd reflection reverses the function. Their separation is delta. Coprimality means each list of N delta translates is distinct modulo 4K, and the two lists coincide by shifting the cyclic index by one. Therefore exactly one coefficient of each sign occurs at EVERY candidate translated point. The cancellation is local and universal, not just a total residue sum or finite arithmetic check.

The other poles are already at most simple and lie in this same orbit, since their differences from R=r0+v are delta and -2delta. The critical triangular coincidence was reduced locally before summing; it supplies no additional order. Bézout applied to delta and 4K gives real period L=4K/N. Imaginary shift 2iK' remains an anti-period. Consequently F on `X=C/(L Z+4iK' Z)` has at most the two simple poles R,R+2iK'. If none existed, compactness would force a constant and anti-periodicity would force zero, contradicting the strictly positive real trace. The anti-period pairs the poles, so both occur with order one.

Cyclic reindexing preserves odd reflection about r0. Since 2v is a period of F, reflection can be centered at R. At R+L/2 reflection is a real-period translation, forcing a zero; the imaginary anti-period gives the other at R+L/2+2iK'. These are distinct and not poles. Degree-zero divisors of a nonzero meromorphic function on a compact torus then give the exact divisor

`(F)=[R+L/2]+[R+L/2+2iK']-[R]-[R+2iK']`.

Translation by L/2 swaps zero and pole divisors, hence the product is holomorphic and constant. No uncomputed residue or unsupported all-period identity is required.

For the original centers, `J_fminus(Q(u))=-J_fplus(Q(u+2K))`. Central reflection has determinant +1 and preserves signed area, so the second focal area is the 2K shift of the first. For odd N, `2K=N L/2` equals L/2 modulo L. This proves exactly the target product; positivity proves it positive. A reversal negates both signed areas. Repeating r times repeats every shoelace summand r times, giving product factor r², including even r when the least period remains odd. An odd total traversal necessarily has odd least period.

For a circular billiard, consecutive boundary tangents give radius `Ro=a/cos(pi tau/N)`; central unit inversion gives radius 1/Ro, so each signed area is `N sin(2pi tau/N)/(2Ro²)`. Under similarity s with fixed unit inversion, inverse displacements scale by 1/s and areas by s^-2; with inversion radius rho they scale by rho⁴. The product factors s^-4 and rho⁸ are correct. These deductions do not claim uniform nonsingular limits at k=1 or collapsed caustics. No unresolved mathematical gap or counterexample was found.

## Fresh falsification evidence and portable controls

`independent_controls.py` uses SymPy1.14.0/mpmath1.3.0 in the supplied Python3.14.6 runtime with bytecode disabled. It proves nine exact zero polynomial residuals, and separately performs 85-digit uncertified numerical diagnostics.

The physical part constructs each next billiard vertex by finding tangent contacts from the current point to the scaled caustic unit circle and intersecting that line with the boundary ellipse. Jacobi values specify only the family and starting point, not subsequent vertices. It then solves Cartesian boundary-tangent intersections, performs Euclidean focal inversions and computes signed shoelace areas. Every specular reflection is checked. It covers 54 families, 108 phases, m=0.04,0.6,0.96, N=3,5,7,9,11,15, and EVERY coprime turning number below N/2 for each N. Thus convex and star cases, including reversed outer-axis ordering, are exercised. Maximum closure error is 1.21e-83, tangent-Q error 3.82e-82, reflection error 1.22e-84 and relative product phase error 4.89e-84. Reversal, twofold/threefold repetition, s=2.1 and rho=1.7 pass; three independent circular convex/star polygons match the radius/area formula below 8.80e-88.

The complex part checks periods, anti-period, odd reflection, quotient real period, opposite-focus shift and complementary zero/product identities in five convex/star/triangle cases. It checks opposite quadratic edge coefficients, nonzero simple trace residues, removable common Jacobi poles, and two N3 critical simple residues. A finite 2,350 coprime-rotation lattice sweep supplements the universal indexing deduction. Values are diagnostics without interval certification, and local eps limits are not exact Laurent proofs. The actual exact argument is above. Counts are not presented as independent theorems.

I inspected the documented ten-job harness, its pinned dependencies, scripts and input/output behavior. It rejects optimized Python and incorrect library versions; verifies complete frozen inventory; copies explicitly listed inputs to disposable folders; runs unmodified scripts there; compares scientific JSON strictly; and rechecks integrity. The only environment-field omissions are explicitly named Python text fields, with mathematical fields retained. No hidden network, installer, Git/provider mutation or downloaded executable code was found. Historical ledger generation is correctly excluded from portable replay because it requires private sources. The review01 package utility intentionally targets its older 133-entry frame and is explicitly documented as historical.

All ten jobs had already been replayed repeatedly in the preceding reviews, and their portable bytes are unchanged. I did not claim a fresh ten-job run. I selected two relevant independent replays on this frozen packet: `exact_triangle` and `meromorphic_divisor`. BOTH passed in disposable folders, BOTH outputs were byte-identical to the frozen results, and the whole 87-file portable inventory stayed unchanged. The first checks the exact manuscript datum 1/3600 versus original-vertex 1/324; the second checks the principal-part/critical-case family. The two `HARNESS_*_REPLAY.json` receipts retain exact versions, digests and timings. My distinct new physical and quotient controls provide additional falsification rather than simply repeating every inherited test.

## Actual primary reading, credit and priority limits

I checked the actual private pinned source bytes against all three recorded primary hashes. I read selected complete relevant passages: v11 printed pp2–3 (ellipse-caustic domain and signed areas), pp9–12 (§3.9 and complete Tables9–10); Stachel printed p1614 (Theorem4.3 and4.9); v10 inverse definitions and complete Table9; the final journal companion's inverse section/table and table inventory. The v11 product is exactly the primed ORIGINAL-focus pair product, odd N, with the outer own-focus construction separately distinguished. The strict nondegenerate confocal ellipse scope matches the pinned source setting. The shorter journal companion omits the product and has no900-series table; its Table10 is a video list, not this target.

I also actually read selected primary passages of Garcia–Reznik Prop15, Reznik–Garcia–Helman v2 Prop7/Conjecture1, Ferudun's original-vertex definitions/theorem and focal-distance/pole lemmas, Roitman–Garcia–Reznik final Cor1 and starred area-table entries, KLS introduction/local identity discussion, and the complete Chavez-Caliz Theorem6 proof. These support the stated distinctions and classical credit. In particular, Chavez-Caliz's even untransformed Poncelet/tangent-area proof already uses complementary zero/pole cancellation. The current note credits that exact antecedent rather than claiming a new elliptic principle. The original-vertex focal norm square cannot be transplanted to this generally nonconfocal outer locus; the exact strict obstruction was independently proved in my controls. A proven k806,a ratio could furnish a bridge, but none is presumed.

Fresh official web access was limited to NIST DLMF22.4,22.8,22.13 to verify period/zero/shift, addition and derivative tables. The actual access ledger is `SOURCE_READING_SCOPE.json`; no new worldwide literature search was performed. The standard periods and shifts are consistent with [DLMF22.4](https://dlmf.nist.gov/22.4); the addition and derivative formulas were checked at [22.8](https://dlmf.nist.gov/22.8) and [22.13](https://dlmf.nist.gov/22.13).

I inspected the two priority-family reports, source-to-claim and access ledgers, root acceptance and prepublication qualifications. I did NOT reread every page of every source in their corpus, independently repeat their author inventories, or independently certify an exhaustive literature search. Current wording accurately reflects that scope: no exact general earlier proof verified in the bounded audited corpus; historical novelty undetermined; no first-proof, absolute-priority or present-worldwide-open assertion. Open author versions are not declared byte-equivalent to the inaccessible complete final *Talented* journal text. Selected-passage, unresolved-sequel/video and classification-reading limits remain explicit. Access through an already authorized library could improve the final-edition comparison; no outreach was prepared or initiated.

## Complete package and review01 repair verification

`package_audit.py` is a new read-only audit, not the historical review01 utility. Results:

| Binding | Independently checked |
|---|---:|
| SOURCE_MANIFEST payload rows | 150 |
| ZIP entries, exactly matching those payloads plus source manifest | 151 |
| portable verification payload rows | 87 |
| full current native packet rows | 39 |
| each paired current top-level native manifest | 12 |
| original intake files, identical in EACH of two archived copies | 19 |
| original intake bytes | 68,274 |
| original authored audit-family manifest rows | 7+6+8+8+11 |
| historical whole-review01 authored seal rows | 11 |

Every listed byte size and SHA256, every archive member, safe path, file type, deterministic timestamp, inventory, current seal, source pin and original provenance row was checked. ZIP CRC validation passes. Names are unique, relative, contain no traversal or forbidden private/cache subtree, and are regular files. The only included PDF is the author's manuscript; no primary PDF, text, HTML, screenshot or other primary payload entered the ZIP. Family seals correctly retain their original bases; relocations are resolved only as documented. Metadata in deposit.json equals metadata.json exactly; the two planned deposit file names and hashes agree. There is no invented DOI or publication receipt.

Current native `PROOF.md`, README, SOURCES, WIP pointer, source_record, source_manifest, metadata, research log, prior-report pointer, author checker/result and legacy independent review files were inspected, with all current/historical manifests. The inherited proof hash intentionally refers to the archived original, and is explicitly labelled historical rather than falsely rebound to the amended proof. Mathematical native sections1–7 are byte-identical to review01; all original19 files are byte-identical to intake in BOTH locations.

For review01 M1, the current source record now has a qualified current assessment, explicit original-source pointer/hash and October2020 attribution; old OPEN-TRIAGE/open/year2021 fields are preserved only as clearly identified immutable history. WIP and imported report are current provenance pointers. Branch identifiers are explicitly historical. README, proof header, status and preparation receipts distinguish their dated snapshot stage from later administrative release facts; none asserts the preprint has already been deposited or merged. Their references to later final receipts are legitimate lifecycle pointers, not an invented completed gate. Parent must still append actual future release facts when performing its authorized workflow.

For elected O1, the active bibliography uses the full arXiv-record title, while source_manifest accurately explains the shorter pinned PDF heading. This is a precision reconciliation for the same source. The changed PDF was rebuilt and actually inspected below. Review01's report/seal and root acceptance remain unmodified historical evidence; duplicated root resolution records match exactly. No contradiction or stale active assessment remains in the reviewed current presentation.

## Six-page visual and metadata audit

The current working PDF hash matches the frozen PDF before reuse of root's existing110dpi PNGs. I actually viewed ALL six images. The PDF also reports six pages, no encryption, form or JavaScript. Title, author, ORCID, date, equations, q⁴, periods, theorem scope, source distinctions, links, references, credits, extensive AI disclosure and unrefereed/no human-peer-review status agree with the TeX and metadata. No clipping, overlap, missing glyph, unreadable equation, unresolved reference or placeholder was found. The bibliography remains together on page6 with comfortable margins. The changed longer source title fits correctly.

## Final disposition and remaining limits

This assigned review is complete: 100% of its scope. No mandatory or optional correction is requested. The strongest verified result is the exact all-period proof within its stated source domain, with fresh independent quotient/Cartesian/complex falsification controls, two current byte-identical portable replays, complete151-entry packet verification and global review01 repair verification.

This verdict is bound only to the exact hashes above. It does not establish first-proof priority, worldwide open status, full final-journal access, independent human peer review, formal proof-assistant verification, or publication clearance. The packet appropriately makes none of those claims. No manuscript, PDF, ZIP or frozen payload was edited. No Git/index/ref/branch, native PR, Queue, database, provider, Zenodo or tracker mutation was made; no individual or unrelated chat/agent was contacted. All authored writes stayed in this dedicated review02 folder; no third-party payload is in its seal. Parent retains every promotion and release decision.
