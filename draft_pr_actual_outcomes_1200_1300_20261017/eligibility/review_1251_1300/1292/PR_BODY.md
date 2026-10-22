## Result and attribution

Problem 30001617 (OWR-4531-020): the unrestricted dyadic tail LIL assertion has a negative answer. This packet gives a complete, self-contained construction of a real L2 function on [0,1) with total realized square function at most one, strictly positive square tails Q_n tending to zero, and

    limsup |f - f_n| / sqrt(Q_n log log(1/Q_n)) = infinity

almost everywhere. Zero extension gives a globally integrable real-line counterexample to Artur Nicolau's question in Oberwolfach Report 49/2010, printed p. 2872.

This negative phenomenon is prior work of Santosh Ghimire, presented in 2011 and developed in his 2012 dissertation, Section 3.3. The proof is an all-positive stopped-block reconstruction, with complete L2 and almost-sure convergence, terminal conditional-mean identification, and a summable future-error budget. Successful-block start indices are used pathwise and are not asserted to be stopping times.

The cited positive theorems assume a uniform within-atom square-tail comparison. The construction directly violates that hypothesis. Selected-time conclusions do not bound the unrestricted full limsup, and no specialized positive LIL theorem is imported or certified.

## Sources and review limits

- [Original Oberwolfach report](https://ems.press/content/serial-article-files/46308), printed p. 2872.
- [Ghimire's 2011 presentation](https://www.math.ksu.edu/about/events/conference/pas/2011/talks/Prairie%20Analysis%20pause.pdf), PDF pp. 51–69.
- [Ghimire's 2012 dissertation](https://hdl.handle.net/2097/13647), Section 3.3, printed pp. 50–59.
- [Acharya–Ghimire (2016)](https://www.nepjol.info/index.php/JACEM/article/view/16100/13051), conditional and selected-time statements.

The packet preserves the completed source-inspection history, including the full dissertation Section 3.3. This publication pass verifies file identity; it does not claim a fresh source review or an exhaustive literature search.

The proof and audit are AI-assisted. No novelty, earlier priority, external human peer review, journal acceptance, or formal proof-assistant certification is claimed. Exact finite checks support the written infinite analytical proof; they do not replace it.

## Exact publication boundary

Adds exactly seven files (39,597 bytes) under `unsolved_math_prioritization/attempts/30001617/`: README.md, PROOF.md, AUDIT.md, ACCEPTANCE.json, SOURCE_PINS.json, CHECK_SUMMARY.json, and MANIFEST.json.

All seven files retain their sealed bytes. The complete accepted proof and all mathematical/source-analysis audit sections are preserved. Historical fields such as `publication_performed=false` describe the pre-publication preparation/audit snapshot; this draft PR is the separate publication event.

Only authored mathematics, audit/acceptance reports, and public source/verification metadata are included. No copied source documents or source text, datasets, scripts, private sources, personal data, or private coordination material are included. QUEUE.md and unrelated files are unchanged. This PR does not merge, release, or request outreach.

## Verification

- Preparation seal and all seven SHA-256 hashes and byte counts match.
- Packet verification reran successfully in normal, -O, and -OO modes, preserving the 1,608-path exact finite-model receipts and analytical acceptance limits.
- Native Git-object reconstruction verified the seven blob IDs and the complete ancestor-tree boundary.
- Base commit: `5c5d4c9d7a2ea547fdf8a35cf874f604cec27bed`.
- Publication tree: `a7ae2a01043de837242dab9203c127c1c44ac6e9`.
- Head commit: `4b30a35a498333cf00fd6a9636e092e8add6b0ce`.
- MANIFEST.json SHA-256: `0cade08ce97d083f18ead76ff7afc9418be4cfd3ac77e60d4dc277a21af20e87`.

Remote readback verified all seven files byte-for-byte, including SHA-256, sizes, and native Git blob IDs. The complete diff is exactly seven added regular files, 878 added lines, and zero deletions. Reconstructed ancestor trees confirm all 137 root siblings, 24 prioritization-directory siblings (including QUEUE.md), and 81 existing attempt siblings are unchanged. PR state is open and draft at the exact head above.

Exact-head CI: NOT_RUN. GitHub reports zero Actions runs, zero check runs, and zero commit-status contexts. Two queued app-suite shells (Vercel and GitHub Pages) each report zero latest check runs; they are not running jobs and do not constitute a CI pass. The per-suite child endpoint is unavailable through this connector; exact-head aggregate check-run and Actions endpoints were successfully read.
