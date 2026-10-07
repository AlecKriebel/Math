# Fresh full-package falsification review: metric candidate 1

Review started 2026-10-07 05:55 UTC. This is a new review of the materially changed eight-page candidate, not acceptance inherited from the older five-page audit note. Final review completed 2026-10-07T06:11:49.246752+00:00. Scoped proof/source review completion estimate: 100%; exact frozen artifact review completion estimate: 100%. These are completion estimates for this review, not for publication or the overall research goal. This estimate is workflow status, not mathematical evidence.

## Verdict

PASS for publication eligibility as the precisely stated modest singular rigidity deduction and cubic boundary application, using the named external theorems. No substantive mathematical, attribution, reproducibility, licensing, or package issue remains identified in the exact v3 candidate. This is an adversarial AI review, not a theorem certification or conventional human peer review. It does not authorize a first-solution claim for the complex cubic comparison, certify global first priority, or verify a remote deposit.

## Exact candidate and review limits

- `main.tex`: SHA256 `de80fb7f84555b632956f21ed8e6e0d1ae6b32da010ee6a89b69a72eb3cf8193`.
- `paper.pdf`: SHA256 `daafa11716afef6207809b02fe567ca5c53c35191f3eb67fcb8f3bd94fe3b71c`, 98,596 bytes, eight pages.
- Final `source-and-verification.zip`: SHA256 `fb1d5a800e6be789fe94a227940a7df4888343fe444a9f64fe1c6b602514cfda`, 226,966 bytes, 26 members.
- Canonical metadata SHA256 `3e3c154f718a4101c07dff9aa4576b2d0ebfeffe89041f0ebea346f03df31a3b`.
- Exact freeze: `receipts/frozen_publication_candidate.json`, v3, 2026-10-07T06:09:39.498001+00:00.
- Owned manuscript checkpoint: `4b685df20381377e223ac351741ebb6bf186debd`; its manuscript blob independently matches the reviewed source.

I read ORIGINAL_REQUEST.txt, all of current main.tex, the rendered actual paper PDF, CURRENT_THEOREM.md, DEPENDENCY_LEDGER.md, APPROACH_TABLE.md, the candidate proof extracts, build/certificate/package code, static publication scope/readme, and priority/source records. I independently inspected the primary statements and the relevant proof passages specified below. I also assigned a fresh independent adversary to Theorem 1; its theorem attack is recorded in `reviews/metric_review1_index_adversary.md`, with the separate curve-descent check preserved verbatim in `reviews/metric_review1_curve_descent.md`.

The review does not certify the full external stable-degeneration, KE existence, splitting, classification, or normalized-volume gap theorems by formal proof. No Lean claim is made. In particular I inspected the pinned gap's exact unrestricted statement, cone/product conventions, entire adjoint-semigroup section, and upper-bootstrap argument and reproduced its selected arithmetic; I did not reconstruct every argument or all cited inputs of that 57-page external paper and its companion. The earlier geometric/semigroup audit notes are read as explicitly limited evidence, not substituted for this candidate's proof. I have not independently certified every lemma of KSZZ or proved global first priority.

## Attempts to falsify the additional theorem

Theorem 1, main.tex 92–215, survives the following checks.

