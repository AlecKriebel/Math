# Independent analytic audit of family 370

Audit timestamp: 2026-10-07 04:28 UTC (2026-10-06 21:28 PDT).
Auditor: independent upstream-analysis agent, with a separately assigned
interval-inequality falsification agent. No external individuals were
contacted. The upstream checkout was not modified.

## Exact audited target and verdict

The dependency needed by the follow-on project is this bounded-entire
statement:

> For integers `n >= 3` and real `p,q > 1` satisfying
> `1/(p+1)+1/(q+1) > (n-2)/n`, a bounded, nonnegative pair
> `(u,v) in C^2(R^n)^2` satisfying `-Delta u=v^p`, `-Delta v=u^q`
> is identically zero.

I read the complete source proof, including its weighted preliminary,
localization, interval, pressure, and closing sections, and independently
reconstructed the crucial pressure estimate in the unweighted specialization.
I found **no substantive mathematical defect** in that specialization.
The proof actually establishes the stronger positive classical entire
nonexistence conclusion without boundedness. The nonnegative bounded
form above follows by the strong maximum principle, as checked below.
This verdict is an analytic audit, not a claim of complete formal verification
or conventional human peer review. The weighted theorem and companion radial
classification are beyond the exact target certified by this audit.

The interval agent's report and reproducible numerical checks are separate
artifacts. Numerical checks can falsify the lemma but do not replace its
elementary proof. No numerical or empirical premise is used in the theorem.

## Input identity

Sources are the copied family 370 files under `sources/family370/build`.
SHA-256 identities of the actually audited sections:

| File | SHA-256 |
|---|---|
| `02-preliminaries.tex` | `9a510ee55bd758d481b57cd3e2160a4bdff7f7059d6a9bd4ed32d4584f69767b` |
| `03-localization.tex` | `a27394bbcb068cf24301f75840ec4eadb5b02ec87bf3c1edea79cb88902c41b0` |
| `04-intervals.tex` | `dc02167e2d6e2388d1c69e0c37817f8eb9468047a6c9ca02df145d8b2e012ef2` |
| `05-pressure.tex` | `5a35f793eef0c4d21029b4d0f0b0c860f2ea1b33f4b4a569ed38182467079f79` |
| `06-conclusion.tex` | `99c8d2df276b477178d163949c85a1fbc16fda4ab7dcdc9afecf62ef883fedb3` |

## Independent proof reconstruction in the needed specialization

Write `f=u^q`, `g=v^p`, `K(x)=|x|^(2-n)/((n-2)|S^(n-1)|)`,
`a=1/(q+1)`, `b=1/(p+1)`,
`alpha=2(p+1)/(pq-1)`, and `beta=2(q+1)/(pq-1)`.

### 1. Source masses and exact potentials precede the energy estimate

Positivity and the Newton comparison imply
`u(x) >= c R^(2-n) int_(B_R) g` and
`v(x) >= c R^(2-n) int_(B_R) f` for `x in B_R`.
Consequently, at radius one,
`M_f >= c M_g^q`, `M_g >= c M_f^p`.
Since `pq>1`, their combination gives universal upper bounds on both
source masses. Scaling, with the **correct source assignment**
`f_R=R^(beta+2) f(Rx)` and `g_R=R^(alpha+2) g(Rx)`, gives

`int_(B_R) f <= C R^(n-2-beta)`,
`int_(B_R) g <= C R^(n-2-alpha)`.

The potential representations `u=c_u+K*g`, `v=c_v+K*f` follow from
the positive entire superharmonic comparison and the fact that a
nonnegative entire harmonic function is constant. A positive `c_u`
would force `int_(B_R) f >= c R^n`, contradicting the source estimate;
similarly `c_v=0`. Thus `u=K*g` and `v=K*f` pointwise.

The dyadic source tails are summable because `alpha,beta>0`.
Fubini and local integrability of `K` then give the universal bounds
`int_(B_4)(f+g+u+v)<=C` and
`int_(|x-y|>=ell) K(x-y)(f(y)+g(y))dy <= C ell^(2-n)`
for `x in B_2`, `0<ell<=1`.
None of these statements assumes a bound on `int fu` or `int gv`.
This order is essential to rule out circularity.

### 2. The compactly supported virial identity has the required sign

Set `d=min(1,(2-|x|)_+)`, `m=n+3`, `k=n(m+1)`, `N=k+n+2`,
and use the source cutoff `eta`, `w=-x.grad eta >= 0`, `X=x eta`.
The exact identity is

`an E_f + bn E_g - a W_f - b W_g = (n-2) int Phi d pi`,

