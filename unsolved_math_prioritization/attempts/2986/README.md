# KP-4.110: bounded Weinstein 2-handlebody partials

Problem **2986**, rank **922**. Canonical queue outcome: **unsolved, 4/5 turns**.
The exact author packet is independently accepted unchanged as four bounded
partial results. No target example, universal existence theorem, full solution,
novelty, formal proof certification, or human peer review is established.

## Accepted scope and remaining gap

1. A periodic Liouville orbit for a specified primitive on the standard four-ball,
   together with a boundary-fixed Liouville homotopy to its standard Weinstein
   primitive. This does not obstruct every Weinstein structure on the ball.
2. Vanishing homology above degree two in every cover of a genuine smooth
   2-handlebody, including the local-coefficient analogue.
3. Persistence of homology in degrees at least three under ordinary attachments
   of handles of index at most two.
4. Conditional mixed-torus reconstruction on the same smooth components when
   compatible Weinstein replacements preserve **all marked attaching embeddings,
   parameterized neighborhoods, and framing**. Unmarked boundary identifications
   or replacements on different manifolds do not suffice.

The exact target remains unresolved: no exact convex smooth 2-handlebody is
constructed with an obstruction to every Weinstein filling on that same smooth
manifold inducing its specified contact boundary. No universal existence theorem
is proved. See [the author report](original/REPORT.md),
[the independent audit](audit/AUDIT_REPORT.md), and
[the exact acceptance](audit/ACCEPTANCE.json).

## Source qualifications

The reconstruction uses Christian–Menke's corrected exact/weak theorem,
[arXiv:1807.03420v4](https://arxiv.org/abs/1807.03420v4), only in its exact case.
The earlier strong-filling formulation was withdrawn and is not used here.

Bibliographic supplement: Breen–Christian, *Torus bundle Liouville domains are
stably Weinstein*, Journal of Topology **18**(4), e70052 (2025),
[DOI 10.1112/topo.70052](https://doi.org/10.1112/topo.70052). The accurate historical
accepted-version attribution in the frozen author packet is preserved byte for
byte. The source review is bounded and is not an exhaustive novelty/open-status
certificate or a verification of every external proof.

## Immutable contents

- `original/`: all nine original author ZIP members, unchanged.
- `audit/`: all twelve independently sealed audit ZIP members, unchanged.
- `releases/`: the original author ZIP and external manifest, the independent
  audit ZIP and external manifest, the exact audit bootstrap, and its independent
  receipt. This directory is an artifact collection, not a GitHub release.
- `PUBLICATION_MANIFEST.json`: hashes and byte counts for all other publication
  files. Its hash and this wrapper's hash must be checked against a separately
  obtained publication receipt before execution.

The frozen author/audit label `partial` describes accepted mathematical scope.
It is historical metadata, not the canonical queue Status, which is `unsolved`.
The frozen manifest's audit-pending field and audit receipt's no-publication
statement also describe their historical preparation stages.

## Replay and trust boundary

After independently verifying the publication manifest and wrapper pins, run:

```sh
python3 -I -B verify_publication.py --corpus-dir /path/to/corpus --source-dir /path/to/sources
python3 -I -B -O verify_publication.py --corpus-dir /path/to/corpus --source-dir /path/to/sources
```

The wrapper verifies all six external artifact pins and every extracted member,
then executes the exactly pinned bootstrap, which verifies the audit ZIP before
extraction and performs isolated, relocated normal and optimized replay.
The three entire corpus files and seven PDF inputs are required for full external
input binding. Their names, sizes, and SHA-256 pins are in the independent receipt
and checker. They are not redistributed. Omitting both input flags is allowed but
explicitly reports that external inputs were not checked in that replay.

The recorded adversarial campaign has **104 executions: 92 expected rejections,
8 baseline successes, and 4 deliberate rebuilt-inner-manifest acceptance controls**.
Those last four are source-metadata/rank rewrites accepted by the inner checker
after its trust root is replaced; the sealed wrapper rejects the rewritten
archives. They are not four additional verified results. Internal manifests
cannot establish their own authenticity. The independently recorded bootstrap
pin is essential. Finite algebra checks do not certify the written mathematical
proofs, source theorem truth, or literature completeness.

Only safe authored proofs/audits, diagnostics, and public verification metadata
are included. No datasets, PDFs, copied source passages, private sources,
personal data, or private coordination material are published.

## Publication checkpoint

2026-10-06: exact accepted packets prepared for draft-PR publication without
mathematical repair. Best-guess completion toward the full target: **0% of a
verified full resolution**; the four bounded results do not supply the missing
fixed-manifold/fixed-boundary obstruction. The approach budget remains 4/5.
The only queue changes are rank 922's Status (`queued` to `unsolved`) and Turns
(`0/5` to `4/5`); Findings and all unrelated bytes are preserved. No merge,
GitHub release, DOI creation, or external outreach is part of this publication.
