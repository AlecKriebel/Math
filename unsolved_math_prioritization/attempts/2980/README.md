# KP-4.104 / 2980: accepted corrected partial results

Status: **UNRESOLVED_PARTIAL; unsolved; five substantive approaches (5/5)**. The smooth-versus-complex, smooth-versus-symplectic, and infinite-family clauses all remain unresolved. There is no complete solution or novelty claim.

Read `audit/public/REPORT.corrected.md` as the current report, then `audit/public/AUDIT.md` and `ACCEPTANCE.md`. The original seven-file packet and original archive remain separately preserved under `original/`. The original Section 4 wording and its compressed gap summary are historical; the explicit correction credits known conversion results and supersedes their suggestion that conversion existence or retention of the unmarked smooth class is itself missing.

Cao–Gallup–Hayden–Sabloff (CGHS), Lemma 4.1 and §4.2, supply moved-boundary symplectic perturbation and complex realization through smooth isotopy. These preserve the underlying unmarked smooth embedding class. What remains unknown here is survival of a separating invariant, including the Casals–Gao Hamiltonian distinction, through the conversions and all allowed isotopies. The fixed-geometric-Legendrian-boundary Stokes obstruction remains valid.

## Preserved evidence

- `original/public/`: all seven original public files, byte-for-byte.
- `original/symplectic_curve_isotopy_2980_sourcefree.zip`: exact original source-free archive, 17,306 bytes, SHA-256 `5a15ce6890e0bfd750f3f67e18043a33200fabd4e3dd8b5ed963ce19691f9881`.
- `audit/public/`: all twelve independent audit files, including the exact correction patch and corrected report.
- `audit/symplectic_curve_isotopy_2980_audit_sourcefree.zip`: exact audit archive, 33,006 bytes, SHA-256 `91c11dc8430ff3dd9c5a3f69a735cb7338f77a0d5256fdf6ba9067083fd533cb`.
- `audit/AUDIT_RECEIPT.json`: preserved archive/member verification receipt.

Only authored mathematics, checker code, correction, audit, acceptance, and public bibliographic/verification metadata are included. No source PDFs, extracted scholarly text, datasets, private sources, or private coordination files are present. The original ZIP inventories are rechecked against the preserved files without extraction.

## Authentication and source-free reproduction

Use a trusted external record of the exact `BOOTSTRAP.py` SHA-256, for example the reviewed draft PR description. Do not establish trust by hashing an untrusted local bootstrap and accepting its own answer. The bootstrap pins the wrapper and manifest; the wrapper pins every preserved historical file and checks a strict recursive allowlist. Self-consistently changing a historical file and its manifest does not satisfy the original pins.

After verifying that external bootstrap hash, run with standard-library Python 3 as actual UID and EUID 1000:

    python -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

Run the authenticated publication controls in each mode, supplying the same externally known bootstrap hash:

    python -I -S -B mutation_tests.py --root /path/to/packet --bootstrap-sha256 EXTERNAL_HASH

Add `-O` or `-OO` before the script name for the other modes. A fresh replay compares every original and independent checker stdout byte with its complete frozen expected output. It reproduces the native 36-run harness (six baselines and thirty intended mutation failures in normal, `-O`, and `-OO`) and compares the complete typed receipt, permitting only the runtime Python version field to differ. The wrapper records full new outputs rather than an extracted PASS token. It reconstructs the corrected report from the original and the exact two-hunk patch with no fuzz or offset.

Files and directories are frozen to `0444` and `0555`; actual append/create attempts must fail. Full publication controls also cover external trust, schema/type errors, missing/extra/linked/special entries, malicious changes followed by repinning, patch errors, and relocation in a hostile read-only working directory. They do not certify mathematical truth or independently prove any cited theorem.

Fresh source and corpus bindings are explicitly `NOT_RUN`. The source audit and retrieval/inspection history are frozen prior evidence, not new source inspection by this portable verifier. A bounded unsuccessful literature search is not a proof of absence.
