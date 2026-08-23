# Independently reconstructed theorem-dependency map

This map was reconstructed from the manuscript and supplement themselves. The packet's `review_maps/` files were not used to establish any dependency or conclusion.

## Base construction

| Node | Exact domain and conclusion | Direct dependencies | Evidentiary type | Source |
|---|---|---|---|---|
| Binary-complex topology | Integer `m >= 3`; species `X_1,...,X_m,Z`; the chain range is empty at `m=3`; every source and product complex has molecularity at most two | Indexed reaction list | Deductive inspection | `main.tex` 145-179; `supplement.tex` 31-37 |
| Proposition 2.1 | `m >= 3`; rank `Gamma_m=m`, image `c^perp`, two-dimensional kernel, positive flux cone `(a 1_m,b,b)`, semipositive conservation covector | Balance equations and one maximal minor | Deductive finite-pattern argument uniform in `m` | `main.tex` 191-220; `supplement.tex` 39-63 |
| Proposition 2.2 | Every positive-equilibrium Jacobian, and only those Jacobians, equals `A_m(a,b)H`, with `a,b>0` and positive diagonal `H` | Proposition 2.1; mass-action Jacobian factorization; explicit rate reconstruction | Deductive algebraic realization | `main.tex` 157-166, 222-253 |

## Topology-wide localization

| Node | Exact domain and conclusion | Direct dependencies | Evidentiary type | Source |
|---|---|---|---|---|
| Lemma 3.1 | `m >= 3`, any principal species set with `0<|I|<m`; exhaustive SCC list, including direct `m=3` handling and deletion of `X_1 -> X_m` when `b=2a` | Explicit Jacobian graph | Deductive graph classification | `main.tex` 260-307; `supplement.tex` 65-101 |
| Boundary-triad Hurwitz lemma embedded in proof | All `a,b,h_1,h_m,h_Z>0`; every nonempty triad principal block Hurwitz | Cubic Routh-Hurwitz; positive 14-monomial expansion; direct order-one/two checks | Exact symbolic identity plus standard cubic criterion | `main.tex` 339-350; `supplement.tex` 97-101 |
| Long-cycle Hurwitz lemmas embedded in proof | All positive parameters and diagonal scaling | Strict closed-right-half-plane product-modulus inequalities | Deductive complex inequality | `main.tex` 326-338 |
| Theorem 3.2 | `m>=3`, all positive `a,b,H`; every nonempty principal block below order `m=n-1` is Hurwitz, while `C_m={X_1,...,X_m}` has a positive real eigenvalue; minimal unstable principal order is exactly `m` | Lemma 3.1; long-cycle and triad Hurwitz results; exact signed core determinant | Deductive graph reduction and exact determinant sign | `main.tex` 309-359 |
| Corollary 3.3 | Endpoint `n-1` is attained inside binary-complex classical mass action for all `n>=4`; a selected realization also supports stable patterns | Theorem 3.2 and Theorem 6.1 | Deductive corollary plus citation-dependent contextual comparison | `main.tex` 361-372 |

## General diffusion ray and topology-specific stationary law

| Node | Exact domain and conclusion | Direct dependencies | Evidentiary type | Source |
|---|---|---|---|---|
| Theorem 4.1 | `n>=2`, real square `J`, `det J=0`, every signed principal minor through order `n-2` positive, and the *sum* of signed order-`n-1` minors positive; for every positive diagonal `D`, a nonzero ray threshold exists iff `beta_1(D)<0`, is unique, and gives exactly one positive-real-eigenvalue band `0<s<s_*`; the critical zero is algebraically simple; nonreal instability beyond the band is not excluded | Principal-minor expansion; coefficient positivity; strict monotonicity in `s` and in real spectral parameter `lambda` | Deductive algebra | `main.tex` 376-424; `supplement.tex` 110-149 |
| Proposition 5.1 | `m>=3`, all positive `a,b,H`; complete order-`m=n-1` omission-minor table: one negative (`omit Z`), two zeros (`omit X_1,X_m`), positive interior omissions | Sparse cycle covers, block triangularization, restricted left/right nullvectors | Exact determinant algebra | `main.tex` 442-489; `supplement.tex` 151-187 |
| Stable realization domain | `S_m` contains exactly positive realizations whose restriction to `c^perp` is Hurwitz; no complete characterization is claimed | Definition | Definition/scope | `main.tex` 491-498 |
| Theorem 5.2 | `(a,b,H) in S_m`, positive diagonal `D`; stationary crossing on `sD` iff `d_Z > 8 h_Z sum_{j=2}^{m-1} d_j/h_j`; unique simple threshold and exact positive-real band; no arbitrary-wave classification | Theorem 3.2 lower-order minors; homogeneous simple zero and positive order-`m` coefficient; Theorem 4.1; Proposition 5.1 | Deductive exact stationary spectral law | `main.tex` 500-553 |
| Theorem 5.3 | Fixed `(a,b,H) in S_m`; nonattained diffusion-contrast infimum `T(H)`; unit value `8(m-2)`; every stationary crossing obeys strict `chi_D chi_H>8(m-2)`; sharp only as an infimum over this topology's homogeneously stable stationary-crossing realizations | Theorem 5.2; `T(H)>1` from equal-damping coefficient; elementary extrema inequalities; existence of unit stable realization | Deductive optimization; later existence input from Theorem 6.1 | `main.tex` 555-593 |

