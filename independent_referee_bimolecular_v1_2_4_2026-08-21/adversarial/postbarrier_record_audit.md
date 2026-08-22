# Post-barrier adversarial audit of author-generated records

**Packet:** `bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`  
**Audit timestamp:** 2026-08-21 22:44 PDT  
**Relation to blind report:** the blind mathematical report was completed and frozen before these materials were opened  
**Completion estimate:** 100% of the assigned post-barrier record audit

## Scope

After the information barrier was lifted, I inspected the previously embargoed audit, preservation, validation, reproduction, research/revision-log, reviewer-checklist, expert-note, manifest, report-copy, archive, metadata, and release-script materials. I did not rerun the canonical suite; that remains the software referee's track. I did perform independent read-only hash, path-coverage, copy-equality, archive-extraction, and public-tag checks.

## Executive finding

The author records substantially agree with the blind analytic assessment and reveal no new mathematical counterexample or proof gap. They are useful claim inventories, but they are not independent scholarly validation: the package itself says the audits arose in an AI-assisted, author-directed workflow and explicitly disclaims prior independent expert-human validation.

The records do, however, strengthen the blind report's release-provenance finding. They show that public release sequencing was still pending, while the manuscript, metadata, CFF file, supplement, and reproduction instructions speak as though the tagged v1.2.4 release already exists. More seriously, `validation/replay_release.sh` does not enforce the exact v1.2.4 tag: it prints `Exact tag: none` and continues. This contradicts the top-level packet README's statement that the standalone runner merely omits the release script's exact-tag assertion. The absent tag therefore is not just a publication-timing issue; the claimed fail-closed tag provenance is not implemented.

This is a material supporting-package defect, but it does not affect the analytic theorem.

## Severity-ranked findings

### Major artifact/provenance finding

**A1. The v1.2.4 release is not publicly anchored, several files prematurely describe it as released, and the clean-checkout replay fails open on the exact tag.**

Evidence:

1. The independent blind check and a fresh public check found no `bimolecular-positive-recurrence-v1.2.4` tag. The exact GitHub tree URL returned 404, and `git ls-remote --tags` returned only the queried v1.2.3 tag.
2. The packet's own records acknowledge the unfinished step:
   - `research_log.md` lines 16–22 says a Zenodo action should occur only after the public-tag replay and that “only public release sequencing remains.”
   - `preservation/VERSION_1.2.3_PROVENANCE.md` lines 3–4 calls v1.2.3 public and v1.2.4 merely “prepared.”
   - `audit/publication_v1_2_4_editorial_audit.md` lines 59–60 says hosted main/tag validation will be supplied “after publication.”
   - `submission/zenodo_deposit_checklist.md` lines 35–39 directs the author to verify the public v1.2.4 tag on deposit day.
3. In contrast, present-tense or release-dated claims occur at:
   - `manuscript/paper_content.tex` lines 1139–1146: supporting materials “are available” in the tagged v1.2.4 directory;
   - `manuscript/supplementary_note.tex` line 136: “From the tagged Version 1.2.4 release directory”;
   - `supplement/ai_use_full_statement.md` lines 12–13: “Stable tagged location”;
   - `submission/biorxiv_metadata.md` lines 98–112 and `submission/biorxiv_upload_instructions.md` lines 117–120: live tag URLs;
   - top-level `CITATION.cff` lines 9–12: version 1.2.4, `date-released: 2026-08-20`, and the nonexistent tag URL;
   - `validation/REPRODUCTION_RECORD.md` lines 3–20: release date, canonical tag, and clone/checkout instructions that currently fail.
4. `validation/GIT_TAG_AND_COMMIT.txt` records the intended tag name but no v1.2.4 tag object or commit. It records only the v1.2.3 parent's exact identifiers. Unlike the earlier preservation records, there is no current immutable identifier to verify.
5. The exact-tag failure is operational:
   - `validation/replay_release.sh` lines 12–18 runs `git describe --tags --exact-match`, but on failure merely prints `Exact tag: none`;
   - no later line compares the discovered tag with `bimolecular-positive-recurrence-v1.2.4` or exits when it is absent/wrong;
   - line 56 can therefore print `PASS: complete Version 1.2.4 release replay` on an untagged or differently tagged clean commit if the package bytes otherwise agree.
