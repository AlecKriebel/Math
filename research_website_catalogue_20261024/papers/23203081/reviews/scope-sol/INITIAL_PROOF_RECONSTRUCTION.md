# Row 189 — original-source INITIAL reconstruction

Status: INITIAL only; the target conclusions remain hypotheses for the full review. This document checks the native argument conditional on explicitly isolated imported inputs. It does not certify those inputs, the upstream logarithmic Brunn–Minkowski theorem, priority, novelty, or any packaged verification assertion.

Scope: Zenodo record 23203081, outer published `zenodo-files/paper.pdf` (five pages, SHA-256 `6192382c55a3ac50ee76ce2514579a330dda1da6d873a32944a03bef26ed3179`) and the native `main.tex`. The complete native published README and metadata/Description were also read before these notes. Thus this is an independent calculation/checking of an already-read author argument, not a blind rediscovery. See `INITIAL_EXPOSURE_LEDGER.md`.

## Exact targets and success criteria

H1. For each ambient integer n >= 2, parameter 0 <= p < 1, and strictly positive even f in C-infinity(S^(n-1)), there exists exactly one positive even h in C-infinity with

    h^(1-p) det Q(h) = f,   Q(h) = spherical Hessian(h) + h I > 0.

The determinant is on an (n-1)-dimensional tangent space. The solution class consists of support functions of smooth full-dimensional origin-symmetric bodies of positive Gauss curvature. No normalization V=1 is imposed. A proof must establish existence, preservation of symmetry, strict interiority of the origin, smoothness, positive curvature, and uniqueness in precisely this class.

H2. If 0 < p < 1 and K,L are full-dimensional compact origin-symmetric convex bodies, equality of the finite Borel measures S_(K,p)=S_(L,p) implies K=L. Smoothness and absolute continuity are not assumptions here. This is a uniqueness assertion for bodies that already exist, not an existence assertion for every measure.

LBM input L. For all such origin-symmetric bodies and 0<=t<=1,

    V(W[h_K^(1-t) h_L^t]) >= V(K)^(1-t) V(L)^t.

This is explicitly imported. No equality classification of L is needed by the native deduction. Initial success means giving a checkable conditional chain and isolating every external interface; full success later requires verifying that the cited primary results actually supply all these interfaces.

## Normalizations checked directly

For full-dimensional origin-symmetric K, h_K is positive continuous even; min h_K>0. The ordinary Minkowski identity gives integral h_K dS_K = n V(K). Therefore nu_K = h_K dS_K/(n V(K)) is probability, whereas the unnormalized cone-volume measure is h_K dS_K/n and S_(K,0) is n times that measure. These three measures must not be interchanged.

Under h -> c h, Q -> c Q and det Q -> c^(n-1) det Q. Consequently both the PDE density and S_(K,p) scale by c^(n-p). In the claimed range n-p>0, fixed unnormalized data fix scale. At p=0, integral f d-omega=nV. Round d-omega is unnormalized area; there is no extra sphere-area factor.

## Wulff first variation: own inequality check

For a positive continuous a, W[a] contains the ball of radius min a and is bounded by the ball of radius max a. Thus the volumes and surface measures used below are nondegenerate. It is not necessary that a itself be a support function.

Let A=W[a]. A boundary point must have an active constraint: if x.u<a(u) for every u, compactness of the sphere gives a uniform positive slack, making x interior. At a boundary point with unique outer normal, each active constraint direction equals that normal. Hence h_A=a at the directions seen by S_A, up to S_A-null sets. This uses the standard almost-everywhere uniqueness of the outer normal on the boundary of a convex body. Always h_A<=a.

For C=W[b], denote X=V(A)^(1/n), Y=V(C)^(1/n). The classical mixed-volume inequality, applied in both orders, yields

    integral (b-a) dS_C / (n V(C)^((n-1)/n))
       <= Y-X
       <= integral (b-a) dS_A / (n V(A)^((n-1)/n)).

