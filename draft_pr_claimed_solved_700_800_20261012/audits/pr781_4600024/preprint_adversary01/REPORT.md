# PR781 whole-preprint adversarial review 01

**Verdict: repair required for one verification-software issue. No mathematical, original-problem, attribution, rendering, metadata or deterministic-package issue was found.**

Target: only eligible claimed_solved PR781/problem4600024, exact original head 4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f. The reviewed source manifest is externally pinned to c893760f12971fd4a36e695996304885bb5a927d7fd8cb68cd99fea78808f66e. INPUTS.json binds the six exact artifacts, release inventory, selected complete public record, and relevant software. This verdict applies to those bytes, including a later archived copy, not silently to any repaired release.

## Actionable issue

**[P2] Reject nonregular manifest and PDF inputs before opening them.**

In source/verify_bundle.py, line 22 executes (ROOT / "MANIFEST.json").read_bytes() before any regular-file check. Line 69 similarly calls pdf.read_bytes() on the optional supplied PDF. A named pipe in either location causes the verifier to wait indefinitely for a writer, rather than produce an integrity failure. This matters to a reproducibility tool advertised to check an externally pinned extracted source tree: malformed package inputs can prevent its custody decision.

I reproduced each input as a FIFO in owned temporary storage, without modifying any candidate file. In normal and -O modes, both manifest-FIFO and PDF-FIFO invocations failed to return before a two-second subprocess timeout. SOURCE_MANIFEST_FIFO_PROBE.json and OPTIONAL_PDF_FIFO_PROBE.json preserve those four initial cases. reproduce_read_guards.py / READ_GUARD_REPLAY.json independently reproduce the same pair of entry points along with nearby controls.

Repair both initial reads using explicit regular-file enforcement before reading, preferably open with O_NOFOLLOW | O_NONBLOCK and then fstat the opened descriptor. Keep the helper authenticated before import. Apply consistent handling to the pinned source/builder readers where appropriate. Add normal and optimized physical FIFO rejection tests, requiring prompt nonzero structured failure and unchanged protected input bytes. Rebuild the closed source ZIP, kit and release inventory and run a new whole-package review. No TeX or proof change is requested.

The helper FIFO and helper symlink already return "Nonregular builder"; a manifest directory, direct source-root symlink and PDF directory also reject. A symlink in an ancestor of the source root accepts identical bound source bytes; I do not count that alone as a defect in this read-only byte-custody interface, whose README specifically promises unsafe-ancestor protection for *outputs*. There is no demonstrated code execution or byte-authentication bypass. The defect is a reproducible blocking read.

## Mathematical review

MATH_DERIVATION.md gives an independent step-by-step reconstruction, including complete selected-problem matching, the regular ideal, all-radius/completion/larger-alphabet normalization, short-word graph language, the common-monoid import, the saturation and exact published profile step, image equality and finite reachability. Every implication has a checkable mechanism. Irreducibility supplies the needed connections; no mixing, synchronized presentation or empirical termination assumption is smuggled into the argument.

I independently fetched the actual PRZ2014 published PDF and inspected pp. 4--6 and 8--9. Its Theorem4.2 has precisely the claimed bound and common recognizing morphism. I also rechecked Boyle's actual author-manuscript p.17, Dykstra's actual thesis printed pp.46--48, and Ballier's actual v1 printed pp.9--13 (including Lemma2.1 and the restricted/existential theorems). The mathematical conclusion and scope match those sources. The general PRZ theorem remains a cited dependency, not a formal or independently rederived certification.

## Priority and attribution

The paper properly credits the older steadiness definition and broader problem in Dykstra2007; Barth--Dykstra is explicitly credited via Ballier with the journal body unread. Ballier's January2013 manuscript, October2013 online date and 2015 issue are distinguished. His closing/continuing and cover-based theorems are substantial prior results; the inspected statements do not directly give the whole prescribed-map criterion. The paper does not claim a solution of Dykstra's unrestricted reducible problem.