6. This contradicts the packet README, lines 52–54, which says the standalone packet omits the release script's “exact-tag and clean-Git-status assertions.” The clean-status assertion exists; the exact-tag assertion does not.

Why it matters:

- The internal hashes authenticate consistency only relative to checksum files shipped in the same unauthenticated packet. With no published tag, trusted external digest, or exact-tag enforcement, they do not establish Git provenance.
- A replay on the wrong clean commit can be reported as a complete v1.2.4 release replay.
- The paper's availability statement and deposit metadata are false at the check time.

Repair:

1. Add a literal expected tag, require `git describe --tags --exact-match` to succeed, and require exact equality with `bimolecular-positive-recurrence-v1.2.4`; fail otherwise.
2. Create and publish the annotated tag only after the exact tree passes the replay.
3. Preserve or publish the resolved tag-object and commit identifiers and an externally anchored ZIP/manifest digest.
4. Recheck every v1.2.4 URL, then correct the release date/present-tense wording if publication has not actually occurred.
5. Run the repaired replay from a fresh detached checkout of the public tag.

### Minor evidence finding

**A2. Claimed “independent computational stress” counts have no reproducible artifact in this packet.**

`audit/publication_v1_2_submission_audit.md` lines 35–41 reports exhaustive checks of 1,687 graphs, 149,058 return witnesses, 366,324 population transitions, and 7,168 ACK episode cases over 1,024 rate vectors. Searching the entire packet found those numbers only in that narrative audit. No script, input enumeration, output, seed record, or transcript reproduces them.

The audit correctly calls the computations falsification aids rather than proof, so this does not harm the theorem. It does mean those particular counts cannot be credited as independently supported evidence. Either include a disposable/reproducible script and expected digest or remove the quantitative claim.

### Minor documentation finding

**A3. The expert-note audit pointer is stale.**

`expert_audit_note.md` lines 229–234 calls `audit/publication_v1_2_submission_audit.md` “the current audit,” although the package includes later v1.2.1, v1.2.2, v1.2.3, and v1.2.4 audit records. This does not change any mathematical statement, but it weakens navigation and version clarity. Point to the v1.2.4 record and label the v1.2 submission audit as the last full adversarial/release audit if that is the intended distinction.

### Notes on evidentiary circularity

**A4. The author-generated audits are not independent corroboration, although the package discloses this appropriately.**

- `supplement/ai_use_full_statement.md` lines 5–10 and 43–66 says AI systems were used for derivation, adversarial review, code, literature work, drafting, revision, and release validation.
- Lines 74–80 says AI output was working material, not scholarly authority or independent expert validation.
- Lines 91–100 says the author curated the package and that no prior independent expert-human validation is claimed.
- The package README lines 148–153 repeats that limitation.

Accordingly:

- `expert_audit_note.md` is a careful restatement/orientation to the manuscript, not an independent referee report.
- `supplement/reviewer_checklist.md` is a strong checklist, not evidence that its checks were performed.
- The successive `audit/` files record author adjudication of AI/model reviews and release activity. Their conclusions cannot be counted as statistically or institutionally independent of the manuscript-development process.
- The three canonical JSON reports are byte-identical copies of one generated object, not three independent validations.
- A manifest and a checksum file shipped with the files establish internal integrity after one input is trusted; they cannot authenticate their own provenance.

This is an evidentiary limitation rather than a hidden circular inference in the mathematical proof. The manuscript itself does not use the tests, reports, or audits as premises.

**A5. Historical validation claims lack raw v1.2.4 transcripts inside the packet.**

The v1.2.4 editorial audit and packet build log say that PDFs were rebuilt twice, 50 rendered pages were inspected, Python 3.11/3.14 tests passed, and release workflows succeeded. `validation/REPRODUCTION_RECORD.md` describes a GitHub Actions artifact that would contain console output after a tagged run. Because the tag/job is absent, that hosted transcript is unavailable. The narrative logs alone do not independently prove the historical multi-version runs or visual inspection.

