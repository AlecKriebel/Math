# Smooth transfer audit (independent approach family)

Audit time: 2026-10-06 21:12–21:16 America/Los_Angeles (2026-10-07 UTC).
Auditor: independent `smooth_transfer` subagent. No external communications, Git writes, or upstream-clone writes.

## Verdict and precise scope

**Verified conditional result:** the even logarithmic Brunn–Minkowski inequality, or its logarithmic Minkowski first-variation consequence, implies uniqueness of smooth positive even support functions with positive-definite curvature matrix solving the logarithmic Minkowski equation. Together with the even `Lp` Minkowski inequality, the same local interpolation mechanism proves the smooth result for every `0 <= p < 1`. The argument works in ambient dimension `d >= 2`, including the circle `S^1` when `d=2`.

**Existence is established independently of the proposed new inequality.** The safe citation chain is symmetry-preserving generalized existence from Bianchi–Böröczky–Colesanti–Yang, Theorem 1.7 / Proposition 7.3; symmetry forces origin interior; then established positive-support regularity from Chou–Wang, Proposition 1.2, yields smoothness for smooth data. This chain avoids overstating what Chou–Wang's Theorem D itself says.

**No unconditional resolution is certified here.** The central upstream inequality is outside this agent's audit scope and remains a dependency to be validated by the lead/upstream auditors. No formal verification claim is made.

Theorem to use in the project, in unambiguous notation:

> Let `d >= 2`, `0 <= p < 1`, and let `f` be a strictly positive even `C^infinity` function on the unit sphere `S^(d-1)`. Assuming the even `Lp` Minkowski inequality for all full-dimensional origin-symmetric convex bodies in `R^d`, there exists exactly one `h in C^infinity(S^(d-1))` which is even, strictly positive, is the support function of a full-dimensional convex body, has `H(h)=nabla^2 h+h I > 0`, and satisfies `h^(1-p) det H(h)=f`. The determinant is of the `(d-1)`-dimensional endomorphism on the tangent space, with the standard round metric and unnormalized spherical area measure.

For fixed `f` no extra scale/volume normalization is imposed: `h -> a h` scales the left side by `a^(d-p)`, so the prescribed data fixes the scale. At `p=0`, `d V(K)=integral f d sigma` follows from the equation. For normalized cone-volume conventions, `dV_K=(1/d)h_K dS_K`; thus the equation prescribes `dV_K=(f/d)d sigma`, not `f d sigma`. Origin symmetry refers to the specified origin; it removes translation freedom. The displayed PDE must not be advertised as an equation for arbitrary smooth functions, without positive support and positive-definite curvature assumptions.

## Primary sources actually inspected

1. Weiyong He and Junbang Liu, *On the uniqueness of even Lp Minkowski problem*, arXiv:2510.21530v1, submitted 2025-10-24 14:54:55 UTC, https://arxiv.org/html/2510.21530v1 and https://arxiv.org/pdf/2510.21530v1. Read Theorems 4, 2.1, 3.1 and the complete Theorem 3.1 proof, equations (3.1)–(3.13), plus definitions and bibliography needed to resolve the dependencies. The version-history page https://arxiv.org/abs/2510.21530 lists only v1 at audit time; no correction/new version was silently substituted.
2. Kai-Seng Chou and Xu-Jia Wang, *The Lp-Minkowski problem and the Minkowski problem in centroaffine geometry*, Advances in Mathematics 205 (2006), 33–83, DOI https://doi.org/10.1016/j.aim.2005.07.004. Inspected the publisher-version PDF hosted in the ANU repository, especially Theorem D on printed p.37, Proposition 1.2 on p.40, and Section 5. Also inspected the author's 2005-06-07 prepublication PDF, https://maths-people.anu.edu.au/~wang/publications/3-p-Minkowski.pdf, for searchable comparison.
3. Gabriele Bianchi, Károly J. Böröczky, Andrea Colesanti and Deane Yang, *The Lp-Minkowski problem for -n < p < 1*, arXiv:1710.04401v2, 2018-10-21, https://arxiv.org/pdf/1710.04401v2. Read Theorem 1.7, Section 7 including Proposition 7.3, Lemma 7.4, Proposition 7.5 and the measure-limit/scaling proof. Journal reference: Advances in Mathematics 341 (2019), 493–535, DOI https://doi.org/10.1016/j.aim.2018.10.032, verified on the publisher page https://www.sciencedirect.com/science/article/pii/S0001870818304262. This is especially valuable because the symmetry-preserving version is explicitly stated and justified.
4. Gabriele Bianchi, Károly J. Böröczky and Andrea Colesanti, *Smoothness in the Lp Minkowski Problem for p<1*, Journal of Geometric Analysis, DOI https://doi.org/10.1007/s12220-019-00161-y, author-hosted publisher PDF https://www.renyi.hu/~carlos/lp-chou-wang-smoothness-jga.pdf. Read Theorem 1.1, the distinction between positive and nonnegative-support equations, and the convex-body/measure definitions. This corroborates the importance of first ensuring origin interior.

