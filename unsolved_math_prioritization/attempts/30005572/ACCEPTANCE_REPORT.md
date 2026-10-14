# Eisenstein reader: independent preservation and publication review

14 October 2026. Problem 30005572. **ACCEPT the corrected reader for publication as a faithful, restricted partial-results collection. The original mathematical problem remains UNSOLVED.**

This is an independent internal AI packaging, preservation, source-labeling and scope review. It adds **zero mathematical passes**, proves no new theorem, and does not claim novelty, journal peer review, human expert validation, or formal proof-assistant certification. The five-pass mathematical investigation is closed at its recorded restricted acceptances.

## 1. Decision and exact artifact

Publish the [corrected reader](corrected_reader/README.md), retaining its complete directory structure, mandatory qualifications, correction history, checks and manifests. The sole discovered publication defect was stale documentary-status wording for P25–P27 in the overview index and preservation inventory. Those statements still described the formal acceptance as pending even though A16 was already present and explicitly accepted the exact three proof hashes. The corrected derivative updates that status; it changes no mathematical scope or argument.

The [explicit packaging correction mapping](corrected_reader/PACKAGING_CORRECTIONS.json) records each changed content file's input/output hashes and byte counts. The input reader and accepted research originals were not edited.

Frozen input reader:

- FILE_MANIFEST.json SHA-256: `79dfe943753601f579caac939fa92fb7c799c37aea4544569bff469e31d6bc2b`
- SHA256SUMS SHA-256: `efa8816dc0010d874abd7f4b86859957392dbb901e47ddfd07c560408fe5a5f7`
- 116 files, 114 manifest members, 115 checksum entries

Accepted corrected reader:

- FILE_MANIFEST.json SHA-256: `01cb9d0bbbafe7c4bbbbdd6734c47dbc212e7da543f5b8ef3d78484aba8e1d66`
- SHA256SUMS SHA-256: `7558eb7a873350a2ce7ed85191c0c166031ef3dc7a2b4cc6059349168eaae324`
- 117 files, 115 manifest members, 116 checksum entries

The corrected directory changes only PROOF_INDEX.md, PRESERVATION_INVENTORY.json, README.md and the two generated file-integrity records, and adds PACKAGING_CORRECTIONS.json. READER.md, all proof/qualification/review texts, all mathematical checks, all frozen outputs, source references, and mathematical correction history remain byte-identical to the input reader. Original VALIDATION.json and REPLAY_RESULTS.json are expressly identified as historical assembly records, not silently relabeled as this review.

## 2. Byte preservation independently established

The [input verification](ORIGINAL_READER_VERIFICATION.json) and [corrected verification](CORRECTED_READER_VERIFICATION.json) record the independent results.

- All 34 full proof/addendum texts and both mathematical qualifications were matched to actual original files by SHA-256 and byte count.
- All 22 internal mathematical review reports were likewise matched to their original bytes.
- Every proof/qualification original hash was found in each acceptance report designated by its inventory entry. In particular, A16 pins the corrected P25–P27 package, not its rejected initial main-note hash.
- The three attribution deletions and two administrative-reference replacements were replayed from original bytes, checking each intermediate hash, offset, removed-slice hash, replacement-slice hash, and resulting complete file.
- Those five operations affect four proof derivatives: P03, P09, P23 and P34. Direct inspection confirms that they remove process attribution or redirect administrative references. They remove no equation, hypothesis, qualification, mathematical source scope, correction or unresolved obligation.
- Every other preserved proof, qualification and review is byte-identical. Both L1 and L2 are unchanged. No additional proof transformation was made during this review.
- All manifest entries and all checksum entries match; exact coverage was checked, not just listed-file validity. No symlink is included.

This establishes faithful preservation of the accepted record. It does not rerun or certify every mathematical argument from first principles.

## 3. Scope preservation

The complete reader narrative and indexed scopes were compared with the accepted record, with focused inspection of the final combined reviews, A16, L1/L2, the final restriction statements, and the correction history. No mathematical claim enlargement was found. The following distinctions are retained explicitly.

