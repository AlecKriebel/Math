# PR883 / PID9900008 — new whole-paper and whole-package review 01

Completed UTC: 2026-10-15T12:53:31.701619+00:00. Review completion estimate: **100% of this review**, not of the overall research/publication program. Decision: **ISSUES**, with one publication-metadata issue (four exact fields). No mathematical, current source-credit, PDF-layout, metadata-content, archive-binding or reproducibility defect was otherwise identified. This is a whole-package review of the exact r1 seal below; it is not a tools-only or disposition-only review, and it is not a CLEAR.

## Exact reviewed object

- Original head: `af25d26e21945a1a132aace5e600485152777070`; 26 original files, 211,771 bytes; author effort `1/5`.
- External original source-manifest SHA-256: `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`.
- Outer root: audit-parent-relative `replay/revision_r1/`; 220 files including its manifest. Externally supplied outer manifest SHA-256: `c44749d8a50f7f61c1d35cd1d27e385ff6d7e693a3d5bb3650260d0ae36fd29b`.
- Expanded portable tree: `preprint/verification_package/`, exactly 180 members; package index SHA-256 `752a263aaeeab30d1ea5a2bf4f23498e381335ad41d3fb0240ce5223b313b279`.
- PDF: 67,331 bytes, four A4 pages; ZIP: 516,468 bytes. Their exact hashes, and all other core pins, are below.
- Tooling manifest authenticated against externally supplied SHA-256 `86290fcc61e5a54a51a2108b55c408961938c45380a9a2bac156fdec8d264585` before code use. The actual script digests, not copied informal descriptions, govern execution.

| Core path relative to reviewed outer root | Bytes | SHA-256 |
| --- | ---: | --- |
| `preprint/note.tex` | 13696 | `c73d440864ce0a2798519218d86e25639ab0b012d7cca62797ecefa141bbe91a` |
| `preprint/output/pdf/note.pdf` | 67331 | `9e3089fc3ef667e9fcdadf0e1a71ef92e83fdd901fa77b4e2e9b00a2ae8c91d4` |
| `preprint/metadata.json` | 5622 | `11a1e472e48e48a157ea52cf8f290aaa40f3f926538768d997a2482add4683fd` |
| `preprint/CURRENT_PRIORITY.md` | 5048 | `13511a67aa4bc017fc669ae672a3c1fc1e263e3b7f974060e8223c3a986171fe` |
| `preprint/README.md` | 8705 | `2c8b2847a9375bafa3cc1a31013be174d841a25fada53e1027a150961e01c539` |
| `preprint/verification.zip` | 516468 | `fddf595a125ab4efa5100d2c477865bdcb94469ff178bb65fe23301b25398b06` |
| `preprint/zenodo-deposit.json` | 5928 | `c873682d7299fd7569aa34a302e7b06d82e4c0f9883c3d714c3f4f1b1106f991` |
| `preprint/build_verification.py` | 17641 | `2b0521d74a49360cbdd6d48427cb02763b586f3a5196766ec16f6ddc2fa41f2c` |
| `preprint/check_originals.py` | 30482 | `e4fb73b16db72ed4387c08c38662a1ad9f836f9b0ecd2ff91778347deb74829b` |
| `preprint/verify_package.py` | 16013 | `e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8` |
| `preprint/verify_current_publication.py` | 21129 | `3fc89372bae6cc3ed2f6a8d4f93d890e94e9fd635b712223853630d26f034672` |

Every one of the 219 manifest rows was independently checked against the complete file bytes, and the actual tree had exactly those rows plus the manifest. All core rows match the external seal. All 180 ZIP members equal their expanded-tree bytes, with no extra or missing member. All 26 originals remain unchanged under portable `source/`; the required 24 outer original copies remain unchanged. All 11 audit-family public allowlists match their declared hashes and closed memberships (the classical historical allowlist declares hashes without byte fields; the current enclosing index binds exact sizes). Read-only Git-object inspection separately confirmed all 220 corresponding target blobs at prepared commit `16f0a28cf22896ade9a8d0dd1f8d15736e48f26c` and exactly one target QUEUE row, literal `claimed_solved`, effort `1/5`, blank DOI. This is a prepared local-commit check, not a fresh remote-state gate or approval to mutate it.

## Required repair — PKG01-1

The public portable tree and the identical public ZIP retain four absolute local-path values. Two are recorded command paths within the researcher's private workspace; two additionally contain disposable `private_replay` directory names in FileNotFoundError diagnostics. They are outside the immutable original 26 files. Their precise locations relative to the portable tree are:

