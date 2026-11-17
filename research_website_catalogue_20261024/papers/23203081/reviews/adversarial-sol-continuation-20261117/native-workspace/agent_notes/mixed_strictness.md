# Conditional uniqueness for arbitrary bodies when 0 < p < 1

Prepared independently by the mixed-strictness route on 2026-10-06, 21:12 PDT
(2026-10-07 04:12 UTC). This is a mathematical research note, not a certificate
that the upstream logarithmic Brunn–Minkowski proof is valid. No upstream
equality characterization, smoothness, or full-support assumption is used.

## Exact claim and dependencies

Fix an integer n >= 2. Let K and L be compact, convex subsets of R^n with
nonempty interior, satisfying K = -K and L = -L. Write V(K) for n-dimensional
Lebesgue volume, h_K for the support function restricted to S^(n-1), and S_K
for the ordinary surface-area measure. Then 0 is interior to each body and
h_K,h_L are strictly positive continuous functions.

Assume the following logarithmic Brunn–Minkowski inequality for every pair
of such bodies and every t in [0,1]:

    V(W(h_K^(1-t) h_L^t)) >= V(K)^(1-t) V(L)^t,                 (LBM)

where W(w) = intersection over u in S^(n-1) of {x : x.u <= w(u)}. No
equality assertion is assumed in (LBM).

**Conditional theorem.** For every 0 < p < 1, if

    h_K^(1-p) dS_K = h_L^(1-p) dS_L,                          (1)

as finite Borel measures on S^(n-1), then K = L. More generally, under (LBM),

    V_p(K,L) >= V(K)^((n-p)/n) V(L)^(p/n),                    (2)

for every p > 0, where

    V_p(K,L) := (1/n) integral h_L^p h_K^(1-p) dS_K.

Equality in (2) holds exactly when L is a positive scalar multiple of K.
The uniqueness statement in this note is confined to the requested interval;
the broader inequality is useful for checking the mechanism and its scaling.

Classical prerequisites, valid for arbitrary full-dimensional convex bodies:

1. V(K) = (1/n) integral h_K dS_K, and
   V_1(K,L) = (1/n) integral h_L dS_K.
2. Minkowski's first inequality:
   V_1(K,L) >= V(K)^((n-1)/n) V(L)^(1/n), with equality precisely for
   positive homothetic bodies (a positive dilation followed by a translation).
3. Hausdorff convergence of full-dimensional bodies implies weak convergence
   of their surface-area measures.
4. The set of boundary points having more than one outer unit normal has
   (n-1)-dimensional Hausdorff measure zero.

These are ordinary convex-geometric facts, independent of logarithmic
Brunn–Minkowski. For completeness, the needed Wulff differentiation is proved
below from 1–4, and the equality part of 2 is recalled as a consequence of the
classical Brunn–Minkowski equality theorem.

## Nonsmooth Wulff first variation: an explicit proof

Let w be a strictly positive continuous function on the sphere and A = W(w).
The inclusions (min w) B <= A <= (max w) B show that A is a convex body
containing 0 in its interior. Here B is the Euclidean unit ball; these are
set inclusions, not pointwise identities between support functions.
By definition, h_A <= w.

The following contact property needs no differentiability of w or A:

    h_A = w, S_A-almost everywhere.                            (3)

Indeed, at any boundary point x, the continuous function
u -> w(u) - x.u is nonnegative. Its minimum is zero: a positive minimum
would make x an interior point of A. Consequently some defining halfspace
is active. At a boundary point with a unique outer normal u, every active
halfspace has that normal, and x.u = w(u) = h_A(u). Push forward boundary
area by the Gauss map and apply prerequisite 4 to obtain (3).

Let w_t be a family of strictly positive continuous functions for t near 0,
such that w_0 = h_K and

    (w_t - h_K)/t -> g uniformly on S^(n-1) as t -> 0.          (4)

Put A_t = W(w_t). Since min h_K > 0, uniform convergence w_t -> h_K gives
for every sufficiently small epsilon and t the inclusions

    (1-epsilon)K <= A_t <= (1+epsilon)K.

