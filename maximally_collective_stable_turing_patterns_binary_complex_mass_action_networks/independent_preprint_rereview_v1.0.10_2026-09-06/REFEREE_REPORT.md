# Independent referee report: v1.0.10

**Paper:** *Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*

**Author:** Alec Kriebel

**Reviewed version:** commit `953c836a12b9d9d474521feb4a96e218c1155203`, tag `maximally-collective-stable-turing-v1.0.10`

**Review completed:** 6 September 2026, America/Los_Angeles (7 September UTC).

## Recommendation

**The mathematical claims survive this new review. All four previous findings are closed. Two bounded corrections remain in the verification and journal-presentation machinery.**

C1 should be repaired before the next preprint/package update: a conflicting coefficient field can cause regeneration to print a false polynomial identity while the mathematical readers and downstream audits pass. The coefficients and tables actually shipped in v1.0.10 are correct, and its immutable hashes detect the demonstrated changes. This is a defect in validating newly regenerated artifacts, not a counterexample to the published theorem.

J1 concerns the SIADS exports: five overfull boxes survive the newly added warning check because that check does not cover the detached journal builds. Four materially exceed the declared six-inch text width. Repair them before using those journal versions. The canonical preprint manuscript and supplement do not have these layout defects.

I found no supported reason to alter the topology, headline theorems, endpoint, exact diffusion profile, nonlinear coefficient, or numerical data. Nor does this review support retracting the current preprint or creating another immutable release merely to update DOI metadata. The remaining changes are specific and testable below.

## Basis and independence

The review used an untouched archive of the exact target, not a moving working tree or the editing AI's validation summary. `SOURCE_INVENTORY.json` records all 1,651 files, totaling 22,425,118 bytes. The source archive SHA-256 is `3c1f76a2cbb309d223ce66337c2531ea13b39bde5d3694094051155635775dfb`. Separate reviewers examined algebra/topology, nonlinear PDE arguments, certificate interpretation, positioning, and release behavior. The parent reviewer inspected all 96 rendered pages, checked source consistency, and independently measured the journal margin incursions. The certificate defect received two additional independent mathematical/parser checks.

The comparisons confirm that the main mathematical arguments did not change in this revision: the main-source differences are release metadata, the supplement explains the new fraction notation, and the scoped data/figure/core/bibliography comparison changes only the generated certificate notation. Unchanged arguments were nevertheless reread adversarially.

## C1 — Generator and readers disagree on a recognized coefficient field

**Location:** `computation/generate_tables.py:69–72`; corresponding readers at `independent_verifier/frontier_verify_mode_certificates.py:229–236` and `independent_verifier/frontier_verify_exposition_identities.py:447–460`.

For any Pareto table row, the generator prefers `coefficient_in_U_ascending` whenever it is present. But the 84-term spatial certificate uses the parameter A, and its exact readers correctly use `coefficient_in_A_ascending`. They accept the additional recognized U field without detecting that the generator will consume it instead.

The reproducible witness changes one row of `pareto_all_m_certificate.json`, in `modulus.spatial.terms`, from

```json
{"powers": [6, 1, 0], "coefficient_in_A_ascending": ["8281/24300"]}
```

to

```json
{"powers": [6, 1, 0], "coefficient_in_A_ascending": ["8281/24300"], "coefficient_in_U_ascending": ["1"]}
```

No verifier or generator code is altered. Both direct mathematical readers accept. Ordinary table regeneration changes the displayed coefficient of `x^6 z` from `8281/24300` to `1`. After regeneration, the complete symbolic suite reports `ALL_SYMBOLIC_CERTIFICATES_PASS`, the source audit reports `MANUSCRIPT_AUDIT_PASS`, and a freshly built scratch supplement passes `PDF_SEMANTIC_AUDIT_PASS`. The supplement still has 19 pages, its final TeX log has no selected warnings, and the bad coefficient really appears on the page.

Independent reconstruction of the boundary factors and exact parsing of all 84 rows proves

\[
\widetilde E_{84}-E_{84}=\frac{16019}{24300}x^6z.
\]

This is not a harmless alternate representation. At `x=z=s=1`, with the allowed `A=4`, the difference is `16019/24300`. The correct leading coefficient can also be obtained directly from the contribution `(91/90)^2 (z/3) |lambda^3|^2` without using the submitted implementation. The original shipped table equals the independently reconstructed polynomial exactly.

**Containment matters.** Before regeneration, the table-freshness check rejects this mutant against the unchanged shipped table. After regeneration it compares the output with the same generator and accepts. The published manifest rejects the changed JSON, TeX table, and PDF; this experiment does not bypass immutable-release integrity. It demonstrates disagreement during validation of a newly generated package. The PDF audit's successful row-spacing check is also not, by itself, an exact polynomial-identity check.

