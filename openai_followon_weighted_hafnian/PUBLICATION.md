# Verified publication

**Nonnegative binary rational hafnians: an exact reduction and approximation and sampling consequences** — Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

Production [Zenodo record 23205294](https://zenodo.org/records/23205294), DOI [10.5281/zenodo.23205294](https://doi.org/10.5281/zenodo.23205294). Preprint date 2026-10-06; publication confirmed 2026-10-07 at 06:42:51 UTC (October6 in America/Los_Angeles). A subsequent read-only inspect confirmed publication and HTTP200 DOI resolution to that record. Full deposition metadata matches the reviewed manifest; the only accepted transformation is Zenodo's added null creator affiliation.

## Exact theorem and scope

Every explicitly encoded symmetric matrix of order 2m with binary nonnegative rational off-diagonal entries admits a polynomial-bit construction of a finite simple graph H and positive integer D such that #PM(H)=D^m haf(A). Each original matching's fiber has D^m times its edge-weight product lifts. The diagonal is irrelevant; the empty hafnian is one; feasibility decides zero exactly.

Using the explicitly cited general-graph unweighted FPRAS of OpenAI, the construction gives a uniform relative-epsilon estimate with failure probability at most delta, for encoded rational 0<epsilon,delta<1, in every-execution bit time polynomial in full input length, epsilon inverse and log(delta inverse). Its output is zero if and only if the hafnian is zero on every execution. For positive hafnians, the sampler always returns a support perfect matching and has total-variation error at most eta in every-execution bit time polynomial in input length and eta inverse. Empty, infeasible, disconnected, subunit-weight, large-denominator and extremely-small-positive cases are covered.

The approximation breakthrough belongs to OpenAI. Logarithmic weight removal and rational weighted-to-unweighted equivalence are inherited from Dell and collaborators and McQuillan; counting self-reduction is classical Jerrum–Valiant–Vazirani machinery. This note supplies explicit proofs, bit/TV analysis, implementation and reproducibility artifacts. No new reduction, first solution or new complexity classification is claimed. It does not cover signed/complex hafnians or unrestricted Gaussian boson sampling.

## Reviewed files and reproduction

The exact reviewed candidate is v5, preserved in reviews/candidate_v5/. The deposition contains three separately downloadable files. Unauthenticated downloads verified each complete file against its approved SHA256, MD5 and byte size:

| File | Bytes | SHA256 |
|---|---:|---|
| [paper.pdf](https://zenodo.org/api/records/23205294/files/paper.pdf/content) |75751|8c93b0f14bc4fd935dbc3a489c5ecca63a8262ba4560a09822b7f65e1036bee7|
| [source-and-verification.zip](https://zenodo.org/api/records/23205294/files/source-and-verification.zip/content) |183748|e79ba53de7b0d937189271d5941ee77eb8e1f10212fef33aa3bb4c4311c666fa|
| [README.md](https://zenodo.org/api/records/23205294/files/README.md/content) |6238|a272e4bc9b525d60a9adfe3ba3a113e8c46c53f246ccd01f16b77eb8958cc1cd|

Extract the source ZIP in a clean directory and run:

```sh
python3 reproduce.py --output reproduction-receipt.json
```

This verifies 28 declared payload hashes and reruns the gadget, sampling-law and upstream finite-cell checks. The source is a standalone main.tex with inline bibliography. The built-in LaTeX compiler succeeded; Tectonic 0.16.9 exported the actual six-page PDF. All six pages were visually inspected, and the fresh clean build's extracted text and page rasters agree with the deposited PDF. The exact counters are exponential reference tools; the sampler uses supplied counting and witness oracles. The full practical upstream FPRAS is not implemented or benchmarked here.

## Review record and verification limits

Five distinct complete-package cycles are preserved with their exact reviewed bytes, reports and responses:

1. V1: manifest-schema, review-wording, citation-locator, optional-inspector availability and dated-status-snapshot repairs.
2. V2: repaired recursion from the documented relative-output reproduction command.
3. V3: repaired the optional inspector command's missing python3 prefix.
4. V4: added Nonnegative to the title throughout source, PDF, README and metadata.
5. V5: fresh complete independent PASS with no required repair, sealed 2026-10-07T06:39:41.257943+00:00. Every material correction preceded a new whole-package review.

The final primary upstream proof/formal-scope and priority gates were independently reconstructed. One initial priority subreview incidentally saw prior agent status summaries; it was superseded by a separate blank-history primary-only priority reviewer that saved its findings before reading the candidate. The chronology and original evidence are retained.

No material upstream manuscript gap was found. Actual Lean endpoint semantics and pinned source closure were inspected, but missing compatible Mathlib prevented an independent kernel rebuild; neither compiled axiom closure nor comparator execution is certified. The follow-on is not formalized. Finite tests and automated reviews are supporting evidence, not proof substitutes or conventional human peer review. AI tools were used extensively in research, drafting and verification; the preprint has not undergone conventional human refereeing. Newly authored prose/data are CC BY 4.0 and code is MIT.

## Tracker and receipts

The specified spreadsheet's numeric tab 1254632077 resolves to **Math Puzzles**. Actual columns are Original Problem, Solution Chat URL, DOI, Notes. After confirmed publication, the current gws resource schema was inspected, the target tab scanned for the exact DOI/record/title, and one RAW/INSERT_ROWS row was appended. The unknown optional chat URL is blank; the title, author, ORCID, date, scope and record link are in Notes. Actual range **'Math Puzzles'!A53:D53** was read back and exactly matches the request. The DOI appears once, the 51 previously read rows remain unchanged, and an unrelated concurrent row 52 was preserved.

[Tracker row 53](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077&range=A53:D53#gid=1254632077). Full spreadsheet snapshots stay private/ignored. Nonsecret project-only receipts are in receipts/: ROOT_RELEASE_APPROVAL_V5.json, PREPUBLISH_VERIFICATION_V5.json, zenodo_check_v5.json, zenodo_stage_v5.json, zenodo_inspect_draft_v5.json, zenodo_remote_draft_metadata_v5.json, zenodo_publish_v5.json, zenodo_inspect_published_v5.json, zenodo_remote_published_metadata_v5.json, zenodo_public_downloads_v5.json, tracker_metadata_resolution.json, tracker_preappend_scan.json, tracker_append_request.json, tracker_append_response.json, tracker_readback.json and tracker_verification.json.

The frozen archive's theorem-state document explicitly describes its prepublication assembly time. Later review/publication/tracker records are retained here and in CURRENT_STATUS.json outside that immutable payload. No new deposit or GitHub release is used for those later records. Owned checkpoints are pushed to remote main through tree-object commits that preserve the shared checkout, index and unrelated remote files.

A bounded independent final receipt audit also returned PASS: fresh unauthenticated record/download/DOI checks and an independent gws read of only A53:D53 agree with the reviewed bytes and saved row. Evidence: reviews/FINAL_RECEIPT_AUDIT.md and reviews/final_receipt_audit/AUDIT_RESULT.json. Its audit checks saved sequence compatibility, rather than certifying an immutable process transcript; duplicate history relies on the saved full scans. Source, manifest, published files and frozen review bytes did not change. The publication/tracker receipts were pushed in main commit 63af989c624e9e95439fb949aff2cd80b833581c and 18 required committed files were independently compared to the local receipts; private full-sheet snapshots are absent.
