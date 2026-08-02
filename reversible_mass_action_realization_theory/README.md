# Reversible mass-action realization theory

This is the separate follow-up program opened after the immutable Version 2
release of *A reversible three-species mass-action continuum without a common
factor*.  Nothing in this directory is part of, or changes, that release.

## Objective

Characterize when a prescribed smooth positive complete intersection

\[
I=(L,Q)\subset \mathbb Q[x,y,z],
\]

with `L` affine linear and `Q` quadratic, is a reduced equilibrium component
of a reversible three-species mass-action system having one linkage class,
full stoichiometric rank, positive rational rates, and coprime coordinate
polynomials.

The first major target is a theorem with explicit hypotheses under which every
positive rational ellipse in an affine plane has such a realization.  The
intended proof architecture separates the problem into three exact layers:

1. **Geometry:** certify that `(L,Q)` is a smooth compact curve contained in
   the positive orthant.
2. **Linear positive feasibility:** for a fixed reversible support, construct
   the rational remainder map `M`; conic preservation is exactly `M k = 0`,
   and positive realization is exactly `ker(M) ∩ R_{>0}^{2|E|} != ∅`.
3. **Open algebraic conditions:** after a positive kernel point exists, test
   coprimality and reducedness at the conic.  A single exact witness proves
   the corresponding good loci are nonempty within that support family.

## Current contents

- `FRAMEWORK.md` gives the first-principles formulation, proved reductions,
  and the next lemmas that remain open.
- `remainder_map.py` constructs the exact fixed-support linear map and checks
  graph and stoichiometric data for arbitrary finite supports.
- `verify_seed.py` is an independent exact seed calculation using the known
  ten-complex support.  It is evidence and a regression test, not a general
  realization theorem.
- `RESEARCH_LOG.md` records checkpoints and claim boundaries.

## Reproduction

From `/Users/alec/Documents/Math`, using the existing project environment:

```text
.venv/bin/python reversible_mass_action_realization_theory/verify_seed.py
```

All discovery in this project begins from exact algebra and finite graph
data.  No external literature was used to formulate this initial framework.

## Claim boundary

At this checkpoint, the general ellipse-realization theorem is a research
target, not a result.  What is established is the exact equivalence between
fixed-support conic preservation and a rational positive-kernel problem, plus
the local rank criterion for a reduced conic component.  The seed support
shows that these conditions can hold simultaneously for one ellipse and a
four-dimensional cone of rates.
