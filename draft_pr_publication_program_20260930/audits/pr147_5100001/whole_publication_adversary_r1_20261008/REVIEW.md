# Fresh adversarial whole-publication review R1: PR147

Verdict: **REQUIRES GLOBAL WORDING CORRECTION**. R1 inspection is 100% complete. The literal k107 counterexample is valid, and no mathematical, extraction, reproducibility, metadata, source-attribution or layout defect remains in the reviewed scope. One inaccurate public provenance sentence must be corrected globally before a fresh independent R2. This report is neither R2 nor publication authorization.

## Exact candidate and independence

This review binds only publication_package_v1 with PACKAGE_MANIFEST.json 17,798 bytes, SHA256 f808086ec611ecdd76acec18ce397f9018f098650eaf4fac936d0999430bdd09. All 89 declared members plus the manifest itself were rehashed and checked against the complete actual 90-file package. No additional member, missing member, differing mode, size or digest was found. Candidate bytes were unchanged at final readback.

The exact PDF is 65,957 bytes / SHA256 8b28daa6acd6d4dd83ebaa9997ad6a0330212aa4952285454c43236038f141f5; its source is 12,494 bytes / SHA256 7021e458a24c665503351e02bc8bdff67b2dd4a71439b57e36f21961df3ba62b. The support ZIP is 98,192 bytes / SHA256 c510caa42e99d80735e1896e146c7f6b9ae75d5e6524a44d0e9f84ea20190a06, with exactly 87 unique safe regular-file members. SUPPORT_MANIFEST.json is 17,410 bytes / SHA256 61c4e4a8ebe08e09d04443e9ad277c83f37d9f2ed1d4f31a60e18cb2695acdb2. The original head remains 502de2f863a63ca205814da4194411847797a7c3.

I read the complete manuscript first, independently derived the continuous-family proof and all theorem quantities, and recorded INDEPENDENT_MATH_CHECKPOINT.md before reading earlier mathematical review reports or calculation programs. I then read the primary definition/table pages and performed the full package review. The later fresh finite program was written after source-code inspection; its independence claim is an independent geometric recomputation, not a claim that the program preceded every earlier checker. Its logic does not import a package checker. The initial analytic checkpoint is the principal separation from earlier reviewers.

All writes, extraction, staged runs, outputs and review records are inside this new review folder. No package, real Git state, native/cache/program3 state, tracker, provider PR, upload or third-party person was changed or contacted. Internal reviewer coordination reports are not external outreach.

## Sole mandatory finding: R1-F1

Severity P2, public provenance accuracy. At k107_counterexample.tex line40 and PDF p1, the sentence says: “The saved PR body contains the two values and a continuous-family certificate.” At priority_and_provenance.md line11, it says its saved body includes a continuous T²=-id certificate.

The complete frozen original_acquisition_raw/PR147.json body actually states the exact values and says the referenced proof “provides a continuous T²=−id family connecting the examples.” It then names the original main artifact. It does not contain the certificate's equations or derivation. The actual certificate is in the separately pinned original-head COUNTEREXAMPLE.md, whose two package historical copies are byte-identical to the original (10,761 bytes; SHA256 d34e4347358f54b20c9cea7d974e2c6a2308a5e69c7abf46de16132d83f9edbd).

This does not falsify the theorem or remove the documented provider dates. It overstates what the provider body alone records. Because the paragraph uses the body as evidence of dated scientific disclosure, the distinction should be precise.

Required global repair:
1. Replace both current-publication body-containment statements with wording that the saved body **states the values and describes/references the continuous-family certificate in the original-head artifact**. For example: “The saved PR body states the two values and describes the continuous-family certificate in the referenced original-head proof.”
2. Preserve the original body, original proof, dated preparatory reports and their pins. They are historical evidence, not editable current prose. The bounded priority report already correctly calls the body's content a continuous T²=-id *claim*.
3. Create the globally corrected successor candidate, regenerate its PDF, support ZIP and affected manifests/status pins, and check every public narrative/metadata for the same body-versus-artifact distinction. metadata.json and zenodo-deposit.json need no forced prose change if their currently accurate statements remain identical.
4. Render and view all successor PDF pages, revalidate exact upload scope and extracted diagnostics, then assign a fresh whole-package R2. Do not promote this v1 package or interpret this review as a later acceptance receipt.

No other mandatory correction was found. Suggestions about shorter prose, proof style, or broader literature searches are not additional blockers.

## Independent mathematical derivation and falsification