| Public JSON | JSON pointer | Exposed value category |
| --- | --- | --- |
| `audits/allocation_audit_01/RECEIPT_NORMAL.json` | `/command/2` | absolute local provenance path |
| `audits/allocation_audit_01/RECEIPT_OPTIMIZED.json` | `/command/3` | absolute local provenance path |
| `audits/artifact_audit_01/ADVERSARIAL_NORMAL.json` | `/probes/11/detail` | absolute ephemeral private replay path |
| `audits/artifact_audit_01/ADVERSARIAL_OPTIMIZED.json` | `/probes/11/detail` | absolute ephemeral private replay path |

The actual absolute values are deliberately not repeated here. `PUBLICATION_METADATA_ISSUE.json` binds each affected original file by byte count/hash. This is publication metadata hygiene and consistent safe packaging, not a mathematical counterexample, credential compromise or claim that file-path disclosure alters the test outcomes. The format-review evidence already applies pointer-level temporary-path normalization; these older fields escaped that treatment.

Preserve the exact originals privately and record their byte/hash pins. Normalize only those values to stable repository-relative or `PRIVATE_TMP` descriptions, record the exact transformed pointers, preserve test results and the distinction between raw-output hashes and normalized-file hashes, then update the affected family manifests and every enclosing copy/index/ZIP/outer seal. Do not rewrite immutable original source evidence. New whole-package reviews must bind the resulting exact seal. A proposed repair is not accepted by this r1 verdict; the current r1 remains an ISSUES checkpoint.

## Independent chronology and mathematical assessment

The original Thorisson Section 4 pp. 5–6 and LT2009 Sections 2–3, Definition 6.1 / Remark 6.2 and Problem 7.5 were read before candidate proof or earlier reports. `SOURCE_CONTRACT.md` was frozen first. The candidate and operative primary bodies were then read, an independent reconstruction and falsification attempt completed, and `ANALYTIC_VERDICT.md` frozen before earlier audit conclusions were consulted. The hand-entered approximate minute labels were corrected against the clock and the correction was logged candidly; no analytic substance or event ordering changed. Parent-supplied seal metadata was read during authentication; its audit-family names were not treated as proof verdicts.

The exact historical implication is refuted by an allowed R² example with constant X. For μ=λ₁⊗(Σδ_n+2Σδ_(n+1/2)), the circle phase is measurably recoverable from the density-one line family. The phase map is vaguely continuous and injective; compactness gives a measurable inverse. The action is jointly Borel, flow-adapted and has stabilizer R×Z. Compact rectangles have finite mass; the measure is nonzero and diffuse, with origin in its support under Q=δ₀.

For an arbitrary original-state measurable displacement π, pointwise covariance forces every light line to use the same translation (a₀,b₀) and every heavy line to use (a₁,b₁). Preservation at the sole Q-supported state gives, by finite segment tests, δ_[b₀]+2δ_[1/2+b₁]=δ₀+2δ_1/2 per period. New residues, collision and swapping fail respectively by positivity, mass three and reversed unequal weights. Hence b₀,b₁ are integers and the root shift fixes the full observed state. Horizontal splitting, independently rearranging integer-indexed lines, and arbitrary reassignment of the null root contradict pointwise covariance itself. No injectivity or spatial regularity assumption is used. The proof covers preservation only Q-almost surely and also the bracketed σ(ξ)-measurability version.

For C=[0,1)², every translated window C−U has exactly one light and one heavy line of horizontal length one, including half-open boundary cases; its mass is always three. Conditional mass resampling gives H(θ_Vμ)=2 with probability 2/3 for the measurable evaluation H(η)=η([0,1)×{0}), whereas H(μ)=1 deterministically. This is a lawful window with Haar-null boundary and no zero-mass conditional case. The first marginal differs, which disproves the full joint identity (θ_Vω,U+V) ≡d (ω,U). Uniform-phase stationarity, intensity three and Palm weights (1,2)/3 independently agree with this calculation but do not replace it.

The transfer lemma was independently verified for every lifted allocation: covariance in the added direction forces (s,u)↦(ρ_y(s),u+b(θ_sy)), and Tonelli gives the image mass of A×B as λ₁(B)ρ_*ζ(A). This proves preservation transfer in both directions using finite rectangle covers and permits arbitrary collisions. Root shifts project through J. The cylinder inverse Dη(A)=η(A×[0,1)) is measurable and locally finite; the product image is an invariant Borel equalizer, so global extension by zero off-image uses no hidden state. LT2009 Example 7.1 and LT2014v1/2015 Section 8 Proposition 1 actually supply the stated full old-input route; the atom-weight counterevent remains visible after taking the ξ marginal. The v1 proof's window-size typo is corrected in v2 and does not affect the proposition or the independently verified product experiment.

