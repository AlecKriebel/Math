# An elementary obstruction to same-ground-set matroid-rank approximation

Alec Kriebel, independent researcher; sole named author. ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0, 14 October 2026. Authored text and code: CC BY 4.0. UNREFEREED; extensive AI assistance in solving, verification, source comparison, coding and writing. No human refereeing, journal acceptance or formal certification.

This credited elementary exposition addresses the source-displayed comparisons `r(S)/alpha <= f(S) <= alpha*r(S)` for one ordinary unscaled matroid rank on the original finite set V. Inputs are nonnegative monotone submodular functions, zero at the empty set and one on every singleton. A constant is conventionally interpreted as dimension-independent; Végh's original contribution does not separately print a quantifier over all V. The note makes that interpretation explicit.

The classical square-root-cardinality function forces `alpha >= n^(1/6)`. Its exact optimum among all ordinary matroids is `min_{integer 1<=R<=n} max(sqrt(R),sqrt(n)/R)`, attained by uniform ranks. On `n=m^2`, the rational function zero at the empty set and `1+(|S|-1)/m` otherwise forces `alpha^2+alpha >= m`. The proof uses a basis and the full ground set, with all n=1, m=1, loop, zero-rank and empty-set boundaries checked. Sharpness is restricted to the square-root family.

Classical concave-cardinality submodularity is credited through Balcan-Harvey to Lovász's 1983 survey (original body unread). DDSSS 2013 Appendix D Lemma D.1 is credited for the prior nonnegative uniform-rank decomposition, stated with corrected direct difference coefficients. GHIM's root-linear output and its query-hard rank inputs are distinguished from this existential obstruction. Schrijver's copied-element expansion, credited there to Helgason, uses a larger domain; Helgason's original body was not read. Exact historical attribution of the one-rank argument and generic envelope remains unknown. No new function, new representation, firstness, global open-status, intellectual-priority or independently evidenced discovery claim is made. The bounded source review and other unread citation-chain limits are recorded in the evidence.

Read the standalone `paper/matroid_rank_obstruction.tex` (the separately delivered PDF is exported from that source), then `SUPPLEMENT.md`. `evidence/INDEX.md` locates all nine exact original bodies and each fresh independent audit stage. `EVIDENCE_COPY_MAP.json` binds every copied authored record to its original path, bytes and SHA-256. Historical originals and their acceptance labels are preserved as dated records, not revised into the new note. `REVIEW_HISTORY.json` identifies stage scope and frozen-input navigation. Machine operational state is in `CURRENT_REVIEW_STATE.json`; static metadata and paper statements describe the dated v1.0 preparation stage.

The support ZIP excludes the PDF, external `zenodo-deposit.json`, private preparation input pins, temporary renders, extracted source text, raw/downloaded third-party bodies and environment caches. It contains authored proofs, source locators, reports, checkers, finite output streams, receipts and manifests. Exact copies of historical scripts may contain fixed original output paths: inspect those scripts, but use the portable checker below to reproduce checks without writing to original review folders. The original nine-file edition had no executable; no omitted historical computation was replayed.

From a clean extraction of the support ZIP, using Python 3.10 or later (standard library only):

```sh
python3 -I -B scripts/verify_package.py
mkdir -p verification_output
python3 -I -B scripts/check_mathematics.py --output-dir verification_output > verification_output/stdout.jsonl 2> verification_output/stderr.txt
mkdir -p paper
tectonic --outdir paper paper/matroid_rank_obstruction.tex
```

Tectonic and its LaTeX bundle are needed only to rebuild the PDF. The saved finite run used exact integers and Fraction arithmetic, enumerated 497 labelled matroids on 1 through 5 elements, and checked the declared finite cardinality sweeps. It supplements the full quantified proofs. Newly rerun output timestamps and script hashes need not match historical bytes; the recorded comparison explicitly excludes those metadata fields. `scripts/build_supportkit.py` rebuilds the deterministic archive from `ALLOWLIST.json`, checks member safety and CRC, and regenerates the non-self-hashed manifest. Extra local reproduction outputs are excluded by the explicit allowlist.

`zenodo_metadata.json` is the exact `{metadata: ...}` request wrapper; `.zenodo.json` contains the identical metadata object. External `zenodo-deposit.json` carries the same object and identifies only the PDF and support ZIP; it is outside the ZIP to avoid a self-reference. These files are local preparation artifacts, not a deposit or publication record.