Thus A_t -> K in the Hausdorff metric, V(A_t) -> V(K), and S_(A_t)
converges weakly to S_K. The numbers V(A_t) remain bounded away from zero.

For any two positive Wulff functions w,v with A=W(w), C=W(v), prerequisite
2 together with h_C <= v and (3) gives

    V(C)^(1/n) - V(A)^(1/n)
      <= integral (v-w) dS_A / [n V(A)^((n-1)/n)].             (5)

To see the constants directly, prerequisite 2 bounds
V(A)^((n-1)/n)V(C)^(1/n) above by V_1(A,C), and

    V_1(A,C) <= (1/n) integral v dS_A
              = V(A) + (1/n) integral (v-w) dS_A.

Interchanging A and C similarly gives

    V(C)^(1/n) - V(A)^(1/n)
      >= integral (v-w) dS_C / [n V(C)^((n-1)/n)].             (6)

Apply (5)–(6) with A=K, C=A_t, w=h_K, v=w_t. For positive t, divide by
t and use (4), weak convergence of S_(A_t), and convergence of the volumes.
The two bounds have the common limit

    integral g dS_K / [n V(K)^((n-1)/n)].

The same calculation for negative t reverses the two inequalities and gives
the same limit. Uniform convergence in (4) and bounded total masses of
S_(A_t) justify the integral limit even though both integrand and measure
vary. The chain rule now yields the full formula

    d/dt V(A_t)|_(t=0) = integral g dS_K.                      (7)

No determinant, Gauss curvature, regular boundary, or unjustified claim
that w_t itself is a support function has entered (7). The Wulff first
variation ordinarily quoted as Aleksandrov's formula has thus been
reduced here to classical facts 1–4 with all constants exhibited.

## From logarithmic Brunn–Minkowski to logarithmic Minkowski

Let a(u)=log(h_L(u)/h_K(u)), a continuous even function, and use

    w_t = h_K exp(t a) = h_K^(1-t) h_L^t.

This family is defined and positive for all real t. Because a is bounded,
(w_t-h_K)/t -> h_K a uniformly. W(w_t) is origin symmetric. Formula (7)
therefore applies, while (LBM) applies for t in [0,1]. Its equality at t=0
and its right derivative give

    integral h_K log(h_L/h_K) dS_K
        >= V(K) log(V(L)/V(K)).                               (8)

Define the cone-volume probability measure

    dnu_K := h_K dS_K / [n V(K)].

Division of (8) by nV(K) gives precisely

    integral log(h_L/h_K) dnu_K
        >= (1/n) log(V(L)/V(K)).                              (9)

This step uses only the inequality in (LBM), not any equality conditions.
One-sided differentiation at 0 is enough; the two-sided variation above
also establishes that there is no hidden nonsmooth derivative issue.

## Jensen strictness and geometric equality

Write r=h_L/h_K. It is continuous, positive, and bounded above and away from
zero on the compact sphere. For p>0, strict convexity of exp(p x) yields

    integral r^p dnu_K
       >= exp(p integral log r dnu_K)
       >= (V(L)/V(K))^(p/n).                                 (10)

Multiplying by V(K) proves (2). Equality in the first inequality of (10)
holds exactly when log r, hence r, is constant nu_K-almost everywhere.
Because h_K is positive, nu_K and S_K have the same null sets. In particular,
one obtains only constancy S_K-almost everywhere, not everywhere on the
sphere.

Suppose equality holds in (2), and put

    c = (V(L)/V(K))^(1/n) > 0.

Both inequalities in (10) are then equalities. Jensen gives r=d
S_K-almost everywhere for some d>0, and integral r^p dnu_K=c^p implies
d=c. Consequently

    V_1(K,L) = (1/n) integral h_L dS_K
             = c V(K)
             = V(K)^((n-1)/n) V(L)^(1/n).                    (11)