The right inequality follows from integral b dS_A >= integral h_C dS_A = n V_1(A,C) >= n X^(n-1) Y and integral a dS_A=nX^n. The left follows from integral a dS_C >= n V_1(C,A) >= n Y^(n-1) X and integral b dS_C=nY^n. This verifies both inequality signs without supposing pointwise equality a=h_A everywhere.

For a_t=h_K+t g+o(t) uniformly, min h_K>0 implies (1-epsilon)h_K <= a_t <= (1+epsilon)h_K, and therefore the corresponding inclusions of dilates of K. The bodies tend to K in Hausdorff distance. Weak convergence of S_(W[a_t]), uniform convergence of (a_t-h_K)/t, and the above sandwich imply

    derivative at 0 V(W[a_t]) = integral g dS_K.

For negative t the sandwich order reverses after division; both endpoints still have the same limit. This checks the two-sided lemma. Only the right derivative is needed for LBM.

Take a_t=h_K exp(t log(h_L/h_K)), so g=h_K log(h_L/h_K). Logarithmic differentiation of L at t=0 gives

    integral log(h_L/h_K) dnu_K >= (1/n) log(V(L)/V(K)).       (LM)

The factor n comes from the normalization of nu, not from the differential of log itself.

## Positive p and the singular surface-measure equality issue

Let r=h_L/h_K, positive and bounded above and below. For p>0,

    V_p(K,L)/V(K) = integral exp(p log r) dnu_K
       >= exp(p integral log r dnu_K)
       >= (V(L)/V(K))^(p/n).

The first step is Jensen for a strictly convex exponential, and the second is LM with its direction preserved because p>0. Equality of the endpoints forces equality in both steps. Thus r=c only nu_K-almost everywhere, equivalently S_K-almost everywhere, and the second step fixes c=(V(L)/V(K))^(1/n).

Almost-everywhere equality is not promoted to pointwise equality when S_K is singular. Instead,

    V_1(K,L)=(1/n) integral h_L dS_K = c V(K)
            = V(K)^((n-1)/n) V(L)^(1/n).

The classical equality case for Minkowski's first inequality gives L=cK+x. Since both bodies have center 0, boundedness forces x=0: two distinct centers would imply a nonzero translation preserves the body. Conversely L=cK realizes equality directly. This establishes the strict mixed-volume transfer conditional on L and the classical inequality/equality interface.

If mu=S_(K,p)=S_(L,p), then V_p(K,L)=(1/n) integral h_L^p dmu=V(L) and the reversed expression is V(K). The transfer gives

    V(L)^(1-p/n) >= V(K)^(1-p/n),
    V(K)^(1-p/n) >= V(L)^(1-p/n).

In the asserted range 1-p/n>0, both volumes coincide. The equality characterization then gives K=L. No smoothness, density, or a support-wide surface-measure assertion entered this step.

## Smooth p=0: own local path and derivative check

Let h0,h1 be two admissible p=0 solutions with the same f. Set M=integral f d-omega, v=M/n and w=log(h1/h0). Both volumes are v, and both nu measures are f d-omega/M. Define, on origin-symmetric bodies,

    F(L)= (1/M) integral f log h_L d-omega - (1/n) log V(L).

LM at either solution proves it is a global minimizer of F. Applying LM in both orders between h0,h1 shows the weighted logarithmic integrals are equal. Consequently integral f w=0.

Set q_t=h0 exp(tw). Positive definiteness of Q(h0), compactness of the sphere and smoothness of t -> q_t give Q(q_t)>0 for |t| sufficiently small. Such q_t are themselves positive even support functions. Thus no assertion about smoothness of an entire Wulff interpolation on [0,1] is needed. For small t>=0, L gives V(q_t)>=v. The logarithmic integral in F(q_t) is constant because integral f w=0. Hence F(q_t)<=F(h0); global minimality supplies the reverse inequality. It follows that V(q_t)=v and q_t is a minimizer for an interval of nonnegative t.

