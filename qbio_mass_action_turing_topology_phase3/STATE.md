# Phase III state

**Execution date:** 2026-08-13  
**Frozen inputs:** the historical STOP archive and candidate T-ALG archive are copied under `frozen_inputs/`; their SHA-256 values still equal the inherited values.  
**Current outcome:** **VALIDATED-TALG**.

## Proved and independently reconstructed

1. The fixed-matrix positive diagonal-damping theorem, including the conservative and designated-mobile variants used here.
2. The positive-equilibrium mass-action parametrization and principal-minor scaling identity.
3. The exact semialgebraic iff characterization of weak all-mobile stationary diffusion-driven instability.
4. Polynomial-size membership in the existential theory of the reals.
5. The open-cube `PARTITION` family, row-splitting similarity, elimination of arbitrary positive right scalings, exact mass-action row realization, and polynomial many-one reduction.
6. Polynomial-time exact decision for every fixed species count, with explicit bit-complexity reasoning.
7. Finite exact algebraic YES certificates and Real-Nullstellensatz NO certificates, without a polynomial size or practical generation claim.
8. The Level-5 data boundary among the six representations considered.

## Independent evidence

- Definition-level Python implementation does not import inherited code.
- Exact bounded enumeration and random rational falsification were performed for every central algebraic identity.
- The reduction was compared with exhaustive `PARTITION` enumeration on 917 small instances and attacked numerically on exact NO instances.
- Circuit enumeration was implemented twice and agreed on 1,159 cases; 3,644 exact cone decompositions were replayed.
- The inherited package was replayed only as a separate regression gate, not as proof.

## Preserved failed or narrower statements

- The determinant-at-zero designated-mobile criterion is false; the exact rational counterexample is retained.
- Restricting a nonzero-mode matrix to the stoichiometric subspace is generally invalid under unequal diagonal diffusion.
- No finite motif characterization, primary-crossing theorem, wave-instability classification, nonlinear pattern theorem, strong NP-hardness, bounded-molecularity hardness, or existential-real hardness is claimed.

## Priority status

A dated search across arXiv, publisher pages, Crossref-indexed records, Semantic Scholar results, Google Scholar-style searches, and accessible citation trails found no prior theorem with the same combination of classical mass-action input, existential rates/equilibrium/diffusion, weak stationary scope, NP-hardness, fixed-species algorithms, and exact two-sided certificate theorem. Database access was incomplete for MathSciNet and direct zbMATH full records. Priority is therefore **good-faith checked, not guaranteed**; three specialist inquiry drafts are prepared but were not sent.

## Remaining risks

- The result has not received external human peer review.
- The reduction uses complexes of unbounded molecularity and establishes only weak NP-hardness.
- The release does not bundle a complete general quantifier-elimination or Nullstellensatz-certificate generator.
- Publication priority can still be affected by terminology differences or inaccessible/unindexed work.