## Unit-equilibrium nonlinear pattern theorem

| Node | Exact domain and conclusion | Direct dependencies | Evidentiary type | Source |
|---|---|---|---|---|
| Homogeneous spectral certificate | `m=3` direct factorization; `m>=4` all complementary homogeneous roots strictly left | Determinant identity; 35-term modulus polynomial with equality only at `lambda=0`; simple conservation zero | Exact symbolic identity and closed-half-plane inequality | `main.tex` 657-671; `supplement.tex` 238-258, 845-855 |
| All-spatial-mode certificate | `m>=3`, damping `t>=1`; at `t=1` exactly one simple zero; otherwise closed-right-half-plane roots excluded | Sparse determinant identity; product lower bound; 77-term modulus certificate; derivative identity | Exact symbolic certificate; all-dimensional telescoping/product argument | `main.tex` 673-704; `supplement.tex` 259-289, 795-814 |
| Critical vectors and transversality | `m>=3`; exact right `r`, left `ell`, `ell^T r<0`, `ell^T D r<0`, so parameter derivative `eta_m>0` | Direct kernel identities and harmonic-sum bound | Exact rational algebra uniform in `m` | `main.tex` 597-617, 688-713; `supplement.tex` 205-236 |
| Stable-mode corrections | Unique `w_0` solving the homogeneous equation under gauge `c^T w_0=0`; unique `w_2` because `A-4D` is invertible | Reaction-derived quadratic tensor; conservation; simple homogeneous kernel; higher-mode certificate | Deductive Fredholm/gauge argument plus exact rational recurrences | `main.tex` 715-726; `supplement.tex` 291-383 |
| Cubic sign | `m>=3`; adjoint-coordinate cubic numerator positive and denominator negative, hence `c_m<0` | Exact Fourier contractions; rational decomposition `R_m+C_m \mathfrak h_m`, where `\mathfrak h_m` is the harmonic sum; shifted-positive denominators and clearing polynomial; harmonic-sum inequality | Exact symbolic identities plus all-dimensional coefficient sign proofs | `main.tex` 724-729; `supplement.tex` 385-465 |
| Theorem 6.1 | For every fixed `m>=3` on `(0,pi)` with Neumann conditions and the displayed rational design: primary simple transverse first-mode stationary bifurcation, negative cubic coefficient, and two nearby componentwise-positive locally exponentially stable branches for sufficiently small `mu>0` within the fixed-integrated-mass `H^1` class | All four nodes above; fixed-mass Fredholm formulation; reflection oddness; center-manifold reduction; Crandall-Rabinowitz; analytic perturbation/exchange of stability; Henry linearized stability | Exact algebra plus standard cited infinite-dimensional bifurcation/semigroup results | `main.tex` 624-772; `supplement.tex` 385-400, 930-953 |
| Stable contrast bounds | `8(m-2) <= chi_stable(m) <= 23(91m-183)/63`; the exact nonlinear infimum remains open | Theorems 5.3 and 6.1 | Deductive bounds | `main.tex` 618-655, 1020-1026 |

## Equilibrium-scaled stable family

