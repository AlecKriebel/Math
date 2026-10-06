# Artifact and provenance audit

The author ZIP's 14,117-byte size and a7feb177dbc27c56674e4333675303fa91cfbf2bfb61905273361934b8cca368 SHA-256 match the assigned anchor. The external manifest is 1,743 bytes with SHA-256 30bd1af52d976b711cc52a6c30abca55f0832ef9e767702232dc38b6e9051a20. Every member matched its manifest, the author directory, and the independent extraction.

## All eight members

- PROOF.md: all definitions, proof steps, logical lemma, counterexample requirements, references and disclaimers reviewed. Necessary proposition accepted; citation/nonempty-torsor precision patched.
- README.md: contents and scope consistent. Pending-audit notice updated in the derivative.
- REPORT.md: full target, source attribution, five routes, terminal gap and inspection limits reviewed. Exact periodicity and odd-prime hypotheses patched.
- research_log.json: five numbered approaches, terminal partial state and no-novelty/no-computation flags agree with the report. Unchanged.
- sources.json: ten entries individually checked; four claimed cached PDF hashes and sizes match. HKPR pointer patched. Remaining historical author inspection descriptions preserved, supplemented by SOURCE_AUDIT.json.
- status.json: identity/rank, five-of-five bound, stalled partial and false solution/counterexample/classification flags agree. Audit state updated only in derivative.
- verification_metadata.json: three entire corpus sizes and hashes plus exact unique ID, statement hash and complete record/report pair recomputed. Six bounded GitHub searches independently repeated with empty returned results. Unchanged.
- verify_packet.py: full code reviewed and pinned before execution. Hash/inventory/path checks, duplicate-key rejection, finite JSON values, claim flags and private-marker guard are schema/integrity checks only. Unchanged.

## Corpus gate

All three original corpus files were read in full and hashed. Exact ID 2931 appears once in catalog and once in complete problems; catalog uses a decimal string ID and complete problems an integer. Normalized IDs, problem number, rank and supplied statement/pair pins agree. The complete selected record and complete empty report were read; the background consists of problem context, bibliographic notes and dated literature triage, with no substantive inherited proof or computation. Its default-sort-keys JSON pair serialization is 4,542 bytes and hashes to 74978e4c1d87ebc102f6be15c3991950f15f85dc1f991004324b483743c1855e. No corpus text is included here. The original author's reported order of historical research operations cannot be independently reconstructed from this content audit.

## Replay and negative tests

The nine author test scenarios were independently reconstructed for each packet, then supplemented by nine cases each: relocation including a path with spaces; same-size mutation; missing member; target, manifest and member symlinks; nonfinite JSON; Boolean byte count; and wrong digest. All 36 runs returned the expected status. Exact member hashes were checked before invoking the packet verifier. A clean extraction also accepted CORRECTIONS.patch via the actual patch program and then matched every corrected byte.

Normal directory, ZIP and relocated ZIP checks return 0. Optimized -O and -OO execution intentionally returns 2, as do the tested tamper cases. Expected rejection is not a mathematical pass. These are bounded tests, not exhaustive hostile-input fuzzing. The separately supplied manifest is an integrity anchor and not a digital signature; malicious simultaneous replacement of packet and anchor is outside its authenticity guarantee.

The original author ZIP, manifest and validation receipt remain byte-for-byte intact. Historical pending-audit notices in the preserved original do not supersede the separate corrected exact acceptance. No source PDF, extract, screenshot, dataset content or private coordination item enters the safe ZIP. No publication or repository/queue mutation was performed.
