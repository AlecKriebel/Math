# PR97: unpublished credited research-note preparation

Custody and workflow state as of 6 October 2026 UTC (5 October in Los Angeles).

**Publication authorization is false.** This is a concrete review package for a possible separately authorized, priority-qualified research note. The PR95 exception does not apply to PR97. Two fresh whole-package adversaries and ROOT adjudication remain outstanding. This README is not a readiness or acceptance certificate.

The short theorem: on a closed oriented smooth three-manifold, let a global nowhere-zero C1 form alpha define a cooriented taut C2 foliation without spherical leaves. If a smooth contact form omega satisfies d alpha = alpha wedge omega, then ker omega is tight in the usual smooth sense. The proof combines the exact constant-volume pencil with a finite endpoint near the foliation, C1 smoothing of alpha while retaining omega, the Eliashberg–Thurston tightness neighborhood, and smooth Gray stability.

The original target is Calegari's 2002 Version 0.78 Question 13.2, printed p.29, with the minimal taut C2, atoroidal, and nonzero evaluated Godbillon–Vey antecedents inherited from Question 13.1. Closedness and orientation are the ordinary-fundamental-class interpretation. No equality with the unread final AMS 2003 text is assumed. Existence of a contact connection form and Question 13.1 remain separate.

Dathe–Khoule 2012, Definition 2.1/Theorem 2.2, pp.102–103, already covers the general affine mechanism. The smooth conclusion is our standard corollary of prior affine/ET/Gray results. Historical priority and present-day open status remain unresolved; no first-solution claim is made. See `PR97_PRIORITY_QUALIFICATION.md` and `PRIMARY_SOURCE_READ_SCOPE.json`.

## Files

- `pr97_note.pdf` and `pr97_note.tex`: four-page draft and its exact editable source.
- `support/CANDIDATE.md`: byte-identical longer credited candidate. It separately gives the accurately qualified C1-omega/C2-disk extras; those extras are not the short note's main theorem.
- `support/verify.py` and `support/review/independent_checks.py`: exact adopted diagnostic sources, unchanged. The duplicate `support/review/author_replay/CANDIDATE.md` satisfies the independent program's existing fixed input path.
- `support/run_diagnostics.py`: portable staging/receipt runner; it does not change the mathematical diagnostic sources.
- `support/receipts/`: actual normal/optimized runs, false-check controls, and compilation/render evidence. Counts are diagnostic counts, not quality metrics.
- `check_integrity.py` and `MANIFEST.json`: separate integrity check, including closure and explicit rejection of symlinks and unsafe ZIP members. Mathematical diagnostics do not silently perform manifest checks.
- `support/test_integrity.py`: normal/optimized positive, tamper, unsafe ZIP member, payload-symlink, and escaping-ancestor-symlink controls, writing only to a separate output directory.
- `support/test_runner_custody.py`: output-ancestor-symlink rejection and saved failure-receipt controls using explicitly synthetic children; it does not alter the theorem programs.
- `zenodo_metadata.proposed.json`: safe proposed metadata only; no deposit, reserved DOI, or external service state exists.
- Separately supplied `pr97_support.zip`: portable archive of the useful files above, without third-party paper bodies/images, private logs, historical bulk archives, or source-cache PDFs. The ZIP is outside the payload directory and is not recursively embedded in itself.

## Reproduce

Use Python 3.9 or newer with SymPy (recorded runs used Python 3.9.6 and SymPy 1.14.0). Integrity checks need only the standard library. From the extracted archive root:

```sh
python3 -B check_integrity.py --root .
python3 -B -O check_integrity.py --root .
python3 -B support/run_diagnostics.py --output-dir ../pr97-rerun
python3 -B support/test_integrity.py --archive PATH_TO_ARCHIVE.zip --output-dir ../pr97-integrity-controls
python3 -B support/test_runner_custody.py --archive PATH_TO_ARCHIVE.zip --output-dir ../pr97-custody-controls
```

The runner resolves output-directory ancestors and rejects any destination inside the package, including outside-named symlinks into it. It stages exact input copies in a temporary folder under the requested output directory and runs both programs normally and under `-O`. It records actual command, PID, timestamps, exit code, streams, digests and input hashes before parsing or rejecting child output, so malformed or failed output retains custody. It then deliberately calls each program's existing check function with a false value under `-O`; both must reject it. Output belongs in a separate disposable directory, so the closed package remains unchanged. The independent program writes its own JSON output into its temporary staging directory.

To inspect an archive before extracting it, use `python3 -B check_integrity.py --zip PATH_TO_ARCHIVE.zip`. All entries are validated and hashed without extraction. ZIP member path traversal, absolute paths, backslashes, duplicate names, symlinks, unsupported compression, encrypted entries, and excessive declared payloads are rejected. Directory checks reject symlinks in the root's ancestry as well as in the payload, including under optimized Python.

For the PDF, use Tectonic 0.16.9 or a normal LaTeX installation with `geometry`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `hyperref`, and `microtype`. The actual export used `tectonic --outdir OUTPUT --keep-logs pr97_note.tex`; Poppler `pdfinfo` and `pdftoppm -r 85 -png` checked and rendered all four pages. Compilation has also succeeded using the app's built-in compiler. No new editor tab was opened and the existing PR50 editor was left unchanged.

## Diagnostic limits and disclosure

These finite exact computations test differential-form identities, signs, local boundary corrections and contact-margin arithmetic. They do not prove the global Eliashberg–Thurston or Gray inputs, verify an arbitrary manifold, or establish historical novelty. The manuscript's proof and actual primary statement pages carry those mathematical roles. Candidate hashes in the original program outputs bind the longer candidate, not the shorter manuscript; the separate package manifest binds both.

AI tools were used extensively in analysis, drafting, source comparison and verification. There has been no conventional human peer review or refereeing. Independent AI audits are not human peer review. Original research effort remains 2/5, with zero extra central proof-search turns in this preparation. Publication remains subject to separate PR97-specific authorization and gates.
