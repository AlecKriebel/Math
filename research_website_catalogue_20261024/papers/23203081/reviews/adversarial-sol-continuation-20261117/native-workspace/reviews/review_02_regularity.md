# Independent review 02: existence and positive-support regularity

Checkpoint: 2026-10-07 04:27:29 UTC. Assigned review complete: 100%.

## Scope and verdict

I independently checked only the existence and regularity assertion in Theorem 1(1), specifically the existence paragraphs at `main.tex:163–165`. I read the three requested primary papers and their local PDF/text versions, without consulting existing audits or other reviewers. I did not assess uniqueness or the upstream logarithmic Brunn–Minkowski result.

**The claimed existence of a positive even smooth support function with `Q(h)>0` is supported for every ambient dimension `n>=2`, every `0<=p<1`, and every strictly positive even smooth density. However, the sentence that local strict convexity follows from positive bounded Monge–Ampère density in affine support charts is false if read as a local density-only implication.** It must explicitly invoke the global convex-body geometry and BBC Theorem 1.1(i). The cited sources already provide a complete repair; no stronger existence or regularity theorem is needed.

This existence result is independent of the new logarithmic Brunn–Minkowski hypothesis. The precise repaired chain is:

1. BBCY Theorem 1.7 and Proposition 7.3 give a full-dimensional origin-symmetric measure solution.
2. Full dimensionality and symmetry imply `0 in int K`, hence a strictly positive support function.
3. BBC Theorem 1.1(i), together with `N(K,0)={0}`, gives `partial K` of class `C^1`; the support-function duality explicitly stated in BBC then gives strict convexity of affine support charts.
4. The positive support permits division of the measure equation, so Chou–Wang Proposition 1.2 applies and gives smooth support regularity.
5. Convexity and the now-pointwise positive determinant give `Q(h)>0`.

## Primary-source evidence and exact hypotheses

All PDF pages below are counted from the first page of the local PDF, not from a web viewer. Text-line references refer to the existing extraction files in `agent_notes/smooth_transfer_sources`.

### BBCY: symmetry-preserving existence

