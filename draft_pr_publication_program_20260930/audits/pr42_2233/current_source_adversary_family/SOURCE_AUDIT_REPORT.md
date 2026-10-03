# Independent current-preparation source adversary: PR42 / EP-653

Disposition at 2026-10-02T23:15:59Z: **one narrow mandatory publication-guard correction; no mathematical or existing-packet defect found.** This is a source-only audit of the exact preparation below. It is not a verdict on an executed current packet: `reviewed_candidate` is absent, ROOT's genuine four prerequisites remain future evidence, and the NEW whole-current source-first gate remains PENDING.

Exact reviewed pins:

- PREPARATION_MANIFEST SHA256 `af4f28f77df2b7541b099a47fb89a5a454dda5a64272be6e9b70254d17b5c5fa`.
- Builder SHA256 `66a5bc427e90032f6f86bd1007479fadf154282e3f41dfb047a9dd44551c8730`.
- INPUT_PINS SHA256 `54c0aa6f06615a0ff6c106f9025a8b4ac788da09f3dfb8c242bc669fa76684f3`.
- Qualification SHA256 `3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570`.

## Mandatory finite guard failure

Builder lines 380 and 381 test `st_mode & 0o777 == 0o444`. This discards set-user-ID, set-group-ID, and sticky permission bits. The contract says every candidate file, including its manifest, is 0444. On this actual macOS filesystem, a newly created own sandbox file has `st_mode=0o104444`, hence complete permission mode `0o4444`. The manually copied current predicate accepts it; `stat.S_IMODE(st_mode) == 0o444` rejects it. `MODE_FALSE_POSITIVE.json` and the actual inspector source/capture retain this concrete counterexample.

Required repair: compare all permission bits, e.g. `stat.S_IMODE(...) == 0o444` or mask `0o7777`, for every staged file and the manifest. Add a separately retained negative mode control. The actual stage producer's `chmod(0o444)` is correct; there is no existing candidate and no observed wrong-mode scientific artifact. The failure is the literal final verification guard's under-enforcement. It does not invalidate any mathematics, byte archive, provenance correction, or pending future ROOT requirement.

Exposure disclosure: ROOT raised the permission-mask class after I had independently read the builder, and mentioned an analogous PR41 audit. I did not read that sibling report. The actual finite reproduction, the PR42 contract interpretation, and the distinction between guard under-enforcement and an existing packet defect are my own work. No claim of pre-exposure independent discovery is made for this class.

## Verified input closure and finite controls

The genuine successful independent inspector ran as PID 13035, 2026-10-02T23:11:23.489541+00:00 to 23:11:26.111605+00:00, exit 0. It retains full prelaunch source/operator, argv, cwd, stdout/stderr and SHA256 values. It completed 435 named checks and individually bound 299 repository input files. The 40 read-only Git child commands each have their own actual PID, clocks, argv/cwd, complete streams, exit and hashes.

Verified complete bytes, original Git mode/blob identities and recursive closure for all 17 original files; verified the full 18-path original diff against actual base `60292bed09f59236aa192cb17aa138f7b4750e1a` and head `099ae5e4d06d8789214cfaaece87309c87e914f9`. The failed wrong-base source export remains empty. All 104 declared retained ROOT closure files and all 14 auxiliary files match their pins. The preparation has exactly its 21 individually listed files plus its self-only excluded manifest.

Both independent closures bind exactly:

- Literal family: 55 historical first-party seal rows become 54 copied rows and 26 individually excluded foreign/derivative rows, plus the self manifest. The 9372-byte `controls/primary_pdf_extract.stdout.txt` is explicitly excluded with SHA256 `1ba9a25031aa504daa3c7ef0077a4d65f017cbe50eede1715babb6ee40ef5aad`; it is not copied or presented as authored paper text.
- Exact family: 42 original own rows including self become 41 copied rows, 5 individually excluded in-root foreign rows, and its self manifest. Every individually listed external read dependency in that manifest also matches its own binding.

All 31 in-family foreign exclusions were individually checked. Neither uses a wildcard authorship exclusion. Dependencies remain rooted at the fixed repository-relative audit root, so canonical copying of the eventual candidate does not invent a scratch-path dependency resolution. Archived code/source bytes in actual Git streams are forensic observations of the original sources, not a claim that this adversary authored those sources.

A second genuine reader ran as PID 15131, 2026-10-02T23:14:26.275786+00:00 to 23:14:26.352934+00:00, exit 0. It completely parsed all 69 bound closed JSON/JSONL files and visited every value, retaining per-file type counts and exact bindings. Duplicate keys and nonfinite numbers are rejected by the copied strict parser. Finite copied-predicate controls rejected boolean byte counts, negative byte counts, uppercase hashes, duplicate row paths, extra row keys, unsafe/noncanonical paths, symlinks, special files, empty directory extras, and non-UTC timestamps. Serialized equality distinguishes true from 1, including nested flag records. The false/null drafts cannot pass the required true flags, current native approval or HEAD fields.

The actual macOS exclusive-rename control rejected an existing destination directory with errno 17, preserved its sentinel and the source stage, and then successfully published only an absent own sandbox destination. No builder was invoked. The sandbox also checked ordinary published 0444 permissions.

