# Proof-first structural reduction sidecar

Status: **EXACT OBSTRUCTION; NO THEOREM PROMOTION**

## Question audited

Can the unfinished local JC containment theorem be reduced conceptually to
the already known triangle-free level-2 theorem and the level-1 triangle
theorem by splitting a triangle-bearing theta blob into a canonical triangle
piece and a triangle-free piece?

## Answer

**PROVED:** the proposed split is not a bridge decomposition.  Every triangle
in a simple standard-strong theta blob and the complementary theta path meet
at both theta poles.  The corresponding tensor factorization is a
two-terminal contraction, and it has a nontrivial hidden-pair gauge.  Neither
the projective bridge theorem nor either cited identifiability theorem removes
that gauge.

**PROVED:** among the four locked theta event cores, `theta-2` is always
triangle-free.  Triangle-bearing expansions occur in exactly three structural
families: `theta-0`, `theta-1`, and `theta-3`, subject to the explicit port-word
conditions in `STRUCTURAL_ANALYSIS.md`.  In every such family the triangle
side has exactly one labelled boundary port; all other selected views lie on
the complementary path.  Thus ordinary three-view hidden-state uniqueness is
not available at the two-pole separator.

**PROVED:** for arbitrary tensors the contraction

```text
P(y,z) = sum_(u,v in G) A(y,u,v) B(z,u,v)
```

is invariant under

```text
A(y,u,v) -> c(u,v) A(y,u,v),
B(z,u,v) -> c(u,v)^(-1) B(z,u,v).
```

The translation-invariant choice `c(u,v)=2` for `u=v` and `1` otherwise is
not a product of separate pole-incidence factors.  The exact verifier checks
this with a nonzero `2 x 2` minor.

**UNRESOLVED:** the gauge transformation above need not preserve the JC
triangle and complementary-path model families.  Consequently this is not a
counterexample to identifiability.  It proves instead that a reduction which
recovers the two pieces from contraction, solely from bridge peeling or
group symmetry, has a missing load-bearing lemma.

The exact missing statement is the **anchored two-terminal JC rigidity
lemma** formulated in `STRUCTURAL_ANALYSIS.md`.  Proving that lemma would be a
genuine replacement for the unfinished local atlas.  Assuming it, or assuming
the local atlas itself, would be circular.

## Files

- `STRUCTURAL_ANALYSIS.md` — core-by-core proof and the exact missing lemma.
- `ADVERSARIAL_REVIEW.md` — hostile review of the obstruction and its limits.
- `verify_structural_obstruction.py` — independent exact replay using only
  Python's standard library and the inert core JSON.
- `verify.sh` — deterministic replay.
- `RESEARCH_LOG.md` — timestamped work ledger.

## Replay

From the project root:

```bash
bash reviews/proof_first_structural_reduction/verify.sh
```