Downloaded audit copies are in `agent_notes/smooth_transfer_sources/` for local checking. The lead should **exclude third-party source PDFs, HTML and extracted text from any publication upload-kit** unless redistribution permission is separately established. The source hashes below are evidence identifiers, not permissions to redistribute.

| Local audit file | Bytes | SHA-256 |
|---|---:|---|
| `he_liu_2510.21530v1.html` | 735666 | `10291e5cb019a0f2f92f9a286ac3c054cd6dd9a1bdb3b32a7f816a1529b43439` |
| `he_liu_2510.21530v1.pdf` | 463756 | `ca9c09c5739561ccb90250575dd27a48c0fdfc1efbe30dc416f5d5c4071e3e3b` |
| `chou_wang_2005_author.pdf` | 338413 | `7ab70e3102b676f2be246afa18faff098dbe30319942663d59c9cb5dff3244ec` |
| `chou_wang_2006_published.pdf` | 387656 | `b0bc60be78ed26b8f7c5f5ecdc4ae05e3cc80fdd2087831e18581dc3425ed0d0` |
| `bianchi_boroczky_colesanti_yang_1710.04401v2.pdf` | 449900 | `da966a25665ba0e18608ef2baff2996e547e6cd97c007ed3f5d5e692f5ea2b24` |
| `bianchi_boroczky_colesanti_2019_smoothness.pdf` | 445385 | `10c8c92763fecbe620240cd81366246c0092e227e20842c16d68477987faa695` |

## Exact He–Liu theorem versus proof dependencies

He–Liu Theorem 4 assumes their displayed inequality (5), which is actually the even `Lp` **Minkowski mixed-volume inequality** (first-variation form), although the theorem calls it the `Lp` Brunn–Minkowski inequality. Its `p=0` interpretation is their displayed logarithmic Minkowski inequality (6). The statement concerns positive smooth even data and a smooth even solution in the support-function/positive-curvature category defined in their introduction.

Their main convention is ambient `R^(n+1)` and sphere `S^n`, with an `n x n` curvature matrix. However, Section 3 unexpectedly uses `R^n`, `S^(n-1)` and volume factors `1/n` in (3.2)–(3.4), then returns to the main convention. This is a notation inconsistency to clean; do not copy those factors mechanically. In our notation every volume factor is `1/d`, matrix traces of the identity are `d-1`, and scaling is `d-p`.

The substantive Theorem 3.1 strategy is valid: the mixed-volume inequality makes every solution a global minimizer of a scale-invariant variational functional; an `Lp` interpolation between two minimizers retains equality; differentiating its common prescribed-curvature equation gives a contradiction unless the endpoints coincide. The proof's global Wulff-path regularity step can be eliminated, as shown below. Its positive-`p` differentiation contains repairable arithmetic omissions, verified in the actual v1 PDF as well as HTML.

Theorems concerning the first even eigenvalue, White's Fredholm/submersion theorem, Putterman's local-global transfer, and the complex pluripotential construction in Section 4 are **not needed** for the direct smooth transfer once the global inequality is available. No circular reliance on uniqueness is needed in the streamlined proof below.

## Existence and regularity audit

