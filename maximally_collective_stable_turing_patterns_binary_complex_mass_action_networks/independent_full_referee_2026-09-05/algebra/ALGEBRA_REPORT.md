# Fresh adversarial algebra and topology referee report

**Target:** commit `6f68ad3e795c`, preserved in `../source_snapshot/`.

**Audit date:** 2026-09-06 UTC (2026-09-05 local).

**Scope:** main manuscript sections 1–5 in full; the reaction-derived algebra supporting homogeneous stability and contrast/asymptotic claims; supplement S1–S5, relevant S6 material, and the contrast proof in main section 7. The nonlinear PDE proofs and literature priority are assigned to other independent reviewers.

**Verdict:** I found no false theorem or missing substantive all-dimensional argument in this scope. The reaction family, complete positive-equilibrium realization space, topology-wide all-spectrum localization, principal-minor diffusion-ray theorem, exact stationary diffusion law, and contrast bounds survive independent reconstruction. Two low-priority proof-exposition statements should be corrected before submission. Both have simple local repairs, and neither changes a result or requires new mathematics.

No prior referee verdict or project audit decision was consulted. No manuscript, source snapshot, or existing project file was modified. All code and evidence described here reside in this `algebra/` folder. This is not a novelty/priority judgment or a blanket acceptance of the separately assigned nonlinear analysis.

## 1. Concrete findings

### ALG-P3-1 — Incorrect literal count of core cycle covers

**Location:** `manuscript/main.tex:485–486` in the preserved snapshot. The sentence says that the core block's “two surviving cycle covers” give its sparse determinant.

For the included boundary case `m=3, a=b=1`, the core matrix is

```text
[-2 -1 -1]
[-1 -1  2]
[ 1  2 -5]
```

Every permutation contributes a nonzero determinant term. In permutation order `(123),(132),(213),(231),(312),(321)`, the signed contributions are `-10, +8, +5, -2, +2, -1`, summing to `2`. Thus there are six nonzero cycle covers under the standard determinant/cycle-cover meaning. One can group and cancel polynomial terms, but the manuscript supplies no alternative grouping that would make “two surviving cycle covers” accurate as stated.

**Repair:** replace the count with a direct reference to the already correct Schur-complement elimination in supplement S2 (`supplement.tex:113–132`). For example: “Omitting Z leaves the complete X-chain block. The Schur-complement calculation in Supplement S2 gives (coreminor), hence (omitZ).”

**Severity:** minor proof exposition. The exact determinant formula is correct, and the supplement already contains its valid all-dimensional derivation. It would be an overstatement to classify this as a theorem failure or major revision.

### ALG-P3-2 — Wrong explicit ordering of the omission blocks

**Locations:** `manuscript/main.tex:488–490` and `manuscript/supplement.tex:188–190`.

Both passages place the retained feed-forward chain fragments *before* the boundary triad and then call that matrix block triangular. For a non-endpoint interior omission, one fragment feeds the triad and the triad feeds the other, so this stated ordering is not block triangular.

For `m=5, a=b=H=1`, omit `X3`. The claimed grouping can be written `(X2),(X4),(X1,X5,Z)`. In that order the matrix is

```text
[-1  0 -1  2  0]
[ 0 -1  0  0  0]
[ 0 -1 -2 -1  2]
[ 0  2  1 -5  2]
[ 0  0  2  2 -4]
```

The nonzero arrows are `X4 -> {X1,X5}` and `{X1,X5} -> X2`. Entries therefore occur on both sides of the displayed block diagonal. A correct block lower-triangular order is `(X4),(X1,X5,Z),(X2)`; reverse it for block upper triangularity.

**Repair:** say “Apply a Frobenius permutation to the chain fragments and the boundary triad,” or explicitly order the upstream fragment, triad, and downstream fragment. The singleton-factor and triad-determinant products are unchanged. A simultaneous row/column permutation does not change the determinant.