where `d pi=f(x)g(y)K(x-y)dxdy`,
`E_f=int eta fu`, `E_g=int eta gv`,
`Phi=((X(x)-X(y)).(x-y))/|x-y|^2`.
The signs follow directly by writing
`-int f X.grad u = a int u^(q+1) div X`.
There is no boundary term at infinity because `X` is compactly
supported. In the unweighted case there is no singular-origin issue.
Kernel-gradient integrals converge absolutely on compact supports;
the tails are dominated by the already finite potentials.

### 3. Localization errors are energy-relative, without an energy bound

Define close pairs by `|x-y|<=delta d(z)^m` at either endpoint.
On such pairs, `d` is comparable along the whole segment. Taylor
expansion of `X` gives
`Phi = eta(x)-w(x) D_(omega_x)(x,y) + O(delta d(z)^N)`.
The two cutoff marginals also differ by `O(delta d(z)^N)`.
Their integrals are bounded by `C delta (E_f+E_g)` because
`d^N<=eta` and the interaction marginals are exactly `fu`, `gv`.

On far pairs the truncated-potential bound and the source masses
give additive constants. The required powers are strictly positive:

* `N-1-m(n-2)=4n+7`;
* `N-m(n-1)=3n+5`;
* `N-n-m(n-2)=3n+8`.

Thus for every `epsilon>0`,
`|E_f-E_g|+|Q|<=epsilon E+C_epsilon`,
where `E=E_f+E_g` and
`Q=int(Phi-eta(x)+w(x)D_(omega_x))d pi`.

### 4. The central interval pressure estimate is non-circular

For fixed direction `e`, use the cap weight
`h_e(x)=w(x) psi(|e-omega_x|/(kappa d(x)))/Z(kappa d(x))`.
The normalization is **exactly** `E_e h_e(x)=w(x)`.
Moreover `h_e<=C_kappa d^(N-n)` and
`|grad h_e|<=C_kappa d^(N-n-1)`.
Taylor comparison and far-source control give

`int|h_e(x)-h_e(y)|d pi <= C_kappa delta E+C_(kappa,delta)`.

The cap direction differs from the radial direction by at most
`kappa d(x)`. Since `d w<=C eta`, angular replacement costs at
most `C kappa E`, with `C` independent of `kappa,delta`.

On the line through `x`, consider the component `I` of `{f>t}`.
Assign `chi_I=inf_I h_e` only if it is bounded and
`|I|<=2 delta inf_I d`; otherwise assign zero.
For `|I|<=ell=delta d(x)^m`, the retained-weight loss is
`<=C_kappa delta d(x)^N`.
If `|I|>ell`, one forward or backward segment of length `ell/2`
lies in the layer. Polar integration therefore gives

`P_e(|I|>ell) <= C/(t ell^n) int_(B_ell(x)) f <= C/(t ell^n)`.

This uses the **source** mass on a fixed ball, not the unknown energy.
At high levels `t>=P d(x)^(-k)`, multiplication by `sup_e h_e(x)`
gives expected loss

`<=C_(kappa,delta) P^(-1) d(x)^N`,

because `k=n(m+1)` exactly cancels the negative powers.
Integration over these levels and against `u(x)` is at most
`C_(kappa,delta)P^(-1)E_f`.
At low levels use the exact cap normalization instead:

`int_0^min(f,Pd^(-k)) E_e(h_e-chi_I)dt <= P d^(-k)w <= CP`,

since `N-1-k=n+1`. The already established `int_(B_4)u<=C`
turns this into the additive term `CP`. The same calculation applies
to `g,v`. Hence the layer loss is

`E_e(L_f+L_g) <= (C_kappa delta+C_(kappa,delta)/P)E+CP`.

This is the pivotal mechanism. Sending `P` large does not change its
relative-coefficient constant; it only enlarges the additive constant.

### 5. Endpoint recovery and integration have no hidden infinity subtraction

For positive `chi_I`, both endpoints lie in the annulus where `h_e>0`.
Continuity and maximality imply `f(x_-)=f(x_+)=t`, so in this
unweighted specialization the endpoint values are **exactly**
`u(x_-)=u(x_+)=t^(1/q)`.

For two distinct parallel lines the geometric interval lemma compares
the two bulk kernel integrals with endpoint averages and
`(n-2) min(chi_I,chi_J) D_e K+|chi_I-chi_J|K`.
All terms are nonnegative prior to integration. Integrating over all
partner components, levels, and transverse coordinates recovers
`K*g` at each selected endpoint. The excluded coincident line is
Lebesgue null, and the endpoint lies off zero, so the recovered
potential is pointwise finite. Each integrated endpoint term is bounded
by its finite marginal `int h_e fu` or `int h_e gv`.
Unbounded components have weight zero and never require their endpoint
evaluation or subtraction of divergent line integrals (including `n=3`).

