# Hostile proof audit

Date: 2026-08-08 (America/Los_Angeles)

Scope: replacement manuscript `main.tex` and the theorem packages it invokes.
No numerical fixation value is used as proof.

## Audit table

| Obligation | Hostile check | Status |
|---|---|---|
| graph independent of fitness | `C_t,q_t,m_t,sigma_*` depend only on `t` and the algebraic phase root; `e_t` is selected uniformly over `I_t` before fitness is quantified | PASSED |
| connected, loopless, undirected | every pair vertex has positive weak edges to every clique vertex; all displayed edges are symmetric and no loops are present | PASSED |
| exact strong lumping | the group acts transitively on every `(h,i,u,v,l)` fibre and both kernels commute with it; an independent labelled implementation checks all 512 states and 108 fibres on the audit instance | PASSED |
| weak-cut limit | fixed finite `C,m,q` is taken before population limits; the fast block is invertible and the Schur complement gives introduction rate times exact local fixation | PASSED |
| uniformly initialized trace | center and pair singleton masses in equation (9) sum to one; hub, ordinary core, leaf, and the two vertices of each pair are all included | PASSED |
| core estimate at the correct scale | `K=A log C`, first-hub charging, product odds, and post-`K` cleanup give `o(q/C)`, not merely `o(1)` | PASSED |
| post-establishment fixation | positive core drift reaches a density strip; resident-deficit comparison and repeated hub blocks complete leaf cleanup with polynomially small chosen failure | PASSED |
| Bd leaf contribution | mark probability per hub excursion is `Theta(1/m)` while loss between excursions is `O(1/C)`; after its initialization mass the error is `o(q/C)` | PASSED |
| dB leaf contribution | death has unit rate and hub activation `O(1/C)`, so the singleton value is `O(1/C)` | PASSED |
| reciprocal invasion | reversed core drift is subcritical and reaching positive density is exponentially small; multiplication by `q` remains negligible | PASSED |
| pair-gate orientation | all four Bd and dB rates were rederived from labelled introduction events; the resulting odds are `sigma(r^2-1)` and `2r(r-1)/sigma` | PASSED |
| post-gate sweep | the exact two-coordinate macro chain retains reversals; `qC'/B -> 0` and the exponentially small reciprocal invasion control all pairs | PASSED |
| complete baseline scale | Bd differs from `p` exponentially and dB by `O(1/C)`; both are `o(q/C)` for `C=t^4,q=t` | PASSED |
| combined coefficients | independent symbolic simplification reproduces `B,D` and the exact rational endpoint margins | PASSED |
| positive coupling diagonal | finite continuity gives a least dyadic exponent with scaled error at most `1/t` uniformly on `I_t`; exact real-algebraic interval decisions make the definition effective | PASSED |
| order of quantifiers | every fixed `1<r<R_hyb` lies in `I_t` eventually, after the graph sequence has already been fixed | PASSED |
| sextic threshold | exact Sturm isolation, quadratic completion, tangency, and derivative signs are independently replayed | PASSED |
| class-optimal wording | the claim is explicitly restricted to the displayed two-mechanism leading regime; no global upper bound is inferred | PASSED |
| affine refutation | exact `K_2-K_20` witness forces `theta>1/3`; clique-pendant sharpness forces `theta<=1/3` | PASSED |
| global conclusion | manuscript states only `R_sim>=R_hyb` and leaves the unrestricted exact value open | PASSED |

## Independent paths

1. `threshold/endpoint_construction_v2` supplies the explicit `C=q^4`
   logarithmic-cutoff proof, labelled orbit verifier, and coefficient
   certificate.
2. `threshold/dilute_pair_leaf_hybrid` supplies an independent iterated
   fixed-density-then-dilute least-integer diagonal, exact optimization, and
   replay integration.
3. `threshold/endpoint_affine_global_v2` supplies two independent exact
   endpoint solves with matching rational hashes.

## Remaining open problem

No universal upper bound matching `R_hyb` is proved. The exact unrestricted
value of `R_sim` remains open. This is a mathematical open problem, not a
gap in the stated lower-bound theorem.
