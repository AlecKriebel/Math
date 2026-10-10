# Fixed-span knot-polynomial values: corrected scoped partials

Problem 10400013 / AMR-103-0013, rank 1009. **Unsolved, 5/5 approaches.**

The recovered original heading is Problem 1.13 (A. Stoimenow), printed p.391 / PDF p.19 of [Ohtsuki's problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf). The descriptive title above is editorial. The queue's truncated Problem cell remains unchanged; recovery is recorded in Findings.

## Accepted scope

- Jones value-finiteness under a fixed braid-index bound, for adequate diagrams with a genus bound on the same diagram, and in a fixed two-strand full-twist exterior.
- The credited Traczyk two-component link family disproves the unrestricted-link Jones clause. It is not a knot counterexample or a resolution of every clause.
- Small-span Jones and Q results are prior literature. The displayed bivariate specialization kernels are formal polynomial families, not realized knot invariants.
- General knot Jones, Q, skein/HOMFLY and Kauffman clauses remain unresolved by this attempt.

Read the [unchanged mathematical proof](audit/corrected_freeze/packet/PROOF.md), [full independent audit](audit/AUDIT.md), [acceptance](audit/ACCEPTANCE.json), and [actual correction patch](audit/CORRECTION.patch).

## Provenance and correction

`author_original/` and `archives/AUTHOR_FREEZE.zip` preserve all 12 original freeze members. `audit/` and `archives/AUDIT_FREEZE.zip` preserve all 26 audit members, including the separately adopted `audit/corrected_freeze/`. Original author claims and receipts are dated provenance snapshots: their audit-pending and no-remote-writes fields are not present publication status.

The correction keeps negative powers of unit monomials in integer arithmetic instead of Python floating-point arithmetic. Only `packet/verify.py`, its `AUTHOR_MANIFEST.json` entry and the bootstrap manifest pin change. The proof is byte-identical. Publication replay actually applies the distributed patch in a temporary copy, with zero fuzz or offsets, and compares all 12 resulting members byte-for-byte to the accepted corrected freeze.

## Verification and limits

Requires Python 3.9 or newer and the standard `patch` utility, run as an unprivileged user. No Python packages or network access are required. First compare the SHA-256 of `BOOTSTRAP.py`, `VERIFY_PUBLICATION.py` and `PUBLICATION_MANIFEST.json` with the external pins in the draft PR. Do not treat hashes supplied by an unauthenticated candidate tree as external trust anchors.

From this directory, run:

```sh
python3 -I -S -B BOOTSTRAP.py
python3 -I -S -B -O BOOTSTRAP.py
python3 -I -S -B -OO BOOTSTRAP.py
python3 -I -S -B TEST_MUTATIONS.py
python3 -I -S -B -O TEST_MUTATIONS.py
python3 -I -S -B -OO TEST_MUTATIONS.py
```

The external bootstrap authenticates the verifier and publication manifest before executing payload code. Exact file and directory inventories reject missing, changed, extra, symlink and nonregular entries. The frozen archives and inner manifests are independently bound. A separate trusted launcher tests candidate-tree corruption, malformed manifests, self-consistent forged claims, hostile executable replacements and hostile imports. This is a static-candidate integrity boundary, not a concurrent hostile-writer sandbox.

The original and corrected author harnesses each check 6 positive replays, 78 integrity rejections and 45 semantic rejections. The independent audit performs 57,250 finite checks, 9 positive replays, 99 adversarial or malformed-input rejections, and 6 exact-arithmetic regression cases. Read-only permissions are actually enforced and write denial is tested. Normal, `-O` and `-OO` publication outputs must agree. These finite executable checks support the mathematical audit; they are not formal theorem verification, knot-realization certificates or GitHub CI.

Default replay is source-free. Fresh PDF and corpus checks report `NOT_RUN` when those optional inputs are absent. Historical source inspection and record-join results remain explicitly historical public metadata. Optional `--source-dir DIR` expects the nine PDFs named by source ID in `SOURCE_IDENTITIES.json`; optional `--problems FILE --research-results FILE` checks both entire corpus byte identities. These optional operations hash private local inputs without publishing their contents. They do not claim fresh scholarly inspection or a fresh record join.

No copied source PDF, extract, dataset content, private source or coordination material is included. No novelty, human peer review, formal certification, merge or release is claimed.