**Severity:** minor proof exposition. The existence of the needed Frobenius form follows from the same graph structure already proved. The literal ordering is inaccurate, but the determinant claim is fully supported after this local correction.

The exact matrices and all six cycle-cover contributions are saved in `exposition_counterexamples.json`.

## 2. Claims, hypotheses, and independent proof reconstruction

### 2.1 Reaction topology, conservation, rank, and flux cone

**Sources:** main `184–235`, `238–268`; supplement `39–71`.

The hypotheses are `m>=3`, strictly positive mass-action rates, and a strictly positive equilibrium. Both source and product molecularities are at most two. At `m=3`, the chain is empty; there are still `m+2` indexed reactions and `m+1` species.

I reconstructed source and target exponent vectors directly from the printed reactions, formed the polynomial vector field reaction by reaction, and differentiated it. No project matrix-construction function was imported.

For the conservation vector `c=(0,4,...,4,2,1)`, each reaction difference is orthogonal to c. Z balance equates the two reversible fluxes. Interior balances equate consecutive chain fluxes and return flux. The terminal balance then equates terminal and return fluxes; the X1 equation sets the feed flux equal to the terminal flux. Thus exactly two independent fluxes remain: `(a*1_m,b,b)`. Rank-nullity yields `rank Gamma=m`, and consequently `im Gamma=c^perp` and the left kernel is exactly the span of c. The independently computed maximal minor specified in supplement S1 is `4(-1)^m`.

The semipositive language is correct: c omits X1, and no positive conservation vector exists because the left kernel is one-dimensional. The paper expressly disclaims the global boundedness or mass-conservation consequences that a positive conservation law would provide.

At an arbitrary positive equilibrium, direct differentiation gives `J=Gamma diag(v) Y^T H`, with `H_ii=1/x_i*`. Conversely, every positive flux pair a,b and positive diagonal H is realized by rates `v_r/(x*)^{y_r}`. Hence `J=A_m(a,b)H` is the complete family, not a selected parameter slice. Exact arbitrary-H reconstruction was checked from the actual field `f(Hx)`, not merely from matrix multiplication.

**Boundary checks:** the empty chain at m=3, b=2a, and all positive column scalings are covered. Sending a, b, or a diagonal H entry to zero exits the strict hypotheses; no uniform stability margin is claimed at those excluded limits.

### 2.2 Exhaustive SCC classification and all-spectrum localization

**Sources:** main `276–377`; supplement `73–132`; `data/triad_routh_gap.tex`.

An independent structural proof makes the exhaustion particularly transparent. If a nontrivial SCC contains any interior species `Xi`, `2<=i<=m-1`, its incoming paths force all interior predecessors back to X2, and its outgoing paths force all interior successors through X(m-1). Only X1 or Xm can close this complete interior chain. Closing through X1 yields the block `X1,...,X(m-1)`; closing through Xm yields `X2,...,Xm`. Retaining both closure vertices, or a closure vertex together with Z, requires at least m vertices and is excluded by `|I|<m`. A nontrivial SCC without an interior species lies in `{X1,Xm,Z}`. Every remaining block is a negative singleton. This reasoning also handles m=3, where the interior chain consists of one vertex.

At b=2a the edge X1->Xm disappears. That edge belongs to neither long cycle. Removing it cannot generate a new SCC; possible boundary splitting is already within the triad-principal class.

For the first long cycle, its characteristic equation is the product of its damped diagonal factors minus `a^(m-1) product(h_i)`. On `Re lambda>=0`, the product modulus is at least `(a+b)a^(m-2) product(h_i)`, strictly larger than the cycle gain. For the second long cycle, the corresponding lower bound is `(4a+b)a^(m-2) product(h_i)`, versus gain `4a^(m-1) product(h_i)`. Thus neither cycle can have a closed-right-half-plane eigenvalue.

