# Route 2: an exact obstruction to a stability-only proof

## Scope warning

The construction below is a potential for a nonnegative Schroedinger quadratic form. It is not asserted to equal lambda* f'(u*) for any extremal semilinear solution. It is therefore NOT a counterexample to the target. It falsifies the proposed implication from form stability, isolated smoothness, and averaged two-sided control alone to a pointwise upper bound.

## Proposition

For every integer n>=3 there is a positive V in C^infinity(B_1 minus {0}), locally integrable on B_1, with all of the following properties:

1. For every phi in C_c^1(B_1), integral V phi^2 <= (3/4) integral |grad phi|^2.
2. There are constants 0<c_n<=C_n<infinity such that

       c_n <= r^(2-n) integral_(B_r) V <= C_n,   0<r<1/2.

3. V belongs to L^q(B_1) for every 1<=q<n/2.
4. limsup_(x->0) |x|^2 V(x) = infinity.

## Construction and proof

Write H_n=(n-2)^2/4. Choose a nonnegative smooth bump psi supported in the unit ball, with psi(0)=1. For k>=1 put

    r_k=2^(-k),  x_k=r_k e_1,  rho_k=2^(-3k-4),  a_k=2^(-k),
    W(x)=epsilon sum_(k>=1) a_k rho_k^(-2) psi((x-x_k)/rho_k),
    V(x)=H_n/(2|x|^2)+W(x).

The support balls are disjoint, contained in B_1, and accumulate only at zero. For adjacent indices their radii sum is strictly less than r_k-r_(k+1); their projections to the first axis are ordered and disjoint. Also rho_k/r_k=2^(-2k-4)<=1/64. Thus the sum is locally finite off zero.

Let P=||psi||_(L^(n/2)(R^n)). Let S_n be any Sobolev constant in

    ||phi||_(L^(2n/(n-2)))^2 <= S_n integral |grad phi|^2.

Set epsilon = [4 S_n max(1,P)]^(-1). The scale-invariant norm calculation gives

    ||a_k rho_k^(-2) psi((.-x_k)/rho_k)||_(n/2)=a_k P.

Since sum_(k>=1) a_k=1, the triangle inequality gives ||W||_(n/2)<=epsilon P<=1/(4S_n). Holder and Sobolev imply

    integral W phi^2 <= (1/4) integral |grad phi|^2.

For completeness, Hardy's inequality follows by expanding

    0 <= integral |grad phi + ((n-2)/2) x|x|^(-2) phi|^2
       = integral |grad phi|^2 - H_n integral phi^2/|x|^2.

One can first cut out a small ball and then pass to the limit; for n>=3 the boundary error vanishes for smooth phi. Consequently, the inverse-square summand contributes at most one half of the Dirichlet energy. This proves item1.

The lower averaged bound follows exactly from the baseline term:

    r^(2-n) integral_(B_r) H_n/(2|x|^2)
        = H_n n omega_n/[2(n-2)] >0.

The upper averaged bound is the cutoff argument of Route 1, now with form bound3/4:

    r^(2-n) integral_(B_r) V <= (3/4) omega_n(2^n-1).

The inverse-square function is in L^q(B_1) exactly for q<n/2; W is already in L^(n/2)(B_1), hence is also in those lower L^q spaces on the finite-volume ball. This proves item3.

Finally, disjoint supports and psi(0)=1 give the exact identity

    r_k^2 V(x_k)=H_n/2 + epsilon r_k^2 a_k rho_k^(-2)
               =H_n/2 + epsilon 2^(3k+8) -> infinity.

This proves item4.

## What this rules out, and what it does not

Even a strict stability margin, smoothness away from a single exceptional point, two-sided scale-invariant mass bounds at every scale, and all subcritical L^q integrability cannot by themselves give the target upper estimate. The semilinear relation between u and V, convexity of one common f, global boundary data, and extremal-branch selection must do essential work. The present construction supplies none of those missing links and makes no claim of a new result in potential theory.

Status: exact obstruction to a weakened implication; target unresolved.
