# A cone-angle proof of Fuchs's labelled length-ratio conjecture

Alec Kriebel, independent researcher; ORCID 0009-0001-9320-500X.
Research note, 12 October 2026. Extensive AI assistance; unrefereed and
not conventionally human peer reviewed.

The note proves Fuchs's Conjecture 2.7 for every regular n-gon, n>=3:
parallel first-vertex trajectories of canonical types A_k,A_l have the
ratio sin((k+1)pi/n)/sin((l+1)pi/n). It includes sides, exact source
dihedral parallelism, segment-parity selection, even double polygons,
folding-chart signs, and the three elementary marked lattices.

Ferudun's October 9, 2026 preprint already proves the same nontrivial
all-n theorem (DOI10.5281/zenodo.23267641). This is an alternative proof
using hyperelliptic commutation and classical cusp reduction. The intrinsic
index agrees with his. No new-invariant, first-resolution or exclusive
priority claim is made. Our September30 repository candidate precedes
that release, but its substantive chart-sign correction is dated
October12UTC and is not backdated. Discovery independence and historical
novelty are not certified. See SOURCES_AND_PRIORITY.md.

## Contents and reproduction

The separate PDF is the manuscript. This archive contains
its standalone LaTeX source, intended metadata, source/priority notes,
standard-library finite exact controls and recorded outputs. No external
paper PDFs, extracted full texts or scans are redistributed.

Copy the entire extracted archive to a scratch directory before running:

    python3 verification/verify_exact.py
    python3 -O verification/verify_exact.py
    python3 verification/exact_reversal_counterexample.py
    python3 -O verification/exact_reversal_counterexample.py

Python3.10 or newer suffices; no third-party packages are needed.
Each script writes its JSON receipt alongside itself and prints it.
Both use explicit checks that remain active under optimization.
The first pins the manuscript source and itself, and performs 19,458
finite exact checks. The second gives 19 exact Q(sqrt(5)) checks for
a four-segment pentagon path of label2mod3 whose physical reverse retains
label2, falsifying the original candidate's unqualified label-negation
assertion. It does not contradict the sine-ratio theorem.

Finite controls do not prove the universal geometric theorem, the
hyperelliptic uniqueness theorem, the classical Veech imports, or all
affine cone-germ transformations. The manuscript gives the argument.
REPRODUCTION_NOTES.md separates these scopes and records the two-mode
replay and false-condition controls.

Compile labelled_length_ratio.tex with a LaTeX system supporting the
listed standard packages, for example:

    tectonic labelled_length_ratio.tex

SHA256SUMS.txt records the sources and the separate PDF.
LICENSE.md covers the author's materials. Cited works retain their rights.