1. **Canonical restriction rather than a numerical root.** A finite normal connected quasi-etale cover is crepant in codimension one; reflexive extension retains `omega_Y^[-1]=f^*L^r`. Restriction over a regular point of the complementary product first uses the smooth canonical formula on a big open, then extends reflexively on the factor. The line bundle retained is actual ample Cartier. This works for any algebraic product cover, and its factor is klt by the smooth-product discrepancy test. It does not pull back or restrict a merely numerical Q-Cartier root.
2. **Index obstruction at negative twists.** KV applies to Cartier `-jA` because `-jA-K=(r-j)A` is ample for every `1<=j<=r-1`. Antiample bundles have no sections on a positive-dimensional projective integral variety. The Euler polynomial has positive leading coefficient `A^d/d!` and is valid on every integer, so these distinct negative roots force `d>=r-1`. Two positive-dimensional factors imply `m>=2(r-1)`, contradicting the strict bound. The degree-zero and rank-one boundary cases introduce no exception. The equality example `P^(r-1) x P^(r-1)` has precisely the asserted root and KE product metric; mixed conjugation really has pullback complex structure `(-J_1,J_2)`. It proves sharpness in the stated general class, and does not prove a cubic-fourfold failure.
3. **Stability descent and arbitrary covers.** The saturated reflexive extension of the etale pullback agrees with it on a big open, with no codimension-one correction. General anticanonical complete-intersection curves avoid the codimension-two complement; their inverse-image bundle degrees scale by the finite degree. This computes the relevant Weil determinant intersection without Q-factoriality. A destabilizing subsheaf downstairs would destabilize the stable one-factor DGP cover. On each further normal connected finite quasi-etale cover, DGP's pullback metric remark and the retained Cartier root allow the same universal argument to run again. This does not assert that arbitrary pullback of any stable sheaf is stable. “Cover” has the usual normal connected variety convention; explicitly adding those words would be an optional clarification only.
4. **Local positive Ricci rather than completeness.** For a parallel orthogonal `I`, the parallel real form `eta=g(I·,·)` has parallel `(2,0)` part. Mean Chern curvature on `Lambda^2 T^(1,0)*` is `-2 lambda Id` on a positive KE manifold, up to the overall convention. Parallel sections have zero curvature action, forcing that part to vanish. Hence `-JIJ=I`, equivalently `IJ=JI`. This is local and requires neither complete regular locus nor global integration. The resulting holomorphic endomorphism extends through reflexive Hom and algebraizes by GAGA. Stable simplicity follows from the kernel/image slope contradiction and the constant characteristic polynomial on normal projective X. `I^2=-1` leaves precisely the two global signs.

Published DGP Theorem A (p.94), Definitions 1–2 (p.96), Remark 3 (p.97), Theorem 6 and final splitting proof have the hypotheses used. The index argument is a short explicit deduction from that external result and the classical Hilbert-root bound, not a newly invented splitting theorem. The harmless multinomial omission in the cited product-mass display is documented in the proof notes; restoring the same positive coefficient on both sides leaves the factor argument unchanged.

## Attempts to falsify the cubic transfer and metric fibers

- The required upstream gap is the upper bound for singular boundary-zero complex algebraic klt germs in every `k=2,...,n`; no equality classification is used. All 21 PINNED_MANIFEST entries independently match `git show` at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Its supplied OpenAI authorship/title/date are respected. The copied formalization catalogue yields no asserted Lean coverage of this theorem.
- Li–Liu v3 Section 6 explicitly assumes a torus-equivariant genuine top form. The candidate treats nontrivial link fundamental group separately: normalized SE Ricci curvature, Myers, and Bishop give density at most `1/d<=1/2`, and `b_k>=1/2`. In the simply connected case the flat canonical connection gives a global parallel top form of Euler weight k; normal reflexive extension and torus equivariance match the setup. Theorem 1.9/6.2 is a minimum over all centered real valuations. Lemma 6.8 and the final limiting proof cover irregular fields without pretending the quasi-regular approximants are Einstein. Lemma 6.3 gives the density normalization after division by the round sphere. The argument uses equality with the infimum, never the invalid reverse inference from an arbitrary test valuation. Van Coevering Section 3 and Collins–Szekelyhidi Lemma 6.1 supply the normal affine, Q-Gorenstein and positive-weight klt eligibility. If smooth affine apex were suspected, global minimization would give density one and Bishop rigidity would force the excluded flat cone.
- SS v1 Theorem 5.2 and its full Section 5.2 supply precisely the actual Cartier hyperplane root and Gorenstein canonical cubic limit, in the polarized smoothable GH setting. Its iteration handles singular links rather than directly applying Li–Liu to them. The transverse range is 2 through n. The density sequence is increasing, and the strict volume threshold reduces to `(1+1/n)^n<e<3`. The cubic index is `r=n-1`, so the new strict criterion applies exactly for `n>=5`.
- Fujita's primary preview gives the Gorenstein del Pezzo cohomology assumptions. The two KV/duality ranges cover every integer twist, with CM supplied by klt; degree three therefore yields the cubic embedding. The universal-family calculation of the CM coefficient checks as `2(n+2)(n-1)^n>0`. The complex comparison is the cited SS continuity transfer, not an independent scheme/stack theorem. LWX Theorem 1.1(iii) supplies the smoothable weak-KE/GH interpretation with its actual Q-Gorenstein smoothing hypotheses. Equal volume alone is correctly rejected as a selection rule.
- DSII v1 Proposition 2.14 identifies intrinsic metric regular points with analytic regular points for these actual GH limits. Its proof gives local smooth metric regularity; Proposition 2.4 uses the bounded regular-locus extension principle and normality. Thus a completion isometry restricts to a local smooth Riemannian isometry and pulls back a parallel orthogonal complex structure. Theorem 1 fixes a single sign. Continuity in the common analytic/metric topology and normal extension of bounded target coordinates, applied also to the inverse, give a global (anti)holomorphic isomorphism. GAGA algebraizes it. No unsupported assertion about every nonsmoothable weak-KE metric completion enters.
- I independently downloaded and inspected SGA2 XII Corollaire 3.7 and Remarque 3.8, p.121: the Picard statement applies to singular global projective complete intersections of dimension at least three. Hence the cubic anticanonical root is unique in torsion-free Picard group. The hypersurface sequence gives `h0(H)=n+2`, so the map is projective linear. In the anti case this is a holomorphic map to the conjugate target and preserves its hyperplane bundle in that formulation.
- Forgetting complex structure is continuous; polarized subsequential compactness lifts every ordinary metric limit. The isometry classification makes the fibers exactly conjugation orbits, including fixed orbits. The induced map is a continuous bijection from compact GIT/conjugation to Hausdorff metric GH space. No effective distance, nonclosed semistable, scheme, stack or moduli-functor conclusion is inferred.