The mismatch is bounded by
`|chi_I-chi_J|<=|h_e(x)-h_e(y)|+(h_e(x)-chi_I)+(h_e(y)-chi_J)`.
The last two integrated terms are precisely the losses `L_f,L_g`.
Finally,

`int_0^f(u-t^(1/q))dt=fu/(q+1)`

recovers `a W_f`; the analogous identity recovers `b W_g`.
Combining these formulas yields

`aW_f+bW_g <= (n-2)int w D_(omega_x)d pi`
`               +(C kappa+C_kappa delta+C_(kappa,delta)/P)E+C_(kappa,delta,P)`.

The choices are sequential: first `kappa`, then `delta`, then `P`.
The constants have exactly the independence required by that order.

### 6. Strict subcriticality closes the argument

Let `gamma=n(a+b)-(n-2)>0` and `T=int w D_(omega_x)d pi`.
The virial identity is exactly

`(an-(n-2))E_f+bn E_g=aW_f+bW_g-(n-2)T+(n-2)Q`.

Pressure and localization imply an upper bound `C epsilon E+C_epsilon`
on the right. Since the left is

`gamma E/2 + (an-(n-2)-bn)(E_f-E_g)/2`,

the marginal mismatch estimate absorbs the second term. Choosing
`epsilon` sufficiently small proves `E<=C` universally. Consequently
`int_(B_1)(u^(q+1)+v^(p+1))<=C` for every entire solution.

The scaled solution has energy

`int_(B_1)(u_R^(q+1)+v_R^(p+1))`
`=R^(alpha+beta+2-n) int_(B_R)(u^(q+1)+v^(p+1))`.

The exponent is positive because
`gamma=(1-a-b)(alpha+beta+2-n)` and `1-a-b>0`.
For `R>=1` the second factor is at least its fixed positive value on
`B_1`; thus the left tends to infinity, contradicting its universal bound.

## Degenerate, limiting, and regularity checks

* If a nonnegative component vanishes at a point, the strong maximum
  principle applied to `-Delta u=v^p>=0` forces that component to vanish
  identically. Its equation then forces the other component to vanish.
  Otherwise both components are strictly positive, so the audited
  positive theorem applies. A one-component positive constant is not a
  solution of both equations.
* For `p,q>1` the functions `u^q,v^p` are locally continuously
  differentiable once positivity holds. The potential-gradient and
  endpoint arguments are therefore valid for `C^2` classical solutions.
* The high cap powers ensure extension by zero across both boundary
  spheres, including when a short component crosses radius one.
* Exit distances and infima are measurable: finite-segment containment
  in an open layer is an open condition, and infima of continuous
  weights can be taken over rational offsets. A component with infinite
  length always receives weight zero.
* Strict hyperbola inequality is essential. At equality `gamma=0` and
  the absorption/scaling contradiction stops; no critical theorem is
  inferred. Radial critical bubbles are consistent with every estimate.
* The singular-line exclusion requires no uniform estimate in its
  transverse separation: Tonelli is applied before any subtraction,
  and subsequent finiteness comes from the exact finite potentials.
* A bounded entire solution remains bounded under each finite dilation;
  no common bound on its amplitude is assumed or needed.

## Status and exact remaining gap

The needed bounded-entire unweighted Liouville dependency is analytically
verified on the inspected source version. No unresolved mathematical gap
in that dependency is presently known to this auditor. Its publication,
provenance, novelty, and formal-verification status require the separate
project audits; this note does not certify those matters. It also does
not independently prove the subsequent half-space or domain estimates.

Final checkpoint: 2026-10-07 04:32:56 UTC (2026-10-06 21:32:56 PDT).
Completion estimate for this assigned analytic dependency: 100%.
This is not a completion estimate for the full research or publication goal.

The independent interval falsification agent found no substantive defect.
Its supplementary exact certificate is

`RHS-LHS=(n-2)c d_0 T+(c_I-c)E_I+(c_J-c)E_J >= 0`,

where `c=min(c_I,c_J)`, `E_I,E_J` are the integrated endpoint
averages, and `T=int hK/(lambda^2+h^2)`. The overlap-density
pairing proves `d_0 T>=0` directly. Its 614 numerical diagnostics,
including deliberately disjoint and unequal intervals and physical
transverse separations `10^-3` and `10^-6`, passed. The largest
midpoint-identity discrepancy was `1.29e-13`; this is diagnostic evidence,
not a rigorous numerical error certificate. See
`upstream_interval_review.md` and `upstream_interval_checks.py`.
