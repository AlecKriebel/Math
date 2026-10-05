# Real-symmetric pre-Schwarzian bounds: rigorous partial results

Target: UnsolvedMath 2306086 / AMR-022-6086, Hayman–Lingham Problem 6.86.
Date: 2026-10-05. Status: partial; no sharp quantitative solution or novelty claim.

## 1. Exact scope and normalization

Let D = {z in C: |z| < 1}, let S consist of injective holomorphic functions on D with f(0)=0 and f'(0)=1, and let S_R consist of those f in S whose Taylor coefficients are real. Equivalently, f(conjugate z)=conjugate f(z). In particular f' never vanishes on D.

Put P_f=f''/f' and

    A_f(z) = (1-|z|^2) P_f(z) - 2 conjugate(z).

The usual universal bound is |A_f(z)| <= 4. For z != 0 this is equivalent to the disk estimate in Problem 6.86:

    |z P_f(z) - 2|z|^2/(1-|z|^2)| <= 4|z|/(1-|z|^2).

The chapter's class S and its normalization are supplied on printed page 114 of the governing 2018 draft; the target and update are on printed page 147. The target itself does not repeat the class definition or explicitly define rho in that display. We use rho=|z| and the standard schlicht-class interpretation. Postcomposition by a real affine map reduces any nonconstant real-on-real univalent analytic function to S_R without changing P_f.

For clarity distinguish three questions:

1. Can a bound depending only on |z| be made smaller for all points on that circle? No, by the real-axis examples below.
2. At an individual fixed nonreal z, does some strictly smaller radius, depending on z, work for every f in S_R? Yes, by the proof below.
3. What explicit sharp radius, or full value region, works at an arbitrary nonreal point? This investigation does not determine it.

The source asks for improvement without specifying a sharpness criterion. The second result settles the qualitative existence interpretation only. To avoid promoting a weaker interpretation as a full research solution, the overall target is left unresolved here.

At z=0 the source's displayed expression is identically zero. A_f(0)=2a_2 is an auxiliary normalized quantity, not that degenerate displayed expression.

## 2. The second-coefficient bound with its equality case

We recall the elementary area argument, including the part needed for rigidity. If an exterior univalent function has expansion

    H(w) = w + b_0 + sum_{n>=1} b_n w^(-n),  |w|>1,

then for each R>1 the area enclosed by the Jordan curve H(|w|=R) is

    pi [R^2 - sum_{n>=1} n |b_n|^2 R^(-2n)].

This follows by substituting the Laurent series in (1/(2i)) integral conjugate(H) dH and using Fourier orthogonality. The enclosed area is nonnegative; letting R decrease to 1 gives the area theorem

    sum_{n>=1} n |b_n|^2 <= 1.

The orientation is positive: H is conformal near infinity and maps the exterior of |w|=R onto the unbounded component of the complement of its image curve. The finite component has the displayed nonnegative area. Termwise integration is justified for R>1 by local uniform Laurent convergence.

For F in S, write F(z)=z+a_2 z^2+..., and define

    H(w) = 1/sqrt(F(w^(-2))) = w - (a_2/2) w^(-1) + ... .

Use the branch given by the analytic zero-free factor F(z)/z with value 1 at zero. H is holomorphic on |w|>1, odd, and univalent: equality of H values implies equality of the corresponding F values, hence the arguments w differ only by sign; oddness and nonvanishing rule out the negative sign. The area theorem gives |a_2|<=2. If |a_2|=2, all further negative Laurent coefficients vanish. Thus

    H(w)=w-lambda/w, |lambda|=1,
    F(z)=z/(1-lambda z)^2.

Conversely these Koebe rotations attain |a_2|=2. This proves the precise equality statement used below, rather than assuming it from a search snippet.

