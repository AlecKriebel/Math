# Sublaminations: source-free author packet

Status: **unsolved, 5/5 substantive approaches**. General characterization and algorithm are not proved. Start with PROOF.md, then APPROACH_LEDGER.json and SOURCE_AUDIT.md.

The packet proves a finite compact-leaf characterization, an explicit circle-suspension exclusion, failure of intrinsic transverse-weight data alone, and finite-regular-cover witness descent. Its fifth approach records the precise carrier-recognition/containment gap. These are scoped elementary or credited classical consequences, with no novelty claim. Independent mathematical review is pending.

verify.py checks bounded graph controls, exact surface arithmetic, input schemas and optional privately supplied source/corpus hashes. It does not mechanically verify the topological arguments. controls.py exercises positive, malformed and wrong-input subprocesses under normal Python, -O and -OO. No correctness check depends on Python assert.

The frozen distribution has an outer MANIFEST.json and bootstrap.py. Before executing, authenticate BOTH files against independently supplied external SHA-256 pins. The bootstrap authenticates the complete payload and its strict inventory before invoking verify.py in isolated Python. It does not make an untrusted bootstrap trustworthy. Use a trusted Python interpreter, standard library, operating system and quiescent filesystem.

Optional source/corpus checking is read-only, requires the caller's local files, and prints metadata only. Copied scholarly documents, extracted source text, raw dataset records, private coordination files and queue copies are excluded.
