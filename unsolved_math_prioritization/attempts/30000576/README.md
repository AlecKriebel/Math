# Chaotic semigroups: prior resolution with an audited scalar bridge

Problem 30000576 / OWR-1323-013; queue rank 658.

**Disposition: already_solved, 1/5 substantive proof-attempt turns. Both answers are no.**
The existence result is attributed to Frédéric Bayart and Teresa Bermúdez,
[*Semigroups of chaotic operators*, BLMS 41 (2009), 823–830](https://doi.org/10.1112/blms/bdp055).
This is a prior-literature resolution with an independently audited scope bridge.
No new counterexample, novelty, or priority is claimed.

The target concerns bounded linear C0-semigroups on separable complex Banach
spaces, with chaos meaning a dense orbit and dense semigroup-periodic vectors.
The published example has no chaotic operator at any positive real time.
Consequently it refutes both the every-positive-time and the some-positive-time
questions. A mixed-time example, or a time-zero obstruction, would not suffice.

## Current verdict and preserved history

The original attribution-only packet in `safe/` and the original independent
audit in `independent-audit/` are preserved byte-for-byte. The original audit's
**HOLD was warranted**: the inspected literature did not directly establish
the example's scalar field. That historical HOLD is not erased or rewritten.

The separately frozen `revision-v2/safe/PROOF.md` supplies a general bridge:
a chaotic real C0-semigroup has a chaotic complexification, and nonchaos of
every individual positive-time operator is preserved. The proof establishes
synchronized real periods, diagonal transitivity and hypercyclicity, the
complex Banach structure, strong continuity, and descent of fixed-time chaos.
The new full independent audit in `revision-v2/independent-audit/AUDIT.md`
passes this bridge and **supersedes the earlier scalar-field HOLD**. If the
published example is complex, it applies directly; if real, the bridge applies.

The full 2009 construction and proof remain an **uninspected published input**.
This package does not independently reconstruct or fully proof-audit that paper.
The original example's scalar field remains directly unverified; the audited
bridge makes direct confirmation unnecessary. The preserved revision-2
author-stage request for independent review is historical; that review has now
passed. The original source-inspection limitations remain visible.

All 39 frozen author/audit files and both seven-file safe audit archives are
unchanged. The new audit contains the complete proof review, source metadata,
binding and executable adversarial controls. No third-party text, PDF, rendered
page, dataset corpus, private source or coordination payload is redistributed.
Public source URLs, hashes, byte counts and inspection history are included.

## Portable checks

Requires Python 3.10+ and its standard library. From any working directory:

```sh
python3 path/to/30000576/verify_release.py
python3 path/to/30000576/verify_release.py --replay
```

The strict wrapper verifies the exact file/directory set, rejects symlinks,
checks hashes and byte counts, validates both audit archives against their
unpacked originals, and optionally reruns both independent audit verifiers.
Those rerun all 14 original packet checks, all 15 revision-2 packet checks and
all 8,369 authored exact controls, plus independent binding/adversarial checks.
Replay runs with assertions enabled even when this wrapper uses `python3 -O`.
Normal and optimized-wrapper negative controls reject extra files/directories,
symlinks, changed bytes, missing files, and modified archives.

Finite controls support the separately inspected infinite-dimensional argument;
they are not a machine proof or a finite-dimensional hypercyclic example.
`RELEASE_VERIFICATION.json` records the exact replay results and frozen anchors;
`RELEASE_MANIFEST.json` binds the release files. The wrapper verifies no live
source or corpus bytes and makes no new source-retrieval claim.
