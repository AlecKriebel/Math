# A quadratic proxy and an endpoint kernel for convex-body SOS upper bounds

Theorem and explicit construction, 2026-10-11.

The claim concerns the normalized Lebesgue-measure hierarchy. No novelty claim is made.

## 1. Exact claim

Let K be a compact convex subset of R^n with nonempty interior, n >= 1, and let f be a real polynomial. All integrals below are with respect to n-dimensional Lebesgue measure. Put

    f^(r) = inf { integral_K f(x) q(x) dx :
                 q is a sum of squares, degree(q) <= 2r,
                 integral_K q(x) dx = 1 }.

For every integer r >= 1, the construction below proves

    0 <= f^(r) - min_K f <= C_n G / r^2,

where L = n+2,

    C_n = 4 L^2 (pi/2)^(2L) (1 + 2^(n+2)),

and G is the maximum of a nonnegative quadratic Taylor upper proxy defined below. In particular the constant is finite for each fixed K,f. The estimate asserts an upper rate, not a two-sided Theta rate for every f. For constant f the error is zero. It does not assert this rate for arbitrary reference measures.

## 2. Quadratic proxy

Fix any a in K with f(a) = min_K f. Let

    gamma = 1 + (1/2) max_{x in K} || Hessian f(x) ||_op,
    ell(x) = gradient f(a) dot (x-a),
    g(x) = ell(x) + gamma ||x-a||^2,
    G = max_{x in K} g(x),
    u(x) = g(x)/G.

Because K is convex, the segment a+s(x-a), 0 <= s <= 1, lies in K. Minimality of a and the right derivative at s=0 imply ell(x) >= 0 for all x in K. Taylor's formula with integral remainder on this same segment gives

    0 <= f(x)-f(a) <= ell(x) + (gamma-1)||x-a||^2 <= g(x).

The added 1 in gamma guarantees g(x)>0 for x != a. Nonempty interior ensures K contains such an x, so G>0. Thus u is a degree-at-most-two polynomial with 0<=u<=1 on K, u(a)=0. For 0<=s<=1,

    g(a+s(x-a)) = s ell(x) + s^2 gamma ||x-a||^2 <= s g(x).      (1)

Only the finite Hessian bound and the first-order constrained-minimum condition are used here. The argument also applies to objectives that are C^2 on an open neighborhood of K, since the density is built from the quadratic proxy rather than from f itself.

## 3. Relative sublevel-volume growth

For every t>0 let

    S_t = {x in K : u(x)<=t},       F(t)=vol_n(S_t).

For 0<s<=t, put alpha=s/t. By convexity of K and (1),

    a + alpha(S_t-a) is a subset of S_s.

Lebesgue measure scales by alpha^n, hence

    F(s) >= (s/t)^n F(t),
    F(t) <= (t/s)^n F(s).                                      (2)

These assertions hold also for t>1, when S_t=K. In particular, for 0<s<=1,

    F(s) >= s^n vol_n(K) > 0.                                  (3)

No boundary smoothness, semialgebraicity, local cube structure, or positive solid-angle lower bound is required. The key is the relative upper estimate in (2), not just the absolute lower estimate in (3).

## 4. An explicit polynomial endpoint kernel

For an integer m>=1 set N=2m+1 and define

    A_m(t) = (1 + 2 sum_{k=1}^m T_k(1-2t))/N,

where T_k is the Chebyshev polynomial determined by T_k(cos theta)=cos(k theta). Thus A_m is a real polynomial of degree m and A_m(0)=1.

For 0<t<=1, put v=arcsin(sqrt(t)), so 1-2t=cos(2v), 0<v<=pi/2. The finite geometric-sum identity gives

    A_m(t) = sin(Nv)/(N sin(v)) = sin(N arcsin(sqrt(t)))/(N sqrt(t)).      (4)

The triangle inequality applied to the defining cosine sum gives |A_m(t)|<=1; (4) also gives |A_m(t)|<=1/(N sqrt(t)). Therefore

    |A_m(t)| <= min(1, (N sqrt(t))^(-1)),       0<t<=1.           (5)

Put h=N^(-2). If 0<t<=h, then arcsin(sqrt(t)) <= (pi/2)sqrt(t), hence 0<Nv<=pi/2. On this interval sin z >= 2z/pi, while v>=sqrt(t). Substitution in (4) gives

    A_m(t) >= 2/pi,                          0<=t<=h.           (6)

At t=0, (6) follows from A_m(0)=1. The elementary arcsine inequality used above follows by convexity of arcsin on [0,1], which places its graph below the chord joining (0,0) and (1,pi/2).

## 5. Moment ratio: the logarithm-free step

Let L=n+2 and define Q_m(x)=A_m(u(x))^(2L). This is nonnegative everywhere in R^n and is exactly the square of the polynomial A_m(u(x))^L. From (6),

    integral_K Q_m dx >= (2/pi)^(2L) F(h) > 0.                  (7)