1. **Target and adopted interpretation.** The absolute integer-ring target, the genuine relative theta prescription, all ideal-class components, proper small levels and exact admissibility requirements are retained. The inverse bad-U condition is labeled an adopted strengthening rather than a Bianchi formula literally printed in the original question. Source calibration is also explicit. Squared absolute norm means scalar factor t^4.
2. **Constants versus the construction.** The ramified-five constant kernel remains a genuine obstruction to the unmodified trace-fixed complex, not a counterexample to the requested map. Quotient exactness, ordinary lifting and canonical trace normalization remain distinct achievements.
3. **Five normalization and Hecke scope.** The canonical eventual-and-T5-fixed family requires auxiliaries prime to five. Arbitrary pullbacks are not asserted to preserve the normalization. The non-Cartesian incidence defect and transfer coboundary are retained. All-good-prime open-map Hecke compatibility is not promoted to an unrestricted integral Gamma0-cohomology identity.
4. **Arithmetic descent and auxiliary removal.** Proper unit-injective levels, all source components and the prime-power localized target remain. The exceptional full-ray character and class-group five-part are not discarded. Final ramified-five removal requires five prime to the class number and no tame level prime of norm one modulo five, with arbitrary depth at five. Full R-removal also retains its separate p-at-least-seven hypothesis.
5. **Bad primes.** The accepted theorem concerns the true inverse correspondence, p at least seven, proper lower level, high-level admissibility, and restricted norm-injective inflated-character blocks. Central ideal-class transport, low-unit multiplicity and marking corrections remain. Norm-zero is not canceled on wild degrees or noninflated characters. No pure-prime-power or five-primary extension is claimed.
6. **Topology versus arithmetic integrality.** Strict all-cusp reflection criteria are distinguished from the broader local-sign-trivial target projection. Existing-map hypotheses remain. Compactification preserves the existing coefficient target and does not remove arithmetic tame residues.
7. **Surviving arithmetic residues.** The q-adic kernel is not renamed the global congruence kernel. Ambient common annihilators and smoothing quotients are not confused with the compatible-family existence obstruction. No finite-module computation is presented as an actual nonzero residue or obstruction.
8. **Theta identities versus calibration.** Cancellation occurs in torsion-free universal groups before specialization, never by arbitrary division in specialized K2. Powered cyclic triangles are not promoted to unrestricted unpowered CM relations. The cyclic-four relative map's zero absolute restriction is not identified with the geometric absolute map. Raw theta-pair residues and the 576/624 comparison do not evaluate the moved arithmetic cocycle.
9. **Mandatory signs and models.** L2 retains the exact sign transport J2 = -Id, J1 = J0 = Id and the unresolved final edge orientation. L1 permits literal primitive transport only with its product-coordinate/transported-primitive hypotheses; independently chosen mixed primitives require a normalized comparison coboundary and orbit regularity before specialization. Neither correction is concealed by sanitization.
10. **Historical errors.** Rejected specialized-unit cancellation, the withdrawn general divided-power construction, the corrected nonprincipal package, the coordinate/fiber-direction correction, the corrected arithmetic example, source mislabeling, and optimized-away historical checks are all acknowledged rather than silently converted into accepted claims.

The final unresolved list still includes unrestricted small levels, surviving auxiliary blocks, actual prime-power integer-ring integrality, remaining cusp restrictions, unrestricted bad-U, and globally compatible unpowered source-signed relative calibration. The Gaussian middle-cusp values remain unevaluated. No counterexample to the complete construction is asserted.

## 4. Independent computation replay and runner inspection

[INDEPENDENT_REPLAY_RESULTS.json](INDEPENDENT_REPLAY_RESULTS.json) records a fresh isolated replay of all **21 checks and 51 executions** using Python 3.12.14 and SymPy 1.14.0. Every complete emitted result matches the frozen expected JSON byte-for-byte. The entire replay record also equals the original assembly replay record.

All 21 script and expected-output pairs were matched to actual original bytes. The runner was inspected for temporary-directory isolation, hash checking, process failures, expected-result selection and JSON comparison. Script imports and output writes were inspected; no script requires a source PDF, raw dataset or network access. Detailed logic inspection included scalar normalization, exact local smoothing/finite-family obstructions, induced residue modules and cusp reflection criteria. These are meaningful finite computations, with explicit limits, rather than prewritten success messages.

