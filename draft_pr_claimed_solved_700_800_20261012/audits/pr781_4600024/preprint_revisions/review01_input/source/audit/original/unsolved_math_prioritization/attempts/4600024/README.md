# Effective criterion for a prescribed block-code extension

4600024 / AMR-045-0024, rank 820. Status: **claimed_solved**, three of five substantive approaches. This is a provisional AI-assisted mathematical result with two independent adversarial AI audits; both accept the frozen proof without mathematical corrections.

For a nonempty two-sided irreducible sofic shift T given by a finite presentation and a specified surjective block map f:T→T, choose any full-shift completion F with window length ell. Construct a common finite monoid M recognizing L(T) and the regular bad-input-word language of F. With N=max(2,ell,4(|M|+1)), an extension from some SFT containing T into T exists exactly when F(T[N]) is contained in T, equivalently equals T. The finite intersection test at N decides this, and a successful test supplies T[N] and the completed rule. The negative outcome excludes every radius and every completion of the specified map.

The source problem assumes mixing; the proof uses only irreducibility. T and the containing SFT may be equal. No receptive-fixed-point assumption is needed.

## Proof, credit, and limits

- [Full authored proof](author/PROOF.md)
- [First independent audit](audit/AUDIT.md)
- [Second independent adversarial review](second_review/REVIEW.md)
- [Three substantive approaches](author/APPROACHES.md)
- [Operative acceptance](VERDICT.json)

The decisive external input is Place, van Rooijen and Zeitoun, *On Separation by Locally Testable and Locally Threshold Testable Languages*, LMCS 10(3:24), 2014, Theorem 4.2: [published paper](https://lmcs.episciences.org/1163/pdf), [DOI](https://doi.org/10.2168/LMCS-10(3:24)2014). It gives the finite LT-separation bound. The saturation argument and symbolic-dynamics reduction are authored in this packet. The external theorem is credited and used, not independently reproved.

[Boyle's 2008 Problem 16.3](https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf), printed page 17, asks about the prescribed map. The separate existential-over-map Problem 16.2 and arbitrary cellular-automaton stability are not decided here. No novelty, priority, human peer review, formal verification, practical efficiency, or implemented general-purpose solver is claimed. The code is a finite-control suite; the universal conclusion rests on the written proof and the cited theorem.

## Frozen artifacts and historical fields

The author, first audit, and second review ZIPs are reproduced byte-for-byte in archives/, with exact extracted copies in author/, audit/, and second_review/. All 36 archived members remain unchanged, including the first audit's nested author copy. ARCHIVE_INVENTORY.json records their byte counts and SHA-256 values.

The author packet's pending-review fields and the audits' no-publication fields describe the historical state when those files were frozen. VERDICT.json supplies the current acceptance without rewriting those histories. Neither audit is human peer review.

## Reproduction

Use Python 3.10+ and the standard library only. Copy the publication-manifest SHA-256 from the accompanying PR receipt as an external trust anchor, then run from any directory:

    python3 -I -B verify_publication.py --manifest-sha256 PIN
    python3 -I -B -O verify_publication.py --manifest-sha256 PIN
    python3 -I -B test_publication.py --manifest-sha256 PIN

The wrapper verifies exact recursive inventories, hashes, all three archive pins and members, historical statuses, both audit dispositions, and source-only ordinary/optimized replays. It rejects unexpected files, directories, bytecode, symlinks, FIFOs, malformed inventories, and changed content. The publication corruption harness exercises 38 actual mutated copies. External pins are essential; an unkeyed manifest cannot authenticate a coordinated rewrite of the entire publication and its expected hash.

Finite suites report 3,456 author checks, 221,468 first-auditor checks, and 22,859 second-reviewer checks, with 32 first-auditor integrity controls and 24 second-review inventory controls. These are supporting finite checks, not formal verification of the theorem.

An optional --source-dir DIRECTORY argument checks locally supplied catalog.json, problems.json, and research_results.json against the public corpus pins, then reselects the complete record/report and verifies their hashes. Default portable replay does not obtain or replay external corpora. PUBLICATION_SOURCE_REPLAY.json records the separate publication-stage full-corpus replay. No source PDFs are replayed by this wrapper; earlier retrieval/inspection histories remain explicitly attributed to their respective audits.

Only authored proof, audits, code, results, public citations, and public verification metadata are included. Source documents, copied extracts, rendered pages, datasets, private sources, personal data, and private coordination are excluded.

## Repository change

The only existing-file edit changes row 820's Status, Turns, and qualified Findings. Chat, DOI, all other rows, and all other queue bytes are preserved. No global queue regeneration or state-history rewriting is performed. This is a draft PR only, with no merge, release, DOI creation, or outside outreach.
