# 9700042: sharp near-one oriented-percolation flow asymptotic

Problem: AMR-096-0042. Queue rank: 937. Research disposition: `claimed_solved`.
Author-attempt budget: **5/5**. Date: 2026-10-07.

## Current result and exact acceptance target

For the canonical north/east Bernoulli-capacity square-lattice model in
[David Aldous's problem statement](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html),
the authored argument proves

\[
1-v(p)\sim\sqrt{2(1-p)}\qquad(p\uparrow1).
\]

Two fresh, separate mathematical audits accept the full argument in
[`TURN_C4_BK_POISSON_REVISED.md`](TURN_C4_BK_POISSON_REVISED.md), **20,646 bytes**,
SHA-256 `8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a`:

- [Full acceptance A](audit_a/INDEPENDENT_ACCEPTANCE_A.md), with its [frozen audit manifest](audit_a/AUDIT_MANIFEST.json)
- [Full acceptance B](audit_b/AUDIT_REPORT.md), with its [frozen audit manifest](audit_b/AUDIT_MANIFEST.json)

Acceptance depends on C1's finite directed duality and marked-list enumeration.
The exact prerequisite is [`TURN_C1_MARKED_DEFECT_BOUND.md`](TURN_C1_MARKED_DEFECT_BOUND.md),
9,957 bytes, SHA-256 `f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120`.
The [C1 audit](audit_c1/AUDIT_REPORT.md) and its
[clarified presentation](audit_c1/TURN_C1_CLARIFIED.md) expand the directed-interface
argument, including four-valent faces. The C1 audit alone accepts only a partial
upper bound with constant e/2; the full conclusion is accepted by audits A and B.

This remains an authored mathematical claim supported by AI mathematical audits.
It is not a novelty certification, human peer review, or formal verification.
Current literature-wide unresolved status has not been certified.

## Explicit external inputs

1. The existence and normalization of the deterministic L1 limit
   `V(n,p)/(2n) -> v(p)`, as stated on Aldous's primary page. The packet does not
   independently prove that existence theorem or use the page's continuum
   heuristic as a theorem.
2. The classical constant-two increasing-chain law and positive-excess
   upper-tail estimate, via the introduction and Theorem 2 of
   [Deuschel–Zeitouni, On increasing subsequences of i.i.d. samples](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf).
   The proof supplies its Poissonization, moment, and mean-convergence steps.
3. Finite Bernoulli-product BK disjoint occurrence. The witness definition and
   product-measure Theorem 1.1 are stated in
   [van den Berg–Jonasson, A BK inequality for randomly drawn subsets of fixed size](https://arxiv.org/pdf/1105.3862).
   The argument uses this product theorem, not a fixed-size sampling inequality.

[Source metadata](SOURCE_METADATA.json) and the audit manifests identify the
inspected public source bytes, dates, URLs, and inspection scope. Those metadata
do not promise that future downloads will have unchanged bytes.

## Preserved revisions and historical labels

The [original C4](TURN_C4_BK_POISSON_CANDIDATE.md), the
[author clarification](C4_AUTHOR_CLARIFICATION_1.md), and the
[actual original-to-revised patch](C4_CLARIFICATION.patch) are preserved unchanged.
The patch corrects segment indexing and a strict inequality, justifies final
rectangle positivity, and makes mean uniform integrability explicit. Acceptance
attaches to the revised file above.

C1's [actual clarification patch](audit_c1/C1_CLARIFICATION.patch) is also supplied.
Original proof and audit files preserve their writing-time status sentences,
including “not yet accepted,” historical preservation statements, and C1's
original novelty wording. Those frozen sentences are historical records; this
README states the current disposition and does not adopt a novelty claim.

C2 and C3 are not prerequisites and are not included in this focused packet.
The full C1–C4 review archive is not being presented as an accepted full proof.
The revised C4 proves its lower bound afresh; no missing historical proof or
audit is a dependency. The [research log](RESEARCH_LOG.md) records only the
supported attempt count and the limited scope of the included work.

## Reproducibility

From this directory, run:

```sh
python verify_packet.py
```

Python 3 and the system `patch` utility are needed. The verifier first checks the
complete packet path set, SHA-256, byte count, and Git blob SHA-1 for every file
listed in [PACKET_MANIFEST.json](PACKET_MANIFEST.json). It replays both actual
clarification patches with zero fuzz and verifies the resulting exact bytes.
It runs five authenticated frozen finite checkers in normal, `-O`, `-I`, and
`-I -O` modes, using `compile(..., optimize=0)` so assertions remain active.
All checker outputs must match the frozen JSON bytes. Corrupt-source,
forced-failure, altered-proof, unexpected-path, and damaged-patch-context
negative controls must fail. Tests use temporary copies and never overwrite
the frozen files. See [REPLAY_RESULTS.json](REPLAY_RESULTS.json).

These checks are finite diagnostics, not proofs of BK, the Poisson theorems,
or the asymptotic claim. Plain direct invocation of an assertion-based frozen
checker with `python -O` would discard its assertions; use this verifier for
optimization-mode validation.

The frozen audit manifests describe their original review inventories, some of
which included source inspection material and duplicate snapshots. They are
not this packet's file inventory. `PACKET_MANIFEST.json` is the authoritative
publication inventory and records relocation of included authored artifacts;
omitted inventory entries are not claimed to be present. No copied source
PDF/HTML, source screenshot, raw corpus record, or private coordination file is
included.

## Repository scope

The only existing repository file changed is `unsolved_math_prioritization/QUEUE.md`:
row 937's Status, Turns, and Findings cells. All other existing bytes, including
the queue header and existing links, are preserved. This package is intended
for one draft PR; no merge, release, DOI deposit, or external outreach is part
of its publication.
