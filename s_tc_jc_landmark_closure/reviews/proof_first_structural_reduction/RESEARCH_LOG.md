# Research log

## 2026-08-12 — input lock and core analysis

- Read the locked topology/model definitions, generator/support theorem,
  candidate local atlas theorem, and inert primitive core encoding in full.
- Reconstructed the path-length formulas for all four theta event cores.
- Determined symbolically, for arbitrary port words, that triangle-bearing
  strong expansions occur only in three structural families (`theta-0`,
  `theta-1`, `theta-3`); `theta-2` is always triangle-free.
- Observed that every surviving triangle has exactly one boundary port on its
  side of the two-pole decomposition.

## 2026-08-12 — attempted literature reduction

- Checked the locally frozen source of Englander et al. v4, including
  Theorems 3.1 and 3.2 and the induced-subnetwork convention.
- Rejected direct application: the complementary path is a factor with two
  hidden state boundaries, not a complete triangle-free network; the triangle
  factor is not separately recovered from the observed blob tensor.
- Rejected virtual-leaf and marginal-deletion shortcuts because containment
  descends under marginalization but does not lift to an extension.

## 2026-08-12 — exact obstruction and adversarial pass

- Proved the two-terminal contraction formula and its state-dependent gauge.
- Gave an exact translation-invariant gauge with a nonzero rank-two minor,
  showing that it is not a product of pole-incidence factors.
- Corrected the scope adversarially: the gauge is not known to preserve the JC
  factor submodels and therefore is not a nonidentifiability theorem.
- Isolated the anchored two-terminal JC rigidity lemma as the exact missing
  model-specific statement.
- Added a standard-library-only exact verifier; no topology census or search
  over arbitrary completions was run.