He–Liu Theorem 2.1 attributes to Chou–Wang an even smooth variational minimizer for all `-n-1<p<1`. The original Chou–Wang Theorem D itself gives a generalized nonnegative solution, with positivity and `C^(2,alpha)` asserted there only when `p<=-n+1` (sphere-dimension convention). It does not explicitly assert the symmetry-preserving minimizer in that statement; the symmetric adaptation is reasonable but should not be cited as if it appeared verbatim in Theorem D.

A completely explicit established route is:

1. With ambient dimension `d`, BBCY Theorem 1.7 / Proposition 7.3 provides a full-dimensional convex body `K`, containing the origin, with `dS_(K,p)=f d sigma`; if the measure is invariant under a closed `G<=O(d)`, the body may be chosen `G`-invariant. Smooth strictly positive `f` is bounded above and below by positive constants. The range `0<=p<1` lies in `(-d,1)` for every `d>=2`. Take `G={I,-I}`.
2. Full-dimensional origin-symmetric `K` necessarily has `0 in int K`. For any interior ball `B(x,r) subset K`, symmetry gives `B(-x,r) subset K`; convexity implies their midpoint ball `B(0,r) subset K`. Thus `h_K>=r>0` on the whole sphere.
3. The measure equation now becomes `dS_K=f h_K^(p-1) d sigma` on the whole sphere. Positivity prevents the singular boundary-origin distinction between this equation and `h_K^(1-p)dS_K=f d sigma`.
4. Chou–Wang Proposition 1.2, together with its stated positive-support local strict-convexity input from Caffarelli, gives `h_K in C^(2,alpha)` for Hölder data; for `f in C^(1,1) intersect C^(k,alpha)` it gives `h_K in C^(k+2,alpha)` for every `k>=1`. Therefore smooth `f` gives smooth `h_K`. BBC Theorem 1.1(iv) independently records the interior-origin regularity conclusion.
5. A smooth support function has `H>=0`. Its determinant is `f h_K^(p-1)>0`, so every eigenvalue is positive. Compactness makes `H` uniformly positive definite. The inverse Gauss parametrization `x(u)=h_K(u)u+nabla h_K(u)` then produces a smooth strictly convex body with positive Gaussian curvature.

The symmetry-preserving existence proof was checked beyond its statement. In BBCY Proposition 7.3, the modified variational optimization is restricted to invariant bodies. The unique optimizing center is fixed by `G`; for `G={±I}` it is zero. The exceptional-normal-set deformation is made invariant by the union of its `G` orbit. The Euler–Lagrange identity, initially tested only against invariant support functions, is extended to all support functions through Haar averaging; for our group this is simply `h_C0(u)=(h_C(u)+h_C(-u))/2`. Weak compactness, a positive limiting multiplier, and scaling by its `1/(d-p)` power then give exactly the prescribed measure. These arguments do not use the log-Brunn–Minkowski conjecture or uniqueness.

For the planar boundary case one can avoid all high-dimensional PDE regularity: an origin-symmetric full-dimensional body has positive Lipschitz support `h`; in angular coordinates the surface measure is `(h''+h)d theta` in distributions. The measure equation gives `h''+h=f h^(p-1)`, a positive continuous right-hand side. Distributional integration gives `h in C^2`; repeated differentiation yields `C^infinity` for smooth data. Moreover `h''+h>0`. This proves the required `d=2` regularity explicitly.

## Self-contained smooth endpoint transfer, using only a local path

This is an independent check/reorganization of the He–Liu mechanism, not a claim to invent that transfer.

Assume the logarithmic Minkowski inequality in ambient dimension `d`:

`(1/(d V(K))) integral h_K log(h_L/h_K) dS_K >= (1/d) log(V(L)/V(K))`

for full-dimensional origin-symmetric bodies. Equivalently, with the normalized cone-volume measure `d nu_K=h_K dS_K/(d V(K))`, `integral log(h_L/h_K) d nu_K >= (1/d)log(V(L)/V(K))`.

Let `h` and `g` be two smooth positive even support solutions of `h det H(h)=f`. Put `M=integral f d sigma`. Both bodies have `V=M/d`, since `d V=integral h dS=integral f`. Define