Classical Minkowski equality gives L=bK+x for b>0 and x in R^n.
Comparison of volumes gives b=c. Since both bodies are origin symmetric,
x=0: otherwise L would have distinct centers 0 and x, and composing the
two central reflections would make L invariant under translation by 2x,
contradicting compactness. Hence L=cK. Conversely L=cK makes (2) an
equality by direct substitution.

For reference, the equality assertion used in (11) follows from the
ordinary Brunn–Minkowski equality theorem without any logarithmic equality
input. Set F(t)=V((1-t)K+tL)^(1/n). The classical theorem makes F concave,
and the mixed-volume first variation gives

    F'(0+) = [V_1(K,L)-V(K)] / V(K)^((n-1)/n).

If equality holds in Minkowski's first inequality, this derivative equals
V(L)^(1/n)-V(K)^(1/n). The tangent bound for a concave function and the
Brunn–Minkowski chord bound coincide, so F is affine on [0,1]. Equality
in classical Brunn–Minkowski at an interior t forces positive homothety.

This is the precise repair of the tempting invalid shortcut: equality in
Jensen alone does not justify support-function constancy in every
direction. The mixed-volume integral sees exactly the measure where
constancy is known, and its equality theorem recovers the whole body.

## Identical Lp surface-area measures imply identical bodies

Assume (1) and write mu for its common measure. Then

    V_p(K,L) = (1/n) integral h_L^p dmu = V(L),
    V_p(L,K) = (1/n) integral h_K^p dmu = V(K),                (12)

because h_L^p dmu=h_L dS_L and similarly for K. Use (2) in both orders:

    V(L) >= V(K)^((n-p)/n) V(L)^(p/n),
    V(K) >= V(L)^((n-p)/n) V(K)^(p/n).                        (13)

Since n-p>0 and both volumes are positive, the first inequality is
V(L)>=V(K), and the second is V(K)>=V(L). Hence the volumes are equal,
(2) is an equality, and its equality case gives L=cK with c=1. Therefore
K=L, with no volume normalization imposed in the hypothesis.

As an independent cross-check of the last recovery step, equal volumes
and equality in Jensen give h_K=h_L mu-almost everywhere. Since

    dS_K=h_K^(p-1) dmu,   dS_L=h_L^(p-1) dmu,

their ordinary surface-area measures coincide. Classical Minkowski
uniqueness then gives equality up to translation, and origin symmetry
again eliminates translation. This cross-check is not needed by the
mixed-volume proof above.

## Endpoint obstruction and boundary audit

For positive numbers a_1,...,a_n let

    Q(a) = product over i=1,...,n of [-a_i,a_i],
    v = V(Q(a)) = 2^n product a_i.

The support function is h_(Q(a))(u)=sum a_i |u_i|. Its ordinary surface-area
measure consists exactly of the 2n atoms at +/-e_i, each with mass

    S_(Q(a))({+e_i}) = S_(Q(a))({-e_i})
                     = 2^(n-1) product_(j != i) a_j
                     = v/(2a_i).

Accordingly, the unnormalized L0 surface-area measure h_Q dS_Q assigns
mass v/2 to every atom, independently of the individual side lengths.
Thus two coordinate boxes of equal volume have identical L0 measures.
For every n>=2, the choices

    K=Q(1,...,1),  L=Q(t,t^(-1),1,...,1),  t>0, t!=1,

give distinct full-dimensional origin-symmetric bodies with identical
L0 measures. Their cone-volume measures have the corresponding masses
v/(2n). This normalization must not be confused with h_Q dS_Q.

For these boxes the ratio r has values t,t^(-1),1,...,1 at the coordinate
normals, and nu_K assigns each of the 2n normals mass 1/(2n). Thus
integral log r dnu_K=0, and log-Minkowski has equality despite K!=L.
For p>0, strict Jensen gives integral r^p dnu_K>1. This verifies directly
why the positive-p mechanism removes the box obstruction.

Boundary checks:

* **Ambient/sphere dimensions:** bodies are in R^n and measures are on
  S^(n-1). No S^n convention from a different paper is silently imported.
* **n=2:** every proof above remains valid, including (13), because
  2-p>0. The boxes reduce to the explicit rectangle counterexample.
