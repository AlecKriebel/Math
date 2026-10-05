# Subcritical reinforcement: audited corrected positive-equilibrium candidate

Problem **30005453**, rank **798**, code **OWR-12697708-006**.

## Exact result and boundary

Two independent AI mathematical reviews passed the corrected candidate. The later [acceptance](v2_acceptance/ACCEPTANCE.md) binds the exact [v2 proof](author_v2/PROOF.md) and includes a [targeted second analytic review](v2_acceptance/REPORT.md). The [first complete audit](first_audit/AUDIT.md), [required corrections](first_audit/CORRECTIONS.md), and [exact proposed delta](first_audit/PROPOSED_V2.diff) are preserved.

For **0 <= alpha < 1**, a **countable undirected simple graph of uniformly bounded degree**, and **0 < p_v <= P < infinity**, the candidate proves existence and uniqueness of an equilibrium **strictly positive on every edge** and almost-sure convergence of N_e(t)/t to it, simultaneously for all edges **coordinatewise**, from unit initial edge counts. The rate infimum may be zero. Isolated vertices can be ignored. The reviewed deterministic positive-integer initial-count extension uses the corrected subtraction H(N_e(0)) in equation (9).

**Literal uniqueness among all nonnegative equilibria is false:** on Z with unit vertex rates, the two phase-shifted alternating 2/0 edge arrays are distinct equilibria for 0 < alpha < 1. The primary report does not explicitly restrict uniqueness to positive equilibria. Calling the positive formulation the source's intended statement is an **inference**, not a source-verified convention. This publication explicitly corrects that formulation.

There is **no uniform spatial convergence claim**, stochastic convergence rate, alpha=1 theorem, negative-exponent result, unbounded-degree extension, initially-zero-edge extension, or audited fractional-initial-count extension. The distinct critical alpha=1 problem [30005454, PR #222](https://github.com/AlecKriebel/Math/pull/222) is not settled here.

Queue status is **claimed_solved, 4/5** substantive approach families, with the literal counterexample and corrected theorem both recorded. This is a candidate for external specialist review. Neither the audits nor finite computation establishes novelty, priority, human peer review, journal/editorial acceptance, or publication readiness. External specialist and novelty review remain pending.

## Immutable review history

All four safe archives and all extracted files are byte-for-byte unchanged. In particular, historical **PROPOSED**, **PENDING**, and **no remote write** language inside the freezes is retained. The later, separately dated and hash-bound v2 acceptance records the subsequent review outcome; it does not rewrite the original author or first-audit history.

The accepted v2 archive is `SUBCRITICAL_REINFORCEMENT_30005453_AUTHOR_V2_PROPOSED_SAFE.zip`, SHA-256 `689cd325db19a449e373441c0c7cb0ede0e103456ec857215a207b7af83d3d8d`, 20,008 bytes. Its proof is SHA-256 `4ab6831e31f2c55969d17089a2cefacdd3d173a54f4b00e8244a5f8a635616f4`. [Publication provenance](PUBLICATION_PROVENANCE.json) identifies all four archives. Sections 2–8 have the exact same 12,593 bytes in v1 and v2; only six approved editorial substitutions in four content files, plus manifest regeneration, changed.

Primary public sources include the [Oberwolfach report](https://doi.org/10.4171/OWR/2023/12), the [Couzinie–Hirsch manuscript](https://arxiv.org/abs/2010.03347), and the [2018 thesis](https://www.theorie.physik.uni-muenchen.de/TMP/theses/couziniethesis.pdf). Their hashes, inspected locations and limitations are recorded inside the audits. The portable publication replay does not claim fresh PDF retrieval or a renewed broad novelty search.

## Reproduction

Python 3.10+ and the standard library suffice. From this directory:

```sh
python -B verify_publication.py --replay
python -B -O verify_publication.py --replay
python -B test_publication_integrity.py
```

The publication verifier checks the exact recursive inventory, SHA-256 and byte counts, safe ZIP structure and CRC, all 52 ZIP-member/extracted-byte identities, all four frozen manifests, the six-edit v2 boundary, and the unchanged analytic core. Replay runs original/v2 author checks, first-audit diagnostics, the independent delta reconstruction with eleven negative controls, and the second-review targeted diagnostics. Newly produced result files are compared byte-for-byte against the frozen outputs. All replay outputs are temporary; no frozen input is changed.

The second review's diagnostics cover 216 local strip tests (including 96 noninteger-beta cases), 100 boundary-pattern edge equations, 125 exact jump/bracket controls, 18 single-edge scalar identities, and four initial-offset controls. The first audit records 2,168 exact rational controls across 56 cases, 300 jump controls and 32 criticality controls. These are diagnostics; the analytic arguments in the proof and review reports support the infinite-graph conclusion.

To check the narrow queue update against downloaded base and branch copies:

```sh
python -B verify_publication.py --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/branch-QUEUE.md
```

Only this row's Status, Turns and Findings change. Every other queue byte, including the pre-existing stale header, is preserved. The full source/corpus provenance check is documented in the frozen first audit and requires separately supplied inputs, which are not bundled.

## Safe payload

Authored proof, code, audits, acceptance, results, four unchanged safe archives, and public verification metadata only. No source PDFs, extracted source text, page images, raw datasets or private coordination material. Draft review only; no merge, release, DOI creation or outside contact.
