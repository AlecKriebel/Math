# Claim comparison: Zhu–Chen–Wang and the present work

**Audit date:** 11 August 2026

**Primary ZCW source:** arXiv:2608.01317v1, posted 2 August 2026

**Audited repository commit:** `c782e8bc2876d5a2c5f068fe8c9007aa1ce0718f`

The official arXiv submission history was rechecked on 11 August 2026 and
showed only version 1, submitted 2 August 2026 at 15:37:41 UTC.

## Executive boundary

The two works independently prove exact analytic fixed-qubit POVM–PVM Bell
separations in the same broad 3×2 input and `(2,2,3)`-by-`(2,2)` output
architecture. Their displayed coefficient tensors and ternary POVMs are
different. Both use a dominant CHSH term together with a weaker ternary
probe. Neither claims the exact fixed-qubit PVM optimum of its functional.

The present paper’s principal distinct result is the universal equality of
the shared-randomness convex hulls of fixed-qubit POVM and PVM behaviors for
every two-input-per-party architecture with arbitrary finite, input-dependent
outputs. Combining that no-go theorem with an exact 3×2 witness gives the
minimum-setting classification. ZCW does not address that two-input theorem.

ZCW’s principal distinct additional result is the exact unrestricted
finite-dimensional tensor-product optimum of its functional, supported by an
exact level-3 noncommutative sum-of-squares certificate. Its Lean 4 project
formalizes the fixed-qubit separation theorem. The present paper proves no
unrestricted optimum for its own functional and contains no proof-assistant
formalization of the universal closure theorem.

ZCW version 1 describes its separation in the abstract, with the qualifier
“To our knowledge,” as the first fully analytic Bell-functional separation
over arbitrary shared two-qubit states. Its discussion contrasts that global
analytic treatment with the fixed-state and numerical arbitrary-state
components of the earlier V\'ertesi--Bene line: it describes the latter as
analytic for a fixed maximally entangled state but numerical for arbitrary
states, and says no earlier closed analytic bound covered arbitrary states,
degenerate binary observables, and every ternary-PVM rank pattern together.
This audit records the wording, the direct theorem overlap, and the public
dates; it draws no inference about misconduct, dependence, unknown private
development, or final priority. The public repository HEAD was also rechecked
on 11 August 2026 and remained the audited commit shown above.

## Exact ZCW scope

- Inputs: Alice has two binary and one ternary input; Bob has two binary
  inputs.
- Bell functional: `B = S + F/100`, where `S` is CHSH and `F` is a signed
  ternary-correlator probe.
- Explicit strategy: a maximally entangled two-qubit state, CHSH-optimal
  binary observables, and a rank-one ternary POVM with nonzero eigenvalues
  `3/4, 5/8, 5/8`.
- Attained value: `2 sqrt(2) + 1/100`.
- Fixed-qubit PVM ceiling:
  `2 sqrt(2) + sqrt(5)/250 + sqrt(2)/32400`.
- Exact certified gap: greater than `1/1000`.
- The fixed-qubit ceiling is a rigorous analytic upper bound, not a matching
  optimum.
- Their behavior lies outside the convex hull of fixed-qubit PVM behaviors,
  so shared randomness does not close their gap.
- Theorem 2 proves that `2 sqrt(2) + 1/100` is the exact value over arbitrary
  finite-dimensional tensor-product states and POVMs for their functional.
- The exact SOS uses 83 reduced words, an 83-by-83 Gram matrix over
  `Q(sqrt(2))`, and a finite-family Naimark step.
- The Lean project formalizes Theorem 1, including the explicit strategy,
  fixed-qubit PVM upper bound, convex-hull exclusion, and strict gap. It does
  not formalize Theorem 2 or the unrestricted SOS certificate.

## Direct overlap

Both works provide:

1. a rational 3×2 Bell functional;
2. an exact rank-one ternary qubit POVM;
3. an exact attained fixed-qubit POVM value;
4. an analytic upper bound covering arbitrary two-qubit states and every PVM
   support pattern;
5. strict separation from the shared-randomness convex hull of fixed-qubit
   PVM behaviors;
6. a CHSH anchor plus a weaker ternary probe; and
7. exact computational verification artifacts.

## Different constructions

The present functional is

`10 S + (3/5)p(0,0|2,0) + (3/5)p(1,1|2,0) + (4/5)p(2,0|2,1)`.

ZCW uses

`S + (1/100)[C_00 -(3/5)C_10 +(4/5)C_11 -(3/5)C_20 -(4/5)C_21]`.

The present simple ternary effects are

`(17I-8X+15Z)/50`, `(17I-8X-15Z)/50`, `(16I+16X)/50`.

ZCW’s effects are

`diag(3/4,0)`, `[[1/8,1/4],[1/4,1/2]]`, and
`[[1/8,-1/4],[-1/4,1/2]]`.

This establishes that the displayed data are different. It is not a claim of
inequivalence under every normalization identity, nonsignaling gauge,
relabeling, splitting, or coarse-graining.

## Present-work-only results

- Universal two-input convexified equality for arbitrary finite,
  input-dependent outputs.
- The common-mixture theorem when one party is binary on both inputs.
- Reduction of every residual separator to one binary PVM and one ternary
  rank-one POVM per party, excluding four-outcome extrema.
- The Lorentz-incidence, strict-multiplier, and rank-trichotomy closure proof.
- The conclusion that 3×2, up to party exchange, is the minimum input
  architecture.

## ZCW-only results

- Exact unrestricted finite-dimensional tensor-product optimum for its
  functional.
- Exact level-3 noncommutative SOS certificate.
- Lean 4 formalization of its fixed-qubit separation theorem.
- An exact interval of separating anchor–probe weights.

## Shared limitations and open directions

- Neither paper claims the exact fixed-qubit PVM optimum of its functional.
- The present paper does not claim the exact global POVM optimum either.
- The present equality is convexified; raw-set equality and same-state
  simulation remain open.
- ZCW’s unrestricted optimization does not itself say that a POVM is
  necessary when arbitrary local dimension is permitted.
- Uniqueness, self-testing, robust experimental certification, higher local
  dimensions, and multipartite minimum-setting laws remain open.

## Sources

- ZCW paper: <https://arxiv.org/abs/2608.01317>
- ZCW audited repository:
  <https://github.com/real-lin-zhu/Exact-Fixed-Dimension-Bell-Separation-between-Qubit-POVMs-and-PVMs/tree/c782e8bc2876d5a2c5f068fe8c9007aa1ce0718f>
- Present July 30 paper record: <https://doi.org/10.5281/zenodo.21699161>
- Present July 30 software record: <https://doi.org/10.5281/zenodo.21699224>

No inference about private development, dependence, misconduct, or final
mathematical priority is made.