AST inspection found assertions in exactly C02, C04, C06, C07, C09 and C10. They run only normally. The other fifteen checks run normally, with -O and with -OO. The runner strips inherited PYTHONOPTIMIZE before running an assertion-based child.

[RUNNER_NEGATIVE_TESTS.json](RUNNER_NEGATIVE_TESTS.json) additionally records disposable-copy tests. Unknown IDs, a modified script, a changed expected-output pin and a changed expected result's semantics were all rejected. C04 still ran normally and matched the expected bytes when the outer environment set PYTHONOPTIMIZE=2. These tests never changed the accepted scripts or reader.

Verification limits remain important: the runner fails on semantic JSON differences; byte equality is separately recorded. No replay evaluates general number-field K2, unresolved moved cocycle residues, Gaussian cusp values, global CM descent, continuity, or unrestricted symbol-to-homology calibration. Successful finite checks are not a new mathematical pass or a formal proof certificate.

## 5. Citations, source evidence and public-link checks

All **11 retained-PDF SHA-256/size pairs** published in REFERENCES.json were independently matched to available original source bytes. Only the matching metadata is reported. No source PDF, extract, image or copied source document enters either deliverable.

The source labels preserve the distinction between the 47-page author-hosted LSSW manuscript and 46-page arXiv v1, without inventing an arXiv v2 or inferring a revision date from retrieval metadata. The historically mislabeled Tate file is identified as Bass; incomplete Kato retrieval is not evidence. Tate's 1976 comparison, the Banaszak–Popescu verification route, the unavailable Cremona PDF/erratum scope and the alternative rigidity reference retain their actual inspection limits. Source-inspection history is attributed to the earlier accepted reviews, not misrepresented as this review's independent reproof.

Every intended local Markdown file link was checked for existence and confinement within its reader directory: **287 in the input and 288 in the corrected reader**. Algebraic bracket expressions such as multiplication on torsion points are separately classified, not counted as missing file links. The author's count of 286 referred to its narrower curated-link set. Historical unlinked filenames in unchanged annexes remain historical identifiers; the preservation inventory and proof/check indexes provide the public locations. Omitted mixed manifests are not represented as supplied files.

All **35 distinct public URLs** appearing in the package were attempted through the web tool. [PUBLIC_URL_CHECK.json](PUBLIC_URL_CHECK.json) records 26 retrieved and nine unavailable through that tool. These are retrieval results, sometimes cached, not a guarantee of continuous live availability. Unavailable endpoints include the original report download, several DOI endpoints and previously limited source mirrors. They do not invalidate the byte-verified retained evidence. No unavailable source is newly claimed to have been fully inspected.

The author-hosted manuscript and fixed arXiv v1 again displayed 47 and 46 pages respectively. The public LSSW introduction retains coefficient, level and target restrictions and does not supply the missing relative calibration. This was a bounded source-labeling check, not a fresh literature search or theorem audit. Unversioned citation URLs may later resolve different bytes; the retained hashes identify the evidence actually preserved.

No repository publication or public artifact-sharing URL was created in this review. Remote accessibility and any eventual commit/PR links must be verified when publication occurs; no guessed share path is certified here.

## 6. Publication exclusions and remaining limits

The exact distributable file set was inspected for unexpected types, embedded PDF signatures, symlinks, private storage/room links and targeted credential markers. JSON files parse. It contains authored mathematical texts and audits, finite-check scripts/results, public citations and verification metadata. It contains no raw source PDF/text bundle, dataset contents, private-source location inventory, private personal information, conversation material or internal coordination document. Public author-hosted URLs containing a directory named Dropbox are scholarly URLs, not private storage links.

This is a bounded structural and content review, not an exhaustive automated privacy guarantee. Accepted proof prose necessarily discusses its mathematical sources and limited historical review status; that is distinguished from redistributing source documents or private coordination material. The review's public results intentionally omit original evidence storage paths.

There is **no remaining publication-packaging blocker** for the corrected reader at these exact hashes. Publication must retain its UNSOLVED status, restricted hypotheses, both qualifications, source limits and internal-AI-review designation. No queue, branch or remote state was edited, and no new mathematical direction was opened.
