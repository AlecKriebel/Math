# Fresh independent source and mathematical-interface review

Review family: `teich_source_01`. PR1033, problem11000026. Submitted head: `6322305d37b8131f034a1b4c3c5e861e4b04844f`. Review performed 2026-10-13 UTC.

**Assigned-family verdict: CLEAN.** The fresh primary-source review supports the submitted exact-metric, original-closed-ball claim for every fixed closed oriented genus at least two. I found no missing center/radius/endpoint/thickness hypothesis, normalization error, closed-boundary loss, source-scope contradiction, or unsupported mathematical step at the theorem-to-claim interface. The checkable independent proof is in `DERIVATION.md`. This verdict uses established external Teichmüller theorems, and does not certify priority, historical novelty, or worldwide current open status.

## Independence and immutable inputs

I first read `SUBMITTED_PINS.json` and the submitted `PROOF.md`, reconstructed the exact claim, retrieved primary bodies afresh, inspected their text and critical page images, and saved my own `DERIVATION.md`. Only afterward did I read the other seven submitted files, including `INDEPENDENT_AUDIT.md` and the acceptance labels. I did not read another new review family's report or communicate with another such family. The old audit was comparison material only and did not determine this verdict.

All eight original authored files were checked against the supplied head capture on input and again on output. The SHA-256 and byte checks are identity controls, not mathematical evidence. No submitted file, candidate file, Git state, index, branch, queue, PR, service, or publication was changed by this review. All review artifacts and downloaded third-party source bodies are confined to `reviews/teich_source_01`; raw bodies, extracted text, and rendered page images are confined further to `sources/raw`. No person was contacted and no agent was spawned.

## Exact hypothesis and success criterion

For each fixed \(g\ge2\), the hypothesis asserts existence of a finite \(c_g\ge0\) before selecting the center, radius, and endpoints. All distances and metric lengths use

\[
d_T(X,Y)=\frac12\inf_h\log K(h).
\]

For every center \(o\), every \(r\ge0\), and every \(x,y\in\overline B_T(o,r)\), success requires an actual continuous rectifiable path \(\gamma\) whose full image is in that same original closed ball, with

\[
L_T(\gamma)\le d_T(x,y)+4c_g.
\]

Thus the constants \(N_g(k)=k+4c_g\), for every fixed \(k>0\), and \(C_g=2+4c_g\) must be chosen independently of the center and radius. A path in a radius-\(r+c_g\) ball, a path in a quasiisometric wall model, or an intrinsic-distance infimum without an actual bounded-length path would not meet the claim. No quantitative numerical value and no constant uniform over genus is asserted.

## Fresh primary-body evidence and exact locators

All four necessary PDFs were retrieved directly on 2026-10-13. `SOURCE_RETRIEVALS.json` records requested and resolved URLs, UTC times, HTTP metadata, byte counts, and hashes. `SOURCE_MANIFEST.json` records exact editions and relevant body/visual locators. `VISUAL_LOCATORS.json` records the 19 page images actually inspected. Fresh source hashes also match the submitted `SOURCES.json` pins, but the mathematical judgment rests on the bodies and derivation.