The Markov matrix (1,2)P=(1,2), P=[[0,1],[1/2,1/2]], defines the stated measurable covariant root-changing preserving kernel. The stationary-background allocation in the supporting allocation audit was also checked analytically: cellwise compression of a light interval to half a heavy interval, expansion of half a heavy interval to a light interval, and retention of the other heavy half produce exactly the target densities. These are valid class-boundary controls. The measure's continuous invariant direction and singularity are permitted by the source question. No one-dimensional, positive-density, free-action, no-invariant-direction, background-augmented or all-Markov result is promoted.

Independent exact finite diagnostics enumerate all displacement-residue pairs on grids m=2,4,8,16,32,64,128,256 and every corresponding window phase, including boundary phases. Only retention preserves the weights and every window mass is three. The saved `independent_checks.py` reproduces `INDEPENDENT_FINITE_CHECKS.json` in normal and optimized mode with explicit guards. These finite computations supplement the analytic argument and cannot prove the universal measurable claim.

## Priority, status and inherited evidence

The complete negative existential conclusion follows from established inputs, not merely a similar construction. The current abstract, note, README, priority notice and metadata state this prominently, display its allocation bridge, credit LT2009 and the 2014v1/2015 proposition, and identify the periodic rational model as an illustration. The actual LT2023 Section 8 / Remark 8.1 and KM2025 final Remark 3.2 were checked: both support the credited parallel-line/invariant-direction and atomic-quotient balancing mechanisms. Their different balancing-existence scope is accurately distinguished from the exact self-preserving-law question. The current note makes no new-discovery, exact-formula novelty, first-recognition or worldwide-current-openness claim.

The two earlier bounded priority reports, their search/edition ledgers, the rejected reclassification proposal, both disposition objections and the separate repair verification were reviewed after the analytic freeze. They are dated evidence. The present account neither redefines `already_solved` to require a recognition event nor turns failure to locate one into proof of openness. Retention of literal `claimed_solved` is explicitly described as an operational judgment based on the complete historical answer and no supplied novelty requirement. I find no additional disposition defect in that qualified presentation and recommend no status mutation. This review does not certify that the historical problem was actually open when the attempt began.

`PRIORITY_ASSESSMENT.md` records eight fresh bounded queries, primary-body checks and the exact limits. All five original source PDFs and all twelve additional PDF/text pairs were independently authenticated, the latter by fresh extraction; seventeen distinct editions is accurate. Authentication is not exhaustive proof review of all seventeen sources. The operative bodies for every current-note credit were inspected; descendant/inaccessible literature remains bounded scope evidence as disclosed. First explicit recognition and periodic-formula priority remain unknown. Those are not hidden by the present novelty disclaimers and are not certified here.

The retained earlier evidence was checked for its actual scope: the initially nonblind source audit discloses its reading-order limitation; the separate blind mathematical audit supplies a separate source-first record; the equal-weight reviewer control was corrected because half-period phases then coincide as observed measures; old parser/closed-tree weaknesses are distinguished from fixed-byte original integrity; the ignored-DEFLATE-suffix defect, repair and fresh finite-format clearance remain separately dated. The current scripts contain the repaired exact-consumption checks. The earlier reports and original accepted ZIPs are not passed off as current package approval. Historical auditor code is evidence requiring its original external inputs, not an extra current entrypoint; the omitted historical executable is expressly absent and not replayed. Other-PR references in frozen originals were not followed and supply no needed current proof assumption.

## Actual reproduction and artifact consistency

All four current script bodies and both original executable bodies were read in full and separately byte-authenticated before executing private copies. Current code pins are in `CODE_AUTHENTICATION.json`; original author verifier SHA-256 is `020486719783210fe4fe714d368f8168c503269f8aaf878e8f37cce021a05887` and original publication wrapper SHA-256 is `ffabe0fb3a3ba791eb7b3bb2af93b755bb1fc9410ce12ac385b353d3f96b63fd`. Execution was isolated with -I -S -B, adding -O for optimized runs; working directories were unrelated to the copied package. All temporary trees were review-owned; candidate and raw corpora were never modified or copied into the package.

The actual commands below use stable placeholders for private ephemeral paths. Raw stdout/stderr receipts remain private; public summaries preserve actual return codes, counts and hashes.

