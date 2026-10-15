# Fresh independent preprint and portable-package audit 02

**Verdict: PASS — no mandatory mathematical, source-credit, manuscript, package, or submission-metadata correction found. Assigned review complete, 100%.**

Reviewed target: PR254 /5100020 /AMR-050-0020 /k403,a. This is the second sequential fresh adversarial preprint review. The mathematical reconstruction was written before reading earlier verdicts. The candidate was treated as a hypothesis, and all final receipts bind the unchanged candidate bytes below. This report does not publish, merge, contact an external individual, certify worldwide firstness, or assign a DOI.

## 1. Exact strongest verified result and limits

For every fixed noncircular ellipse with a>b>0, strict nested nondegenerate confocal elliptical caustic, least odd period N>=3, and every admitted coprime star winding 0<tau<N/2, the ordered signed shoelace area of the original-side origin pedal times that of the original-vertex origin antipedal is phase independent. The actual antipedal lines are P dot X=P dot P, and every consecutive real intersection is uniquely finite. The proof allows zero derived signed area and never divides by it. Reversal negates both areas; an r-fold repetition of an admitted primitive cycle scales their product by r². Circular primitive stars have the separately established product N²R⁴sin²(theta)/4. The exact same-caustic N4 diamond/rectangle pair has products225/4 and289/4 and disproves an unrestricted even extension.

**Remaining mathematical gap within this scope: none found. Mandatory corrections: none. Optional editorial suggestions: none needed for readiness.** Hyperbolic/collapsed caustics, unsigned region areas, parity obtained by repeating a list, and other derived polygons do not follow from this theorem. No assertion of nonzero antipedal area is needed. The general theorem is established analytically; computations below are finite exact corroboration and non-interval numerical diagnostics. Human journal review, proof-assistant certification, and historical firstness are not provided and are not claimed.

## 2. Independent checkable derivation and adversarial challenge

The complete pre-verdict reconstruction is in `INDEPENDENT_DERIVATION.md`. Its decisive steps are summarized here so that the verdict does not depend on an earlier PASS.

1. **Actual area, no hidden normalization.** For edge P,Q, solve the named antipedal lines to obtain the outgoing intersection P+[(H(Q)-P dot Q)/det(P,Q)]JP, where J(x,y)=(-y,x). Solve the preceding intersection similarly. The local determinant equals H(P) times the sum of the incoming/outgoing coefficients. Grouping each original edge's two half-determinant contributions gives exactly F(P,Q)=[H(P)H(Q)-(H(P)+H(Q))(P dot Q)/2]/det(P,Q). Thus U=sum F is the actual signed area. Complex dot products are bilinear; no division by H(P), square-root normalization, convexity, or area nonvanishing is used. A fresh finite complex example with isotropic P=(1,i) confirms the named intersections and this identity.

2. **Canonical input and complete determinant divisor.** With v=2Ktau/N, delta=2v, p=iK', s=sn(v), c=cn(v), d=dn(v), canonical coordinates give B(u)=2absc dn(u)/D(u), D=1-k²s²sn²(u). Real positivity follows from s,c,dn(u)>0 and D>=1-k²s²>0. For complex u, sn² has degree two on the2K,2p support cell: D has a double pole at p and exactly two simple roots p±v, with D'=±2cd/s. Consequently B has simple poles at p±v, a simple zero at p, and a simple zero at K+p with D=c². These exhaust its support and orders. The support cell uses the imaginary antiperiod only as a congruence; the proof's actual torus below has period4p.

3. **Opposition is retained; coincidence is removed.** At midpoint p, both endpoints are regular and opposite; a regular numerator over the simple B zero has at most a simple pole, and this contribution must remain. At midpoint r=K+p, endpoints are regular and coincide. The numerator identity4num=(H(P)+H(Q))H(P-Q)-(H(P)-H(Q))² gives order at least two, including isotropic vectors, so division by a simple determinant zero is removable. A reviewer-owned isotropic local control gives numerator -z²-z³/2 and F tending to zero; it does not require an identically-zero numerator.

4. **Incident double poles cancel exactly.** At a vertex pole, only that vertex is singular, both neighbors are regular, and an individual incident F has order at most two. The identities P(p-z)=-P(p+z), previous-neighbor reflection, F antisymmetry, and joint-negation invariance make the two incident terms exactly G(z)-G(-z). The possible even z^-2 Laurent term cancels. Odd coprimality precludes two singular endpoint vertices on one edge. For N3, the edge between the two regular neighbors is the separate opposition contribution, bounded by a simple pole. It is explicitly included.

