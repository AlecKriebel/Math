# Runtime and hardware

The verifier requires Python 3.10 or newer, Bash, and a SHA-256 utility.
Pinned Python dependencies are in `environment/requirements.txt`.
On first use, `verify.sh` creates `.venv` and installs those pinned packages;
this requires either package-index access or a populated local wheel cache.
Once installed, all mathematical replay and regeneration steps are local and
make no network requests.

The reference release was checked on macOS with an Apple M1 Pro and 16 GB of
RAM.  The exact computations are CPU-only.  The full and regeneration modes
use temporary disk space roughly equal to the extracted bundle size because
they preserve the proof object and operate on a copy. Approximate reference
times are recorded in the run logs distributed beside the archive.
`regenerate-all` intentionally performs two complete isolated regenerations
and therefore takes substantially longer than `full`.

No specialized phylogenetic-network package is used.
