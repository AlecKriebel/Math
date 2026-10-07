# Reproduction and package construction

The final publication archive contains only the files explicitly listed in
`package_files.json`. Third-party manuscripts, source trees, installed
runtimes, credentials, private coordination and unrelated repository files
are excluded. Immutable source locations and byte hashes are retained in the
source records. The necessary exact rational planar input tables are included
as attributed mathematical facts in
`publication/support/data/planar_certificate_tables.json`; no upstream
verification implementation is imported by the authored checkers.

## Environment

The recorded environment is CPython 3.12.14 and python-flint 0.9.0, with
Tectonic 0.16.9 for the publication PDF and Poppler's `pdftotext` for comparison.
Use a Python 3.12 virtual environment **outside** the extraction directory.
No installation is performed by the reproducer. Assertions must be enabled;
do not use `-O`, `-OO`, or `PYTHONOPTIMIZE`.

```sh
python3.12 -m venv /absolute/path/to/reproduction-environment
/absolute/path/to/reproduction-environment/bin/python -m pip install -r /absolute/path/to/extracted-package/reproducibility/requirements.txt
```

The requirements file pins the only nonstandard Python dependency needed for
the decisive computation replay. NumPy 2.3.5 is optional floating-point
exploration and is not needed for validation. The external mathematical
proofs and dependency audits must also be read; a successful computation run
does not establish their analytic or topological steps.

## From a clean extraction

Extract the ZIP into a new empty directory. Keep the virtual environment and
all output outside that directory, because the manifest verifier rejects
unexpected files. Then run:

```sh
/absolute/path/to/reproduction-environment/bin/python -I -B /absolute/path/to/extracted-package/reproducibility/reproduce.py --output-dir /absolute/path/to/new-reproduction-output --pdf
```

The full run checks every packaged file hash and the package identity,
replays the exact group-theory constants, noncommutative wreath orientation
controls, exact lattice/boundary controls, planar scalar error/tail bounds,
all 51-node inverse/residual finite gates, and all 2,436 Bernstein
inequalities by adaptive Arb integration. It additionally runs the separate
standalone 192-bit Bernstein checker, which uses independently written Fejér
quadrature and the audited analytic quadrature remainder bound. The adaptive
checker does not depend on that fixed-quadrature error allowance.

The full adaptive run takes about eleven minutes in the recorded environment;
the second Bernstein run adds time. All stdout, stderr, new computation
receipts and a summary receipt are saved. The scripts run in a temporary copy,
so the archived historical receipts are preserved. The final status must be
`PASS_ALL_AUTHORED_COMPUTATIONS`. The coverage must include 51 finite nodes,
two matrix signs, 102 residual pairs, 84 half-gap intervals and 2,436 Bernstein
inequalities. An interrupted, partial or assertions-disabled run is
insufficient. Use `--quick` only for a subset diagnostic; its status is
`PASS_QUICK_SUBSET` and cannot satisfy full reproduction.

Receipt timestamps, elapsed times and exact output-ball representations can
vary. Reproduction requires the certified thresholds and coverage to pass,
not byte identity of new receipts. Receipt/script hashes identify versions;
they do not by themselves certify mathematics. The publication build uses
the packaged LaTeX source and compares normalized text from every page of the
rebuilt and supplied PDFs. PDF metadata can prevent byte identity. Every
page still requires separate visual inspection; the text comparison cannot
detect every layout defect.

The associated Lean construction is explicitly outside the retained
torsion-free prime-field proof route. The formal audit states its actual
theorem and unbuilt environment; no formal verification is claimed.

## Building an archive

From a program checkout, review the exact whitelist, source versions,
claim-to-evidence map, publication status, licenses and final reviews before
building. The builder creates deterministic ZIP entries and never overwrites
an existing archive:

```sh
python3 -I -B reproducibility/build_package.py --output /absolute/path/to/new-package.zip
```

The archive is labeled `verification-materials`. Publication clearance is a separate repository record, excluded from the archive to avoid a self-referential approval/hash cycle. Retained fresh review decisions and clean-reproduction receipts bind the unchanged archive identity. The default builds the verification kit.
`--release` additionally requires every explicit gate in
`publication/support/RELEASE_STATUS.json` to be true. That status record must
be backed by the retained proofs, reviews and reproduction receipts; changing
flags is not a substitute for satisfying the gates. The clearance record is
needed for `--release` in the research checkout; it is not part of an extracted
kit and is not an input to the mathematics or archive identity. Neither script uploads,
publishes, contacts anyone, or updates a tracker.

`PACKAGE_MANIFEST.json` records every other file's exact size and SHA-256.
The package identity is the SHA-256 of the sorted file inventory serialized
as canonical compact JSON with sorted keys. The manifest excludes itself to
avoid a self-hash cycle. The builder reports the ZIP's separate exact SHA-256.
Any file change gives a new package identity and requires the applicable
review/reproduction steps before publication.
