# Fresh R2 adversarial whole-publication review of PR110

Verdict: **PASS for this exact immutable candidate; no required repairs.** The real mathematical result is a complete proof of the ordinary positive focal antipedal sum equality for every regular nonretracing closed orbit between the specified strictly nested confocal ellipses. The source-domain match, attribution, appropriately bounded priority wording, portable verifier, four-page PDF and support archive pass this fresh review. This report is an independent AI-agent review, not conventional human refereeing or permission to publish, merge, release or deposit.

R2 began from scratch, derived its own verdict before sealing, and did not inspect the R1 review folder/report. Root/author clearance flags were authenticated as historical inputs and were never used as mathematical proof or a novelty certificate. Writes were restricted to this R2 folder; no candidate, Git, service, publication state or UI tab was changed. No individual was contacted. Review completion: 100% of the assigned R2 scope, with the literature boundaries below retained.

## 1. Exact input and archive authentication

The external candidate seal is 6,538 bytes, SHA-256 `691ae196a8a18472bac50df9202477fb1eb48428091b27258a371fecdfc946c7`. All **34** actual candidate files match its path/size/hash rows with no missing, extra or symlink member. The candidate PDF is 65,142 bytes, SHA-256 `e22022885002a991cbe6737f14b86a49d758dcb8095305bf4778927f4aa40215`. The support ZIP is 113,446 bytes, SHA-256 `6265802b2f049f06f7d1313b04774e0064fedd65c21ea298e72863579cf5d684`.

All **33** unique ZIP members were fully decompressed, CRC-checked, checked for safe relative paths and symlinks, and compared byte-for-byte with the adjacent files. ZIP membership is precisely all candidate members except the ZIP itself. `PACKAGE_MANIFEST.json` covers precisely the 31 payload files excluding itself, `SHA256SUMS` and ZIP; `SHA256SUMS` covers precisely the 32 non-ZIP/non-sums files. Every digest matches. The earlier 15-file source manifest and its seal remain internally consistent and are clearly described as an earlier source-only checkpoint.

The exact manuscript is 12,111 bytes, SHA-256 `c942322cf81a5083e0bc9a7c0ebe07b2604db75b68ef56b0258afbf28a149e64`. Binding, source manifest, both authored verifier outputs, both root reproduction outputs, build provenance and candidate seal all agree on those bytes. All **16** original preserved authoring source pins match actual files. `INPUT_PINS.json` additionally pins the exact primary PDFs and boundary ledgers used here. It distinguishes complete source reading, targeted reading and historical coverage metadata; no third-party source bodies are included in this public review payload.

The original `source_record.json`, `PROOF.md` and nonempty imported prior report were read. The imported `OPEN-TRIAGE` report expresses an earlier literature search and is not accepted as current proof of openness. Its proposed reduction through signed-area invariants lacks a valid observable transfer and is unnecessary to this proof. The modern package corrects both the source-domain interpretation and that historical/current-status distinction.

## 2. Independent reconstruction and attempted falsification

### Ordinary antipedal norm

After translating the focus to zero, the two defining lines require `Q·A=|A|²` and `Q·B=|B|²`. Put `A=(r,0)` and `B=(s cos α,s sin α)`. Solving gives `Q=(r,(s-r cos α)/sin α)` and

`|Q|²=(r²+s²−2rs cos α)/sin² α=|A−B|²/sin² α`.

The unsigned triangle-height formula is `h=rs|sin α|/|A−B|`. Hence the positive root is **`|Q|=rs/h`**. Noncollinearity guarantees uniqueness and finiteness; positive `r,s,h` guarantees strict positivity. No sign of an oriented radius is silently selected. This is also the elementary triangle identity `|Q|=2R_triangle`; neither this classical ingredient nor generic telescoping is claimed new.

### Orientation: the essential global step

Every contact point of a tangent to the strictly inner ellipse is inside the outer ellipse and strictly between the two outer chord endpoints. At a boundary vertex the two rays toward the two caustic contacts form the visible tangent cone and put the entire inner ellipse on opposite sides of these two outward-from-vertex rays. The incoming edge points oppositely to its ray toward the preceding contact. Continuing along the **other** tangent therefore preserves the side occupied by the caustic. By induction, every nonretracing orbit has one consistent side; reversing the full list selects the left side.

This local propagation uses neither vertex ordering nor polygon convexity. Self-intersections do not invalidate it. It also applies when an odd primitive polygon is repeated and the total list length becomes even: central pairing is not substituted for the actual continuation rule. An arbitrarily assembled polygon with branch switches or immediate retracing would not satisfy the hypothesis and does not inherit this conclusion.