```text
python3 -I -S -B <R>/verify_current_publication.py c44749d8a50f7f61c1d35cd1d27e385ff6d7e693a3d5bb3650260d0ae36fd29b --root <R>
python3 -I -S -B -O <R>/verify_current_publication.py c44749d8a50f7f61c1d35cd1d27e385ff6d7e693a3d5bb3650260d0ae36fd29b --root <R>
python3 -I -S -B <P>/build_verification.py <P> 752a263aaeeab30d1ea5a2bf4f23498e381335ad41d3fb0240ce5223b313b279 e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8 <FRESH_NORMAL_OUTPUT>
python3 -I -S -B -O <P>/build_verification.py <P> 752a263aaeeab30d1ea5a2bf4f23498e381335ad41d3fb0240ce5223b313b279 e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8 <FRESH_OPTIMIZED_OUTPUT>
python3 -I -S -B <P>/check_originals.py 752a263aaeeab30d1ea5a2bf4f23498e381335ad41d3fb0240ce5223b313b279 --root <P> --verify-only --catalog <ORIGINAL_CATALOG> --problems <ORIGINAL_PROBLEMS> --reports <ORIGINAL_REPORTS> --pdf-dir <ORIGINAL_FIVE_PDF_DIRECTORY>
```

R is the private copied outer root; P its portable subtree. All five commands exited zero, empty stderr, PASS. Each of the first four performed exactly six direct plus sixteen nested archival executions, retaining requested/effective isolation flags and exact historical outputs. The two outer receipts are identical across interpreter modes. Each builder emitted the sealed 516,468-byte / 180-member ZIP with SHA-256 fddf595a125ab4efa5100d2c477865bdcb94469ff178bb65fe23301b25398b06 under Python 3.14.6 / zlib 1.2.12. Compression equality is limited to identical inputs and the same runtime, as the documentation says.

The optional source command independently streamed/authenticated the three complete original corpora, parsed them sequentially, matched the complete canonical 5,255-byte record/report pair and statement/catalog binding, and authenticated the five original PDF editions. It reported zero direct/nested archival executions, as --verify-only promises. No 180 MB corpus copy, chmod or truncate occurred. An additional valid/restored outer --verify-only run each passed with zero archival executions; an added unlisted file and a same-length note-byte change each rejected on the intended membership/pin layer. These mutations were private-copy-only and restored before final verification. The checks authenticate bytes and stated finite diagnostics; they prove neither universal mathematics nor novelty or publication authorization.

## PDF, metadata and public-content QA

The original sealed PDF was rendered read-only with Poppler at 90 dpi, and every page was visually inspected. All four pages have legible mathematics and references, consistent A4 margins/numbering and no identified clipping, overlap, missing glyphs or unresolved references. The proof spans pages 2–3 with H at the foot of page 2; the continuation is readable. Author and ORCID match. `pdfinfo -url` confirms the intended ORCID, Thorisson, four DOI and two arXiv-version targets (nine external annotations because one long URL spans lines). URLs match the TeX targets; primary-body authentication is separate from annotation correctness. The PDF was not regenerated.

Parsed `metadata.json` equals exactly `zenodo-deposit.json`'s metadata. The deposit has exactly these two ordered path/name pairs: output/pdf/note.pdf → diffuse-allocation-note.pdf; verification.zip → diffuse-allocation-verification.zip. Date/version/title/author, full old-input credit, scope limits, extensive AI-use and unrefereed/no completed human or formal review disclosure agree with the note. The plain PDF has no filled form, JavaScript or encryption according to Poppler. No DOI, upload or tracker action is inferred from local receipts.

Closed inventories, archive-member inspection, ordinary content/filename inspection and the explicit public manifests found no raw third-party publication files/extracts, whole corpus records or credential material distributed in the candidate. The four local path strings in PKG01-1 are the identified publication-metadata exception; they do not contain the referenced private file bodies. This was an ordinary scientific artifact review, not a hostile-software security audit.

## Final scope and remaining gap

Strongest verified result: the entire source-scoped universal-allocation counterexample and full known-input deduction are sound under the primary conventions; the paper honestly presents an explanatory historical answer; sealed artifacts reproduce and the four-page PDF is usable. The sole required package repair is PKG01-1. Historical firstness/current-openness remain unestablished and unclaimed. No live eligibility, merge, production upload, DOI, tracker entry or overall program completion is approved. This exact r1 package does not count toward a successive CLEAR sequence.

No outside individual was contacted, no outreach was prepared, no other PR/chat was inspected, no Git mutation or remote publication occurred, and all review writes stayed within the dedicated review folder. Public distribution is restricted to this review's explicit PUBLIC_MANIFEST.json allowlist; raw sources, extracts, receipt originals, copied packages, builds and renders are excluded.
