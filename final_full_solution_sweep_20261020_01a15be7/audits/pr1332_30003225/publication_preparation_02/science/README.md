# A free-chain counterexample to a Nash-intersection conjecture

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Version1.0.0,22October2026. Unrefereed preprint; extensive AI use disclosed.

Read paper.pdf (five pages) or editable main.tex. SOURCE_AUDIT.md supplies actual source/priority coverage and interpretation limits. SOURCE_PROVENANCE.json binds primary bodies and original PR provenance. CODE_PROVENANCE.json separates new programs from unavailable historical executables.

The universal proof computes complete complex free-center families and closed Nash cylinders including satellite limits and zero arcs. Five blowups refute each explicitly mapped reference-multiple formulation even after fixing c3. The source's bare relation/index issue is not an authenticated erratum. The intersections are Nash sets of OTHER toric divisors. No arbitrary-divisor negative, Conjecture2, broader Nash-problem solution or nonreduced-scheme equality is claimed.

## Reproduce exact supplementary checks

Use Python3.10 or later and only its standard library:

    python3 -I -S -B reproduce.py

This checks every declared source file and complete membership, then executes exact_checks.py and run_mutations.py under normal,-O,-OO interpreters. The complete outputs must match the committed expected JSON bytes. Explicit RuntimeError checks remain active with optimization. These finite diagnostics supplement the written universal proof and do not certify complex-family exhaustion, Zariski density, all integer multiplicities, source interpretation or priority.

To reconstruct all six publication products, use a NEW empty destination outside this source folder:

    python3 -I -S -B build_package.py /absolute/path/to/empty-output

The builder copies the frozen paper.pdf and deterministically constructs the source ZIP and upload kit. It does not typeset TeX or prove source/PDF equivalence by copying. All paths in zenodo-deposit.json are relative to the resulting release directory. The source ZIP includes the exact PUBLIC_MANIFEST.json and all authored supporting files; it excludes private captures, raw third-party PDFs, credentials and service actors.

## Typesetting

main.tex uses standard article11pt, T1/lmodern, amsmath,amssymb,amsthm,geometry and hyperref. A conventional LaTeX/XeLaTeX installation can regenerate the paper. Preparation used a pinned cached Tectonic with SOURCE_DATE_EPOCH=1792627200, denied network and denied writes outside its own preparation folder. That deterministic PDF metadata timestamp is a build convention, not a claim about the actual time the research occurred. Compiler logs and visual receipts are repository audit evidence. Portable archive reconstruction uses the reviewed PDF; byte equality across arbitrary TeX distributions is not promised.

Authored prose is CC BY4.0; authored code is MIT licensed. Referenced third-party works retain their own rights and are not redistributed here. Two new independent complete-package reviews and root adoption/live duplicate gates remain required before publication; this preparation grants no service authority.