The triad's cubic coefficients match the printed formulas. Its coefficients and its three pairwise determinant/negative-trace conditions are positive for every positive a,b,h1,hm,hZ. I independently expanded `(c1*c2-c3)/a` and obtained exactly fourteen monomials, each with a positive coefficient. Therefore every triad principal block is Hurwitz by the standard quadratic/cubic criteria. SCC triangularization now proves all proper principal blocks below order m are Hurwitz for all positive parameters, not merely determinant-stable.

For the core determinant, the correct supplement elimination factors the lower-bidiagonal `X3,...,X(m-1)` block, with determinant `(-a)^(m-3)` and bottom-left inverse entry `-1/a`. Its Schur complement on `(X1,X2,Xm)` is the printed three-by-three core matrix, whose determinant is `2a^2b`. The m=3 case is exactly this three-by-three matrix with an empty eliminated block. Restoring positive column factors gives the claimed negative signed determinant `-2a^(m-1)b product(h_i)`. The core characteristic polynomial is negative at zero and positive for large positive lambda, so it has a positive real eigenvalue.

**Conclusion:** the maximum all-spectrum localization order m=n-1 follows exactly. I found no missed SCC or parameter-cancellation case.

### 2.3 General principal-minor diffusion-ray theorem

**Sources:** main `395–452`; supplement `135–174`.

The theorem assumes `det J=0`, positive signed principal minors through order `n-2`, and a positive *sum* of order-`n-1` signed minors. The sum condition is essential to the monotonic-characteristic argument; no assumption of exactly one negative omission minor is imposed in this general result.

Multilinearity gives

```text
p_D(s)=sum_I a_I product_(j notin I)(s d_j)
      =s[beta1+beta2 s+...+beta_n s^(n-1)].
```

Every beta_k for k>=2 is strictly positive. Thus the bracket is strictly increasing for s>=0, tends to infinity, and has a positive root exactly when beta1<0. That root is unique, and `p_D'(s*)=s* q_D'(s*)>0`.

For fixed s>0,

```text
chi_s(lambda)=sum_I a_I product_(j notin I)(lambda+s d_j).
```

Its derivative receives individually positive contributions from all lower-order minors; its entire order-(n-1) contribution is the assumed positive sum. Hence `chi_s'(lambda)>0` for lambda>=0. The determinant sign therefore gives exactly one positive real eigenvalue for `0<s<s*`, and none for s>=s*. At s=s*, `chi_s'(0)>0` makes zero algebraically simple. The implicit derivative of that zero branch is `-p_D'(s*)/chi_s*'(0)<0`, so it is a genuine transverse crossing as s increases.

The equality boundary beta1=0 has no positive s threshold: the bracket is strictly positive for s>0. The lower endpoint n=2 also works; the empty signed minor supplies beta2>0. I independently tested the n=2 matrix `[[1,-2],[1,-2]]`: for `D=diag(1,d)`, `p_D(s)=s(2-d+d s)`, giving crossing, equality, and no-crossing cases at d=3,2,1 respectively.

The proof makes no claim about nonreal unstable eigenvalues away from the threshold. The manuscript states this limitation prominently. Homogeneous stability is unnecessary in this abstract theorem beyond the stated coefficient condition, and is imposed separately for the network interpretation.

### 2.4 Omission minors and exact stationary diffusion criterion

**Sources:** main `461–565`; supplement `176–228`.

Deleting Z gives the negative core signed minor. Deleting an interior Xj leaves the triad and m-3 feed-forward singleton blocks after a correct Frobenius permutation; their signed determinant is `16a^(m-1)b` before column scaling. Deleting X1 leaves a nonzero restricted left conservation vector. Deleting Xm leaves the restriction of the right kernel vector `H^-1(2,-2,...,-2,0,1)`, whose omitted coordinate is zero. The two remaining minors vanish exactly.

All order-m minors therefore give

```text
beta1(D)=2a^(m-1)b product_(i<=m)(h_i)
         [8 h_Z sum_(j=2..m-1)(d_j/h_j)-d_Z].
```