By (5), Q_m<=1 on K and, when u>0, Q_m <= (h/u)^L.
Decompose K into {u<=h} and the pairwise disjoint shells

    E_j={x in K : 2^j h < u(x) <= 2^(j+1) h}, j=0,1,2,... .

Only finitely many shells are nonempty because u<=1. On the core,

    integral_{u<=h} u Q_m dx <= h F(h).

On E_j, use u<=2^(j+1)h, Q_m<=2^(-jL), and (2) to obtain

    integral_{E_j} u Q_m dx
      <= 2^(j+1) h 2^(-jL) F(2^(j+1)h)
      <= h F(h) 2^(n+1) 2^(j(n+1-L)).

Since L=n+2, the geometric sum over j>=0 is 2. Consequently,

    integral_K u Q_m dx <= h F(h) (1+2^(n+2)),

and division by (7) yields

    (integral_K u Q_m dx)/(integral_K Q_m dx)
       <= (pi/2)^(2L)(1+2^(n+2))/(2m+1)^2.                     (8)

The oscillation and zeros of A_m cause no difficulty: the denominator uses its uniformly positive core, and every tail estimate is an absolute-value upper bound. No probability mass is silently discarded outside a simplex or local model.

## 6. Degree, normalization, and all integer orders

For r>=2L choose m=floor(r/(2L))>=1. Since degree(u)<=2,

    degree(A_m(u)^L) <= 2mL <= r,
    degree(Q_m) <= 4mL <= 2r.

Thus

    q_r(x)=Q_m(x)/(integral_K Q_m dx)

is a feasible, single-square SOS density for the exact hierarchy in Section 1. Equations (8) and f-f(a)<=Gu give

    0 <= f^(r)-f(a)
       <= integral_K (f-f(a)) q_r dx
       <= G (pi/2)^(2L)(1+2^(n+2))/(2m+1)^2.

For r>=2L, writing b=r/(2L)>=1 gives 2 floor(b)+1>=b, so

    (2m+1)^(-2) <= 4L^2/r^2.

This proves the stated estimate for r>=2L. For 1<=r<2L use the feasible constant density 1/vol_n(K), whose error is at most G; since C_n/r^2>=1, the same estimate holds. This finishes the proof for every integer r>=1.

## 7. What this does and does not establish

The displayed construction proves the scoped Lebesgue-normalized O_{K,f}(r^-2) statement for all fixed convex bodies. A source still listing a weaker bound does not itself establish novelty. No claim that the proof is new is made.

The result does not establish O(r^-2) for every unspecified reference measure: the change-of-variables volume identity behind (2) is specific here to Lebesgue measure. It does not prove the same rate for the weaker push-forward hierarchy using only polynomials of the original objective f, because our density instead uses the quadratic proxy g. It does imply the analogous rate for that push-forward construction when the objective itself is convex, after normalizing its range and adapting the degree count.

No universal positive lower bound applies for each f, since constants have zero error. This proof supplies no counterexample, no exact asymptotic coefficient, and no sharp dimension dependence.


## 8. Source context

The normalization integral_K q dx=1 is essential. Laurent's 2018 workshop contribution prints an incomplete integral constraint in its equations (3) and (4); this document explicitly supplies the probability-density normalization used in the full papers. This is a mathematical scope repair, not an OCR correction.

Slot and Laurent's Theorem 11 proves O(log^2(r)/r^2) for this same convex-body Lebesgue hierarchy. Their Lemma 20 and Corollary 5 control the tail by a global volume bound, divided by a degree-dependent absolute lower bound for the normalization. In the present proof, the relative bound (2) ties each tail shell to the same F(h) appearing in the denominator, so that this factor cancels before the geometric series is summed. The Taylor upper proxy is already a standard reduction in their Lemma 4; the complete endpoint-kernel and relative-volume argument is proved here without importing a convergence theorem.

References (public primary sources):

1. M. Laurent, joint work with E. de Klerk, “Convergence analysis of Lasserre measure-based approximations for polynomial optimization,” Oberwolfach Report 50/2018, printed pp. 2991-2993, PDF pp. 23-25. https://ems.press/journals/owr/articles/16633
2. L. Slot and M. Laurent, “Improved convergence analysis of Lasserre's measure-based upper bounds for polynomial minimization on compact sets,” arXiv:1905.08142v2, Theorem 11, Lemma 20, Corollary 5, and concluding questions. https://arxiv.org/abs/1905.08142 ; DOI: https://doi.org/10.1007/s10107-020-01468-3
3. L. Slot and M. Laurent, “Near-optimal analysis of Lasserre's univariate measure-based bounds for multivariate polynomial optimization,” arXiv:2001.11289v2. https://arxiv.org/abs/2001.11289 ; DOI: https://doi.org/10.1007/s10107-020-01586-y
4. M. Laurent and L. Slot, “An Overview of Convergence Rates for Sum of Squares Hierarchies in Polynomial Optimization,” final 2026 chapter, Table 1 (printed p. 159; PDF p. 11). https://doi.org/10.1007/978-981-95-1446-5_8 ; author-hosted final chapter: https://ir.cwi.nl/pub/36052/36052.pdf