5. **Odd lattice and actual torus.** Put ell=2K/N. gcd(2tau,N)=1 gives real period ell from the2K and delta periods. Reflection under2p preserves dot products and reverses determinants, so U is2p-antiperiodic. Vertex-pole phases p-jdelta and opposite-midpoint phases p-v-jdelta become the same p,3p classes because v=tau ell. Thus U is meromorphic on X=C/(ell Z+4p Z), with only possible simple poles at p,3p.

6. **Trace uniqueness and complete forced zero divisor.** S=sum dn(w+jdelta) is even, ell-periodic and2p-antiperiodic. Exactly one summand contributes at p with residue-i; the residue at3p is+i. Therefore the two simple poles cannot cancel. Negation followed by ell+2p fixes p+ell/2 and negates S, forcing a zero; likewise at3p+ell/2. They are distinct nonpoles. Total zero order equals total pole order on the compact torus, so these two zeros are complete and simple. S(w)S(w+ell/2) is holomorphic and constant. Matching a function's residue at p to S matches the3p residue by antiperiodicity; the holomorphic difference is a constant forced to zero by its antiperiod. Hence U=c_star S, including the zero function. This does not assume the desired area product.

7. **Credited actual pedal, not a substituted polygon.** The caustic tangent normal n=(-sn(u)/alpha,cn(u)/beta) satisfies n dot n=dn²(u)/beta², giving actual origin foot Q=(-alpha k'^2 sn(u)/dn²(u),beta cn(u)/dn²(u)). Q vanishes holomorphically at common Jacobi poles; its only possible coordinate poles are double at dn zeros r and translates. Reflection Q(2r-z)=Q(z) makes its pole chart even. The incident determinant sum contains Q(r+delta+z)-Q(r-delta+z)=O(z), so the pedal area trace T has at most simple poles at r,r+2p. Its correct real period and imaginary antiperiod give T(u)=c_p S(u+K) by shifted uniqueness. Actual sides use u=w+v.

8. **Conclusion, units, and boundaries.** The product is c_p c_star S(w+v+K)S(w). Since (v+K)/ell=tau+N/2 is half-integral, it is the proved half-shift constant. Both coefficients have area units; the product scales as length⁴. Strict inequalities keep every local coefficient and neighbor regularity valid pointwise, including arbitrarily close interior limits. The circle is handled directly with radii Rcos(theta/2) and R/cos(theta/2), not by inserting k=0 into a degenerate torus. No central difficulty is transferred to an equivalent unsupported claim.

The independent derivation, generic symbolic code in the package, and reviewer-owned exact controls jointly test construction identity, pole support, pole order, N3 collision, signed reversal/repeats, isotropic normals, limits, and units. No mathematical counterexample or hidden assumption was found.

## 3. Candidate integrity

Every supplied expected hash independently matched before extraction, and the final audit rechecks the same bytes.

| Candidate path relative to preprint | Bytes | SHA256 |
|---|---:|---|
| odd_origin_area_product.tex | 16257 | e2f115f1eee7489a9d888b9d1b639ac851e5442402fd453556612c1f39e3e8fd |
| output/pdf/odd_origin_area_product.pdf | 70407 | 687c633a92a61f1962d719be628ef5e119e077846254456f89a088d5fd13f34f |
| odd-origin-area-product-verification.zip | 170660 | 99666e523c0b78c2c8f73b8d42ed993d207a210b50cf12cd908c455cc4ad6d26 |
| metadata.json | 2011 | e468d37d5e5aea602e7572bc22f12c4576c28f74e4554e1568f77c177167b3d7 |
| zenodo-deposit.json | 2236 | f70de8848c1a874a7a582cc39dfffd16141bf067bee9c7337664c54397ec86a0 |

Safe extraction checked absolute paths, traversal components, duplicate names, and symlinks. The archive has exactly50 files. Its49-entry MANIFEST hashes every file except itself; every size and hash matches, and the file set is closed with no unexpected entry. Package manuscript/metadata bytes equal the standalone versions. Nine unique CHECKSETS entries match the current scripts and expected files. `INITIAL_INTEGRITY.json` and `PACKAGE_INTEGRITY.json` record all pins.

The archive contains authored proofs, reports, construction code, expected receipts and bibliographic pins. It contains no whole external PDF/archive/source text, rendered third-party image, or raw web/provider response. Historic manifests preserve original paths and excluded-reading-copy pins; README correctly explains that these are provenance and not runtime dependencies. The original candidate/pending-review labels belong to the historical proof, while current manuscript and root acceptance identify the current state. Initially failed historical reviewer scripts are absent from executable successful checksets. Fresh manuscript reviews remain outside this frozen ZIP, so their creation does not silently alter the reviewed package.

## 4. Actual reproduction and portability

I read the complete frozen runner, original proof and all nine complete checker programs. I then ran the extracted frozen runner using the supplied read-only runtime: Python3.14.6, SymPy1.14.0, mpmath1.3.0. The runner passed all nine complete receipt comparisons. A second execution of the same frozen runner retained actual full receipts via reviewer-only capture; all nine again match, ignoring only top-level `utc` and `elapsed_seconds`. This extra replay was to retain full receipt artifacts and their hashes, not to enlarge sampling evidence.

| Checkset | Reproduced evidence |
|---|---|
| author_exact | 14940 exact assertions;1104 finite odd lattice families;300 rational polygons |
| author_numeric | 19296 diagnostics;72 families;95 digits;maximum scaled residual3.7521231e-91 |
| original_independent_exact | 15698 exact assertions;240 rational polygons |
| original_independent_numeric | 1820 diagnostics;14 families;80 digits;maximum scaled residual3.2532814e-79 |
| complex_exact | 25369 exact assertions and finite lattice controls |
| complex_near_poles | 3494 diagnostics;19 families;220 digits;maximum residual2.96395561209e-121 |
| cartesian_exact | 302 exact construction/symbolic checks;4141 finite primitive odd lattice controls |
| cartesian_numeric | 139411 diagnostics;94 noncircular families/282 phases;180 digits;five circular families |
| priority_construction | Complete exact construction-distinction receipt matches |

`REPRODUCTION.json` pins source, expected, actual full and normalized receipts, including the exact ignored-key list for each checkset. `RUNNER_OUTPUT.json` preserves the actual runner's outcome, and `actual_receipts/` retains all nine full computed receipts. These are authored computational outputs, not raw external-provider responses.

The runner copies each self-contained checker to an isolated scratch directory and leaves the distributed package untouched. The code imports only standard-library modules and the two pinned dependencies; it has no repository-path, historical-manifest, external-reading-copy, NumPy/SciPy, network, or credential dependency. README's Python>=3.11 instructions and Windows executable adaptation are consistent with the code. Actual execution was on macOS/Python3.14.6; every OS/Python combination was not separately executed. Numerical checks are expressly diagnostics, and none is promoted to an interval certificate or universal proof.

Reviewer-owned `independent_controls.py`/`INDEPENDENT_CONTROLS.json` independently verify the isotropic complex line identity and removable coincidence, exact reflected/tangent same-caustic N4 products, and the actual failure of the focal-to-origin/central-pair transfer. One initial reviewer control assertion mistakenly demanded an identically-zero isotropic numerator; it was corrected to the relevant exact second-order condition and logged. This was a reviewer-only control mistake and required no candidate change.

## 5. Source authentication, credit, and earlier-combination test

The original three primary PDFs match their source-manifest hashes. I checked source definitions in full relevant sections and visually inspected v11 Table5 p7 and the published Table5 p348. Both show the unprimed original-origin signed product with odd N. The authentic v11 PDF title is *Eighty New Invariants in the Elliptic Billiard*, which the manuscript cites correctly despite the landing-page title difference.

The published Stachel Theorem4.3/(4.9), [DLMF22.4](https://dlmf.nist.gov/22.4), [DLMF22.8](https://dlmf.nist.gov/22.8), [DLMF22.9](https://dlmf.nist.gov/22.9), AST complex billiard precedent, KLS §2.1.1 and Khare–Sukhatme equations13–15 all agree with their stated roles. The note expressly calls the parametrization, complex analysis and cyclic/Landen tools established. It credits RGK's observation and the earlier immutable PR204 pedal mechanism. It makes no claim to discover the invariant, the generic F formula, or the analytic method.

The strongest tempting covering combination is earlier PR204 plus a proved constant A*_O/A. I read PR204 completely, read the original deposited focal-product manuscript completely, and tested the latter's actual antipedal lemma beyond its title. It requires a centrally paired orbit and a fixed focus. Odd nonzero primitive vertices have no central pairing; padding repeats does not create opposite vertices. Its focal norm identity imposes c²=a²-b², so c=0 specializes to a circle. For the strict reflected odd triangle with outer squared axes8,5 and caustic squared axes32/9,5/9, the fresh exact origin ratio is441/80; the earlier focal coefficient is36/5, and its origin norm specialization has residual-3. Thus this transfer fails two actual hypotheses. Extending it would introduce the very construction-specific claim still needed, so the route is blocked absent a new bridge.

The AST odd original/outer ratio, even original/outer product, conic-grid/polarity, triangle and smooth-envelope routes use different actual lines or functionals. An origin antipedal line has normal P and varying offset H(P); the boundary tangent uses diag(a^-2,b^-2)P and fixed offset. Circular polarity of the correct inverse vertex lies on a quartic. Merely invoking a conic theorem or an N-fold circumcenter similarity does not establish the missing single original-origin area trace. These mechanisms were tested rather than rejected by title.

`SOURCE_AUTHENTICATION.json` independently confirms41 primary/classical source-pin entries (three repeated primary entries),11 original deposited-file SHA256/provider MD5 pairs,21 current adjacent archive/manuscript pairs,7 earlier repository proofs, and all23 original intake files. All21 adjacent abstracts and theorem statements were freshly screened; the strongest focal proof received a full read. I read the included authored mathematical/priority reports and derivations after forming the independent mathematical conclusion. `FRESH_PRIORITY_NOTES.md` records exact fresh searches and attribution reasoning.

The fresh [primary catalogue](https://eulersolve.org/papers/) and [focal-product page](https://eulersolve.org/papers/amr-050-0021/) were reopened. Direct0020 access failed; the failure is explicitly not absence evidence. No earlier full or genuinely covering proof was located in the bounded inspected corpus. This does not certify worldwide firstness, current global openness, causality between authors, or absence of inaccessible/private/unindexed/non-English work. The manuscript's bounded framing accurately reflects those limits.

## 6. Actual five-page rendering and metadata

Independently rendered the actual70407-byte candidate PDF with `/opt/homebrew/bin/pdftoppm` at120dpi and visually inspected all five pages. The title, author, independent-researcher affiliation, ORCID0009-0001-9320-500X and date13October2026 are correct on page1. Equations, signs, subscripts, cross-references, theorem/lemma numbering, bibliography links, page numbers, and both N4 product values are legible and match the source. No clipping, overlap, missing glyph, black box, broken formula, or unreadable reference was found. Ordinary proof and sentence continuation across pages2–4 preserves content. Page5 carries the extensive AI disclosure and unrefereed/no external human review/no proof-assistant statement.

Poppler reports exactly five letter pages, PDF1.5, unencrypted, no forms or JavaScript, title *An odd-period pedal-antipedal area invariant in elliptic billiards*, author Alec Kriebel. The creation timestamp is2026-10-13UTC (displayed locally as12OctoberPDT), consistent with the dated paper. Source/PDF substantive content agrees. `RENDER_VERIFICATION.json` pins each actual render separately; `SUBMISSION_METADATA_CHECK.json` preserves PDF metadata and checks.

The standalone, archive, and deposit metadata agree exactly: publication/preprint, open access, version1.0, publication_date2026-10-13, CC-BY4.0, correct author/ORCID and same carefully bounded description. LICENSE applies to authored materials and excludes external papers/raw extracts. The deposit's `files` contains exactly two OBJECT paths, the reviewed PDF and ZIP. Both exist with the reviewed pins. No candidate DOI or phantom DOI appears. Existing cited DOIs concern actual prior sources. The candidate is a reviewable upload kit; upload, publication, tracker updates and native merge are the parent's later actions.

## 7. Review custody and final disposition

All reviewer-authored work is under `preprint/review_02/`; no candidate, branch, Git index/ref, deposit, tracker or Sheet was changed. Main was confirmed. No external individual, unrelated chat, source author or provider was contacted, and no outreach was drafted. Only the authorized research-agent team received progress.

The final manifest separates authored reports/code/computed receipts from rendered pages and excludes `private_reading/`, extracted candidate copies, and all third-party raw sources. Self-hashing is omitted to avoid recursion. All candidate pins and actual receipt hashes are frozen there. Parent can independently verify this report and manifest before proceeding with its authorized publication workflow.

**Final assigned verdict: PASS, completion100%, mandatory_corrections=[]; strongest verified result is the universal exact scoped signed-area product theorem with finite real constructions and direct circle extension. No unresolved substantive concern remains within this review.**
