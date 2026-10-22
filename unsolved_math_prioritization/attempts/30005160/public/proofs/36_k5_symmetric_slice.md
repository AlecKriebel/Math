# Proof 36  Symmetric extreme bounds on zero two five

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Statement and scope

Let 4<p<6 and q=p/2. For all nonnegative A,B,

    ||a+bz^2+cz^5||_p <= ||A+Bz^2+Az^5||_p

whenever a,b,c are real and |a|<=A, |b|<=B, |c|<=A.

The fixed-magnitude sign gap

    D=E|A+Bz^2+Az^5|^(2q)-E|A-Bz^2+Az^5|^(2q)

is strictly positive when A,B>0. This gives the full prescribed real coefficient box whose two extreme-frequency bounds agree. It includes points of the strict triangle region and all values of the middle bound B. It does not prove the unrestricted majorant property when the two extreme bounds differ, or any four-frequency theorem.

## 1. Conditioning on a Chebyshev level

Put z=e^(2is), with s uniform on [0,2pi]. Multiplication by e^(-5is), which has modulus one, transforms the two polynomials to

    2A cos(5s) +/- B e^(-is).

Their squared moduli are

    B^2+4A^2 cos^2(5s) +/- 4AB cos(5s)cos(s).                       (1)

Let

    T_5(x)=16x^5-20x^3+5x,

so T_5(cos s)=cos(5s). For -1<v<1, write x_1(v),...,x_5(v) for the five distinct real roots in (-1,1) of T_5(x)=v. For every continuous function H of two variables,

    E_s H(cos(5s),cos(s))
      = (1/(5pi)) integral_(-1)^1
         sum_(i=1)^5 H(v,x_i(v)) / sqrt(1-v^2) dv.                 (2)

To verify (2), set t=5s modulo 2pi. The five preimages are s=(t+2pi j)/5, j=0,...,4, with equal weights. For 0<t<pi their cosines are precisely the five roots of T_5(x)=cos t. The interval pi<t<2pi supplies the same unordered root set. Then substitute v=cos t. Thus (2) is an exact conditioning identity, with no assumptions of independence.

The roots at level -v are the negatives of those at level v, because T_5 is odd. The integrand of the sign gap in (2) is therefore even in v.

## 2. A monotone polynomial trace

Fix 0<v<1, and put

    a_v=B^2+4A^2v^2,
    c_v=4ABv.

Assume A,B>0, so c_v>0. Since a_v-c_v=(B-2Av)^2>=0, the function

    f_v(x)=(a_v+c_v x)^q

is smooth on the open interval (-1,1), including when a_v=c_v. Its fifth derivative is

    f_v^(5)(x)=(q)_5 c_v^5 (a_v+c_vx)^(q-5)>0,                  (3)

where (q)_5=q(q-1)(q-2)(q-3)(q-4)>0 for 2<q<3.

Define for -1<w<1

    R_v(w)=sum_(i=1)^5 f_v(x_i(w)).

The roots are simple, so differentiation gives

    R_v'(w)=sum_(i=1)^5 f_v'(x_i(w))/T_5'(x_i(w))
           =(1/16) f_v'[x_1(w),...,x_5(w)] > 0.                  (4)

Here the bracket denotes the order-four divided difference. The second equality follows from

    T_5'(x_i)=16 product_(j!=i)(x_i-x_j)

and the elementary Lagrange formula for a divided difference. Its positivity follows from the mean-value formula

    f_v'[x_1,...,x_5]=f_v^(5)(xi)/4!

for some xi between the smallest and largest nodes, using (3). This only uses smoothness on a compact interval strictly inside (-1,1), so a possible endpoint zero causes no issue.

Consequently R_v(v)>R_v(-v). The symmetry of the root sets identifies this difference exactly as

    sum_i (a_v+c_vx_i(v))^q - sum_i (a_v-c_vx_i(v))^q > 0.         (5)

## 3. Integration and full-box extension

Applying (2), the evenness in v, and (5), gives

    D=(2/(5pi)) integral_0^1 [R_v(v)-R_v(-v)]/sqrt(1-v^2) dv >0.

The integral is finite, since the original polynomials are continuous on the circle. If A=0 or B=0, equality follows directly.

At fixed magnitudes on {0,2,5}, a global sign sets the constant coefficient positive, and z -> -z sets the frequency-5 coefficient positive without changing frequency 2. Thus the two norms compared above exhaust all real sign vertices for bounds (A,B,A). Convexity of the Lp norm then proves the entire stated box.

## Optional explicit positive lower bound

For A,B>0, (3) is bounded below on (-1,1) by

    (q)_5 c_v^5(a_v+c_v)^(q-5),

because q-5<0. Equations (4) and the divided-difference mean-value formula therefore give

    R_v(v)-R_v(-v)
      >= v(q)_5 c_v^5(a_v+c_v)^(q-5)/192.

Since a_v+c_v=(B+2Av)^2, one obtains

    D >= [(q)_5 (4AB)^5/(480pi)]
           * integral_0^1 v^6(B+2Av)^(2q-10)/sqrt(1-v^2) dv >0.

The qualitative theorem does not require evaluating this integral. This proof is independent of the constant-dominant-cone coefficient expansion and of any numerical search.
