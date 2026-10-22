# Reviewed supercritical percolation counterexample

Problem 10000037 / AMR-099-0037, queue row 1785. Publication edition: 14 October 2026.

The accepted construction is a deterministic degree-four graph quasi-isometric to Z². Every actual edge has the same independent bond parameter. Its critical probability is at most 0.9, and at p = 0.95 the probability of at least two infinite clusters is strictly greater than 2200741829/6461571200, hence greater than 1/3.

The result answers the context-supported full-supercritical uniqueness formulation negatively. The source sentence leaves the parameter quantifier implicit. It is an open question, not an incorrect published theorem. Historical novelty and priority remain uncertified. This is independently AI-reviewed mathematical work, not a claim of external human peer review or formal verification.

## Read the work

- [Research reader and scope](reader/README.md)
- [Complete construction proof](reader/pass1_construction/CONSTRUCTION_PROOF.md)
- [Independent mathematical acceptance](reader/pass1_audit/INDEPENDENT_ACCEPTANCE.md)
- [Independent public-package acceptance](review/PUBLIC_PACKAGE_ACCEPTANCE.md)
- [Reproducibility and integrity](reader/REPRODUCIBILITY.md)

The 35 reader files and seven review files are exact copies of the accepted archives. Both complete original public archives are preserved in [archives/](archives/). Their byte counts and SHA-256 values, and the complete publication inventory, are in [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json). No source documents, source extracts, raw corpus contents, private siblings, or superseded drafts are included.

## Offline verification

From this directory, run:

```sh
python3 -I -B reader/verify_package.py --manifest-sha256 251ddc64465a0e7f7378fb99a955c967e9294f5194f4ccddfca5408fa5ccfab3
python3 -I -B review/replay_package_review.py archives/PERCOLATION_1785_COUNTEREXAMPLE_PUBLIC.tar.gz
```

Compare the second output with review/INDEPENDENT_REPLAY.json. The pre-publication replay matched that retained result exactly: six checker executions, 45 packaged tamper rejections, and 27 additional independent tamper rejections. These finite checks establish arithmetic and integrity properties; the infinite-event claim rests on the authored proof and its mathematical audit.

One substantive research pass was completed. Package preparation and independent packaging review add no mathematical passes. QUEUE.md changes only this row's Status to claimed_solved, Turns to 1/5, and the qualified Findings cell. All unrelated queue bytes, existing notes and chat links are preserved. No exact critical threshold, exact cluster count, almost-sure multiplicity, novelty, or critical-parameter conclusion is claimed.