For any smooth even additive test eta, openness of positivity and positive curvature allows a two-sided sufficiently small variation q_t+s eta. At fixed such t,

    0=(1/M) integral f eta/q_t d-omega
      -(1/(n v)) integral eta det Q(q_t) d-omega.

Since nv=M and the integrand is even, arbitrary even tests imply q_t det Q(q_t)=f pointwise. The one-sided interval of identities suffices for two right derivatives at t=0, because q_t is a smooth explicit path.

Write h=h0, Q=Q(h), A=Q(hw). Direct product differentiation gives

    q'_0=hw,  q''_0=hw^2,
    Q(hw^2)=2w A - w^2 Q + 2h dw tensor dw.

Differentiate log q_t + log det Q(q_t)=log f. The first derivative is

    w + tr(Q^-1 A)=0.

The second derivative of log q_t is zero, not w^2. The remaining derivative is

    0=tr(Q^-1 Q(hw^2)) - tr((Q^-1 A)^2)
     =2w tr(Q^-1 A) -(n-1)w^2
        +2h Q^-1(dw,dw) - tr((Q^-1 A)^2)
     =-(n+1)w^2 +2h Q^-1(dw,dw) - tr((Q^-1 A)^2).

This checks the ambient/tangent dimension coefficient n+1. Although Q^-1 A need not be symmetric, it is similar to the real symmetric Q^-1/2 A Q^-1/2, so the trace of its square is nonnegative. At a global maximum and a global minimum of w, dw=0 and the equation forces each extremal value to be zero. Thus w=0 identically and h0=h1. This is a conditional smooth endpoint deduction, including n=2, with no imported LBM equality case.

## Existence and regularity: exact conditional gap

The source invokes BBCY Theorem 1.7 and Proposition 7.3 for a full-dimensional symmetry-preserving measure solution when -n<p<1 and f is bounded above and below positively. The required action G={I,-I} preserves even f. If that exact primary interface is valid, the resulting origin symmetry plus full dimension yields 0 in int K and h>=m>0. Existence is not proved from LBM in this note.

For n>=3 the regularity chain is imported. The precise needed initial conclusion is a C1 boundary (and, as stated natively, no boundary segment) for the solution with 0 interior, via BBC Theorem 1.1(i). The elementary dual implication can be checked: C1 boundary of K makes the polar K-polar strictly convex; its gauge is the homogeneous support function h_K. On any affine hyperplane avoiding 0, two distinct points cannot lie on the same positive ray, so strict convexity of the polar gives the strict-convexity hypothesis of a support chart. Chou-Wang Proposition 1.2 is then invoked to obtain C^(2,alpha) regularity, and higher regularity is asserted. Whether its exact weak-solution notion, chart hypotheses, p range and dimension range apply must be checked in the primary papers after INITIAL.

Once h is C2 and remains a support function, Q(h)>=0. The measure equation then identifies det Q(h)=f h^(p-1)>0 pointwise. A positive determinant with nonnegative eigenvalues forces every eigenvalue positive. Compactness gives a uniform positive lower eigenvalue; positive min h removes the singularity in h^(p-1). Smooth elliptic bootstrapping can then apply. These algebraic and compactness steps do not supply the missing initial regularity theorem themselves.

For n=2, provided the weak measure solution exists, the equation is the distributional ODE h''+h=f h^(p-1). Positive continuous h gives a continuous right side. Therefore h is C2; repeated one-dimensional differentiation gives smoothness and h''+h>0. This is a direct lower-dimensional regularity check, conditional only on existence and the standard measure/support-function identification.

## Strongest INITIAL result and non-promoted claims

The native follow-on deductions have a checkable conditional mechanism: LBM plus classical nonsmooth mixed-volume facts imply H2 and smooth uniqueness in H1; existence and higher-dimensional regularity require the cited primary interfaces. This statement is not an unconditional validation of H1 or H2. The upstream analytic theorem, exact cited existence/regularity statements, formal scope, package checks, and priority/novelty assertions remain unread or unverified at this gate. No finite computation can discharge the general upstream theorem merely by agreeing on examples. No scientific execution occurred.