**Required repair:** choose the coefficient field and parameter explicitly by table: U for the homogeneous 22-term table and A for the spatial 84-term table. Reject a conflicting recognized field, or ensure it can never influence rendering. Add the dual-field witness as a regression, including regeneration followed by validation. An independent comparison of generated exact coefficients with the defining polynomial would further strengthen the boundary, but no change to the correct published coefficients is needed.

**Evidence:** [certificate report](certificates/CERTIFICATE_REVIEW.md), [mutation results](certificates/CONFLICTING_FIELDS_RESULT.json), [PDF acceptance results](certificates/MUTANT_PDF_GATE_RESULT.json), [independent mathematical check](algebra/CONFLICTING_FIELD_MATH_RESULTS.json), and [independent parser cross-review](certificates/render_equivalence/CROSSREVIEW.md). The scripts and original output logs are retained beside these files.

## J1 — Journal exports exceed the text width, and their logs escape the warning gate

Fresh builds of the unmodified journal sources produce these five warnings:

| Shipped PDF | Page | Source | TeX excess width |
|---|---:|---|---:|
| SIADS manuscript | 17 | `manuscript/main.tex:1008`, verifier command | 33.31522 pt |
| SIADS manuscript | 19 | `data/contrast_table.tex:1`, included at `main.tex:1101` | 22.83739 pt |
| SIADS supplement | 14 | `manuscript/supplement.tex:888`, verifier command | 59.06581 pt |
| SIADS supplement | 20 | `data/sign_certificate_tables.tex:65`, polynomial and rational identity | 48.98580 pt |
| SIADS supplement | 23 | `manuscript/supplement.tex:1008`, operator/space definitions | 1.66727 pt |

These are actual shipped-source warnings, not just synthetic adversarial cases. The journal geometry puts the right text edge at 522 PDF points. Independent measurements of the shipped PDFs place the two command endpoints at about 557.31 and 581.11, the contrast-table entry at 538.77, and part of the rational display beyond 559.27. Thus the first four cases materially enter the margin. The final 1.67-point warning is small; normal punctuation protrusion elsewhere must not be confused with a substantial layout defect. None of these observations establishes clipping off the physical page or a scientific-content error.

The failure loop in `release/refresh_packages.sh:34` inspects only canonical manuscript, supplement, theorem-summary, and proof-skeleton logs. The detached journal builds at lines 421–447 and the cover-letter build at lines 449–460 are copied and packaged without an equivalent final-log check. The analogous final-document loop in `release/one_command_replay.sh` has the same coverage limit. The current journal PDF audit checks semantics, page counts, fonts, and the modulus tables, rather than the complete text-area boundary or all final build warnings.

The parent review's initial 96-page overview established readability and caught no clipping; it did not establish strict conformity to the journal text area. The later final-log inspection and independent coordinate measurements resolve that distinction. The canonical preprint builds have no corresponding selected warnings.

**Required repair for the journal versions:** allow the long commands to break, fit the contrast table within the journal width, and split the two long displays. Apply the same final-log policy to all canonical, detached journal, and cover-letter builds before copying or packaging their PDFs. Rebuild and inspect these pages, regenerate affected PDF evidence and bundles, and retain a journal-only overfull-box negative control. A synthetic journal-only overflow already demonstrates that the current refresh script otherwise packages a changed journal PDF successfully.

**Evidence:** [release report](release/RELEASE_REPORT.md), [unmodified final-log findings](release/DETACHED_FINAL_LOG_WARNINGS.json), [parent PDF-coordinate check](documents/ROOT_JOURNAL_MARGIN_CHECK.json), and [journal-only negative control](release/JOURNAL_WARNING_WITNESS.json). Full clean journal logs are retained in `release/logs/`.

## Previous findings: all closed

| Previous finding | Fresh verification | Disposition |
|---|---|---|
| N1: missing diagonal-D and singular-J assumptions in standalone statements | Source and rendered theorem-summary page 1 / proof-skeleton page 2 now contain the required assumptions; the main theorem was already correct. | Closed |
| N2: certificate variable ordering | Four certificate sections reject swapped declarations in 14 reader/generator calls; all 26 current unpacked implementations and 12 reader copies inside the seven current ZIPs match. C1 is a distinct coefficient-interpretation issue. | Closed |
| N3: Conradi–Mincheva–Uecker CSV columns | Both current CSV rows parse correctly and agree with the primary paper's numerical continuation and stable branch segments. | Closed |
| N4: ambiguous `a/bA` notation | Independent exact parsing checks all 218 rows in both versions; exactly 50 changed expressions preserve their coefficients. All five current table copies match. | Closed |