| Primary source | Edition and verified locator | Fresh PDF bytes / SHA-256 |
|---|---|---|
| [Lenzhen–Rafi](https://www.math.toronto.edu/rafi/Papers/Convexity.pdf) | JDG88(2011),267–295. Setting and Theorem A: printed267/PDF1. Theorem C and constants: printed268–269/PDF2–3. Main theorem: printed282/PDF16. Its case proof: printed283–284/PDF17–18. Ball theorem/proof: printed284–285/PDF18–19. Earlier setup and estimates: printed269–281 body text; Definition12 and Lemma14 additionally inspected visually on printed279 and281. | 267927 / `179455d195b0f24cac238283063bc82d34db1d529a9b26f0f0193b7f14aaa409` |
| [Farb](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf) | Original chapter in the public book PDF. Printed10/PDF17 defines closed oriented \(\Sigma_g\); printed24/PDF31 defines distance-two almost convexity; printed25/PDF32 asks Question3.5. PDF metadata creation:2006-07-24. | 2724624 / `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a` |
| [Fortier Bourque–Rafi](https://arxiv.org/pdf/1606.05170v3) | arXiv1606.05170v3,2017-08-29; title-page version and [version page](https://arxiv.org/abs/1606.05170v3) freshly checked. §2 p4 gives half-log normalization; p5 gives minimizing Teichmüller lines through every pair; p6 gives Kerckhoff (2.2); p7 gives continuity and closed-ball description. | 519853 / `a49397b9921f675846f396a38bec398794b4b470dc0226c66f58ecacd02d0376` |
| [Petyt–Zalloum published PDF](https://link.springer.com/content/pdf/10.1007/s00208-026-03534-1.pdf) | Mathematische Annalen396:38(2026), DOI10.1007/s00208-026-03534-1. Actual57-page publisher PDF; p1 publication stamp:2026-09-15; p7 definition, Theorem I, and scope discussion visually inspected. | 1496964 / `114c0b088c9bb8b9cf34f71789c3c6d2d88e192e3b4906e5a2b3fb83eca56e6d` |

The browser tool failed to retrieve the DOI wrapper with an Internal Error. The separate publisher-PDF HTTP retrieval succeeded: it returned the genuine application/pdf body, whose typography, first-page DOI/title/publication date, total57pages, and critical p7 were verified. The resolved URL gained a cookies-not-supported query, which is recorded rather than suppressed. FR's PDF creation metadata is2021-07-05, while its manuscript version is explicitly v3 dated2017-08-29; rendering metadata is not treated as a version date. No failed fetch, search snippet, abstract-only reading, or current-status label supplies theorem evidence.

## Whole theorem-interface audit

### Topology and the actual metric

The submitted fixed closed oriented genus \(g\ge2\) surfaces have negative Euler characteristic and finite topological type, exactly within LR's conformal/hyperbolic setup. There are no puncture, boundary, marked-point, or low-complexity qualifications introduced by the deduction. LR works directly in Teichmüller space equipped with the Teichmüller metric, not a wall, curve-graph, marking-graph, or thick-part metric. FR §2 p4 independently fixes the same half-log dilatation normalization and homotopy class of the marking change.

FR §2 p5 states both needed existence assertions: Teichmüller lines are minimizing geodesics and every distinct pair lies on one. That gives radial and middle minimizing segments, whose metric lengths equal the corresponding actual distances. The source says more (uniqueness), but this deduction needs only existence. Constant paths cover equal endpoints. The proof does not need compactness, a geodesic projection, a continuous selection of geodesics with varying endpoints, or a global radial map.

### Uniform extremal-length input, including the thin cases

LR Theorem15 p282 puts \(K\) before all measured foliations, all Teichmüller geodesics, and all ordered triples. LR's p268–269 notation convention makes all comparison constants depend only on the topology of the fixed \(S\). The proof is consistent with this quantifier order:

| Source proof component | Mechanism and uniformity audit | Remaining dependence |
|---|---|---|
| Thick-thin setup, p269; estimates through p278 | Thresholds are fixed small constants, with a bounded number of pieces for fixed topology. Short curves are retained and handled by annular terms. No lower bound on the actual surface's injectivity radius is assumed. | Earlier length-comparison results cited by LR are established external input. |
| Theorem8, pp275–276; Corollaries9–10, pp277–279 | Extremal length is estimated using thick components, short-curve annuli, and twisting. Finite piece counts ensure at least one contribution is a topology-uniform fraction of the whole. The choice of piece can vary with the surface/curve without varying the eventual comparison constant. | LR's cited Minsky/Rafi estimates are not reproved here. |
| Lemmas13–14, pp279–281 | Contributions of subarcs and changes in decompositions are controlled with topology-only comparisons. The bounds explicitly accommodate pieces changing as the geodesic moves. | Technical geometric lemmas remain within the published LR theorem foundation. |
| Theorem15 reduction, p282 | Uniform curve bounds pass to all weighted curves and then all measured foliations by density/continuity. One fixed multiplicative constant survives the limit. The proof separately treats a short curve at the intermediate time rather than discarding it. | Continuity/density and LR's cited short-curve results. |
| Proposition16 cases1–2, p283 | A significant horizontal thick-piece or flat-annulus contribution grows at least at the geodesic stretch rate; comparison scales cancel that growth. If an annular core ceases to be short, the proof switches to the new decomposition. This is exactly the situation that would invalidate a hidden thick-part-only argument. | No new thickness, time interval, or radius parameter. |
| Proposition16 case3, pp283–284 | Expanding-annulus contribution is recovered using the arc estimate; the exponential factors cancel inside a logarithmic ratio. Reversing geodesic time treats the vertical alternative. | Same topology-only constants. |
| Theorem17, pp284–285 | Extrema of distance are bounded using Theorem15 and the half-log extremal-length ratio. The proof explicitly gives a non-strict pointwise center-distance inequality. | Kerckhoff's formula. |

I do not represent this review as a new proof of every foundational estimate in LR's bibliography. The interface inspected here is the complete route used to state a uniform Theorem15 constant and convert it into the required center-distance bound. No dependence on radius, center, endpoints, the chosen foliation, thickness, or injectivity radius is introduced by that route.

### Direct half-log conversion and closed boundary

Enlarge LR's constant to \(K_S\ge1\) and define \(c_S=\frac12\log K_S\). For each essential simple curve \(\alpha\), divide its Theorem15 inequality at \(z\in[a,b]\) by \(\operatorname{Ext}_o(\alpha)>0\) and take one half of the logarithm. Each endpoint ratio is at most its Kerckhoff distance. Taking the supremum over curves gives

\[
d_T(o,z)\le\max\{d_T(o,a),d_T(o,b)\}+c_S.
\]

This works for arbitrary \(o\), which need not be on the geodesic. It avoids needing to choose a maximizing measured foliation. The p284–285 printed proof proves this same non-strict inequality, independently of what LR means by unadorned \(B(x,r)\). Endpoint and constant-segment cases are immediate with \(K_S\ge1\). Thus the source result includes the exact closed-ball boundary needed for inward-retreat points at radius \(r-c_S\).

### Source presentation observations

LR's printed Theorem17 proof switches between \(\mu\) and \(\gamma\). Its intended single extremal-length argument is unambiguous, and the supremum-over-curves proof above removes the notation and any attainment concern altogether.

Also, printed Definition12(3), p279, omits an orientation condition for the expanding-annulus restriction that Proposition16's Case3 explicitly includes on p283. This is an upstream presentation ambiguity: a literal use of that definition alone would overstate the proposition's proved case. It does not add a missing hypothesis to the submitted invocation of Theorem15. Theorem15 p282 actually selects a significant contributing restriction, distinguishes its horizontal/vertical direction, and reverses time for the vertical case; thus its use supplies the condition printed in the Case3 proof. The submitted proof cites the universal theorem itself rather than invoking the overbroad literal definition. Orientation ties can be included using weak comparisons (the exponential lower estimate has the same fixed factor) or continuity. I record this observation because the whole source interface was inspected, without promoting a typographical omission to a counterexample to the theorem.

These are not candidate-blocking findings. An optional exposition improvement would be to include the explicit supremum-over-curves conversion from `DERIVATION.md` in a future author revision. The current submitted proof correctly states the conversion and does not require that change.

## Attempts to falsify the source-to-original-question bridge

| Potential failure | Check | Result |
|---|---|---|
| Radius-dependent quasiconvexity allowance | LR TheoremC and17 quantify one constant before every center/radius; Theorem15 proof/notation fixes topology dependence only. | Rejected. |
| Foliation-dependent allowance or limiting loss | Theorem15 quantifies one K before every measured foliation; continuous limits use that same K. Curves already suffice for the metric formula. | Rejected. |
| Center constrained to the segment or a thick subset | The denominator in Kerckhoff's formula is at arbitrary \(o\); LR ball theorem quantifies every center. | Rejected. |
| Extra two-fold normalization factor | Both FR's metric definition and (2.2) use half logarithms. The correct allowance is \(c_S=(\log K_S)/2\). | Rejected. |
| Only an enlarged final ball obtained | Apply the inequality to retreat points inside radius \(r-c_S\); the allowance returns exactly radius \(r\). | Rejected at application interface. |
| Closed boundary excluded | Non-strict pointwise inequality is printed and independently derived. No open-ball shorthand is used. | Rejected. |
| Radial retreat cannot be placed exactly | Minimizing segments are isometric intervals; select a point at the stated radial distance, or the center. | Rejected. |
| Path length computed in a different metric | Every segment and its metric length uses FR's actual Teichmüller distance. | Rejected. |
| Only an intrinsic infimum, not a path, established | Three actual minimizing segments concatenate into a continuous rectifiable path with the stated upper bound. | Rejected. |
| Fixed distance-two definition not covered | Farb's original preceding definition is distance two; the estimate specializes to \(2+4c_g\) for all centers/radii. | Rejected. |
| PZ's disclaimer is a contrary theorem | Actual publisher p7 applies TheoremI to \(X_C(S)\) and distinguishes that theorem's reach from original metrics. It states no obstruction to an independent LR deduction. | Rejected. |
| Nonconvex Teichmüller balls contradict bounded detours | FR's nonconvexity concerns the direct geodesic. The path constructed here has radial pieces and a different middle geodesic. | Rejected. |
| Claim requires genus-uniform constants | The submitted claim fixes genus before choosing the constant, matching the source's topology dependence. | Rejected. |

The corner cases \(r<c_g\), \(r=c_g\), \(r=0\), \(c_g=0\), coincident endpoints, endpoints at the center, and boundary endpoints are all consistent with this interface. The independent general-metric family has been assigned the full retreat-lemma verification. I have not used its report as evidence here.

## Original question and PZ scope

Farb's p10 notation fixes a closed oriented genus-g surface. His p24 sphere-pair definition uses separation2 and a radius-independent path bound inside the original ball, before p25 asks Question3.5 in the Teichmüller metric. The submitted theorem is stronger: it covers every pair in the closed ball and all centers, and immediately specializes to that definition. The broader every-fixed-k formulation is separately stated on PZ's actual p7. The submitted theorem independently gives that formulation as well, with \(N_g(k)=k+4c_g\). No claim that all conceivable definitions are equivalent is needed.

PZ TheoremI gives \(k+6\) in the dual wall space \(X_C(S)\). The following discussion limits what their own theorem answers after an equivariant quasiisometry; it does not deny the existence of exact-metric paths, and imposes no additional condition on LR's theorem. The submitted proof correctly attributes its substantive geometric input to LR and uses no \(k+6\) constant or quasiisometric transfer. This source check neither establishes nor rejects historical priority of the elementary deduction.

## Comparison with all eight authored files

After the independent derivation, the public `PROOF.md` and frozen `PROOF_AUDITED.md` were compared: the two recorded editorial changes clarify Theorem15 as the extremal-length part of TheoremA and label the intrinsic-distance estimate a consequence. The mathematical claim and argument agree. The current wording is more precise.

`README.md`, `ACCEPTANCE.md`, and `STATUS.json` describe the same fixed-genus, all-center, all-radius, closed-ball, actual-metric result, and disclose the external published foundation and lack of numerical, formal, or computational proof. `SOURCES.json`'s four PDF identities freshly match the retrieved editions and locators. `MANIFEST.json` lists exactly the eight authored files and correctly pins the other seven. The older `INDEPENDENT_AUDIT.md` reaches a compatible mathematical conclusion, but it supplies no premise or evidence for this fresh verdict.

No authored-file mismatch requiring repair was found within this assigned source/theory family. I have not certified every historical provenance statement or the older bounded novelty-search conclusion; novelty/current worldwide status are outside this assignment and not needed for the mathematical deduction.

## Strongest verified result and exact remaining gap

**Strongest verified result:** with the standard published LR Theorem15, half-log Kerckhoff formula, and Teichmüller minimizing-geodesic theorem as explicit external dependencies, the submitted theorem applies uniformly to every fixed closed oriented genus \(g\ge2\), every center and radius, and every endpoint pair in the original closed ball. The bound is \(d_T(x,y)+4c_g\), including \(N_g(k)=k+4c_g\) and Farb's distance-two specialization.

**Remaining mathematical gap in this assigned family:** none at the published-theorem interface or source-to-question deduction. The external dependencies are not claimed as newly proved, and technical source presentation observations are recorded above. No computational experiment is needed for this symbolic proof and none has been offered as mathematical evidence. Input/output pin checks confirm immutable materials only.

**Required repair:** none in this family. **Optional improvement:** add the direct curve-supremum derivation to the public exposition if the author wants a completely explicit conversion. **Unresolved questions outside this family:** priority and historical/current literature status, plus independent assessment of the general metric lemma by its separately assigned family.