For a in D introduce the normalized Koebe transform

    T_a f(w) = [f((a+w)/(1+conjugate(a) w))-f(a)]
               /[(1-|a|^2) f'(a)].

It belongs to S. Its second coefficient is

    a_2(T_a f) = [(1-|a|^2) P_f(a)-2 conjugate(a)]/2
              = A_f(a)/2.

Consequently |A_f(a)|<=4, and equality forces T_a f to be a Koebe rotation. In particular, equality forces f(D) to be the complement of a single straight half-line, since its range is a complex affine image of a Koebe slit domain.

## 3. Equality rigidity in the real class

Suppose f in S_R and |A_f(a)|=4. Its image is symmetric about the real axis and is the complement of one straight ray. That ray must itself be invariant under complex conjugation. Its endpoint is therefore real and its outgoing direction is real. Because 0 lies in f(D), the omitted ray is either [c,infinity), c>0, or (-infinity,c], c<0.

The normalized map of D onto either of these ray complements is unique: the quotient of two such conformal maps is a disk automorphism fixing zero, and its derivative being 1 makes that automorphism the identity. Explicitly the maps with derivative 1 are

    k_+(z)=z/(1-z)^2,   k_-(z)=z/(1+z)^2,

with the corresponding omitted endpoint -1/4 or +1/4. To see why another endpoint is impossible, rescale k_+ or k_- by 4|c|. This gives a conformal map onto the stated slit complement with derivative 4|c|. Comparing it with f gives a zero-fixing disk automorphism, whose derivative has modulus 1, so 4|c|=1.

For either sign, direct algebra gives

    |A_{k_+}(z)|^2 = |A_{k_-}(z)|^2
                  = 16 - 48 (Im z)^2/|1-z^2|^2.                 (1)

For nonreal z the deficit on the right is strictly positive. Therefore equality |A_f(z)|=4 is impossible for every f in S_R at every nonreal z.

On the real interval (-1,1), direct differentiation instead gives

    A_{k_+}(x)=4,   A_{k_-}(x)=-4.

Thus the constant 4, and the source radius 4r/(1-r^2), cannot be uniformly decreased at all points of a circle of radius r>0, even within S_R.

## 4. A genuine uniform-in-f strict gap at each nonreal point

It is important not to confuse pointwise strictness for each f with a uniform strict bound over f. Compactness supplies the missing step.

The class S is compact for local uniform convergence. Here is the needed normal-family argument. The bound already proved gives

    |P_f(re^{i theta})| <= (4+2r)/(1-r^2).

Integrating the corresponding upper bound for the radial derivative of log|f'|, with f'(0)=1, yields

    |f'(z)| <= (1+|z|)/(1-|z|)^3,
    |f(z)| <= |z|/(1-|z|)^2.

Thus S is locally bounded and Montel-normal. A locally uniform limit retains derivative 1 at zero, so it is nonconstant. Hurwitz's theorem, applied to divided differences with a fixed second point (or the standard univalent-limit argument), implies that it is injective. Therefore S is also closed. S_R is a closed subset, since its reflection identity passes to limits, and is compact.

For fixed z, the functional f -> A_f(z) is continuous: derivatives converge locally uniformly and the limiting derivative does not vanish. Hence

    M(z) := max_{f in S_R} |A_f(z)|

exists. By Section 3,

    M(z)<4 for Im z != 0,      M(x)=4 for -1<x<1.               (2)

Consequently for each fixed nonreal z there exists epsilon(z)>0 such that

    |z P_f(z)-2|z|^2/(1-|z|^2)|
       <= [4-epsilon(z)] |z|/(1-|z|^2)    for every f in S_R.

One may choose epsilon(z)=4-M(z). This is an existence result, not an explicit computable formula.

The same proof gives a uniform epsilon_K>0 on every compact K contained in D\R. Indeed S_R x K is compact and (f,z) -> |A_f(z)| is jointly continuous. No such uniform positive gap extends to points approaching the real axis or to all of D\R; Section 6 provides explicit limiting obstructions.

## 5. Reduction by real disk automorphisms

For real a in (-1,1), let phi_a(w)=(w+a)/(1+a w) and g=T_a f. This transform preserves S_R and is bijective on S_R, with inverse T_{-a}. The chain rule gives

    A_g(w) = [(1+a conjugate(w))/(1+a w)] A_f(phi_a(w)).       (3)

The prefactor has modulus 1. Therefore M(w)=M(phi_a(w)). Also M(conjugate(w))=M(w).

The invariant

    delta(z) = |Im z|/|1-z^2|

is unchanged by these maps, because both its numerator and denominator are multiplied by (1-a^2)/|1+a z|^2. It belongs to [0,1/2), since

    |1-z^2|^2 = (1-|z|^2)^2 + 4(Im z)^2.

Every nonreal point can be carried to i t or -i t, with 0<t<1, by a real disk automorphism. One explicit choice, with x=Re z and r=|z|, is

    a = 2x / [1+r^2 + sqrt((1+r^2)^2-4x^2)],
    w = (z-a)/(1-a z).

The denominator is positive and |a|<1; the quadratic x a^2-(1+r^2)a+x=0 shows Re w=0. Moreover

    delta = t/(1+t^2),
    t = 2 delta/[1+sqrt(1-4 delta^2)].

Thus determining M on D reduces to determining the one-variable function M(i t). This is a true symmetry reduction, not an evaluation of that function.

## 6. Exact lower bounds and two distinct limiting obstructions

Equation (1) gives the Koebe lower bound

    M(z) >= 4 sqrt(1-3 delta(z)^2).

There is a second admissible map h(z)=z/(1-z^2). Its denominator never vanishes in D, and

    h(z)=h(w)  implies  (z-w)(1+z w)=0,

so it is injective in D. It has real coefficients and derivative 1 at zero. Direct differentiation at i t gives

    A_h(i t) = 8 i t/(1+t^2).

By the bijective transforms in Section 5, this yields a second lower bound at every point:

    M(z) >= 8 delta(z).

Together,

    max{4 sqrt(1-3 delta^2), 8 delta} <= M(z) < 4,             (4)

for nonreal z. The lower-bound branches meet at delta=1/sqrt(7). At z=i/2, the squared values are respectively 208/25 and 256/25, so the Koebe functions cannot alone be extremal there.

As delta decreases to 0 the Koebe bound tends to 4, and as delta increases to 1/2 the second bound tends to 4. In particular a universal epsilon>0 valid for every nonreal point is impossible. The second limit is already realized along z=i t, t increasing to 1. These are different boundary mechanisms: approach to the real geodesic, and approach to the unit circle away from its real endpoints.

The lower bound in (4) is not claimed to be the sharp answer. The numerical search below gives evidence that it is not sharp.

## 7. Why the convex-hull / typically-real relaxation loses the problem

The target is nonlinear in f, and the real univalent class is not convex. Consider the average of two admissible Koebe maps:

    q(z) = (k_+(z)+k_-(z))/2 = z(1+z^2)/(1-z^2)^2.

It has real coefficients and is typically real: each k_+ and k_- maps the upper half-disk into the upper half-plane, so their average does too. That sign property follows for any real normalized univalent map by reflection, injectivity, and its positive derivative at zero.

But

    q'(z) = (1+6z^2+z^4)/(1-z^2)^3

vanishes at z=i(sqrt(2)-1), a point of D. This zero is simple and q'' is nonzero there, so P_q has a pole. Therefore replacing S_R by its convex hull, or by the typically-real class, yields no finite bound for this functional near that point. An extreme-point theorem for linear functionals cannot simply be applied to f''/f'. This is an exact obstruction, not only the absence of a convexity proof.

## 8. Switched real-symmetric Loewner exploration

This section is an exploratory construction, with numerical values clearly separated from the preceding proofs. No numerical value here is a certified lower bound.

For real u in [-1,1], set

    p_u(w)=(1-w^2)/(1-2u w+w^2),    v_u(w)=-w p_u(w).

Writing u=cos(theta), p_u is the average of the two functions
(1+e^{i theta}w)/(1-e^{i theta}w) and its conjugate-parameter partner. Hence Re p_u>0 on D. The differential equation dw/ds=v_u(w), with piecewise constant real u(s), generates injective holomorphic disk self-maps, real under conjugation, fixing zero, with derivative e^(-s) there. Solutions stay in D because d|w|^2/ds=-2|w|^2 Re p_u(w)<=0. Holomorphic dependence and uniqueness, including local backwards uniqueness between any two trajectories meeting at a positive time, give injectivity.

For a tail parameter u_*, define

    h_{u_*}(w)=w (1-w)^(u_*-1) (1+w)^(-u_*-1),

with branches normalized at zero. Its logarithmic derivative satisfies

    w h'_{u_*}(w)/h_{u_*}(w) = 1/p_{u_*}(w).

The real part is positive, so the standard starlikeness criterion implies that h_{u_*} belongs to S_R. In the saved experiment u_*=+1 or -1 at every returned maximizer, giving an ordinary Koebe map and requiring no fractional-power evaluation. For a finite flow w_T, the map e^T h_{u_*}(w_T(z)) therefore belongs to S_R.

For derivative jets d=partial_z w, e=partial_z^2 w, the equations used are

    w_dot=v_u(w),  d_dot=v'_u(w)d,
    e_dot=v''_u(w)d^2+v'_u(w)e,
    P_f(z)=P_{h_{u_*}}(w_T(z)) d_T(z)+e_T(z)/d_T(z).

The saved code searches two constant-control time intervals and a tail parameter, then recomputes each returned point at a tighter floating-point tolerance. At t=0.45 it finds |A_f(i t)| approximately 3.61249, whereas the exact elementary lower bound is approximately 3.04599. This is evidence that the elementary lower-bound envelope is not sharp. It is not a proof of that inequality: no interval ODE error enclosure was performed. The construction class is mathematically admissible, but floating-point evaluation and optimization are not proof certificates and do not establish an upper bound.

## 9. Final limits

The qualitative strictness theorem, compact-set gap, covariance identity, exact elementary lower bounds, and convex-hull obstruction are proved above. The explicit sharp function M(i t), its extremizers, and the full variability region have not been determined. No independence or novelty claim is made for these elementary consequences of the classical area theorem. The overall research target remains incomplete under a quantitative/sharp interpretation.

Primary scope reference: W. K. Hayman and E. F. Lingham, Research Problems in Function Theory (New Edition), arXiv:1809.07200v2, https://arxiv.org/abs/1809.07200v2, printed pages 114 and 147. This note contains an independently authored treatment, not copied source prose.
