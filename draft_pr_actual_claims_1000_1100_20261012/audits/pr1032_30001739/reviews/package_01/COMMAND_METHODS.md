# Actual command methods and read scope

Core subprocesses and their exact argv, working directories, start/end UTC, exits, stdout/stderr byte counts and SHA256s are in COMMAND_RUNS.json (57 commands, no omitted failures in that runner). Supplementary three exact argv/exits/output identities are in SUPPLEMENT_RESULTS.json. The actual authored runners are run_package_checks.py and supplement_checks.py; they write only in this review directory. They are a reproducible account of the tests actually executed, not a claim to replay an old historical permission fixture.

New finite derivation commands, actually run in this directory after the new checker was written:

    python3 -I -B independent_checks.py > independent.normal.json
    python3 -I -B -O independent_checks.py > independent.O.json
    python3 -I -B -OO independent_checks.py > independent.OO.json

The first normal execution preceded an extension from28 to40 scalar rows; it was then rerun and the three final outputs above agree. INDEPENDENT_CHECK_RECEIPT.json pins the final three full outputs. No discarded initial normal output is claimed preserved; the checker edit and rerun are explicit in the tool transcript.

Standalone compilation and raster commands actually run from this review directory:

    tectonic --only-cached --untrusted --keep-logs --outdir rebuild ../../preprint_v1_0/paper.tex
    pdfinfo ../../preprint_v1_0/paper.pdf
    pdfinfo rebuild/paper.pdf
    pdftoppm -r 100 -png ../../preprint_v1_0/paper.pdf renders/page
    tectonic --only-cached --untrusted --keep-logs --outdir standalone standalone/paper.tex
    pdftoppm -r 100 -png standalone/paper.pdf rebuild_renders/page
    pdftoppm -f 80 -l 80 -r 130 -png ../analytic_01/sources/raw/JPSS-published.pdf source_renders/JPSS
    pdftoppm -f 79 -l 79 -r 130 -png ../analytic_01/sources/raw/JPSS-published.pdf source_renders/JPSS
    pdftoppm -f 31 -l 31 -r 130 -png ../analytic_01/sources/raw/JPSS-published.pdf source_renders/JPSS
    pdftoppm -f 1 -l 1 -r 100 -png ../../sources/raw/owr2011.pdf source_renders/OWR
    pdftoppm -f 9 -l 9 -r 100 -png ../../sources/raw/owr2011.pdf source_renders/OWR

Their stdout/stderr and PDFinfo are retained in receipts/. The standalone/paper.tex is an unchanged local copy of the candidate source. The PDF was not authored or edited by this review; compilation is a verification operation on that exact source. Actual image viewing used view_image on all renders/page-1.png through page-9.png and the three JPSS/two OWR source images. A mistaken JPSS-080.png request failed and was corrected to JPSS-80.png; see ERRORS_AND_LIMITS.json.

Read-only navigation/source inspection used pwd, rg --files, rg -n, ls, scoped find, cat, sed, head and small Python page-splitting readers. Exact mathematical/source read scopes are in SOURCE_INSPECTION.json; the full manuscript, all kit code, all current kit metadata/docs, and the13 selected historical documents were read. The broad raw-PDF global find was explicitly interrupted withCtrl-C and returned130; it supplied no evidence. Some large combined reads were truncated, then the relevant reports and source sections were reread in bounded calls. The persistent source copies were never altered or re-downloaded.

The native uploader was inspected first, then only `check` was executed. Its run returns before local-state lookup, token_for, client construction or service operations. The runner uses a new subprocess environment with PATH, LANG and PYTHONDONTWRITEBYTECODE only. There is no credential-variable read, stage, inspect, publish, DOI resolution, network call or external mutation. Direct metadata JSON comparison and the semantic prose review are distinct from native parser success.

Terminal/read tool commands remain visible in the original tool transcript; the core mathematical/package subprocess streams needed to reproduce this report are preserved here. No shell command, exit status, source read, render or output outside the above actual work is claimed.
