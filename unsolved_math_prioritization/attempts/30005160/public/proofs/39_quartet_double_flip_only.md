# Proof 39  Only the double flip comparison on factorized odd quartets

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Statement and scope

Let 4<p<6, q=p/2, beta=q-2, and let K>=3 be odd. For a,b,c,d>=0 define

    P_+(z)=(a+bz^2)(c+dz^K),
    P_-(z)=(a-bz^2)(c+dz^K).

For n>=0 write

    C_n(u,v)=E |u+v e^(it)|^(2q) cos(nt),

where t is uniform on [0,2pi]. Then

    E|P_+|^(2q)-E|P_-|^(2q)
      >= 4 C_K(a,b) C_2(c,d) [1-beta/20] >= 0.             (1)

The gap is strictly positive if all four factor parameters are positive. The bracket exceeds 19/20.

In coefficient notation (A,B,C,D)=(ac,bc,ad,bd), this proves the comparison of (A,B,C,D) against (A,-B,C,-D) on the nonnegative factorized surface AD=BC. In particular it applies to Q_3={0,2,3,5}. It proves neither of the two single-flip comparisons, nor a full real coefficient-box theorem, nor unrestricted MP_p for Q_3. The larger-K result does not conflict with known counterexamples, which need not lie in this factorized comparison.

## 1. Fourier coefficients of one binomial

It suffices to analyze f_r(t)=|1+r e^(it)|^(2q), 0<=r<=1, since swapping u,v preserves the modulus and scaling contributes max(u,v)^(2q). If r=0, all positive-index Fourier coefficients vanish. Assume r>0 and let c_n(r) be its nth Fourier coefficient, which is real.

The binomial series is absolutely uniformly convergent, even at r=1. Thus

    c_n(r)=sum_(j>=0) binom(q,j+n)binom(q,j) r^(2j+n).              (2)

For n>=3, expanding (1-r^2 t)^q and integrating term by term against a beta density gives

    c_n(r)=binom(q,n) r^n / B(n-q,q+1)
      * integral_0^1 t^(n-q-1)(1-t)^q(1-r^2 t)^q dt.               (3)

Indeed the jth integrated coefficient is

    binom(q,n) (-1)^j binom(q,j) (n-q)_j^+/(n+1)_j^+,

which equals binom(q,n+j)binom(q,j). All beta parameters are positive. The formula is first obtained for r<1 and extends to r=1 by continuity or dominated convergence.

The prefactor binom(q,n)/B(n-q,q+1) alternates sign without changing magnitude as n increases: its successive ratio is -1, by the beta integral recurrence and binomial recurrence. At n=3 it is positive. Consequently

    sign c_n(r)=(-1)^(n-3) for n>=3.                              (4)

Moreover, for n>=m>=3, formula (3) gives

    |c_n(r)|/|c_m(r)|
      = r^(n-m) * [integral t^(n-m) w_m(t) dt]/[integral w_m(t) dt]
      <= 1,                                                      (5)

where w_m(t)=t^(m-q-1)(1-t)^q(1-r^2t)^q>=0.

A sharper consequence for m=3 is

    |c_n(r)|/c_3(r) <= (3-q)_(n-3)^+/(4)_(n-3)^+
                     <= 6/[n(n-1)(n-2)],  n>=3.                  (6)

For the first inequality, t^(n-3) is increasing and (1-r^2t)^q is decreasing. Their covariance under the probability beta density proportional to t^(2-q)(1-t)^q is nonpositive. This elementary covariance assertion follows by integrating

    [g(t)-g(s)][h(t)-h(s)]<=0

against the product probability measure. Removing the decreasing weight can only increase the moment. The beta-integral moment is (3-q)_(n-3)^+/(4)_(n-3)^+. The final inequality uses 0<3-q<1 and (3-q)_j^+<=j!.

For c_2, equation (2) has only one negative summand: j=2. Its j=1 positive summand dominates it because r<=1 and

    |binom(q,4)|binom(q,2) / [binom(q,3)binom(q,1)]
      = (3-q)(q-1)/8 < 1.

The remaining summands are nonnegative. Hence

    c_2(r)>=binom(q,2)r^2>0.                                    (7)

Formula (3) for n=3 also gives c_3(r)<=binom(q,3)r^3, since (1-r^2t)^q<=1. Therefore

    c_3(r)/c_2(r) <= (q-2)r/3 <= beta/3.

Combining this with (6) yields the useful all-index estimate

    |c_n(r)|/c_2(r) <= 2 beta/[n(n-1)(n-2)],  n>=3.               (8)

Equations (4), (5), (7), and (8) continue to hold after arbitrary nonnegative binomial scaling, with ratio statements used only when the denominator is nonzero.

## 2. Exact product resonance and the tail estimate

The Fourier series of each binomial modulus is absolutely convergent. Orthogonality for frequencies 2 and K, with gcd(2,K)=1, shows

    E|P_+|^(2q)=C_0(a,b)C_0(c,d)
                    +2 sum_(l>=1) C_(Kl)(a,b) C_(2l)(c,d).

Replacing b by -b multiplies C_(Kl)(a,b) by (-1)^(Kl)=(-1)^l. Therefore the exact gap is

    D=4 sum_(l>=1 odd) C_(Kl)(a,b) C_(2l)(c,d).                    (9)

Its l=1 term is positive. Every odd l>=3 has Kl odd and 2l even with 2l>=6, so (4) says that each remaining term is negative. By (5), since Kl>=K>=3,

    0<C_(Kl)(a,b)<=C_K(a,b).

By (8),

    sum_(l>=3 odd) |C_(2l)(c,d)|/C_2(c,d)
      <= sum_(n>=6) 2 beta/[n(n-1)(n-2)] = beta/20.               (10)

The last sum is exact by telescoping

    2/[n(n-1)(n-2)]
      = 1/[(n-1)(n-2)] - 1/[n(n-1)].

Equations (9) and (10) prove (1) for positive factors. Zero factor parameters follow directly or by continuity. No sign comparison absent from (9) is inferred.
