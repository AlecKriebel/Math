# Weighted affine-line endpoint partials

Problem 30003235 / OWR-15169-009, queue rank 995. **Unsolved, 5/5 substantive author approaches.**

Read [publication acceptance](PUBLICATION_ACCEPTANCE.md), the complete [authored proof](original/PROOF.md), all five cumulative [checkpoints](original/checkpoints/), and the [full independent mathematical audit](independent_audit/FULL_REPORT.md). Both frozen packets are preserved byte for byte. No mathematical correction is required and no sixth proof-search approach is added.

The accepted scoped endpoint theorem covers positive weights and nonzero-slope lines containing a rational point, via heavier-coordinate inversion and a credited coordinate-fiber theorem. The general irrational-slope case with b outside Q+Qa remains unresolved. The horizontal counterexample addresses only a wider literal scope omission. No novelty or exhaustive current-openness claim is made.

## Reproduction

Python 3 and its standard library suffice. Obtain the outer-manifest and verifier SHA-256 pins from a separately trusted publication record. Authenticate VERIFY_PUBLICATION.py before execution; a verifier cannot establish its own initial trust using hashes shipped beside itself. Then run:

    python3 -I -B VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_OUTER_SHA256
    python3 -I -B -O VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_OUTER_SHA256
    python3 -I -B -OO VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_OUTER_SHA256

Each default invocation replays all three child optimization modes. Use --mode ordinary, --mode optimized or --mode double_optimized to select one. --check-only validates strict inventory, pinned frozen bytes, JSON and executable syntax without replaying finite controls.

After authenticating TEST_MUTATIONS.py through the pinned inventory, run:

    python3 -I -B TEST_MUTATIONS.py --packet . --expected-manifest TRUSTED_OUTER_SHA256 --expected-verifier TRUSTED_VERIFIER_SHA256

The mutation program uses a separately pinned bootstrap and disposable fixtures. Inputs may be relocated and read-only. Historical control runners receive an exact writable temporary staging copy because they mutate disposable fixtures. All input bytes are checked again after replay. Original optional --probes accepts repeated kinds; this wrapper authenticates the fixed shipped bytes and does not claim to harden that interface.

Source documents, extracted texts and datasets are absent. The portable replay does not reverify source bytes or independently prove any infinite theorem. These are bounded diagnostic and integrity checks, not human peer review, proof-assistant certification, a hostile-code sandbox or a filesystem-race guarantee.