### Independent endpoint-angle derivation

For a left-oriented edge the origin is strictly on its left, so `det(A,B)>0`. In the outer-ellipse angle parameter choose consecutive lifted endpoints `s−d,s+d` with `0<d<π/2`. Write `C=cos s`, `S=sin s`, `U=cos d`, `V=sin d` and `D²=C²/a²+S²/b²`. The line is

`xC/a+yS/b=U`.

Confocal tangency gives `U²=1−λD²` and `V²=λD²`. With `e=c/a` and `Hσ=U−σeC`,

`H+H−=(b²−λ)D²>0`, `H++H−=2U>0`.

Both focal heights are therefore the ordinary positive distances `hσ=Hσ/D`; no edge passes through a focus. The endpoint focal distances are `a−σc cos(s∓d)>0`. Direct multiplication yields

`Rσ=a²Hσ²+b²V²`,

and the independent norm formula becomes

`qσ=D[a²Hσ+b²λD²/Hσ]`.

Subtracting, using the height product, gives

`q+−q−=(2c/a)DC[−a²+b²λ/(b²−λ)]`.

Since `Δy=2bCV=2b√λ DC`, the coefficient is exactly

`Γ=c/(ab√λ)[−a²+b²λ/(b²−λ)]`.

This independently reconstructs the paper's identity without assuming its completed-square support equations. I also checked those equations directly: `K=a²u²+b²v²>0`, `ρ²=K−λ`, `M=(a²ρu/K,b²ρv/K)` lies on the chord, the cross term in the outer quadratic vanishes, its coefficient is `K/(a²b²)`, and its roots are `±ab√λ/K`. Their x-sum/product give the paper's `Rσ=(a²hσ²+b²λ)/K`. Both approaches agree, including every factor of `a`, `b` and `√λ`.

### Closure and boundary cases

The fixed caustic supplies a single `λ` and `Γ` to every left-oriented edge; `ΣΔy=0` by cyclic closure. The ratio denominator is positive because every `q−` is finite and positive. This proves equality for all admitted periods and windings, including odd primitives and stars. Repeating a cycle multiplies each sum; reversal preserves each antipedal intersection and norm but negates the displacement coefficient. There is no unjustified inference that the same unsigned per-edge difference changes sign on reversing endpoints.

Horizontal chords have `u=0`, `Δy=0` and equal focal norms; the derivation never divides by either. `Γ=0` at `λ=a²b²/(a²+b²)`, strictly between zero and `b²`; its opposite signs on the two sides leave both norms positive. The author’s closed diamond controls happen to use precisely this zero-coefficient caustic and establish a genuine but easy closed case; nonzero-coefficient odd/star cancellation is separately tested here.

For fixed strictly admissible parameters all denominators are positive. As `λ→0`, the chord shrinks and `Γ` can diverge while its product with the displacement stays finite; this does not admit a new nondegenerate finite-period endpoint case. As `λ→b²`, heights can collapse and antipedal distances can diverge. A two-bounce/focal chord violates the noncollinearity or continuation hypotheses. Hyperbolic caustics are not treated. A circle has coincident foci and trivial equality, but is outside `a>b`. The paper states these exclusions rather than extrapolating its divisions through them.

## 3. Literal source scope and attribution

Fresh actual-PDF checks of RGK arXiv **2004.12497v11**, 29 October 2020, and the published Arnold Mathematical Journal **7 (2021), 341–355**, agree on the decisive points. Their introductions define the elliptic billiard using **two confocal ellipses**. Their §3.5 defines antipedals by consecutive perpendicular supports at original vertices. Their §3.7 defines the starred focal quantities as ordinary absolute Euclidean distances. Table 7's **k603** row is the ratio of the **sums of unprimed starred quantities**, value **1**, **all N**, **5/20**, with **?** in the proof field. It is not a primed outer-polygon perimeter or pedal-foot observable, and signed polygon area conventions do not make these norms signed.

Thus the manuscript proves the literal ordinary-distance source target in its actual elliptical-caustic setting; excluding hyperbolic trajectories is not an unannounced truncation of that source introduction. The source's use of rays identifies perpendicular supporting lines; the standard consecutive intersections are precisely the full-line construction made explicit here. No extra positive ray-direction requirement is used to invent a different polygon.

The observation, construction and historical experimental date are credited to Dan Reznik, Ronaldo Garcia and Jair Koiller. The question mark is explicitly historical, with no claim that later literature still calls it open. The proposed added contribution is the ordinary-positive per-edge norm-difference reduction and consequent all-period proof. Classical support, polarity, antipedal geometry, central pairing and telescoping are distinguished from that proposed contribution.

