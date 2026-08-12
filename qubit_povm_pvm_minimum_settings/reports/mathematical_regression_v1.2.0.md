# Mathematical regression check — version 1.2.0 final hardening

**Pre-hardening checkpoint:**
`49215a87df29b094b05f14f98ad9cc3590878d0a`

**Public comparison tag:** `qubit-povm-pvm-minimum-settings-v1.1.0` at
`773356a1de85290c3e85a361e0019f5f82b8e6d9`

**Checked:** 12 August 2026

## Result

**PASS — no pre-existing theorem hypothesis, proof mechanism, Bell
functional, exact witness, certified bound, or conclusion changed.**

The source still contains 21 Main Theorem/theorem/lemma/proposition/corollary
blocks. After the requested notation renaming, 19 of those 21 blocks normalize
identically to the pre-hardening checkpoint. The only two changed result
blocks are:

1. `thm:physical-completeness`, which now names Definition 5.2 explicitly and
   displays POVM normalization and steering recovery already required by its
   existing reconstruction; and
2. `prop:smooth`, which now quantifies over the newly numbered “genuine
   residual incidence point” definition rather than the former unnumbered
   paragraph.

Neither alteration changes the quantified physical stratum or the conclusion.

## Equation-level comparison

An automated extraction found 132 displayed main-text math blocks before the
hardening revision and 134 afterward. After reversing only the approved
notation substitutions, every pre-existing display matches in sequence. The
two new displays are the explicit identities

\[
\sum_{j\in B_y}N_j^T
=\Xi^{-1}\!\left(\sum_{j\in B_y}S_j\right)\Xi^{-\dagger}
=\Xi^{-1}\rho_A\Xi^{-\dagger}=\mathbb I
\]

and

\[
\Theta_\Xi(N_j)=\Xi N_j^T\Xi^\dagger=S_j.
\]

One rank-one display now prefixes the existing identity
`ker D^T={mu:mu_j0=0}` with its defined symbol `mathcal K`; its mathematical
content is unchanged. Appendix A contains 74 displayed math blocks both before
and after the revision, and all 74 normalize identically after reversing the
approved variable renames.

## Approved notation substitutions

- `(x,y)=(n_z,m_z)` → `(xi,zeta)`;
- Bloch overlap `u` → `nu`;
- Schmidt matrix `D` → `D_eta`;
- compression map `Phi_B` → `mathcal C_B`;
- second-form matrix `S` → `Sigma`;
- metric kernel `K` → `mathcal K`; and
- compatible space `H_K` → `H_mathcalK`.

The same local-name substitutions were applied to the separation verifier and
machine-readable closure-formula descriptions. Exact coefficient and strategy
files were not altered.

## Numerical and symbolic regression

The final release run passes, and the frozen verifier report records:

- both coefficient encodings;
- both explicit POVM strategies and exact values;
- the global PVM-bound identities and strict exact gaps;
- all 39 closure checks; and
- the exact rank-zero simulator.

The executable checks remain a finite certificate/regression layer. They do
not formally verify the manuscript's universal convexity, extremality,
physical-reconstruction, multiplier, or rank-exhaustion arguments.

## Contextual additions

The numbered independent-existence remark remains non-load-bearing. Added
Bell/CHSH/fixed-dimension citations, the residual-definition split, and the
local-exactness motivation do not enter the theorem dependency graph. The
scope limitations on raw sets, same-state simulation, operator-level
simulation, global optima, unrestricted dimension, self-testing, and private
randomness remain unchanged.