The manually copied prospective queue operation on the live whole preimage changes exactly one target row and only Status, Turns and Findings, preserves other fields and rows byte for byte, and preserves Chat/DOI. Its current preimage is queued 0/5. The exact single SOURCE_AUDIT sentence repair is reversible to the archived original and distinguishes absent key from SQL fallback and dated background. Reviewed-to-final PARTIAL differs only by the exact header sentence replacement.

At inspection, live main HEAD was `3166abcb75a95767b4cf9619c887df0aee42a7d0`; history.jsonl and state.json differ from preparation-time native13 observations. This is not a stale-input failure: the builder properly awaits genuinely approved fresh ROOT thirteen-file preimages and their actual current main HEAD. Exactly ten native inputs are Git tracked, and all three ignored cache files remain explicit whole-byte dependencies. The complete current raw research-results JSON has no EP-653 key. Ignore status never exempts a file from the byte check.

## Mathematical and source assessment

I read the complete current builder, all preparation authoring/capture/closure sources, contracts, drafts, overview, qualification, ROOT expectations and current status; the original mathematical/source/review notes, two checker sources, ledger and source metadata; the complete main independent control sources and their mechanisms/verdicts; and the ROOT genuine replay source. Hash-equal retained source copies do not create independent proof authority.

The local E95 complete-page renderings of manuscript pages 14 and 15 were visually inspected. They identify distinct planar points, the pinned counts, the spectrum question and n-o(n), and the Saldanha product credit. The E95 use of g(n) elsewhere for unit-distance multiplicity is not confused with the present spectrum parameter.

The original written proofs are sound under their stated hypotheses: full independent translation space and all required external equalities excluded; singleton and one-block boundaries; exact positive-radius line/circle support and arc span below pi; m=n-t>=2 with center pins treated as exceptions; distinct pair centers and positive integer count spectrum representatives; n=2 and s=1 limits. Generic deficit spectra union rather than add, and finite hierarchies with sublinear largest leaves stay sublinear. The exception bound has the claimed one-half asymptotic barrier. The classical square-root defect is compatible with the full ratio-one target. No route supplies the unrestricted n-o(n) construction or a universal fixed-proportion obstruction.

Complete typed ROOT replay results preserve author18306, reviewed-author18306 and independent1263, all 1263 original check labels, the expected header-dependent hash distinction, and the exact two-turn ledger. Their declared whole raw dimensions are 149266659 bytes and 15458 SQL rows. I inspected and independently bound the entire result and actual capture evidence; I did not execute the scientific helpers or repeat ROOT's SQL join reproduction. The present inspection therefore does not fabricate a second scientific replay. The raw absent-key fact was independently inspected directly.

All historical model/reasoning/window, access/search and PASS claims remain explicitly attributed records. The current wrappers consistently retain UNSOLVED, original2/5, new0, audit0, no novelty, no priority/best-known assertion, no paper/DOI/tracker product and explicit null current runtime/verdict. The complete 1997 manuscript and complete Erdős–Fishburn/Csizmadia–Ismailescu proofs remain unavailable/unverified as disclosed. Janzer and the 2026 preprint arguments are source claims with reading limits, not elementary-proof premises. This audit does not broaden a literature absence claim or certify their proofs.

## Preserved failure and scope limits

Own inspector attempt 1, PID 12113, exit 1, failed because I copied the wrong pending-review header string into my own byte-equivalence check. The frozen preparation did not cause that failure. Its complete original prelaunch source/operator, 40 read-only Git commands, stderr traceback, stdout, clocks and exit remain retained. The retry corrected only this family's inspector. No failed evidence was overwritten or converted into a PASS.

The deliberately constructed own symlink and FIFO members were removed only after their negative checks, with the exact paths and removal fact recorded in `NONREGULAR_FINITE_CONTROL_RECORD.json`; their containing empty test directories are explicitly retained in this family's closure. No historical/builder failed stage or input was removed. `FINITE_CONTROL_SANDBOX_v2/mode_probe_04444` remains a concrete wrong-mode test object and is individually listed with its actual mode; it is not a candidate artifact.

Every closed input was byte-bound; JSON structures were fully parsed. These statements do not claim semantic certification of every historical stdout line or every external-paper proof. No scientific helper or proposed builder was imported, compiled or executed. All writes stayed in this new family. No Git/index/native/canonical/remote write, branch change, release, DOI or outside human communication occurred.

Optional hardening: checking current input filesystem modes is distinct from the required original Git mode/blob check and target candidate 0444 guard. Preparation/family pins do not declare per-file frozen filesystem modes, so such additional input-mode enforcement is not a mandatory failure under this particular contract. A final native/dependency recheck after stage construction would further narrow concurrency windows; no actual changed-input packet or separate mandatory finite defect was found here. ROOT's genuine reading and four future approval bindings remain required, not invented by the source preparer or this audit.

Source-audit completion: **100% of this exact preparation inspection**. Publication readiness is blocked on the narrow mode-guard repair and its re-review. Estimate toward full EP-653 discovery: **0% new contribution from this audit**; the original scoped partial remains valid, and the unrestricted target remains UNSOLVED.