The target is exactly K=(A'/A) product sin(theta_i/2), using original internal angles and consecutive tangent intersections on the outer ellipse, at N divisible by4. A primitive N=4 example is admissible. I checked the complete definition/table contexts: preprint v11 pp2–5 (full pp3–5 rendered/viewed) and journal pp342–345 (full pp343–345 rendered/viewed). Both Table2 rows print k103*k105, a period congruent to0 mod4 condition and “?” in the proof column. Their individual odd-period rows for k103/k105 do not prohibit forming the defined product at N=4. Signed area is explicitly defined by shoelace sums.

In a positively oriented orthonormal normal basis (n,m), let M=[[h²,eta],[eta,k²]], S=h²+k² and D=h²k²-eta²>0. Boundary points are P=(h,eta/h), Q=(eta/k,k). The edge and incoming diagonal satisfy
Q-P=((hk-eta)/(hk))(-h,k), P+Q=((hk+eta)/(hk))(h,k).
Both coefficients are positive since hk>|eta|. Normalized travel directions are (h,k),(-h,k),(-h,-k),(h,-k), divided by sqrt(S). Reflection across successive tangent lines x=±h,y=±k changes the relevant component. Thus the claim uses physical unit-speed reflection, with the correct incoming/outgoing branches.

lambda=D/S satisfies0<lambda<b². The fixed caustic C=M-lambda I has semiaxes squared a⁴/S,b⁴/S; their difference a²-b² matches the boundary's focal distance. It is positive definite and strictly nested. For first two chord normals w+=(k,h), w-=(k,-h), their nonzero offsets are hk+eta and eta-hk. Direct expansion gives w±^TCw±=u±². The unique contacts Cw±/u± are P+(k²/S)(Q-P) and Q+(h²/S)(-P-Q). Parameters lie strictly in(0,1); negation proves the other contacts. Consequently no remote line extension is substituted for an actual tangent segment.

det(P,Q)=D/(hk)>0 establishes a simple strictly convex counterclockwise central parallelogram with four distinct vertices and no shorter oriented period. The normal parameter varies over a continuous circle, and all denominators h,k,S,hk±eta remain nonzero. The two witnesses are connected through that single nondegenerate caustic family, not merely compared as isolated orbits.

Outer intersections are (h,k),(-h,k),(-h,-k),(h,-k), so A=2D/(hk), A'=4hk and AA'=8D. The internal angle at P is between (-h,-k) and (-h,k); its positive half-angle sine is k/sqrt(S), with h/sqrt(S) at Q. Thus H=h²k²/S² and K=2h⁴k⁴/(DS²)=32D³/(S²A⁴). At phase0 this gives2D/S²; at phase pi/4 it gives S²/(8D). Since S²-4D=(a²-b²)²>0, K_D<1/2<K_R. For4,3: A=24 and576/25, A'=48 and50, H=144/625 and1/4, K=288/625 and625/1152, gap58849/720000>0.

I challenged signed area, reversal, internal/supplementary angle conventions, normalization, caustic contacts, primitive period, singular intersections, continuity and scaling. Reversal flips both areas; the ratio is preserved. The circular limit yields1/2 and removes strict separation as stated; b=0 is outside the hypotheses. Dimensions cancel correctly in K. No deduction requires a quotient replacement, all-period invariant, numerical orbit fitting or formal proof assistant. No central mathematical gap was found.

independent_finite.py independently recomputes the two exact endpoint geometries using Fraction arithmetic: 141 executed checks including meaningful negative cases. It returns the advertised areas, products, values and contact parameters9/25,16/25 for the diamond and1/2 for the rectangle. A wrong but strictly nested confocal caustic fails at tangency; an inscribed convex rational square fails at physical reflection; an off-boundary point fails at boundary membership. Normal and optimized output bytes agree.

## Complete package and reproduction scope

All88 nonbinary package files were fully read as UTF-8 and all JSON parsed; all package files were pinned. The complete manuscript, READMEs, current provenance/metadata, all five checker programs, runner, original proof, distinct preparatory reports, priority comparisons, source/history manifests and baseline science were inspected. Identical duplicate historical proof/report copies were checked by exact bytes rather than represented as new independent readings. Full raw stdout/stderr and recorded receipt/output-map bodies were read back and hash-validated; their24 historical child records and48 portable raw bindings close.

The archive was extracted into extracted_support in this review folder. Every archive member equals its package counterpart; all86 support declarations plus the support manifest close exactly. No absolute/traversal path, duplicate, symlink or unexpected member was found. Extracted regular-file modes match declarations. The archive contains authored source/code and inspection descriptions, not third-party full papers, screenshots, external source ZIPs, private caches or operational staging. The PDF and outer package manifest are correctly excluded from the support ZIP.

The extracted runner was run using existing /opt/homebrew/opt/python@3.14/bin/python3.14 with -E -S -B -P for standard-library code and /Users/alec/Documents/Math/pr9_adversarial_review_20260929/algebra_env/bin/python with -E -B -P for the library families. It reports SymPy1.14.0 and completes:
- all5 families normally and under optimization (10 runs);
- all12 real guard controls (6 true exits0,6 false exits1);
- all24 children exited as expected, were reaped and had empty process groups;
- complete outputs equal the declared baselines (author10073, inherited8397, finite175, polynomial6, nonsymmetric30).

I additionally altered the expected rectangle value in a copied actual checker and exercised its certificate on a convex on-boundary rational square that violates billiard reflection. Both scientific controls fail normally and under optimization at the intended mathematical guard, rather than merely calling a bare false predicate. Full outputs and actual PIDs/exits/group closures are retained under actual_outputs. No copied mutation entered the candidate.

SOURCE_HISTORY.json origins and destinations were verified byte for byte. The original code differences are precisely the documented three author assert guards and one inherited assert guard replaced by explicit failures; calculation expressions, cases and scientific outputs are unchanged. The original manuscript/reference history remains frozen. The runner's dependency requirements are stated, it installs nothing, stages all writable outputs outside the package and successfully runs from the extracted archive.

## Attribution, source rights and chronology

The official Garcia–Reznik2022 PDF, full printed pp58,68–69, was rendered/viewed. Props4.7/4.9 and AppendixB.3 already supply the parallelogram/outer rectangle, AA'=8a²b², full simple4 construction, caustic, perimeter and area extrema. The January2021v3 title and construction p18 were separately checked. Its version-specific title differs from the final journal title, and the current bibliography handles this correctly. Those building blocks are expressly prior work.

All4 pages of Ferudun's contemporary note were read, and full pp2–3 rendered/viewed. Its Lemma1 proof matches the normal-coordinate mechanism, and its Theorem2 gives the same K values and full-family formula. The current abstract, sections1–2, bibliography, provenance and metadata credit this exact overlap. The public contribution is a narrow explicit correction of the retained table entry corresponding to an earlier dated repository artifact. The package does not claim new four-periodic geometry, exclusive/global first priority, independent discovery, or current unresolved status.

The frozen provider body has created2026-09-30T12:00:24Z, updated2026-09-30T12:03:07Z and the stated original head. The retrieved Ferudun Zenodo JSON has created2026-10-01T06:10:26.790158+00:00, updated06:10:27.243370+00:00, publication_date2026-10-01, version1.0 and public/submitted status. These support the bounded observed chronology after the R1-F1 wording correction, not a complete independent archive of every earlier body revision or a global-priority/causal-independence conclusion.

I independently read the relevant Connes–Zagier article text pp909–914, all spatial-integral article text, and the selected Stachel2021 Lemma2.2/relevant pp24–27 and motion Eq2.5/Section5 pp1617–1621. They support known background and the exterior-angle warning, without an explicit k107 correction in those passages. Detailed limits are in SOURCE_AND_CUSTODY_READBACK.json. I do not claim independently reading or reproving every unrelated theorem in the two Stachel papers. The saved primary-read scopes distinguish each preparatory lane's fuller readings from the root's narrower comparisons. Negative search results are expressly bounded, not novelty evidence. The separately unidentified2020 in-preparation reference15 was read in the original source and its access limit is explicit; it is not equated with the later low-period paper.

Author name, independent-researcher affiliation and ORCID0009-0001-9320-500X agree across manuscript and metadata. Extensive AI use, unrefereed status and absence of conventional human peer review are explicit. Authored content's CC BY4.0 license is identified; cited external works retain their own rights and none is distributed as a full-text support member.

## PDF, metadata and preparation labels

The exact latest4-page PDF was rendered and all4 complete pages viewed twice, including the final custody-recorded rendering. Text is legible within page bounds, equations/table labels and references agree with the full TeX, and no orphan reference page, clipping, missing glyph, overlap or substantive source/PDF discrepancy was observed. Dates7October2026 local and audit closure8October UTC are compatible.

metadata.json exactly equals the metadata object in zenodo-deposit.json. Upload scope is exactly k107_counterexample.pdf and k107_counterexample_support.zip. No record DOI, later upload or publication is fabricated.

PUBLICATION_PREPARATION.json says PASS_ROOT_VISUAL_AND_TEXT_QA and explicitly says whole-package R1/R2 pending. PACKAGE_MANIFEST.json likewise says whole-package reviews pending; audits/README.md calls included reports dated preparatory source records. The historical proof's pending-review status is clearly contextualized in both READMEs. These labels are adequate candidate snapshots, not future execution receipts. The records remain accurate as historical preparations after this new R1; any successor acceptance must bind its own exact bytes.

## Closure

Strongest verified result: the original primitive four-period counterexample rigorously refutes the literal product for every noncircular ellipse in the stated family, with exact rational witness4,3. Exact mathematical gap: none found. Publication gap: correct R1-F1 globally, regenerate and verify a successor, and obtain a fresh full R2.

Review artifact manifest and final readback bind all local outputs and candidate pins. This audit does not itself modify an original queue or increase the original author2/5 effort count; all current activities are verification, with zero new original discovery approaches. ROOT owns any later authorized checkpoint/publication action.
