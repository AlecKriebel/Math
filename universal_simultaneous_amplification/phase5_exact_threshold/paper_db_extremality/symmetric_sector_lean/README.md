# Symmetric-sector formalization

Work in progress on the symmetric-balanced component of “Local Complete-Graph Optimality at Fitness Two and Strong-Selection Rigidity under Death–Birth Updating.” Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

## Exact scope

The intended principal result is positivity of the actual reduced scalar `reducedScalar N` for every integer `N≥3`, connected to the genuine active-chain expression `ν₀ Δ G Δ G q` for symmetric balanced real perturbations. This project does **not** yet claim that principal result. Completed checkpoints and remaining obligations are tracked in `RESEARCH_LOG.md` and `CORRESPONDENCE.md`.

The matrix `coefficientK` is the transpose of Appendix A's printed `H`. Good ranks are `1,…,N−1`, bad ranks `2,…,N−1`, and `N=n−1`. `reducedScalar` is defined by the mathematical matrix inverse; its invertibility is proved independently for all `N≥3` in `RowBounds.lean`. No scalar positivity is included in a definition or axiom.

## Pinned environment and clean build

Lean: `leanprover/lean4:v4.19.0`. Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The manifest pins transitive dependencies. With elan installed, from this directory:

```
lake update
lake exe cache get
lake build
```

`lake update` should preserve the exact revisions in the committed manifest. The initial local development reused the sibling Bell project's already downloaded mathlib package cache via an ignored `.lake/packages` symlink; **no Bell theorem or project assumption is imported**. A fresh checkout resolves the pinned packages normally.

The build contains ordinary kernel-checked proofs. Generated certificate tactics use `norm_num` or ordinary `decide`; they never use native evaluation to establish a theorem. The external exact solver discovers rational witnesses; the equations, inverse identification, and signs are verified in Lean.

## Certificate discovery

To regenerate small-system witnesses (not needed to check the committed proofs):

```
python3 -m venv .venv
.venv/bin/pip install python-flint==0.9.0 sympy==1.14.0
.venv/bin/python tools/generate_small.py
```

`tools/generate_margins.py` is the separate finite phase certificate generator. Python and these libraries belong to the untrusted discovery path, not the theorem trust base. See `reports/FINITE_MARGIN_CERTIFICATES.md` for its one-sided grid witnesses and exact N=40 check.

## Audits and limitations

`reviews/` records independent model, arithmetic, and trust reviews. The trust audit prints every principal theorem's dependencies. Ordinary mathlib foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) are acceptable and explicitly reported. The final claimed scope must be read from the theorem statements, not inferred from a successful build of supporting lemmas.

Outside this symmetric component: coverage/collision representation as fixation, stationary perturbation and analyticity, complete tangent decomposition, other sector signs, and the resulting fixation local-maximum theorem. No strong-selection or global conjecture claim is part of this project.
