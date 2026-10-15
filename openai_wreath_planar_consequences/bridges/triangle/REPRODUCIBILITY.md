# Triangle bridge reproduction

This subset contains independently written proofs and exact finite controls.
It does not contain or validate OpenAI's proposed sharp planar certificate.

Run `python3 check_exact_lattice.py` from this directory. The script uses
only Python's standard library. The recorded execution used CPython 3.14.6
and exited with status 0. Compare the JSON to `exact_lattice_receipt.json`,
allowing `checked_utc` and the reported Python version to reflect the new
environment. Every mathematical field is an exact rational or integer fact;
no floating-point calculations are used. The current script hash must match
the recorded `script_sha256` for a byte-identical script reproduction.

The controls independently represent Q(sqrt(3)), construct the lattice and
its Fourier-dual basis, verify their exact pairing and norms, check all 625
integer coordinates in [-12,12]^2, and check 2,401 lattice pairs including
96 axis pairs, 48 nonzero coincident pairs, and 732 boundary pairs. The
proof that all integer vectors and all lattice pairs meet the required
conditions is analytic in `BRIDGE_PROOF.md`; finite enumeration cannot
replace that proof.

Read `BRIDGE_PROOF.md` for the exact problem and the corrected product
comparison. Read `DUALITY_AUDIT.md` for the relevant infinite-dimensional
duality arguments and their model translations. `source_versions.json`
and `pr487_source_versions.json` record retrieved versions and hashes.
Third-party audit sources under `../../sources/triangle/` are excluded from
publication material; their public immutable URLs allow fresh retrieval.
The AIM page is a mutable primary page, so its retrieval hash and date are
recorded rather than claiming that its URL is immutable.

Neither a PASS finite-control receipt nor agreement with the earlier PR
packet is a certificate for the sharp upper equality L_2=2/sqrt(3). That
input remains a separate substantive dependency.
