# A modular-storage proof of NP-completeness for chip-firing halting

This complete attributed paper answers the historical simple-digraph question
in Farrell--Levine, Section 3.1. Its exact scope is ordinary conservative
HALTING, finite loopless simple strongly connected directed graphs, at least
two vertices, and supplied nonnegative binary configurations. The main
construction permits antiparallel arcs. A separately proved oriented
construction forbids them. Hardness holds with polynomial numerical total
chips and a specified root whose deletion leaves a depth-at-most-one DAG.
The full proof covers preprocessing, legality, conservation, arbitrary legal
schedules without fairness, every size bound and NP certificate bits.

The literal bank multiplicities and parallel priming specialize
Holroyd--Levine--Winkler, arXiv:1511.00422v2, Lemma 4.1. The prime Boolean and
clause-product encoding is the classical Stockmeyer--Meyer STOC 1973 Theorem
6.1 construction, also reconstructed by **Gregor Gramlich alone**, MFCS 2003,
Fact 3, presented in complement form. The full allowed intersection is the
complement of the earlier invalid-variable or failed-Boolean-clause union;
extra nonBoolean members of a local clause complement are already variable
invalid. Neither ingredient nor avoiding global-period expansion is claimed
as new. Farrell's thesis/FL Section 2 supply antecedents for root-last mass
comparison, FL Section 3 supplies membership, classical least action and tree
periods are prior, and Eriksson already supplies long simple-graph games.

Full-result, conservative simple/oriented realization and remaining method
priority, and preexisting worldwide openness, remain **UNKNOWN** after the
bounded audit. See SOURCE_NOTES.md, SOURCE_LEDGER.json and CLAIM_SCOPE.json.
AI tools were used extensively in solving, verifying, adversarial review,
source comparison, programming and writing. The paper is unrefereed, without
external human peer review, journal acceptance or proof-assistant certification.

## Downloads and a clean reproduction

The deposit is designed to contain paper.pdf and pr1098_support_v1_0.zip.
The ZIP contains the full TeX source and support payload, including a required
binding for the external PDF. It omits that PDF to avoid duplicating it.
Extract into a new real directory. Copy the two original downloads into that
directory with their exact names. All commands below are run from that
directory, with Python 3.10 or later. No network, token, third-party Python
package, old omitted program or mathematical source download is needed for
the standard-library commands.

```sh
python3 -B code/verify_kit.py
python3 -B code/run_checks.py
python3 -O -B code/verify_kit.py
python3 -O -B code/run_checks.py
```

`run_checks.py` writes JSON only to stdout. Its guards use explicit exceptions,
so optimization does not disable them. `--invalid` deliberately fails in both
modes. Fresh finite controls check the exact bank and HLW substitution, the
independently implemented classical failed-clause union, actual main/oriented
graphs, individual conservative firings, full small successor graphs, rooted
tree periods and corrected certificate slack. Separate damaged physical
dynamics change a YES outcome with an extra root chip and a NO outcome by
deleting return chips. These are new diagnostics, not replays of historical
omitted programs or a substitute for the unbounded written proof.

The following destinations must be absolute, previously absent leaves whose
real parent directory already exists **outside both this extracted kit and the
original research audit tree**. Replace the example paths with appropriate
fresh paths on your system. A file or symlink may not already occupy either
leaf. Case aliases and symlink ancestors do not bypass these restrictions.

```sh
python3 -B code/rebuild_archive.py --output /absolute/existing/parent/new-support.zip
python3 -O -B code/rebuild_archive.py --output /absolute/existing/parent/new-support-optimized.zip
python3 -B code/build_pdf.py --out-dir /absolute/existing/parent/new-pdf-build
python3 -O -B code/build_pdf.py --out-dir /absolute/existing/parent/new-pdf-build-optimized
```

The archive is ZIP_STORED with fixed timestamps, sorted names and fixed modes;
its bytes are read only after the ZIP is closed. The two reconstructions must
equal the downloaded ZIP byte for byte. The PDF command needs Tectonic on PATH
and its TeX resources (first use may download resources); it creates the TeX
copy, all compiler products and logs only in the new build directory. A fixed
source date makes builds reproducible under the recorded compiler/resources;
other compiler editions can produce a visually equivalent PDF with different
bytes. Inspect every page after any source change. The exact canonical PDF is
bound by ARTIFACT_BINDINGS.json, which is mandatory even in an extraction.

MANIFEST.json binds each distributed payload member. The archive contains that
manifest but does not recursively hash itself. The verifier requires the
external PDF and original ZIP, validates all regular input paths before JSON
parsing, checks the mandatory PDF binding, and compares the complete closed
ZIP reconstruction. A separate preparation DEPOSIT_BINDING.json outside the
archive binds the two upload files and native upload manifest, avoiding a
hash cycle. The native manifest is publication/zenodo-deposit.json and has
exactly `metadata` and `files` (`path`, `name`) fields. Its metadata equals
metadata.json, zenodo-api.json and the independent code constant exactly.
The repository uploader's `check` is local only; no stage or publish command
was run during preparation.

## Custody and dated workflow state

INPUT_FREEZE.json hashes every prior regular audit file before authoring.
CUSTODY_SELECTION.json individually partitions all of them into exact authored
copies under history/ or explicit exclusions. Third-party bodies and converted
source extracts are omitted. Historical executables are also omitted; new
controls import none. Preserved historical statuses, seals, pins and reports
retain their dated meaning, including access failures and corrections. They
are not current workflow decisions or claims that every past dependency can
be replayed from this portable package. Public bibliographic names are corrected
in SOURCE_LEDGER.json; opaque old acquisition names do not create coauthors.

At the preparation checkpoint dated 16 October 2026 UTC, mathematics had
passed two independent families and ROOT adoption, and the two required
priority credits had been incorporated into these materials. Zero **new
complete whole-package** reviews had been completed, at least two were
required, readiness and publication were false, and external actions were
held behind PR #1032. STATUS.json records that past checkpoint. It does not
forecast or relabel a future review, DOI, merge or publication. All original
PR bytes remain unchanged. No person was contacted.

Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Version 1.0, 16 October 2026. Authored materials: CC BY 4.0.