Homogeneous stability means stability on the invariant space c^perp. In a basis adapted to c^perp, J has a stable invertible m-by-m block and one zero diagonal quotient block. Thus the conservation zero is algebraically simple and the coefficient of lambda in its characteristic polynomial is positive. Together with the smaller-block Hurwitz result, every hypothesis of the general theorem follows.

The exact stationary-ray criterion, uniqueness, algebraic simplicity, positive-real-eigenvalue band, and inverse scaling `s*(gamma D)=s*(D)/gamma` all follow without a hidden a,b restriction. The criterion is independent of a,b, while the threshold location need not be; the manuscript retains a,b in threshold notation.

I additionally checked the conservation boundary. At `h_Z=1/[8(m-2)]` and all other h=1, T(H)=1; rank J remains m while the lambda coefficient vanishes, so zero is not algebraically simple. At half that h_Z, T(H)<1 and the negative lambda coefficient forces a positive real homogeneous eigenvalue. These checks corroborate, rather than extend, the stated stable-domain requirement.

### 2.5 Contrast sharpness and asymptotic interpretation

**Sources:** main `574–612`, `832–903`, `1046–1061`; supplement `214–228`; `proof_audit/asymptotics.tex` and `heterogeneity_tradeoff.tex`.

On the homogeneously stable domain, the positive equal-damping coefficient is proportional to T(H)-1, so T(H)>1. A crossing gives `d_Z>d_min T(H)` and therefore `chi_D>T(H)`. Conversely, take all X diffusivities equal to 1 and `d_Z=T(H)+epsilon`. Since T(H)>1, the maximum and minimum diffusivities are indeed the ones used to compute the contrast. This proves the exact nonattained fixed-H infimum. At H=I it is `8(m-2)`.

Since `h_Z/h_j>=1/chi_H`, every stationary crossing obeys `chi_D chi_H>8(m-2)`. Sharpness over the stable realization domain is witnessed by the a=b=1,H=I realization plus the approaching diffusivity sequence. The paper does not infer a stable patterned branch from that approaching sequence; the nonlinear stable infimum remains separately open.

I independently verified a=b=1,H=I homogeneous stability to support this sharpness witness. The reaction-derived determinant satisfies the printed `(1+lambda)^(m-3)P-R` identity. The m=3 quotient is `(lambda+7)(lambda^2+5lambda+2)`. Independent symbolic expansion of `|1+lambda|^2|P|^2-|R|^2` in x=Re lambda and z=(Im lambda)^2 gives 35 positive-coefficient nonconstant terms, including strictly positive x and z terms. Its only zero in x,z>=0 is the origin. The modulus comparison therefore excludes every nonzero closed-right-half-plane root for all m>=4, and `q_m(0)=16m-34>0` establishes simplicity.

For the trade-off family, the explicit interior h_i decrease with i, their minimum is at least 1 on the certified L interval, and boundary h values are 1. Physical interior diffusivities are `1/(L K_(i-1))`; the minimum is at X2 and the maximum is the boundary value 23/63. Hence the exact contrast formulas, constant contrast product, and monotonicity in L are correct. The displayed endpoint ratio is greater than 1, so max(chi_D,chi_H) is uniquely minimized within the certified family at L0. Substituting L0 gives both contrasts of order sqrt(m).

The lower bound `max(chi_D,chi_H)>sqrt[8(m-2)]` follows directly from the product bound. Thus exponent 1/2 is optimal for this topology's stationary-crossing class once the separately audited stable family is established. The paper correctly avoids constant-optimality and a global Pareto-frontier claim.

## 3. Independent computational evidence

The primary script `independent_algebra_check.py` imports only the Python standard library and SymPy. Reaction exponents are transcribed from the printed reactions; the field is assembled and differentiated. SCCs are computed by all-pairs reachability rather than the project's Tarjan implementation. Hurwitz matrices use a transposed indexing convention relative to the project implementation. No project code or certificate data is imported.