Source: Bianchi–Böröczky–Colesanti–Yang, [arXiv:1710.04401v2](https://arxiv.org/abs/1710.04401v2), Theorem 1.7, PDF p. 4, text lines 181–184; Proposition 7.3, PDF p. 18, text lines 1056–1058. The PDF itself was checked at the theorem page.

Theorem 1.7 assumes `-n<p<1` and a Borel measure `mu=f H^{n-1}` on `S^{n-1}`, where `f` is bounded and has strictly positive infimum. It produces a convex body `K in K_0^n` with `S_{K,p}=mu`; if the measure is invariant under a closed subgroup `G` of `O(n)`, the body can be chosen invariant under that group. Proposition 7.3 states the group-preserving conclusion explicitly with the same hypotheses.

Here `n` is ambient dimension, and `K_0^n` consists of convex bodies with nonempty interior containing the origin; the definitions are in BBCY PDF p. 1, text lines 14–17 and 42–45. Thus this is genuinely a full-dimensional solution, not merely a lower-dimensional compact convex set.

Theorem 1.7 guarantees `0 in int K` directly only when `p<=2-n`. That restricted statement must not be used to infer positive support throughout the current parameter range. The manuscript instead correctly uses symmetry: the even density is invariant under the closed subgroup `{I,-I}`, and Proposition 7.3 gives `K=-K`. If `B(x,r)` lies in `K`, then `B(-x,r)` also lies in `K`; convexity gives `B(0,r)` in `K`. Hence the origin is interior for every `0<=p<1`, including `p=0` in dimensions above two.

Since the sphere is compact and `f` is strictly positive and smooth, its positive lower and finite upper bounds hold automatically. The normalizations agree: round area measure in the manuscript is the same unnormalized Hausdorff area measure used in BBCY. There is no scale or volume normalization restriction on this existence theorem.

### BBC: the missing global strict-convexity mechanism

Source: Bianchi–Böröczky–Colesanti, [DOI 10.1007/s12220-019-00161-y](https://doi.org/10.1007/s12220-019-00161-y), Theorem 1.1, PDF p. 3, text lines 118–129. The PDF itself was checked at this page.

Its hypotheses are: `K in K_0^n`, ambient `n>=2`, `p<1`, `dS_{K,p}=f dH^{n-1}`, and `f` bounded above and below by positive constants.

Part (i) defines

`X_0={x in partial K : N(K,x) is a subset of N(K,0)}`,

and asserts that `X_0` is closed, every point of `X=partial K minus X_0` has a unique tangent hyperplane, and `X` contains no segment. With the origin interior, BBC defines `N(K,0)={0}`. Every boundary normal cone contains a nonzero normal, so `X_0` is empty. Therefore every boundary point is `C^1`-smooth and the boundary contains no segment.

The distinction between the two resulting properties matters. Immediately before the theorem, at PDF p. 3, text lines 110–114, BBC states:

- `h_K` is `C^1` on the sphere iff `K` is strictly convex.
- `h_K` is strictly convex on every affine hyperplane avoiding the origin iff `partial K` is `C^1`.

Thus the **boundary `C^1` conclusion**, not merely the absence of boundary segments, supplies the strict convexity of support-function charts needed by Chou–Wang.

Part (iv) additionally states: if the origin is interior and `f` is positive and `C^alpha` for some `alpha>0`, then **the boundary** is `C^{2,alpha}`. This is useful corroboration, but it does not literally state support-function regularity. Using Chou–Wang Proposition 1.2 after part (i) avoids conflating those two regularity assertions.

The proof explains the extra mechanism. BBC PDF pp. 21–22, text lines 1103–1147, first obtains chart density bounds (4.2). To exclude a nontrivial boundary normal cone, it chooses an extremal ray of that cone outside `N(K,0)`, subtracts an affine support function from the chart, and obtains a contact set with an interior extreme point. Caffarelli's localization statement, BBC Theorem 3.6(i), PDF p. 20, text lines 1032–1039, prohibits that configuration for a nonsingleton contact set. This proves boundary smoothness (4.3). The proof then explicitly deduces strict convexity of the chart in text lines 1135–1142. The density bounds are one input to this global support-cone argument; they are not the whole argument.

### Chou–Wang: support regularity and the convention change

Source: Chou–Wang, [DOI 10.1016/j.aim.2005.07.004](https://doi.org/10.1016/j.aim.2005.07.004), Proposition 1.2, journal p. 40 = local PDF p. 8, text lines 352–379. The published PDF itself was checked at this page. Section 6 is journal pp. 67–69 = local PDF pp. 35–37, text lines 1803–1899.

Chou–Wang uses `S^m` in `R^{m+1}`; for the present manuscript substitute `m=n-1`. Its generalized equation is

`dS_K=h^{p-1} dm`,

not merely the weighted equation at a possibly vanishing support function. Once `h>0`, the manuscript's equation `h^{1-p} dS_K=f d omega` is equivalent to this equation by division, globally. The possible discrepancy at zero support, discussed explicitly in BBC PDF pp. 3–8, does not arise here.

Proposition 1.2 assumes that the support function is locally strictly convex away from `Z={h=0}`. It gives `h in C^{2,alpha}` there for `f in C^alpha`, `0<alpha<1`, and `h in C^{k+2,alpha}` when `f in C^{1,1} intersect C^{k,alpha}` for `k>=1`. The smooth datum satisfies those conditions for every finite `k`, with a fixed `alpha`, and `Z` is empty. These are exactly the hypotheses needed for `h in C^infinity`. No additional symmetry assumption enters the regularity theorem; evenness is retained from the original body's symmetry.

Section 6 independently discusses establishing support-chart strict convexity by contact-set extreme points (journal pp. 68–69, text lines 1865–1899). Its conclusion again uses support geometry, rather than a bare local determinant bound. Theorem E's range in the `p<1` case is `-m+1<p<1`; after changing conventions this is `2-n<p<1`. This encompasses the target for `n>=3`, but excludes `n=2,p=0`. One should not silently cite Theorem E alone for that endpoint. Proposition 1.2 and BBC provide the relevant general chain, and the manuscript's scalar argument below gives a direct endpoint check.

## Explicit falsification of the density-only statement

In three chart dimensions, on the convex cylinder

`Omega={(x_1,x_2,t): x_1^2+x_2^2<1, |t|<1/4}`,

set

`v=1+(x_1^2+x_2^2)^{2/3}(1+t^2)`.

This is positive and `C^1` everywhere. Write `r=(x_1^2+x_2^2)^{1/2}`. Away from the axis, its Hessian in radial, angular, and `t` coordinates is

```
[ (4/9)r^(-2/3)(1+t^2)          0                 (8/3)t r^(1/3) ]
[             0          (4/3)r^(-2/3)(1+t^2)           0         ]
[      (8/3)t r^(1/3)            0                    2r^(4/3)  ].
```

The radial–`t` block determinant is `(8/9)r^{2/3}(1-7t^2)>0`. Hence the Hessian is positive definite off the axis, and

`det D^2v=(32/27)(1+t^2)(1-7t^2)`.

This determinant is a smooth density bounded between `17/24` and `32/27`. Convexity holds across the axis too: the derivative along any line is increasing off the axis and continuous at an axis crossing; a line lying on the axis gives a constant function. The subgradient of every axis point is `{0}`, so its Monge–Ampère measure is zero and there is no singular mass on the axis. Thus the displayed determinant is the complete Alexandrov density.

Nevertheless, `v(0,0,t)=1`, so every neighborhood of any interior axis point contains a nontrivial affine contact segment. Local strict convexity fails. This concrete calculation was independently checked by a separate read-only algebra subagent.

The example falsifies the unrestricted local implication even for positive functions and smooth positive determinant density, starting at ambient dimension four (three-dimensional support charts). It is not a global convex-body solution with the manuscript's smooth spherical datum and does not contradict the target existence theorem. Its contact set extends to the edge of the chart, exactly the configuration not ruled out by density bounds alone.

## Final passage to the claimed solution and boundary checks

For `n>=3`, apply the chain above. Once `h in C^{2,alpha}`, the surface-area density is `det Q(h)`, and the weak measure equality becomes a pointwise equality because both sides are continuous. Convexity of the degree-one extension gives `Q(h)>=0`; since

`det Q(h)=f h^{p-1}>0`,

every eigenvalue is positive. Compactness of the sphere then gives a uniform positive minimum eigenvalue. The higher regularity in Proposition 1.2, or ordinary elliptic bootstrapping after this step, gives `C^infinity`. The inverse Gauss-map parametrization `u -> h(u)u+grad h(u)` therefore produces a smooth body with strictly positive Gauss curvature.

For `n=2`, in angular coordinates the surface-area equation is the distributional scalar equation

`h''+h=f h^{p-1}`.

The original positive support function is continuous, so the right side is continuous. The equation gives `h in C^2`; iteration gives `C^infinity` because `f` is smooth and `h` is bounded away from zero. The scalar curvature radius `h''+h=f h^{p-1}` is strictly positive. This includes `p=0` without relying on an open parameter endpoint in Theorem E.

The endpoint `p=0` creates no singularity in this existence/regularity argument because the support is positive. `p=1` is outside the claimed range; no assertion about its boundary is needed. Without the symmetry-derived interior-origin condition, positive bounded data alone do not justify the same global positive-support argument: BBC's Theorem 1.1(iii) only forces interior origin for `p<=2-n`, and its Example 4.2 shows why this distinction matters beyond that range.

## Minimal required correction

Replace the density-only sentence by a statement with the correct logical dependency, for example:

> Since the origin is interior, Theorem 1.1(i) of Bianchi–Böröczky–Colesanti gives a `C^1` boundary. The support-function duality stated there makes its affine support charts locally strictly convex. Chou–Wang Proposition 1.2 therefore applies to the globally nonsingular measure equation and gives the asserted support regularity.

This makes the proof source-complete, identifies the indispensable global ingredient, and preserves all hypotheses and conclusions of Theorem 1(1).
