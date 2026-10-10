# Route 3: differentiating the potential and attempting annular Harnack control

## Exact identity and scope

For this route ONLY, add f in C^3 on the range under consideration, and work away from the isolated singularity where u is classical. Put F=lambda* f and V=F'(u). The chain rule gives

    -Delta V = F''(u) F(u) - F'''(u) |grad u|^2
             = (lambda*)^2 f''(u) f(u)
                         - lambda* f'''(u) |grad u|^2.           (1)

The original differentiable-convex assumptions do not justify a C^3 calculation without this additional assumption, and even smooth convex nonlinearities do not give a useful sign to the last term. In particular, V is not automatically subharmonic, harmonic, or a solution of a linear equation with uniformly bounded rescaled coefficients.

If one additionally had f'''>=0 and f'' f <= A(f')^2, then (1) would give -Delta V<=A V^2. Neither condition is furnished by the source hypotheses. Also, this critical quadratic inequality has not yielded an L^infinity estimate here; invoking an L^q coefficient theorem with q>n/2 would add another missing assumption.

## Exact tests against hidden nonlinearity assumptions

### A. Convexity does not imply f'''>=0

Take

    f(t)=exp(t) [1+(2/5)sin(t)].

This is smooth and positive on R. Its first two derivatives are

    f'(t)=exp(t)[1+(2/5)(sin(t)+cos(t))],
    f''(t)=exp(t)[1+(4/5)cos(t)].

They are strictly positive because 1-(2/5)sqrt(2)>0 and 1-4/5>0. The source integrability and superlinearity hold because (3/5)exp(t)<=f(t)<=(7/5)exp(t). But

    f'''(3pi/4)=exp(3pi/4)[1-(4/5)sqrt(2)]<0.

Thus the troublesome sign really occurs inside the smooth source class.

### B. Convexity does not bound f''f/(f')^2

Choose b in C_c^infinity((-1,1)), b>=0, integral b=1, and b(0)>0. Define H(s)=integral_(-infinity)^s b and h(s)=integral_(-infinity)^s H. Then h>=0, h'=H in [0,1], h''=b>=0, and h vanishes for s<=-1. For k>=1 set

    t_k=k log(2),  a_k=2^(-k),  delta_k=2^(-k^2-4),
    f(t)=exp(t)+sum_(k>=1) a_k delta_k h((t-t_k)/delta_k).

The sum is locally finite, so f is C^infinity. All summands are nonnegative, nondecreasing, and convex, and exp(t) makes f,f',f'' strictly positive. Since f>=exp(t), both source growth conditions hold. At t_k,

    f(t_k)>=2^k,
    f'(t_k)<=2^k+sum a_j<=2^k+1<=2^(k+1),
    f''(t_k)>=b(0) a_k/delta_k=b(0)2^(k^2-k+4).

Consequently,

    f''(t_k) f(t_k)/f'(t_k)^2 >= b(0)2^(k^2-2k+2) -> infinity.

This is an exact smooth source-admissible nonlinearity test, not a solution of the PDE and not an extremal counterexample.

## A conditional annular bridge

If V>0 and one could prove |grad log V(z)|<=K/|z| in a punctured neighborhood, then for y in B_(|x|/4)(x), integration on the straight segment gives

    V(y)>=exp(-K/3)V(x).

Every segment point has radius at least 3|x|/4. Route 1, with theta=1 and c=exp(-K/3), would therefore give

    |x|^2 V(x)<=16(2^n-1)exp(K/3).

But grad log V=(f''(u)/f'(u)) grad u. No such pointwise bound has been derived here from the source hypotheses or the averaged stability estimate. Using a Harnack constant depending on the already-unknown rescaled supremum of V would be circular.

## Remaining gap

The differentiation/Harnack route requires a new quantitative spatial estimate, not just convexity or an unqualified invocation of elliptic regularity. The explicit nonlinearities above disprove two tempting hidden assumptions. No universal upper estimate has been obtained.

Status: blocked at the nonconcentration/regularity step.