Run command:

```text
/Users/alec/Documents/Math/.venv/bin/python independent_algebra_check.py
```

**Outcome:** PASS, exit code 0, 12.46 seconds, SymPy 1.14.0. Complete output: `independent_run.log`; structured results: `independent_results.json`.

- 49 generic-a,b symbolic omission identities for m=3,...,9.
- Exact rank, flux kernel, conservation, displayed Jacobian, and right-kernel identities in those dimensions.
- Direct arbitrary-positive-H equilibrium and Jacobian reconstruction for m=3,...,6.
- 263,945 SCC classifications over every principal set of order below m for m=3,...,12 and b/a=1,2,3. This explicitly crosses and includes the b=2a cancellation surface.
- 422 exact Hurwitz checks of distinct SCC matrices and 630 direct exact Hurwitz checks of entire principal subsystems.
- Independent triad Routh certificate and all pairwise trace/determinant signs.
- Reaction-derived homogeneous characteristic identities for m=3,...,13, plus independent verification of the all-dimensional 35-term modulus certificate and equality set.
- 31 tested dimensions through m=1000 for unit contrast and both endpoints plus midpoint of the trade-off family: 93 exact physical/equilibrium/product comparisons.
- Exact n=2 abstract crossing/equality/no-crossing examples; network diffusion coefficient expansion and strict/equality boundaries for m=3,...,6 at unit and nonunit rational H.

Additional run:

```text
/Users/alec/Documents/Math/.venv/bin/python boundary_stress_check.py
```

**Outcome:** PASS, exit code 0, approximately 0.92 seconds. Complete output: `boundary_stress_run.log`; structured results: `boundary_stress_results.json`.

This performs 759 additional exact Hurwitz checks under flux rates with a ratio up to 10^16 and H entries ranging as far as 10^-22 to 10^19. It includes b=2a. It also verifies the T(H)=1 and T(H)<1 conservation-boundary behavior for m=3,...,8. All arithmetic is rational/exact; no floating eigenvalue tolerance supports these conclusions.

These finite tests are regression and counterexample-search evidence. The infinite-dimensional quantifiers in m and continuous positive parameters are supported by the explicit structural, modulus, Schur, and coefficient arguments reconstructed above, not by finite testing alone.

## 4. Existing verifier review and limits

I read the load-bearing implementations before treating their architecture as evidence: `independent_verifier/stable_core.py`, the reaction/matrix/Hessian sections of `common.py` and `core.py`, and the complete relevant bodies of `verify_family.py`, `verify_all_spectrum.py`, `verify_principal_minor_diffusion_ray.py`, `verify_network_one_bad_minor.py`, `verify_order_m_minors.py`, `verify_diffusion_criterion.py`, and `verify_contrast_bounds.py`.

Their reconstruction and coefficient/Hurwitz logic are consistent with the manuscript. Their finite regressions are accurately labeled as such. The assertion-rejection preambles prevent an optimized Python run from silently dropping the displayed checks. I did not substitute their successful outputs for fresh reconstruction, and did not need to rerun the project's full validation suite, which is assigned to the software reviewer.

The exact full homogeneous stable region S_m is not classified, and I have not assumed T(H)>1 is sufficient. The diffusion-ray theorem does not eliminate wave instability for arbitrary profiles. The nonlinear coefficient and PDE-stability claims require the separate PDE review; literature priority and submission-package integrity require the other assigned reviews.

## 5. Completion and strongest verified conclusion

At this checkpoint the assigned algebra/topology audit is complete. Its strongest verified conclusion is that the main all-dimensional algebraic theorem chain is valid under its printed strict hypotheses. The exact remaining changes in this scope are the two small proof-exposition repairs in section 1. Neither correction changes any topology, equilibrium, threshold, contrast, or theorem conclusion.