| Node | Exact domain and conclusion | Direct dependencies | Evidentiary type | Source |
|---|---|---|---|---|
| Admissible interval | `nu=m-2>=1`; closed interval `[L_0(nu),L_1(nu)]`; exceptional `nu=1` lower endpoint `1/sqrt(3)`, otherwise `sqrt(5)/(2sqrt(nu))`; endpoints are certificate boundaries, not claimed dynamically sharp | Direct inequalities | Deductive algebra | `main.tex` 776-802; `supplement.tex` 467-498 |
| Homogeneous scaled certificate | `nu=1` by cubic Routh-Hurwitz; `nu>=2` by 22-term modulus certificate on the full closed interval; simple conservation zero | Physical-to-normalized row scaling; product lower bound; equality case at `lambda=0`; derivative identity | Exact symbolic certificate plus standard cubic criterion | `main.tex` 878-921; `supplement.tex` 542-590, 830-843 |
| Scaled spatial certificate | Every `t>=1`, all `m>=3`, full closed interval; only critical equality is `(lambda,t)=(0,1)` | Row-scaled determinant; chain product inequality; 84-term modulus certificate; inherited unit kernel and separate algebraic-simplicity pairing | Exact symbolic certificate and inequalities | `main.tex` 850-876, 953-975; `supplement.tex` 499-540 |
| Scaled gauge and cubic sign | Same domain; transformed left vector, physical mass covector, gauge shift, `N_m(L)>1/200`, denominator negative, hence `c_m(L)<0` | Unit corrections/signs; exact `tau` and `S_m`; monotonicity and endpoint bounds | Exact rational inequalities uniform in `m,L` | `main.tex` 923-989; `supplement.tex` 592-742 |
| Theorem 7.1 | Every fixed `m>=3` and every `L` in the closed certified interval: primary simple transverse first-mode bifurcation and two nearby positive locally exponentially stable fixed-mass `H^1` patterns; exact contrast formulas/product; within-family minimizer at `L_0`; both contrasts `Theta(sqrt m)` there; exponent `1/2` optimal only for this topology's stationary-crossing realizations | Three scaled certificate nodes; Theorem 6.1 local functional-analytic mechanism; Theorem 5.3 product lower bound | Exact algebra plus cited local PDE theory | `main.tex` 804-1006; `supplement.tex` 744-777 |

## Auxiliary scope results

| Node | Exact domain and conclusion | Direct dependencies | Evidentiary type | Source |
|---|---|---|---|---|
| Near-threshold example | One affine path at `m=3`, `0<epsilon<=10^-3`; cubic coefficient positive; this is a boundary example, not a universal gap | Exact elimination and rational remainder bounds | Exact finite-dimensional rational calculation | `main.tex` 1027-1035; `supplement.tex` 875-928 |
| Proposition 8.1 | Fixed `m` and certified `L`; sufficiently small perturbations *within* the positive-equilibrium realization manifold, diffusion ratios, and interval length admit a unique nearby retuned scalar diffusion multiplier preserving the local supercritical/stable conclusion; no uniform radius | Simple-eigenvalue continuation, IFT, low/high mode gap control, smooth normal-form dependence | Deductive local perturbation argument conditional on standard analytic perturbation/semilinear results | `main.tex` 1053-1073; `supplement.tex` 942-953 |
| Numerical illustrations | `m=3,5,8`; simulations illustrate already-proved branches and are not used for an all-dimensional or theorem claim | Galerkin solver and refinement data | Floating-point numerical provenance only | `main.tex` 1088-1104; `supplement.tex` 955-969 |

## Dependency spine

`reaction list -> flux cone/rank/conservation -> complete Jacobian family -> SCC exhaustion + block Hurwitz -> maximal localization -> lower-order signed minors`

`principal-minor expansion + coefficient hypotheses -> general diffusion-ray theorem`

`omission table + homogeneous relative stability + general diffusion-ray theorem -> exact stationary law -> fixed-H and product contrast bounds`

`unit determinant identities + modulus certificates + exact kernels/corrections/cubic sign + fixed-mass PDE theory -> unit stable pattern theorem`

`row/concentration scaling + scaled modulus/gauge/cubic certificates + same local PDE theory -> scaled stable family -> square-root within-family design; stationary product lower bound -> topology-specific exponent optimality`