Primary sources directly inspected include the cited LL/vC HTML, published DGP PDF, original DSII and SS PDFs/text, original CS publisher PDF, SGA2 PDF, Fujita preview, LWX and OSS original PDFs/text, PW v2, KSZZ supplied public PDF and current primary author page, Horing's revised author PDF, and Spotti's thesis Theorem 1.1.1 and its smooth sign-rigidity corollary (printed pp.14–16). Foundational source proofs are not claimed fully reconstructed.

## Priority and publishable scope

The original complex K/GIT target is already publicly stated more strongly in KSZZ Theorem 1.1; the publicly linked manuscript was checked against its actual statement. Its earliest posting date is unestablished. SS already provides this gap-to-cubic transfer mechanism. PW supplies smooth cubic tangent stability; Spotti supplies the smooth positive-KE factorwise-conjugation precedent; OSS expressly states ordinary metric quotient by conjugation for singular del Pezzo surfaces; DGP supplies singular splitting. Those exact scopes do not themselves state the new high-Cartier-index criterion or give the present all-boundary higher-dimensional metric-fiber proof. Horing further reinforces the established status of the algebraic product mechanism.

The manuscript's restrained framing as an additional singular rigidity deduction and boundary application is appropriate for a modest consequence/extension note. The exact checked proof obligations add mathematical content beyond merely rewriting the old conjugation convention. This scope judgment is not a guarantee of first disclosure or a proof that no equivalent corollary exists elsewhere. Publication as a first solution of the complex cubic K/GIT problem would not be justified; the current title, abstract and attribution avoid that claim. AI use and absence of conventional human peer review are disclosed accurately.

## Reproduction and visual inspection

Independent clean `build_paper.py` export with Tectonic 0.16.9 exited zero and found no undefined references. Three distinct bibliography paragraphs produced harmless underfull-box warnings, with no clipping. Extracted text of the rebuilt PDF exactly equals that of the supplied PDF; byte hashes differ as expected from creation metadata. I rendered and visually inspected all eight supplied PDF pages: formulas, dependency displays, references, accented names, page breaks and margins are readable; no unresolved labels or layout defect found. All fonts are embedded. PDF title, author and subject match the candidate, and it contains no JavaScript, encryption or forms.

Both supplied certificate scripts reproduced. Exact values include exponential upper `917330371/241805655`, lower `1957/720`, final upper `3879/2000<2`; the fourfold positive margin is `209183/1440000`, with the stated low-dimensional margins. Boundary polynomial residual is zero, all four branch-line triple determinants are nonzero, and the Sym2(P2) degree computation is 6/2=3. These arithmetic outputs do not certify their geometric use or KE existence. Build and preliminary nonsecret receipts are under `reproducibility/tmp/metric_review1/`.

## Frozen payload review

The actual deposit manifest lists exactly two separately downloadable payloads: `paper.pdf` and `source-and-verification.zip`. The outer kit is a convenience bundle. I checked all 13 files in the v3 frozen receipt against their actual sizes and hashes, the manifest and selection, canonical metadata objects, static README, theorem/dependency record, source provenance, licensing, every source member, all four original code files plus the arithmetic helper, and the archived JSON receipts. The selected root source is standalone and its bibliography is included. Live theorem/log/status files were read for research context but are excluded from the deposit; all complete-package review reports are likewise excluded, avoiding review self-reference.