`F(a)=M^(-1) integral log(a) f d sigma -(1/d)log V(a)`

for any positive origin-symmetric support function `a`. Applying the logarithmic Minkowski inequality with `K` equal to the body of `h`, whose cone-volume probability measure is `f d sigma/M`, gives `F(a)>=F(h)`. Applying the same statement with `g` gives `F(a)>=F(g)`. Taking `a=g` and `a=h`, respectively, gives `F(h)=F(g)`. In particular, `integral log(h)f=integral log(g)f`.

Set `q_t=h exp(t w)`, where `w=log(g/h)`. Because `H(h)>0` on a compact sphere and `q_t` depends smoothly on `t`, for all `|t|<epsilon` the function `q_t` is a smooth positive support function with `H(q_t)>0`. Only this local interval is needed. For `0<=t<epsilon`, the log-Brunn–Minkowski inequality gives `V(q_t)>=V`: its Wulff body is already exactly the smooth body supported by `q_t` on this interval. Also `integral log(q_t)f` equals the common endpoint integral. Thus `F(q_t)<=F(h)`. Global minimality gives equality, so `V(q_t)=V`, and `q_t` is again a global minimizer of `F`.

At each such `q_t`, arbitrary smooth even additive support perturbations remain positive strictly convex for sufficiently small parameter. The classical volume first variation is `D V(q_t)[eta]=integral eta det H(q_t) d sigma`. Differentiating `F` gives

`0=integral eta [ f/(M q_t) - det H(q_t)/(d V) ] d sigma`.

The bracket is even and smooth. Its pairing vanishes against all smooth even `eta`, so it vanishes pointwise. Since `d V=M`, `q_t det H(q_t)=f`. This holds for `0<=t<epsilon`; hence first and second right derivatives at `t=0` agree with ordinary derivatives of the smooth path.

Write `H=H(h)`, `B=H^(-1)` and

`a_ij=h w_ij+h_i w_j+h_j w_i`,

`A=H(h w)=w H+a`,

`C=H(h w^2)=w^2 H+2w a+2h(dw tensor dw)`.

Twice differentiating `log q_t+log det H(q_t)=log f` gives

`d w+tr(B a)=0`,

`tr(B C)-tr((B A)^2)=0`.

Now

`tr((B A)^2)=tr((B a)^2)+2w tr(B a)+(d-1)w^2=tr((B a)^2)-(d+1)w^2`,

`tr(B C)=(d-1)w^2+2w tr(B a)+2h B^ij w_i w_j=-(d+1)w^2+2h B^ij w_i w_j`.

Subtracting yields the exact identity

`tr((B a)^2)=2h B^ij w_i w_j`.

Choose a point where `|w|` is maximal; at this point `dw=0`. Since `a` is symmetric and `B` positive definite, `tr((B a)^2)=||B^(1/2) a B^(1/2)||_F^2>=0`, with equality exactly when `a=0`. Therefore `a=0` at that point. The first-derivative identity gives `d w=0` there; hence `max |w|=0` and `g=h`.

All dimensions and constants check: `tr(B H)=d-1`, the first logarithmic derivative coefficient is `d`, the cancelling quadratic coefficient is `d+1`, and the compact maximum argument works on `S^1`. No strict log-Brunn–Minkowski equality characterization is assumed. No global interpolation regularity is needed. No normalized-probability uniqueness is confused with the actual prescribed equation.

## Positive-p transfer and arithmetic correction in He–Liu v1

For `p>0`, normalize the two candidate bodies to equal volume using the functional

`F_p(a)=(1/p)log integral a^p f d sigma -(1/d)log V(a)`.

The even `Lp` Minkowski inequality makes each candidate a global minimizer. Equal volume and equal minimal energy imply equal `I_p=integral a^p f`. Thus their normalized equations have one common multiplier `c=dV/I_p`. For the local smooth path `q_t=((1-t)h^p+t g^p)^(1/p)`, positive-definite curvature again holds near `t=0`. Its integral `I_p` is constant, and `Lp` Brunn–Minkowski gives `V(q_t)>=V`, so minimality forces `V(q_t)=V` and then local stationarity gives `q_t^(1-p)det H(q_t)=c f`.

