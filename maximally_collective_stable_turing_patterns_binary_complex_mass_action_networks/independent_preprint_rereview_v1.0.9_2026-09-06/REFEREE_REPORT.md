# Independent preprint referee report: v1.0.9

**Paper:** Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks.

**Audited version:** `94d5177485b9680be8b77f13448abf1f923963e8`, frozen as `maximally-collective-stable-turing-v1.0.9`. Review date: 2026-09-06. This report evaluates the released files themselves, not the editing agent's account of them. The preserved project archive contains 1,372 files; its SHA-256 is `13adedcc95d64d257f0534f9b26b867126218cb238b546908095380f6f23d496`.

## Recommendation

**Minor revision before the next preprint upload.** The main mathematical conclusions survived a fresh independent algebraic and PDE review. I found four bounded repair groups: omitted hypotheses in the standalone theorem exports, a semantic certificate-validation gap, a misplaced literature-comparison row, and ambiguous fraction notation in the supplement. None requires changing the network, headline theorems, numerical profile, certified endpoints, or central proof strategy.

The current main manuscript states the hypotheses implicated by the first finding correctly. The currently shipped certificate coefficients and variable orders also check correctly. The concern is the accuracy of the supporting theorem statements and the integrity of future certificate regeneration, together with two presentation errors. After the repairs and the targeted checks below, I would consider the scientific package ready for preprint circulation within its stated scope. This is a referee assessment, not a guarantee of editorial acceptance.

## Required corrections

### N1. Restore essential hypotheses in both standalone theorem exports

