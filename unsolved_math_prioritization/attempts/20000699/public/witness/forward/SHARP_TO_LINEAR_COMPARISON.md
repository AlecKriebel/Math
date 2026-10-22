# Quantified sharp-kernel and endpoint comparison

Row 1795 / ID 20000699, shared pass 1. This authored lemma supplements FORWARD_TRANSFER.md. It gives the two elementary approximation errors needed before a separate CK Mellin calculation. It invokes no arithmetic conjecture and no GRH. The density is unchanged.

## 1. Objects and result

Use all notation and the corrected parameter range 0<psi<=phi<1 from FORWARD_TRANSFER.md. In particular B=2 pi A, eta=exp(B/T)-1, N=floor(T^lambda), r=a/log N, and D_T is the closed four-shift polydisc of radius c/log N. Write

    D_z(h) = [zeta(1+gamma-alpha) zeta(1+delta-beta)]^(-1)
             * sum_(q>=1) c_q(h)F_(alpha,gamma)(q)F_(beta,delta)(q)/q^2,
    s=alpha+beta.

Then dm_z^+(x,h)=dm_z^-(x,h)=D_z(h)x^(-s) dx.

Define the linear kernels

    Ktilde_h^sigma(x) = x^(-1) f(sigma T h/(2 pi x)),  sigma in {+1,-1},

and the corresponding main functional

    Qlin_(T,N)(z)
      = exact diagonal
        + T sum_(h>=1) D_z(h) integral_1^N x^(-s)
                        [Ktilde_h^+(x)+Ktilde_h^-(x)] dx.            (1.1)

This is a finite h sum: only h<=floor(BN/T) can contribute. For sufficiently large T, its lower endpoint can equally be written 0 because every nonzero kernel requires x>=Th/B>=T/B>1.

There is a constant C, depending only on fixed parameters and w, such that

    sup_(z in D_T) |Q_(T,N)(z)-Qlin_(T,N)(z)|
       <= C N/(T (log N)^2).                            (1.2)

Both main functionals are holomorphic on a neighborhood of D_T. Therefore every mixed derivative in two distinct shift variables at the center has comparison error at most

    C rho^(-2) N/(T (log N)^2)
       = O(N/T)
       = o(T),                                                     (1.3)

using lambda<2. The diagonal has not been approximated. Neither (1.2) nor (1.3) identifies a Mellin main term or suppresses a residue from a subsequent contour shift.

## 2. Explicit elementary pointwise and summatory profile bounds

Here is a self-contained bound sufficient for summing both errors. Put

    d1=alpha-gamma, d2=beta-delta,
    d0=1-2^(-7/8)>0.

Take T sufficiently large that |d1|,|d2|<=1/8. For each prime put

    b_p = p^(-2+Re(d1+d2))
          / [(1-p^(-1+Re d1))(1-p^(-1+Re d2))].

The absolute Ramanujan series has an Euler product bounded by

    sum_(q>=1) |c_q(h)F_(alpha,gamma)(q)F_(beta,delta)(q)|/q^2
      <= product_p [1+|c_p(h)| b_p].                                (2.1)

This follows from the squarefree support of F, multiplicativity of c_q(h), and |1-p^(-1+d_j)|>=1-p^(-1+Re d_j). Convergence follows from the bounds below. Since |c_p(h)|=1 for p not dividing h and |c_p(h)|=p-1 for p dividing h,

    b_p <= d0^(-2) p^(-7/4).

Consequently the contribution of all primes not dividing h is at most

    C_abs = exp(d0^(-2) sum_p p^(-7/4))
          <= exp(d0^(-2)(zeta(7/4)-1)).                             (2.2)

For 1<=h<=N, every p dividing h is <=N and |d1|,|d2|<=2c/log N. Hence

    (p-1)b_p <= e^(4c) d0^(-2)/p = C1/p.

Choose the fixed integer k=ceil(C1). Then

    product_(p|h) (1+C1/p)
       <= [product_(p|h)(1+1/p)]^k
       <= [sum_(d|h) 1/d]^k
       <= (1+log h)^k.                                             (2.3)

No estimate for the distribution of primes is needed here.

The local function g(v)=1/zeta(1+v), with g(0)=0, is holomorphic near v=0 and has g'(0)=1. Choose fixed delta0>0 and M_zeta<infinity such that |g(v)|<=M_zeta|v| for |v|<=delta0. Taking T still larger if necessary,

    |g(gamma-alpha)g(delta-beta)|
       <= 4 M_zeta^2 c^2/(log N)^2.

Combining (2.1)--(2.3), for every integer 1<=h<=N and every z in D_T,

    |D_z(h)| <= C_D (1+log h)^k/(log N)^2,                         (2.4)

where C_D=4 M_zeta^2 c^2 C_abs. The same proof on a slightly larger shift polydisc gives local holomorphy and domination. The reciprocal zeta zeros have been retained, not discarded; they explain the two logarithmic savings in this bound.

Finally, for 1<=x<=N and z in D_T, r>=0 gives

    |x^(-s)| <= exp(2c) = C0.                                     (2.5)

A stronger summatory estimate removes the harmless pointwise logarithmic loss. For squarefree q,

    |c_q(h)| = product_(p|q) [1+(p-2) 1_(p|h)].

Expand the product and use floor(J/d)<=J/d to get

    sum_(h<=J) |c_q(h)| <= J product_(p|q) (2-2/p).