Set `z=q_t'/q_t`, so `q_t''=(1-p)q_t z^2` and `z'=-p z^2`. With `A=H(q_t')`, the first differentiated equation is

`(1-p)z+tr(B A)=0`.

Its **correct** second differentiated equation is

`0=-tr((B A)^2) -(1-p)(d+1-p)z^2 +2(1-p)q_t B^ij z_i z_j`.

Derivation: write `A=zH+a` with `a_ij=q_t z_ij+(q_t)_i z_j+(q_t)_j z_i`. Then `tr(Ba)=-(d-p)z`, and

`tr(B H(q_t''))=(1-p)[(-d-1+2p)z^2+2q_t B^ij z_i z_j]`.

The term from differentiating `(1-p)log q_t` a second time is `-p(1-p)z^2`; adding it gives the stated coefficient. At a point where `|z|` is maximal, `dz=0`, so the identity is a sum of two nonpositive terms whose vanishing forces `z=0`, because `(1-p)(d+1-p)>0`. Thus the normalized endpoints coincide. The original candidates are homothetic, and the scaling law `a^(d-p)` plus the same prescribed `f` forces their dilation factor to be one.

In He–Liu's sphere-dimension notation `n=d-1`, (3.12) drops the `+n(1-p)z^2` contribution in the next line, and (3.13) omits the `-p(1-p)z^2` logarithmic contribution. Their final coefficient `2(1-p)(n+1-p)` is therefore not the correct coefficient; the correct one is `(1-p)(n+2-p)`. The corrected coefficient is still strictly positive, preserving the argument. Their `p=0` proof is algebraically sound but its statement `max w=0`, then `w=0`, should be completed using the minimum as well or, as above, a maximum of `|w|`.

## Falsification/boundary checks

- `d=2`: matrix dimension is one, and all traces/matrix-square positivity arguments remain valid. Source restrictions on some unrelated eigenvalue conjectures do not remove this case from the local interpolation proof.
- `p=0`: fixed `f` fixes actual volume `M/d`; the functional alone is scale invariant, and does not fix scale. The equation does.
- `p>0`: use exponent `d-p`, not `d-1-p`. Constant support `h=R` gives `f=R^(d-p)`, providing a direct check.
- Symmetry is needed to apply the assumed even inequalities and to guarantee origin interior in the existence construction.
- Strict positive data is used both in the regularity/curvature conclusion and to avoid non-full-dimensional degeneracy.
- The smooth endpoint proof assumes smooth positive-definite curvature candidates; it does not establish uniqueness among arbitrary nonsmooth measures.
- Equal-volume coordinate boxes have equal `p=0` surface measure weights `V/2` at each signed coordinate normal (cone-volume weights `V/(2d)`), while shapes can differ. They lie outside the positive smooth data/curvature class and remain counterexamples to any broader endpoint statement. The lead corrected an earlier factor-two typo in this bullet before the first complete-package review; the mixed-strictness derivation and manuscript already had the correct factor.
- A translated support function is `h+a dot u`, and its curvature matrix is unchanged but `h^(1-p)` is not for `p<1`; origin symmetry fixes the origin and excludes this apparent classical translation ambiguity.
- No computational/numerical theorem claim was used. The identities are exact derivations. No Lean declaration was checked by this agent.

## Remaining exact gap and recommended paper treatment

The transfer mechanism and established existence/regularity dependencies do not block the core target. The exact gap remaining outside this report is whether the upstream all-dimensional even log-Brunn–Minkowski inequality is actually proved under its stated hypotheses, including all bodies needed for the mixed-volume consequence. Any material upstream gap leaves our uniqueness conclusions conditional.

If the upstream inequality passes, the smooth result must be framed as a newly available consequence of that inequality and the established He–Liu transfer, with existence/regularity attributed to their original sources. A cleaned self-contained endpoint account is useful verification, but it is not evidence that we invented the transfer. The positive-`p` arbitrary-body proof should be handled and independently checked by the separate mixed-volume/Jensen approach family. Publication/novelty remains for the lead's priority audit and full-package adversarial review.