**Locations:** [theorem summary, lines 50–56](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/external_audit/theorem_summary.tex#L50) and [proof skeleton, lines 47–55](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/external_audit/proof_skeleton.tex#L47). The passages occur on page 2 of both PDFs.

Both generic diffusion-ray statements use only `D ≻ 0`. Neither has previously defined this `D` as diagonal. The theorem summary defines diagonal `D` in the *following network application*, while the skeleton immediately uses diagonal entries `d_j` in its determinant identity. The skeleton additionally factors out `s` without first assuming `det J=0`. Those assumptions are explicit in the main theorem and should be explicit in these independently distributed statements.

These are necessary hypotheses, not merely preferred notation. Set

\[
J=-I_3+uv^T,\quad u=(100,1,1)^T,\quad
v=(1/300,1/3,1/3)^T,
\qquad
D=\begin{pmatrix}4/3&-2/3&0\\-2/3&4/3&0\\0&0&1\end{pmatrix}.
\]

Then `J` has eigenvalues `0,-1,-1`; all signed singleton minors are `2/3` and all signed two-species minors are `1/3`. Thus it meets even the stronger stable-spectrum interpretation of the stated Jacobian assumptions. The symmetric positive definite matrix `D` has eigenvalues `2,2/3,1`, but

\[
\det(sD-J)=\frac{s}{450}(600s^2-8801s-9451),
\]

so `β₂=-8801/450<0`, contradicting the exported positivity assertion if general positive definite `D` is allowed. Independently, `J=-I₂`, `D=I₂` satisfies the skeleton's listed minor conditions but gives `det(sD-J)=(s+1)²`, which has no factor `s`.

**Repair:** state `D=diag(d₁,…,dₙ)`, `d_j>0`, in both generic statements; add `det J=0` before the skeleton's expansion. Rebuild the two PDFs and the audit packets containing them. Keep the main theorem unchanged. The examples and a second referee's contextual cross-check are preserved in the algebra and PDE evidence below.

### N2. Validate the ordered variables used to interpret and print each certificate

**Locations:** [mode-isolation reader, lines 21–51](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_verifier/verify_mode_isolation.py#L21), its duplicate and the frontier readers, and [table generator, lines 37–55](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/computation/generate_tables.py#L37).

The revised readers correctly validate support, row counts, unique exponent tuples and coefficients. They still interpret exponent tuples using a hard-coded variable order without checking the JSON `variables` list. The generator then uses that unchecked list as the printed degree-column headings.

**Reproduced failure:** changing only the homogeneous section's `variables` in `independent_verifier/improved_modulus_certificate.json` from `["x","z"]` to `["z","x"]` leaves the direct verifier successful. The altered JSON represents `E(z,x)` instead of `E(x,z)`. Independent reconstruction of the defining complex-modulus expression gives

\[
E(1,2)=238914,\qquad E(2,1)=2004282.
\]

Leaving the generated TeX untouched correctly triggers the freshness check. However, after regenerating the table from the altered JSON, the **complete symbolic aggregate succeeds** with `ALL_SYMBOLIC_CERTIFICATES_PASS`, even though the degree headings now misidentify the polynomial represented by the rows.

This is not a false theorem in the shipped release: its variable lists are correct, and its immutable hash manifest rejects the changed files. The particular variable permutation also preserves coefficient positivity. It is nevertheless a real failure to verify the exact displayed identity, exposed during regeneration rather than when checking untouched release hashes. A field consumed in mathematical column headings is not harmless descriptive metadata.

**Repair:** validate the exact ordered variable tuple for every known certificate in the relevant readers and generator, or derive the displayed tuple from a trusted specification. Preserve the `U`/`A` coefficient-parameter distinction. Add a negative control that swaps variables, regenerates the table, and still must fail the mathematical aggregate. This request does not require rejecting harmless descriptive metadata or arbitrary reorderings of distinct rows.

### N3. Correct the Conradi–Mincheva–Uecker CSV field mapping

**Location:** [literature/theorem_comparison.csv, line 15](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/literature/theorem_comparison.csv#L15), also copied to `public/repository/literature/theorem_comparison.csv`.

The revised main prose now appropriately acknowledges numerical continuation and numerically stable branch segments in the comparison paper. The CSV repair inserted the values into the wrong columns:

| Column | Released value | Required value |
|---|---|---|
| Exact diffusion law | numerical continuation | no |
| Nonlinear branch | numerically stable segments | numerical continuation |
| Stable branch | no | numerically stable segments |

Section 4.3 of the [primary Conradi–Mincheva–Uecker paper](https://arxiv.org/html/2605.16049v1) describes the stable portion of the numerical branch after a fold. The current row still denies those stable segments in the column intended to record them. The manuscript-text gate checks the corrected prose, not the CSV mapping.

**Repair:** shift these entries into their proper fields in the canonical CSV, refresh its portable copy, and check the parsed column mapping. This completes the previous literature-positioning repair; it does not call for expanding the main-text discussion again.

### N4. Parenthesize rational coefficients before an adjacent parameter

**Locations:** [generator, lines 18–33](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/computation/generate_tables.py#L18) and [84-term table, beginning at line 176](https://github.com/AlecKriebel/Math/blob/94d5177485b9680be8b77f13448abf1f923963e8/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/data/certificate_tables.tex#L176). See canonical supplement pages 14–15 and journal supplement pages 17–19.

The prior physical overlap has been repaired. But converting rational coefficients to slash notation and then concatenating `A` produces entries such as `8281/8100A` and `8281/8100+4420871/182250A`. This is visually ambiguous between a coefficient multiplying `A` and a denominator containing `A`. Fifty rows of the 84-term table contain this pattern.

**Repair:** render `(8281/8100)A`, `8281A/8100`, or another unambiguous compact form, consistently for every affected coefficient. Keep the successful row-spacing repair and rerun its geometry gate after regeneration. This finding concerns ambiguous printed notation; it is not a claim that the exact JSON coefficient is wrong or that the new overlap gate fails its intended geometric test.

## What this round independently established

Three initially separate review routes examined algebra/topology, nonlinear PDE arguments, and software/release integrity. The parent reviewer checked the revision diff, literature, metadata, and all 96 supplied PDF pages. After the independent work, the mathematical reviewers adversarially cross-checked the standalone counterexamples and near-threshold interpretation; a second reader also independently evaluated the variable-order polynomial witness.

The parent reviewer additionally reconstructed the Bernstein bases from their defining polynomials and solved for the cubic and crossing coefficients by matrix inversion. All 36 coefficients are strictly positive after extracting the known positive epsilon power; exact reconstruction recovers all four numerator/denominator polynomials. A final hash check confirms that the entire 1,372-file source snapshot remained unchanged throughout the audit.

| Review route | New evidence and result | Limit of the evidence |
|---|---|---|
| Topology and algebra | Generic realization/minor identities; 24,258 retained-set SCC checks; 135 corrected block-order checks; 21 exact conservation-boundary cases; 45 exact contrast endpoint/interior checks, including large dimension. The general proofs were separately reconstructed. | Finite enumeration is a check on the all-dimensional proof, not its replacement. |
| Near-threshold example | Reaction-field differentiation and harmonic solves recover the cubic; a separate Bernstein-basis argument certifies diffusion, pairing, crossing and all six Routh expressions for `0<ε≤1/1000`, `t≥1`. | The endpoint `ε=0` and an ε-uniform bifurcation neighborhood are correctly excluded. |
| Main local PDE results | Independently regenerated all 35/77/84/22 modulus identities and equality cases; read the generic recurrence proof; checked symbolic mass-gauge and cubic-margin identities, finite exact contractions and eight algebraic endpoints. Fixed-mass, Fredholm, high-frequency, reflection and retuned robustness hypotheses were examined. | Classical center-manifold and linearized-stability theorems are invoked. No global attraction or dimension-uniform neighborhood is claimed. |
| Current computational package | **32 tests, no skips; 39 normal verifier passes; 39 optimized-Python rejections; minimal replay and complete clean portable replay passed.** All 15 numerical illustration cases ran. | These execution counts are not counts of independent mathematical proofs. |
| Builds and release integrity | Three clean detached source builds, six rendered-text matches, seven regenerated ZIP byte matches, nine downloaded release-asset byte matches. The remote tag resolves to the audited commit. | Local builds used the pinned toolchain; no live preprint portal submission was performed. |
| PDF review | All **96 pages** inspected visually. Current table spacing passes for all 218 rows in each supplement; minimum clearance is **3.108212 points**. Current geometry code rejects the historical collision using the old PDF with current source. | Geometry does not adjudicate the notation ambiguity in N4. |

The source manifest has 1,371 entries, exactly the archived project file set excluding the manifest itself. The portable manifest has 212 entries. The 13 selected exact generated baseline artifacts also match the released bytes after replay. Unlike the previous review, the fresh TeX and portable campaigns are now complete; the existing pinned tools were available.

## Disposition of the previous findings

| Previous issue | Current disposition |
|---|---|
| R1: extra/duplicate/missing certificate terms | Original defect repaired and exercised by the fresh tests. N2 identifies a different remaining semantic field. |
| R2: colliding exact fractions | Physical collision repaired; the new geometry gate catches the historical defect. N4 addresses a new notation ambiguity introduced by the flattening. |
| R3: determinant description and Frobenius order | Correctly repaired. New SCC and exact-minor checks support the changed text. |
| R4: reaction-derived cubic and complete near-threshold onset | Fully repaired and independently verified by a different positivity mechanism. |
| R5: nonexistent release target and declarations | Closed: the tag and actual assets exist and match; the user confirms the three declarations. No further declaration question is needed. |
| R6: numerical stable-branch literature credit | Main prose repaired; N3 remains in the CSV. |

No new central theorem, endpoint, contrast-law, conservation, or local PDE-stability counterexample was found. The optional wording improvement about the well-mixed Jacobian's restriction to `c^perp` remains optional; its context already resolves the intended meaning.

## Preprint scope and remaining limits

The earlier project plan names bioRxiv, and this round also checked the supplied arXiv source package. BioRxiv's [official screening description](https://connect.biorxiv.org/news/2022/06/13/screening_procedures) asks whether a manuscript presents biological research. This synthetic reaction-network paper's placement is therefore an editorial scope judgment; its systems-biology motivation should remain distinct from any claim of biological experimental validation. The screening description does not justify declaring that theory papers require new wet-lab experiments. This is a destination consideration, not an additional mathematical correction.

For arXiv, the current [TeX submission instructions](https://info.arxiv.org/help/submit_tex.html) explicitly support automatic Biber/BibTeX processing when a bibliography source is supplied without a `.bbl`. Accordingly, the intentional absence of `main.bbl` in this source package is **not** a defect. The fresh pinned-toolchain build passed. This round did not reproduce arXiv's current hosted TeX environment or operate either preprint portal.

The optional historical-lineage preflight was attempted and stopped because its five external input archives are absent. The inspected script uses them for its initial historical checksum check, not as inputs to the current proofs, figures or builds. Their absence does not negate the successful current portable replay. No successful historical-lineage replay is claimed.

Preserve the existing immutable v1.0.9 record. Make the four repairs in a later revision, regenerate affected documents and packages, rerun the new semantic negative control and existing relevant regression/spacing checks, and verify the final submitted copies. Another open-ended search for new results is not required by these findings. No manuscript repair, tag replacement, submission or external outreach was performed during this review.

## Checkable audit artifacts

All evidence is in the same dedicated audit folder as this report:

- `algebra/`: independent boundary campaign, exact omitted-hypothesis counterexamples and algebra report.
- `pde/PDE_REREVIEW.md`, `independent_pde_checks.py`, `INDEPENDENT_RESULTS.json`, and `EXPORT_HYPOTHESIS_CROSSREVIEW.md`: proof review, separate interval mechanism, exact checks and adversarial cross-review.
- `software/SOFTWARE_REPORT.md`, `VALIDATION_SUMMARY.json`, `VARIABLE_ORDER_WITNESS.json`, `CSV_COLUMN_WITNESS.json`, `PDF_GATE_RESULTS.json`, and `RELEASE_ASSET_INTEGRITY.json`: fresh execution outcomes and reproducible failures, with scripts and raw logs.
- `documents/PDF_INVENTORY.json`, extracted document text and `NOTATION_WITNESS.json`: all-page inventory and all 50 affected table rows.
- `SOURCE_INVENTORY.json` and `RESEARCH_LOG.md`: immutable target hashes, provenance and timestamped completion checkpoints.
- `check_audit_evidence.py` and `ROOT_EVIDENCE_CHECK.json`: final source-byte check and independent reconstruction of the interval-certificate bases.

Disposable extracted builds and rendered page images are excluded from Git. The extraction and rendering scripts recreate them. The review's exact counterexamples and compact execution evidence are retained.
