# Modern K3 Problem 3.72 / catalog 2870: audited scoped partials

**Controlling release disposition: unsolved, five of five approaches used.**
Neither part (a), an infinite-rank countable free subgroup of the smooth
integral-to-rational homology-cobordism kernel, nor part (b), a direct summand
of that kernel, is proved by this packet. There is no worldwide-openness,
historical-priority, novelty, or human-peer-review claim.

## Read the audit clarification with the frozen proof

The nine files under `author/` are the unchanged author freeze. Its README and
STATUS still describe the historical pre-audit stage. The six files under
`audit/` are the unchanged independent audit. This guide and
`RELEASE_STATUS.json` record the later release disposition without rewriting
either freeze.

The controlling audit verdict is **PASS_SCOPED_UNSOLVED_WITH_CITATION_ADDENDUM**.
Read [the audit's ordinary-d versus upper-involutive-d clarification](audit/AUDIT.md#audit-clarification-ordinary-d-versus-upper-involutive-d)
alongside the optional ordinary-d paragraph after Proposition 4.2 in
`author/PROOF.md`. Lee–Savk Theorems 2.5 and 3.1 directly give the upper
involutive correction term. The bridge to ordinary d is **Dai–Manolescu,
Involutive Heegaard Floer homology and plumbed three-manifolds, Theorem 1.2**,
for the boundary orientation of negative-definite AR plumbings.
See the [bibliographic record](https://arxiv.org/abs/1704.02020) and
[inspected author-hosted PDF](https://web.stanford.edu/~cm5/HFIplumbed.pdf).
The audit supplies this missing citation and checks the orientation hypothesis;
the present publication makes no additional mathematical change.

The principal supported deduction is that the standard
Dai–Hom–Stoffregen–Truong free summand intersects the rational-filling kernel
trivially, by the credited filtered-instanton rational-independence criterion.
That argument does not depend on the optional ordinary-d cross-check. It is
an obstruction to recycling this existing summand into a solution, not a
solution of either target part. The other preserved results are elementary
reductions and conditional rank-transfer/splitting criteria with explicit gaps.

## Verification and scope

- Author freeze manifest SHA-256:
  `8074d0a6a5ec04ee4ba269300bb0bddad6b49595e955f456d26a10898b757888`.
- Frozen proof SHA-256:
  `4ae92f8adaabff6700ee8a6da5a178e629321729cbd4420153d6c2f64975ac36`.
- Audit manifest SHA-256:
  `9a35d1eeb6b10378ceae1aea66ff8da42d7d35d2a765c8b58d24ecdcbc0fb841`.

Run from any working directory with Python 3.10+ and its standard library:

```sh
python3 /path/to/2870/verify_release.py
```

The wrapper checks all three manifests and their file inventories, verifies
the audit bindings, and replays both programs with byte-for-byte output checks.
The author program has 9,495 assertions; the independently written audit
program has 6,470 probes. These are finite algebra diagnostics, not proofs
of Floer invariant values or independence of actual manifolds. The written
arguments rely on the explicitly credited external topology/Floer inputs.
An AI audit is not formal verification or human peer review. Local replay
does not imply GitHub CI passed; an empty checks list is not a CI pass.

Only authored work, executable diagnostics, audits, and public bibliographic,
retrieval/inspection, and hash metadata are included. Source PDFs, extracts,
screenshots, dataset contents, and private coordination are excluded. Public
corpus manifest values are recorded as such; no independent corpus rehash is
claimed. The queue change is limited to catalog 2870's Status and Turns.
All other queue bytes, including its existing literal metadata-looking header,
are retained. The target is modern K3 3.72, not the unrelated 1997 numbered
convergence-group problem.