The software referee's current replay can independently establish what passes now in its environment, but should not retroactively certify the claimed historical environments or hosted workflow.

## Independently verified internal consistency

The following local consistency claims are affirmatively supported without relying on the author narratives:

| Claim | Independent result |
|---|---|
| Two package manifests agree | PASS: `supplement/MANIFEST.sha256` and `validation/MANIFEST.sha256` are byte-identical. |
| Manifest size and durable-tree coverage | PASS: 82 entries cover every one of the 84 package files except the two manifest copies themselves. There are no symbolic links. |
| Manifest hashes | PASS: independently recomputing SHA-256 for all 82 listed files produced zero mismatches. |
| Canonical report copies | PASS: `code/verification_report.json`, `supplement/verification_report.json`, and `validation/VERIFICATION_REPORT.json` are byte-identical, each SHA-256 `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`. |
| Archive membership/content | PASS: the supplied ZIP has 84 members; extracting it and recursively comparing against the 84-file package tree gave no difference. ZIP SHA-256 is `66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f`. |
| Packet checksum coverage | PASS: `PACKET_SHA256SUMS.txt` has 89 entries covering all 90 packet files except itself; independent recomputation produced zero mismatches. |
| Deterministic regeneration of report/PDF/ZIP | Not repeated in this record audit by assignment. Equality of supplied copies/content does not alone prove deterministic reconstruction. |
| Git-tag provenance | FAIL at check time: public v1.2.4 tag absent; release replay has no fail-closed exact-tag assertion. |

These checks show that the copied packet and ZIP are internally coherent. They do not turn the packet into a Git-authenticated release or establish the universal theorem.

## Comparison with the frozen blind report

### Agreements

The author records and blind report agree on:

- the exact theorem and its one-linkage/bimolecular scope;
- all twelve load-bearing analytic interfaces;
- treatment of the zero complex, faces, repeated species, self/parallel/equal-displacement channels, parity/lattice classes, absent species, absorbing states, zero-length paths, separated rates, and zero-weight divergent coordinates;
- the ACK example and rate-degeneration calculations;
- the distinction between finite falsification and universal proof;
- the current primary-source account of Anderson--Cappelletti--Kim, Paulevé--Craciun--Koeppl, Xu v2, and the announced two-species work;
- the absence of prior independent expert-human validation.

No author record exposes a mathematical disagreement with the blind reconstruction.

### Additional coverage found after the barrier

The reviewer checklist explicitly names two attacks that the blind report subsumed under broader reasoning but did not list verbatim:

- a deviation whose target coincides with a later designated-path vertex; the episode still stops because continuation is channel-specific, so this creates no recursion defect;
- exponentially separated divergent coordinate scales with a pure-double source on the slower coordinate; retaining all divergent coordinates in \(I\) handles it.

These are useful additions to the coverage inventory, not gaps in the blind conclusion.

### Disagreement/omission

The only substantive disagreement is with release claims, not mathematics. The blind report classified the missing public tag as a repairable availability defect. The post-barrier record audit shows that:

- author records implicitly knew publication/tag sequencing remained unfinished;
- no record reconciled that fact with the manuscript/CFF's present-tense release claims; and
- the supposed exact-tag replay is not fail-closed.

That makes the provenance defect sharper than could be seen from the manuscript alone.

## Bottom line

The post-barrier materials add no reason to retreat from the blind analytic conclusion. They also should not be cited as independent confirmation: they are transparently author-curated, AI-assisted records, and much of their mathematical content paraphrases the manuscript.

The internal package bytes, manifests, report copies, and archive content are coherent. The v1.2.4 Git release/provenance claims are not: the public tag is absent, present-tense release metadata is premature, and the purported release replay does not enforce the expected exact tag. This must be repaired and independently replayed before the supporting package can be described as a validated tagged v1.2.4 release.