Thus, by nonnegative summation and the same prime majorant,

    sum_(h<=J) |sum_q c_q(h)F_(alpha,gamma)(q)F_(beta,delta)(q)/q^2|
      <= J product_p [1+(2-2/p)|F_(alpha,gamma)(p)F_(beta,delta)(p)|/p^2]
      <= C_avg J,

where

    C_avg = exp(2 d0^(-2)(zeta(7/4)-1)).

Retaining the reciprocal-zeta factors, put C_S=4 M_zeta^2 c^2 C_avg. Then, for every J>=1,

    sum_(h<=J) |D_z(h)| <= C_S J/(log N)^2.                        (2.6)

Unlike (2.4), this does not even require J<=N. This argument independently reproduces the summatory lemma in reverse/REVERSE_THEOREM.md. All later estimates use (2.5) and (2.6).

## 3. Exact extension of the cutoff N-h to N

Extend the exact logarithmic-kernel off-diagonal from x<=N-h to x<=N, writing the resulting functional as Qext. Since the kernel support is x>=L_h=h/eta, the enlarged sum has only

    h<=J:=floor(N eta).

Make T large enough that eta<=1/2, so J<=N/2. The difference Qext-Q is exactly the integral over the removed strips N-h<x<=N, summed over h<=J and both orientations. For h>H=floor(N eta/(1+eta)), the exact-cutoff integrand was already identically zero, and the same strip formula still accounts for the entire enlarged term. Thus no h-endpoint discrepancy is omitted.

Using the exact bound |K_h^sigma(x)|<=M0/x,

    |Qext-Q|
       <= 2 T M0 C0 sum_(h=1)^J |D_z(h)| log(N/(N-h))
       <= (4 T M0 C0/N) sum_(h=1)^J h |D_z(h)|.                  (3.1)

The second inequality uses h/N<=1/2. Let

    Dbar = C_S/(log N)^2.

By (2.6), sum_(h<=J) h|D_z(h)|<=J sum_(h<=J)|D_z(h)|<=Dbar J^2. Hence

    |Qext-Q| <= 4 T M0 C0 Dbar J^2/N.                            (3.2)

Since eta<=B exp(B/T)/T and J<=N eta, this is

    |Qext-Q| <= 4 M0 C0 B^2 exp(2B/T) Dbar (N/T).                (3.3)

If J=0 all off-diagonal terms vanish and the estimate is automatic.

## 4. Exact logarithm to linear argument

Let y=h/x. The logarithmic and linear arguments are

    u=T log(1+y)/(2 pi),
    v=T y/(2 pi).

Since log(1+y)<=y, the linear kernel support x>=Th/B is contained in the union support x>=L_h. Both kernels vanish below L_h. At every x>0,

    |[x(x+h)]^(-1/2)-x^(-1)| <= h/(2x^2),

by 1-(1+y)^(-1/2)<=y/2, and

    |v-u| <= T h^2/(4 pi x^2),

by 0<=y-log(1+y)<=y^2/2. The mean-value bound for the smooth, possibly complex function f on the real line gives

    |K_h^sigma(x)-Ktilde_h^sigma(x)|
       <= M0 h/(2x^2) + M1 T h^2/(4 pi x^3).                     (4.1)

The bound is used only on x>=L_h; outside that region the difference is exactly zero. The union h range in x<=N is h<=J, since eta>=B/T. Also L_1>=1 for sufficiently large T. Therefore

    integral_1^N |x^(-s)(K_h^sigma-Ktilde_h^sigma)| dx
       <= C0 [M0 h/(2L_h) + M1 T h^2/(8 pi L_h^2)]
       = C0 [M0 eta/2 + M1 T eta^2/(8 pi)].                       (4.2)

Summing (4.2) over h<=J and both orientations and using (2.6) yields

    |Qext-Qlin|
       <= 2 T C0 J Dbar [M0 eta/2 + M1 T eta^2/(8 pi)]
       <= C0 Dbar [M0 B^2 exp(2B/T)
                    + (M1 B^3/(4 pi)) exp(3B/T)] (N/T).          (4.3)

No asymptotic Taylor remainder, unrecorded h tail, or density replacement occurs in this estimate.

## 5. Combination and scope

Adding (3.3) and (4.3) proves the explicit bound

    |Q-Qlin| <= C0 Dbar (N/T)
                [5 M0 B^2 exp(2B/T)
                 + (M1 B^3/(4 pi)) exp(3B/T)].                    (5.1)

This proves (1.2) uniformly on the original complex polydisc. In the corrected range psi<=phi, the strict inequality lambda(1-psi)<1 also gives lambda(1-phi)<1. Hence N/(T(log N)^2)=o(N^phi), and the forward theorem additionally yields R=Qlin+O(N^phi) under the same explicit arithmetic hypothesis. This is still only a statement about the displayed linear arithmetic main functional. Holomorphy follows from the normally convergent profile and finite supported h sums; their x domains are compact and independent of the shifts. Applying the two-variable Cauchy formula with radius rho proves (1.3).

The separate Euler/Mellin proof must evaluate Qlin and account for every contour residue. In particular, if whole-line w with nonzero w(0) creates a low-time contact term, (5.1) gives no license to omit it: this comparison is smaller by a factor of order T than a term of size N/(log N)^2. Correctly shifted arithmetic Dirichlet-series arguments are likewise the responsibility of that exact Mellin identity.