* **Full dimension:** it supplies V(K)>0 and min h_K>0, needed by every
  logarithm, ratio, and root division. Lower-dimensional sets are outside
  the statement.
* **Scaling:** S_(cK)=c^(n-1)S_K and
  S_(cK,p)=c^(n-p)S_(K,p). Thus fixed data determine scale when 0<=p<1
  and n>=2. p=n is a scaling obstruction if considering extensions.
* **Translation:** S_K is translation invariant, but h_K^(1-p)S_K
  generally is not. Origin symmetry fixes the center in all steps.
* **PDE compatibility only:** for a smooth strictly positive support
  function with positive definite spherical curvature-radius matrix,
  dS_K=det(nabla^2_(S^(n-1))h+hI) d sigma. The determinant is on the
  (n-1)-dimensional tangent space, so the displayed PDE scales as c^(n-p).
  This note neither supplies smooth existence nor treats arbitrary
  unconstrained functions as support functions.
* **No full support:** surface-area measures of boxes are atomic. All
  equalities above are formulated measure almost everywhere, and the
  passage back to bodies uses classical geometric equality.
* **No origin-symmetry-free theorem:** (LBM) is invoked only for symmetric
  bodies, and its general nonsymmetric analogue cannot be presumed.

## Sources, attribution, validation status

Primary source consulted on 2026-10-06 PDT:

K. J. Böröczky, E. Lutwak, D. Yang, G. Zhang,
*The log-Brunn–Minkowski inequality*, Advances in Mathematics
231 (2012), 1974–1997,
DOI [10.1016/j.aim.2012.07.015](https://doi.org/10.1016/j.aim.2012.07.015).
Author-hosted full text:
[LBMI.pdf](https://math.nyu.edu/~yangd/papers/LBMI.pdf).

Precise locations inspected: Section 2, formulas (2.7)–(2.10), Lemma 2.1;
Section 3, the log-Minkowski/log-Brunn–Minkowski equivalence and the
Lp transfer; Theorem 1.8 for the planar strictness comparison. This note
independently derives the needed variation and all-dimensional equality
argument; it does not claim the known transfer machinery as novel.
The author's accessible PDF bears a February 25, 2013 manuscript date,
whereas the journal article is published in 2012; neither date is used
as a priority claim for a new result.

The recent He–Liu source was inspected only to confirm its dimensional
convention and the division of labor: Theorem 4 at
[arXiv:2510.21530v1](https://arxiv.org/html/2510.21530v1) concerns smooth
data on S^n (bodies in R^(n+1)). Its proof and applicability to the smooth
endpoint are assigned to a separate route. This note does not rely on it.

The local 091 scope document was read and its claimed general log-Wulff
inequality recognized as exactly (LBM); its actual formalization and
upstream analytic proof are **not audited in this note**. Accordingly,
the strongest verified result of this route remains conditional on (LBM).

| Mechanism | Evidence | Status | Exact remaining gap |
|---|---|---|---|
| Classical mixed-volume sandwich for Wulff differentiation | Equations (3)–(7), valid without smoothness | Complete relative to classical facts 1–4 | None in the displayed deduction |
| Log first variation followed by strict Jensen | Equations (8)–(11) and homothety recovery | Complete conditional deduction | Validity of the all-body log-BM input |
| Equal-measure volume comparison | Equations (12)–(13) | Complete conditional deduction | Same log-BM input |
| Direct surface-measure recovery cross-check | Equality of densities relative to common mu | Complete alternative recovery | Same log-BM input |
| Extend arbitrary-measure uniqueness to p=0 | Explicit equal-volume coordinate boxes | Falsified, permanently excluded | Cannot be repaired without extra data hypotheses |

Checkpoint estimate for this assigned route: conditional mathematical
derivation 97%; integration into an independently reviewed publication
package 0%. The remaining 3% is reserved for fresh adversarial checking
of this exact note, not evidence against a specific unresolved step.
The overall upstream validation, priority audit, smooth transfer, package,
and publication percentages must be recorded separately by the lead.