## 4. Closest mechanisms and bounded priority

Salmon, Arts121–122 (1879), defines the continuous negative pedal by the perpendicular-radius envelope and relates it to polarity of an inverse. The focal-ellipse example remains an envelope calculation. The credit is appropriate; there is no finite closed-orbit focal radial-sum theorem in the inspected scope. I do not infer a discrete norm-trace identity merely from a continuous envelope.

BT Lemma4.2 states exactly the focal sideline-height product used here: the square of the minor semi-axis of the common confocal caustic. Its direct support proof yields `h+h−=b²−λ`. Neighboring statements concern squared pedal norms, vector/centroid identities or even-period product symmetry. These supply background but do not identify `rs/h` with the target all-period antipedal norm sum. Their support cancellation mechanism is related; the manuscript credits the known ingredient and ordinary telescoping. The cited journal volume/pages are confirmed by [the primary publisher metadata](https://link.springer.com/article/10.1007/s40879-020-00428-7).

Roitman–Garcia–Reznik’s bicentric Theorem2 and Corollary1 prove limiting-point pedal/focus-inverse **perimeter** constancy. Inversion sends an original edge to length `|A−B|/(|A−f||B−f|)` (unit inversion), while the present summand is `|A−f||B−f|/h`. Their antipedal/polar construction arrows must be followed with the correct source polygon; they do not turn those unequal summands into the requested antipedal(original) radial trace. A transfer would require new metric algebra rather than merely renaming a polygon. I found no such covering transfer in the read primary sections.

The complete supplied eleven-page GKR journal final, SHA-256 `8df802b8b6255aae648934fd83aab4079a5d6b4c66382a9b1b26a6cd3237eac3`, and complete nine-page precursor were independently read and compared. The final changes the title, authors’ order, introduction, linearizing-measure exposition, formal theorem presentation and curvature-average treatment; it is not certified through the precursor alone. Its observables remain chord length, angle cosines, curvature and outer-cosine geometric mean. Neither body defines/proves the target antipedal norm trace. [Publisher metadata](https://link.springer.com/article/10.1007/s10883-022-09608-y) confirms volume29 pp757–767 (2023), online10 August2022, matching the manuscript. This selected final-version gap is substantively closed.

No generic spatial-average-to-every-finite-period inference is accepted. In normalized angle coordinates a rational rotation `x→x+2π/N` and observable `cos(Nx)` have spatial mean zero but finite orbit sum `N cos(Nx)`, depending on phase. R2's guard checks explicit opposite-phase values for N=5. A finite sum identity requires a suitable discrete coboundary, symmetry valid on that period, or another demonstrated mechanism; the manuscript supplies the coboundary.

The July2021 IMPA **final printing was not fully read**. R2 authenticated all145 preserved June7 author-source files against size, SHA256 and Git-blob OID at commit `0b5b417fe2ba3185087979749bc8bcf8c702315d`; it read the full identified invariant chapter and targeted experimental/other contexts. It does not infer final-book equivalence from that corpus or the fifteen-page official preview. Lockwood's full original, Ameseder/other monographs and experimental video/notebook bodies remain incompletely read. Other primary families retain their exact section/preprint/final boundaries and finite search-index coverage. Those limitations prevent an absolute-first or exhaustive-priority conclusion. They are accurately disclosed in `source_audit_summary.md`, not erased by root’s updated gate. A relevant newly identified covering theorem would reopen priority.

The strongest defensible priority statement is therefore the manuscript's **dated bounded audit found no earlier full cover in the inspected corpus**, with background credited and a candidate added proof mechanism. This R2 review does not convert that into a universal claim about all literature. No new broad search was needed without a new lead; the primary mechanisms, supplied final and historical boundaries were the relevant tests.

## 5. Portable reproduction, guards and independent numerical controls

The actual ZIP was extracted only into R2's private scratch. `verify.py` ran in normal and optimized Python; `run_verification.py` ran there and wrote fresh receipts only in that scratch. Both positive runs reproduce **1,456 directed chord cases**, **63,346 explicit guards**, **714 paired reversals**, **80 horizontal chords** and coefficient signs **1,040/60/356** negative/zero/positive. All four internal mandatory wrong coefficient/height/sign/manuscript-binding controls are rejected. The runner performs eight genuine negative child processes, normal and optimized, with expected reason and exit2. Their actual PIDs/argv/UTC/output hashes are retained in `REPLAY_execution_envelope.json` and the actual outer execution receipt.

R2 additionally executed each of those eight faulty subprocesses directly and retained the real raw stdout/stderr and real process receipts. Empty stdout, expected stderr reason, actual child PID, optimization mode and exit2 agree. The candidate's existing author/root envelopes were read completely: real child-PID/result consistency, expected operation count, mode, positive stream hashes and negative stderr hashes reconstructed in the verifier's actual field order all agree. No fake PID or simulated failure is counted. A JSON object reserialized in alphabetic envelope order naturally has different bytes; reconstructing the original emitted field order resolves that serialization detail.

The code was fully inspected. It solves both antipedal linear equations, checks the *positive* square-root branch rather than only squared identities, derives tangency from actual rational endpoints, checks support/chord/height/product identities and reversals, and uses explicit exceptions. Python optimization cannot erase the guards. Four axes and rational chords are finite evidence, not a proof for all real parameters. The README explicitly says the exact program does not check a closed odd orbit; no mismatch is hidden between its code and all-period manuscript proof.

The separate R2 `verify.py` uses explicit guards and an independent caustic-contact parameterization, trigonometric outer intersections and direct linear antipedal solves. **3,240 directed floating chord cases** include irrational axes, near-circular/eccentric shapes, endpoint-near λ, horizontal chords, all coefficient signs and reversal. Worst relative norm-difference residual is `5.209e−8`, concentrated in ill-conditioned limiting choices; the numerical tolerance is `3e−6`, clearly falsification evidence and not interval-certified arithmetic.

R2 independently implements the outgoing tangent map and tunes a common caustic to five genuinely closed odd cases: `(N,winding)=(3,1),(5,1),(5,2),(7,2),(9,2)`. All have a unique consistently oriented tangent branch and the direct norm sums agree. Maximum endpoint closure residual is `3.192e−13`; maximum relative sum residual is `2.843e−12` for the near-degenerate5/2 star. Reversal is executed on each cycle; repetition multiplies its sums as checked numerically. These controls materially differ from rerunning the author's identities and exercise nonzero-coefficient odd/star cancellation. They remain numerical controls, not a replacement for the exact argument.

## 6. PDF, metadata, portability and release-boundary review

All four PDF pages were freshly rendered and visually inspected in full. Equations1–9, title, author/affiliation/ORCID/date/version, proof, attribution, six references, status and disclosure agree with the TeX. No clipped formula, overlap, missing glyph, unresolved citation or broken reading order was seen. Build log, actual compiler receipts, built-in compiler diagnostics, PDF information and source/PDF hashes agree; source and export/build records are distinct and honestly described.

Both intended metadata objects are exactly identical. They identify Alec Kriebel as independent researcher with ORCID0009-0001-9320-500X, title exactly matching the paper, date2026-10-06, version1.0, preprint publication type, CC BY4.0, the correct PDF/ZIP planned filenames and cited source identifiers. The description stays within the theorem's actual domain. Original authored material is licensed separately from cited third-party works. The extensive AI-use disclosure and explicit unrefereed/no-conventional-human-peer-review status are prominent and consistent across manuscript/README/metadata.

There are no third-party PDF bodies, extracted source text/images, credentials, caches or private-source folders in the candidate archive. Public receipts do contain reproducibility paths to original custody locations; these are historical provenance, not portable dependencies of the mathematical verifier. The custody sealing script intentionally depends on surrounding repository evidence and is expressly unnecessary for running the portable theorem controls. Commands use adjacent manuscript/binding files and standard-library Python3.10+ syntax; no third-party Python package or network is needed.

`README.md` preserves the source-only preparation stage while `PACKAGE_README.md` explicitly explains the enlarged release, actual PDF, separate root replay and later pending reviews. That historical layering is clear and does not falsely claim the source-only sealer built this PDF. Immutable ZIP/manuscript bytes should remain unchanged unless a substantive finding requires global repair and renewed review.

## 7. Findings and disposition

**Required findings: none.** No missing proof assumption, source-domain mismatch, positive/signed norm error, orientation/closure gap, invalid priority inference, counterfeit subprocess claim, archive inconsistency, metadata mismatch or disclosure failure was found.

**Optional only:** the fourth page has ample whitespace because it contains the remaining references; tighter pagination would be cosmetic. The portable exact program's closed controls all use Γ=0; adding a nonzero-coefficient closed exact case in a future version would improve breadth, but the all-real proof and broad exact edge controls are already sufficient, and R2 separately exercises odd/star cancellation numerically. Neither suggestion justifies mutating this immutable candidate or withholding this review pass.

Root must authenticate this report's full public payload, input pins, genuine receipts and output seal against the current candidate before using its verdict in the publication gate. A pass flag alone is insufficient. No publication authorization is issued here.