All 26 unique archive member names are safe relative paths, with no symlinks. Each size/hash matches PACKAGE_MANIFEST. SOURCE_SHA256SUMS covers exactly the other 25 members. README.md is byte-identical to the static deposit README. Canonical archive/kit metadata and the locally serialized source metadata and deposit manifest metadata are equal JSON objects; the raw serialization difference is explained rather than mistaken for a content mismatch. The selection's hashes match the frozen source inputs. Copyright/author/ORCID, date, version, title, scope, attribution and AI/nonhuman-review disclosures agree. CC BY 4.0 applies to original prose/manuscript and MIT to original code; third-party inputs are linked and hashed, with no third-party PDF, source clone or reading cache redistributed. No invented affiliation, coauthor, first-priority assertion, or already-published claim was found.

I extracted v3 afresh under this project's reproducibility/tmp, compiled its main.tex cleanly, reran both scripts including the fourfold helper, and reconstructed the selected source archive. The archive is byte-for-byte identical to the final intended payload. The outer kit and exact deposit manifest also reproduce byte for byte. The fresh v3 PDF has SHA256 `74eed1c31c2bc39b4690a38aa5482c477706f3ce9e817a067c038e21c4106962`; its extracted layout text is byte-identical to the supplied paper, SHA256 `1552ef7cfc52d18cc537b062ce560b04c244b374b2c5a465520c2bf763afab20`. Creation metadata explains why a newly compiled PDF is not the copied deposit PDF. The PDF byte hash accepted for deposit is the unchanged supplied `daafa117...b71c` above.

Two nonmathematical findings were repaired before this verdict. The old archived Reeb audit ambiguously used “GH” and “forgetting” for the coarse complex space; v2 now expressly says complex/polarized GH and retains the complex structure, and sends ordinary metric forgetting to the separately proved conjugation quotient. V2 also contained two broken supplemental relative links; v3 now resolves them to publication/boundary_index_proof_notes.md and agent_notes/boundary_isometry_extension_audit.md. I independently inspected the final changed lines and checked every local Markdown link in the archive; all resolve. No repair to the theorem, PDF, or metadata was needed. Optional explicit “normal connected” wording for quasi-etale covers remains a clarification, not an identified defect under the standard variety convention.

The full receipt `receipts/metric_package_review1.json` records exact hashes/sizes of every reviewed frozen file and every source member, clean-build output, certificate output, reproducibility checks, inspected-source records and review limits. Its scratch evidence is under `reproducibility/tmp/metric_review1/`; these review artifacts are outside the immutable payload. Remote Zenodo stage/inspect/publish, DOI resolution and spreadsheet insertion are outside this review and remain operations for the lead researcher. No candidate/source PDF edits, Git mutations, publishing, tracker changes, outreach, or external individual communication occurred in this review.

### Actual complete source archive inspected

The following is the entire archive, including generated records. Complete per-member SHA256/byte receipts are supplied separately; these names are enumerated to make the reviewed payload unambiguous.

- `README.md`
- `SOURCE_SHA256SUMS.txt`
- `agent_notes/boundary_isometry_extension_audit.md`
- `agent_notes/fourfold_constants_check.py`
- `agent_notes/high_index_priority_adversary.md`
- `agent_notes/reeb_bridge_audit.md`
- `agent_notes/root_index_sharpness.md`
- `agent_notes/spotti_sun_source_hashes.json`
- `agent_notes/spotti_sun_transfer.md`
- `agent_notes/upstream_geometric_audit.md`
- `agent_notes/upstream_semigroup_audit.md`
- `main.tex`
- `publication/LICENSES.md`
- `publication/README_FOR_DEPOSIT.md`
- `publication/SOURCE_PROVENANCE.json`
- `publication/THEOREMS_AND_DEPENDENCIES.md`
- `publication/boundary_index_proof_notes.md`
- `publication/boundary_rigidity_proof_notes.md`
- `publication/metadata.json`
- `publication/package_selection.json`
- `receipts/boundary_examples_check.json`
- `reproducibility/build_paper.py`
- `reproducibility/build_publication_package.py`
- `reproducibility/verify_boundary_examples.py`
- `reproducibility/verify_constants.py`
- `sources/PINNED_MANIFEST.json`