I reviewed the root priority synthesis, second independent final report/peer challenge, and associated finite distinction/checker code after freezing my independent initial position. I recounted 52 queries/14 batches and 58 queries/16 batches in the two stored ledgers; I did not rerun those 110 historical queries. My own twelve new searches are recorded separately. They mostly returned known sources or irrelevant terminology and provide weak absence evidence. The actual primary-body checks, not result titles, support the comparisons.

The paper's explicit non-certification of originality, historical firstness and present worldwide openness is necessary and accurate. The inaccessible final Barth--Dykstra and Ballier bodies remain genuine gaps in historical coverage. No inspected full predecessor was found, and no exhaustive priority exclusion is claimed. The prior general LT theorem alone is not evidence that this exact dynamics reduction was previously published.

## Artifact and reproduction review

I independently rendered and visually inspected all four pages of the actual 59,427-byte PDF, SHA256 cb18c7e8627574d625d9b4d1d471ae499a9d5aeef5b6f5e52be671daf152a7d6. Text, equations, profile floors/ceilings, citation references, author/ORCID, version, date and disclosures are legible. No clipping, overlap, missing mathematical glyph or unresolved citation was found.

The deposited PDF and companion archive are the intended two Zenodo objects. The convenience kit has the same metadata and exact payload. The six artifacts rebuilt byte for byte from the pinned source tree and exact PDF; archive contents were independently matched to that tree. Source ZIP:150 unique sorted regular0644 members; kit:5 unique sorted regular0644 members; every timestamp is the stated fixed date. Source ZIP members match the source tree, and kit PDF/source ZIP match the separate objects. Recompiling TeX is correctly distinguished from byte-identical rebuilding.

All48 originals, their Git identities and three original ZIPs remain bound. Nested ZIPs have9,18,9 authored-text/code members and no redistributed primary full PDFs. The source tree has150 files with only .py/.json/.tex/.md/.txt/.zip suffixes. Metadata title, author, ORCID, license, version, date, problem scope, credited dependencies and extensive AI/unrefereed disclosure agree with the paper. No actual DOI, Zenodo publication or external human peer review is falsely predicted.

Twelve independent physical output-guard controls also rejected late FIFO/symlink destinations, protected hardlinks, a symlink ancestor, inside-source output and directory destinations in normal and optimized modes before changing protected source/sentinel bytes.

I read the builder and bundle verifier in full, the mandatory explicit-exception math-custody replacement, the current priority checkers/comparison challenge, and both fresh finite mathematical programs. The historical assertion-based symbolic custody program is preserved as history and is not the current enforcement gate.

Fresh replay: Python3.14.6 normal and Python3.12.14 optimized, each executing18 normal/optimized child commands, both returned PASS with identical complete stdout. These replays cover original inventory, fresh math and priority custody, three original and two fresh finite math programs. They are finite/reproducibility evidence, not proof certificates or a general solver. My separate ternary profile program tested35,676 long words,14,977 signature classes and13 periodic controls, with an actual boundary-omission negative example; both runtimes returned identical results.

## Readiness decision and independence

Do not publish this exact package until the blocking-read defect is repaired and a fresh whole-package adversary checks the new bytes. The mathematical result requires no identified repair. Original proof-attempt budget remains3/5; this work is validation, not a new search attempt.

The initial position was saved after reading the complete selected record and paper, before opening prior/root review conclusions. Parent-history context was technically inherited and is disclosed in that initial position. No candidate input, Git state, native record or external account was changed. No individual, outside researcher or other shard agent was contacted. Findings were reported only to the assigning parent as required by the authorized review workflow.

The packet is staged on the parent's owned RAM volume. Canonical persistence is the parent's responsibility; no durable repository claim is made here. Third-party source bodies and rendered scratch pages are outside this flat authored packet.
