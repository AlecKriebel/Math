# Borderline soliton–potential interactions: corrected partial results

Problem 30001591 / OWR-4429-002, rank 978. **Unsolved, 5/5 approaches.**

Read [the corrected proof](audit_release/PARTIAL_RESULTS.corrected.md), [full independent audit](audit_release/FULL_AUDIT.md), and [acceptance report](audit_release/ACCEPTANCE.json). The original research is preserved byte-for-byte in `release/`; its README's pending-audit wording is historical. The subsequent audit and its actual [correction patch](audit_release/CORRECTION.patch) are preserved in `audit_release/`.

## Accepted scope and repair

The accepted results concern the reduced modulation ODE, conditional logarithmic ODE escape, stationary-state exclusion, a cubic compactness obstruction, energy and signed-integral restrictions, broad-tail counterexamples, and a perturbed-invariant identity. Section 5 now explicitly assumes a′>0: strict increase alone permits a flat cubic crossing that prevents finite-time reflection. Boundedness in the cubic argument and the distinction between profile scale and center velocity are also clarified.

No classification of the actual critical PDE dynamics is proved. The missing step is a fixed-ε, all-late-time modulation/radiation analysis with signed accumulated-error and tail control. In particular, the ODE logarithmic law is not asserted for the PDE. These authored AI-assisted partials and their independent AI-assisted audit are neither human peer review nor formal verification. No novelty, priority, or exhaustive current-literature claim is made.

## Portable reproduction

Requires Python 3.12 and SymPy 1.14.0 (see `requirements.txt`). Obtain the PUBLIC_MANIFEST.json SHA-256 from the draft PR description or another separately trusted record, then run:

    python3 -B verify_publication.py TRUSTED_PUBLIC_MANIFEST_SHA256
    python3 -B -O verify_publication.py TRUSTED_PUBLIC_MANIFEST_SHA256
    python3 -B -OO verify_publication.py TRUSTED_PUBLIC_MANIFEST_SHA256
    python3 -B mutation_tests.py TRUSTED_PUBLIC_MANIFEST_SHA256
    python3 -B -O mutation_tests.py TRUSTED_PUBLIC_MANIFEST_SHA256
    python3 -B -OO mutation_tests.py TRUSTED_PUBLIC_MANIFEST_SHA256

An optional second positional argument to the verifier selects a relocated package. The outer verifier rejects unexpected files/directories and symlinks, checks exact bytes against the externally pinned inventory, pins both frozen manifests and both proofs, actually applies the unified correction patch, and independently launches the algebra scripts in optimization modes 0, 1 and 2. A runtime probe confirms each child's actual optimization mode. It also replays both frozen verifiers. The original verifier itself does not forward optimization to its algebra child; direct child runs supply that separate coverage.

The author script has 43 exact checks and 3 wrong-identity rejections; the independent script has 78 exact checks and 9 wrong-mathematics rejections. The public mutation suite adds 15 inventory/anchor corruption cases and 6 direct corrupted-algebra runs across actual child modes 0, 1 and 2. Passing these checks authenticates consistency and finite calculations, not the infinite-time PDE claim.

The outer manifest deliberately excludes itself. Trust comes from a digest obtained separately, not from recomputing a digest inside an untrusted package. A changed verifier cannot authenticate itself; use a separately trusted verifier and manifest pin when examining a suspect copy.

## Sources and chronology

[Public source metadata](release/PUBLIC_SOURCE_METADATA.json), [source reconciliation](release/SOURCES.md), and [audit source metadata](audit_release/AUDIT_SOURCE_METADATA.json) give public titles, URLs, byte counts, hashes and inspection limits. Public source PDFs, extracts, screenshots, datasets, private gates and coordination files are excluded. Reproduction needs none of those external source bytes. Dataset hashes preserve provenance only; no new remote-revision authentication is claimed.

The frozen [five-approach ledger](release/TURN_LEDGER.json) records author-supplied first-write checkpoints. Auditing, correction, replay and publication are not additional mathematical approaches. See [publication status](PUBLICATION_STATUS.json) for the accepted scope and frozen anchors.
