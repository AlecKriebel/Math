# Pure point Dirichlet spectrum on quasi-conical domains

Alec Kriebel · ORCID 0009-0001-9320-500X · version 1.0 · 15 October 2026.
The note and authored supporting material are CC BY 4.0.

For each integer d >= 2 the paper constructs some connected open quasi-conical
domain whose form-defined Dirichlet Laplacian has a complete orthonormal
eigenbasis, spectrum = essential spectrum = [0,infinity), dense positive
eigenvalues, no zero eigenfunction, and no absolutely or singular continuous
spectral subspace. Both expanding cube widths and positive shrinking apertures
are chosen. The windows are openings in zero-thickness screens. There is no
claim for arbitrary fixed widths, smooth boundaries, Neumann conditions,
positive-length passages or effective aperture bounds.

Krejcirik–Lotoreichik (BLMS 2024, Sections 2.2, 3, 5 and Remark 3.1) supply the
geometry, freedom of later widths, finite-window convergence and partial
spectral results. Hempel–Seco–Simon (JFA 1991, Proposition 1.4) already use whole
spectral families for multiplicities. The additional exhaustive geometric
transport and repeated dense test family prove completeness. Standard
finite-dimensional reducing-space diagonalization is not a new abstract method.
The precise dated existential OWR/KL question is answered by the proof here.

Bounded primary-source, citation, author and direct Zenodo searches located no
full matching predecessor. They do not certify firstness or current worldwide
openness. Some older full bodies (Rauch–Taylor, Witsch, Post), a restricted
finite-dimensional gap-note body, unindexed work and nonpublic work remained
outside the comparison. See the priority reports and their explicit limits.

AI tools were used extensively in solving, writing, reproducing, checking and
adversarially reviewing this work. This is an unrefereed preprint, without
external human peer review or proof-assistant certification.

## Contents and preserved history

- paper.tex is the standalone LaTeX note. The separately deposited paper.pdf
  is bound by PREPRINT_BINDINGS.json; no PDF is duplicated inside this ZIP.
- historical_candidate/ preserves all 39 original files at PR #765 head
  021518f6f65a86658f72e0b31bfa0814bf1aa25d, including three original ZIPs and
  their identical extracted payloads. Original historical status statements,
  dates, metadata and checks are preserved, not rewritten to current status.
- audit/ contains two independent mathematical reconstructions, a separate
  correction addendum, two closed priority reviews, and root provenance/checks.
  The spectral-family report and associated historical discussion erroneously
  state that the two survey p.16 formulas lack closure bars.
  review_spectral_family_addendum/CORRECTION.md explicitly supersedes that
  source-reading statement: both formulas have closure bars. The theorem and its
  mathematical review verdict did not change. Do not repeat the superseded error.
- MANIFEST.json lists every other regular file with SHA-256 and byte size.
  It is an integrity inventory, not an independent authenticity signature.
  Fixed original and review-manifest pins add preservation checks; no hash
  certifies a mathematical theorem.
- Third-party copyrighted full texts, private source corpora, credentials,
  current shared queue files, temporary renders and external contact material
  are not included.

Root reproduction receipts are dated evidence, not standalone portable
entrypoints. This archive's entrypoint is verify_bundle.py. The historical
candidate's optional whole-queue/external-source modes are not run: those
excluded inputs are not portable and the shared queue evolves.

## Offline verification

Extract into a new directory. Use Python 3.11 or later, without third-party
Python packages. Run from any working directory:

    python3 -B /absolute/extracted/verify_bundle.py --pdf /absolute/downloaded/paper.pdf
    python3 -O -B /absolute/extracted/verify_bundle.py --pdf /absolute/downloaded/paper.pdf

The PDF argument is optional; without it no downloaded-PDF byte check is claimed.
The integrity-only option omits diagnostic child programs. Outer guards use
explicit exceptions and remain active under optimization. Children use isolated
normal assertion mode (-I -B, no inherited optimization); author assertions
are required. No check writes into the closed source tree. Disable bytecode
creation as shown: an extra __pycache__ correctly breaks exact closure.

The checks cover every source/review byte and recursive inventories, three
original ZIP/extraction identities, 4187 author assertions, 2911 portable first
audit assertions (2923 with the author ZIP), and 2304 second-audit tail checks.
Independent spectral controls use exact rational arithmetic. Geometric grids
are rational; auxiliary floating capacity diagnostics allow relative rounding
tolerance 1e-12 with zero absolute tolerance across mathematical libraries.
All other structures and values compare exactly. Nine negative integrity
controls exercise the actual historical verifier through an in-memory
filesystem adapter; they are not a physical filesystem certification.
The spectral diagnostic's historical adjacent-file write is intercepted and its
captured and printed JSON must agree with the preserved result.

These finite checks do not certify the infinite PDE theorem, norm-resolvent
limits, capacity proof, eigenbasis completeness, effective apertures or
exhaustive priority. The paper and independent derivations supply the arguments.

## Rebuild and compile

To reproduce all six publication outputs from these exact inputs and the
downloaded PDF, choose an output directory outside this extracted source tree:

    python3 -B /absolute/extracted/build_package.py \
      --output-dir /absolute/new-output \
      --pdf /absolute/downloaded/paper.pdf

This rebuild leaves all closed inputs unchanged. ZIP entries are sorted,
timestamped 15 October 2026 at 00:00:00, use regular mode 0644 and DEFLATE level 9.
Byte reproduction of compressed ZIPs assumes the same zlib implementation;
semantic file/metadata equality can be checked across different implementations.
PACKAGE_INVENTORY.json is a dated output receipt, outside the source ZIP, and
is not expected to have an identical build timestamp.

Use an output path without existing symlinks in any ancestor. All seven output
destinations, including the inventory receipt, are checked before any write.
Existing destinations must be ordinary single-link regular files and must not
alias a source file or the supplied external PDF. Keep that downloaded PDF
outside the generated output paths. Every changed output is written through
a fresh temporary regular file and atomic replacement. The complete source
inventory/bytes and supplied PDF bytes are checked again afterward.

Compile a copy of paper.tex with a standard LaTeX installation or Tectonic.
The PDF uses standard packages. Compilation success, complete page renders
and mathematical review are separate checks. A fresh compiler may embed another
creation time or use different fonts; recompilation need not reproduce PDF bytes.

The deposit has exactly two files: paper.pdf and source-and-verification.zip.
The outer zenodo-upload-kit.zip is a convenience package with those files,
matching flat-path deposit/metadata JSON, and instructions; it is not a third
deposit file. Both metadata copies and the deposited metadata must agree.
