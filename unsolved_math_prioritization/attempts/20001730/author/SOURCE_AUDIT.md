# Source and assumption audit

## The problem being attempted

The live AIM page, http://aimpl.org/equibdynsysgeom/5/ , was retrieved successfully over HTTP on 5 October 2026. Its Problem 5.1 is attributed to Kurt Vinhage. The problem asks whether commuting hyperbolic maps and a potential admit leafwise conditional measures with cocycle-type transformation laws. The displayed status field is empty. This is the construction target; it does not supply the additional hypotheses assumed in the reconstructed compatibility theorem. An empty status field is not proof that no solution exists in the literature.

The web-reader HTTPS route first failed with 502; a direct read of the publicly linked HTTP page succeeded. `SOURCE_METADATA.json` binds the inspected page bytes. The raw page is outside this release.

## Classical leafwise background

Manfred Einsiedler and Elon Lindenstrauss, *Diagonal Actions on Locally Homogeneous Spaces*, notes dated 27 August 2008, https://math.huji.ac.il/~elon/Publications/TopErgThySp07.pdf . Inspected title page and printed pages 20–22, especially Theorem 6.3, Remarks 6.4, and Example 6.5.1. These describe measurable projective leafwise measures, local conditional restrictions, exceptional null sets, and the distinction between whole intrinsic leaves and finite local plaques. The irrational-flow example uses Haar length on noncompact leaves.

Their stated setting is a locally free group action with further hypotheses; it is not a theorem constructing our prescribed Gibbs normalization for arbitrary Anosov data. The present note assumes its own kernels, conditional classes, and transport laws, and separately proves its claimed consequence. The reference is background and a scope check, not a substitute for those assumptions.

## Parameter-dependent Radon–Nikodym derivatives

Dmitry Novikov, *Hahn Decomposition and Radon–Nikodym Theorem with a Parameter*, arXiv:math/0501215v1, https://arxiv.org/abs/math/0501215 . Inspected the title, Theorem 1.1, and its initial proof setup. That theorem uses a fixed dominating probability. Our two plaque kernels can both vary with the plaque; the fixed-denominator statement is therefore not cited as a verbatim theorem covering our application.

The Mathlib project's primary documentation, *Radon–Nikodym derivative and Lebesgue decomposition for kernels*, https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Kernel/RadonNikodym.html , was inspected at its introductory hypotheses and main statements. It provides jointly measurable densities for finite kernels on a countably generated target and explicitly explains why arbitrary pointwise choices of ordinary densities do not give joint measurability. The note uses ordinary plaque coordinates, finite kernels, and an explicit partition-ratio construction. If using a uniformly bounded finite-kernel formulation, divide both kernels by 1 plus their total masses, which leaves the density unchanged. No Lean formalization of this research note was performed.

## Hypothesis crosswalk and limits

- Uniform backward leaf contraction is explicitly assumed; it is checked directly in the toral example.
- Common invariance and f-ergodicity are assumptions in the compatibility theorem; the example verifies them by integer matrices and a Fourier argument.
- Holder a,b, the scalar square, and the exact Gibbs rebasing formula are explicit sufficient hypotheses of this reconstruction. The normalized g rebasing identity is proved by telescoping.
- Measurable plaque kernels and conditional-class equivalence are assumed, with their precise role stated. They are not inferred from bare existence of a potential.
- The f transport identity and g measure equivalence are whole-leaf hypotheses, not conclusions smuggled in from local disintegration.
- Birkhoff recurrence and standard Radon–Nikodym/martingale facts are the classical measure-theoretic inputs. The passage from local equality to whole-leaf equality is written out using recurrence and contraction.
- Intrinsic Radon measures need not have finite mass on ambient open sets for dense leaves. The note never assumes that stronger property.
- The exceptional-leaf example shows a genuine domain-quantifier obstruction, not a negative solution to the original measure-construction question.

These sources and arguments do not establish the existence hypotheses for arbitrary source data. This release remains an independently unreviewed, conditional partial correction.