The comparison credits Conradi–Mincheva–Uecker's subcritical branch with stability after a fold, as shown in [their Section 4.3](https://arxiv.org/html/2605.16049v1). No new literature-attribution repair emerged from the bounded primary-source update search. The fixed-interval, stationary-spectrum, local-stability, and exponent-optimality limitations remain correctly stated. The review does not turn optional adjacent citations into submission requirements.

## Scientific verification and its limits

The [algebra review](algebra/ALGEBRA_REREVIEW.md) reconstructs realization, SCC localization, signed minors, the diagonal diffusion-ray theorem, conservation boundaries, and contrast/minimax proofs. A fresh reaction-derived exact program checks 912 principal matrices and 3,172 Hurwitz determinants, 85 omission identities through `m=12`, 30 conservation-boundary cases, all three `n=2` threshold-sign cases, and 24 contrast cases through `nu=10007`. An independent nonreal-instability example confirms why the general ray theorem's explicit wave limitation is necessary; it does not contradict that theorem.

The [PDE review](pde/PDE_REFEREE_REPORT.md) independently reconstructs the modulus identities, harmonic corrections, conservation gauge, scaled adjoint, dynamic cubic, crossing, and local stability argument. Its 453 exact checks include reaction-derived correction solves at six dimensions. Twelve additional exact Bernstein certificates verify the stated near-threshold positivity and Routh conditions throughout the prescribed epsilon interval and `t>1`. The integrated-mass constraint with unequal diffusivities, reflection symmetry, spatially varying patterned linearization, high-frequency control, and retuned robustness were checked explicitly; the delicate patterned-state spectral argument received a reciprocal algebra review.

These finite calculations support the general proofs; their counts are not claims of formal verification or independent proofs in every dimension. No new nonlinear simulation was run by the mathematical reviewers. The release lane did freshly regenerate the existing numerical provenance as part of portable replay. No new theorem gap or counterexample to a shipped result survived these checks.

## Release and document verification

Fresh execution confirmed 39 regression tests with no skips, all 39 normal verifier entrypoints, all 39 explicit optimized-Python rejection controls, the complete symbolic suite, minimal replay, and full current portable replay including numerical regeneration/provenance. All seven regenerated bundles are byte-identical to the released bundles. Three detached source builds compile successfully, with all six main/supplement text streams matching their intended shipped PDFs; the journal warning qualification is J1 above.

The tracked manifest covers 1,650 files, exactly excluding itself from the 1,651-file source archive. The portable 214-entry baseline remains unchanged; the regenerated 216-entry manifest verifies. Wrong-toolchain, manifest/data mutation, forged self-consistency manifest, canonical-warning, and stale-PDF-evidence controls behave as intended. All nine downloaded GitHub release assets match both their declared digests and corresponding target bytes, and the remote annotated tag resolves to the reviewed commit.

All seven PDFs were rendered and all 96 pages inspected: canonical manuscript 19, canonical supplement 19, theorem summary 3, proof skeleton 6, SIADS manuscript 24, SIADS supplement 24, cover letter 1. Fraction legibility and restored hypotheses are confirmed. See the [document review](documents/DOCUMENT_REVIEW.md), [release report](release/RELEASE_REPORT.md), and [positioning report](positioning/POSITIONING_REPORT.md) for detailed evidence and scope.

The optional five-archive historical-lineage replay could not be completed because its external inputs remain unavailable. Its nonmutating, failure-sensitive preflight was tested, including preservation of an archived-success log sentinel. This is not a historical replay success. The complete current portable replay needs none of those archives and did pass. Google Drive contents, a live submission portal, and a preprint service's server-side build were not checked this round.

The user-confirmed declarations are present and are not reopened. DataCite confirms the exact v1.0.10 DOI [10.5281/zenodo.22559244](https://doi.org/10.5281/zenodo.22559244). Current source accurately links the immutable tag and concept DOI and labels the older exact DOI as v1.0.9. Using the newly registered exact DOI in later submission metadata is optional maintenance, not a publication blocker.

## Reproduction and scope of this audit artifact

`recreate_snapshot.py` reconstructs the reviewed source using `SOURCE_INVENTORY.json`; the bulky snapshot and disposable mutation/build trees are intentionally ignored. `check_audit_evidence.py` checks source identity, retained evidence syntax, and the report's local links. Each lane's report names its scripts, dependencies, output logs, exact witnesses, and limitations. Independent mathematics uses SymPy 1.14.0; official release replay and PDF mutation use the recorded pinned CPython 3.9.6 and TeX Live 2022 toolchain. Toolchain paths in the retained local drivers may need adjustment on another machine.

Only this independent review folder is changed by the review. No manuscript repair, tag replacement, new immutable release, submission, or external outreach was performed. Completion of the referee round means the supported findings and checkable evidence are delivered; it does not mean C1 or J1 has already been repaired.
