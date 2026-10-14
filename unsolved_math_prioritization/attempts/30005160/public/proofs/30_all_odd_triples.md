# Proof 30  Every odd collinear triple with frequency at least seven fails

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Theorem and explicit coefficients

For every odd integer K >= 7 and every fixed real 4 < p < 6, there are positive coefficients x,y with x+y<1 such that

    D_p(x,y) = integral_T |1+x z^2+y z^K|^p
                - integral_T |1-x z^2+y z^K|^p < 0.      (1)

The following formulas are one explicit choice. Set

    q = p/2,             beta = q-2 in (0,1),
    a = K-q,             h = K-p-1 > 0,
    C_beta = 2 beta / (Gamma(1-beta) Gamma(3+beta)),
    delta = min(1/4, [C_beta 2^(-K-3)]^(1/h)),
    y = sqrt(1-delta),    r = (1-y)/2,
    A = 4 binom(q,K) binom(q,2) y^2,
    x = min(r/4, sqrt(A r^(K+2))/32).                    (2)

Here generalized binomial coefficients use the finite falling-product formula. All the displayed quantities are positive. Both x and y may depend on p; this theorem does not assert one triple works throughout 4 < p < 6. The construction does, however, cover every odd K >= 7, with no frequency threshold or unenumerated residual odd family.

## 1. Analytic expansion in the middle coefficient

For fixed 0 < y < 1, let

    M(w) = integral_T (1+y z^K+w z^2)^q
                        (1+y z^(-K)+w z^(-2))^q.

For |w| < 1-y, both factors before taking powers have positive real part, so their principal powers define a holomorphic M. For real w in that interval, M(w) equals the corresponding pth absolute-value moment. Hence D(w)=M(w)-M(-w) is an odd holomorphic function whose real values are (1).

Writing B(z)=1+y z^K, expansion at w=0 gives the coefficient indexed by nonnegative j,l:

    binom(q,j) binom(q,l) w^(j+l)
       integral_T z^(2(j-l)) B(z)^(q-j) B(z^(-1))^(q-l).

The remaining factors have only Fourier frequencies divisible by K. Thus a term can survive only if K divides 2(j-l), equivalently K divides j-l because K is odd. If j+l is odd and smaller than K, no such term survives: j-l is odd and has absolute value less than K. At odd degree K, the only possible pairs are (j,l)=(K,0) and (0,K).

Expansion in y, absolutely convergent because y<1, therefore yields

    D(w) = d_K w^K + sum_(l>=K+2, l odd) d_l w^l,

    d_K = 4 binom(q,K)
             sum_(N>=0) binom(q-K,N) binom(q,N+2)y^(2N+2)
        = 4 binom(q,K) binom(q,2)y^2 F(y^2),             (3)

where

    F(t) = 2F1(K-q,2-q;3;t)
         = 1 - sum_(N>=1) a_N t^N,

    a_N = 2 (a)_N beta (1-beta)_(N-1)
                   / [N! (N+2)!] > 0.                  (4)

The notation (b)_N denotes the rising product. Equations (3)-(4) can also serve as the definition of F, so no hypergeometric continuation or sign theorem is assumed. The falling-product signs show binom(q,K)>0 for odd K>=5: precisely K-3 factors are negative, an even number. Thus A in (2) is strictly positive.

## 2. Positive integral and explicit negative sign

The beta integral applied termwise to the positive series in (4) gives, for 0 <= t < 1,

    F(t) = 1 - C_beta integral_0^1
        u^(-beta-1)(1-u)^(beta+2)
        [(1-tu)^(-a)-1] du.                             (5)

Indeed, expand the bracket as sum_(N>=1) (a)_N (tu)^N/N!. The integral of the Nth term is

    Gamma(N-beta) Gamma(3+beta) / Gamma(N+3),

and multiplication by C_beta gives exactly a_N. All terms are nonnegative, so the interchange is justified by Tonelli's theorem. For t<1 the integral is finite: near u=0 the bracket is O(u), and near u=1 it is bounded.

Let 0 < delta <= 1/4 and t=1-delta. Restrict the integral to

    1-delta <= u <= 1-delta/2.

On this interval, u^(-beta-1) >= 1, 1-u >= delta/2, and 1-tu <= 2delta. Moreover a=K-q>4, so (2delta)^(-a) >= 2 and

    (1-tu)^(-a)-1 >= (1/2)(2delta)^(-a).

The length of the interval is delta/2. Consequently the integral in (5) is at least

    (delta/2)(delta/2)^(beta+2)(1/2)(2delta)^(-a)
      = 2^(-K-2) delta^(-h),                            (6)

because a+beta=K-2 and beta+3-a=p+1-K=-h. Thus

    F(1-delta) <= 1-C_beta 2^(-K-2)delta^(-h).

The choice (2) satisfies delta^h <= C_beta 2^(-K-3), proving

    F(y^2) <= -1,       d_K <= -A < 0.                 (7)

This both proves the negative sign and specifies y. In particular it avoids inferring a sign from finitely many exponents or frequencies. Equivalently, (4) has a divergent positive coefficient sum at t=1, since a_N is asymptotic to a positive constant times N^(K-p-2); the proof above does not need that asymptotic.

## 3. Explicit control of every higher power

On the closed complex disk |w| <= r=(1-y)/2,

    |1+y z^(+/-K)+w z^(+/-2)| <= 1+y+r < 2.

The real parts remain at least r>0. Since q is real, each principal power has modulus equal to the corresponding modulus to the qth power. Hence

    |M(w)| < 2^p < 64,       |D(w)| < 128.

Cauchy's estimate gives |d_l| <= 128 r^(-l). Since D is odd and all its degrees below K vanish, for 0 < x <= r/2 the entire tail is bounded by

    |D(x)-d_K x^K|
       <= 128 (x/r)^(K+2)/(1-(x/r)^2)
       < 256 r^(-K-2) x^(K+2).                         (8)

The x specified in (2) obeys x<=r/4 and x^2 <= A r^(K+2)/1024. Substitution into (8) therefore gives

    |D(x)-d_K x^K| <= (A/4)x^K.

Together with (7),

    D_p(x,y) <= -(3A/4)x^K < 0.

Also x <= (1-y)/8, so x+y<1. This proves (1), including effective domination of all higher terms.

## 4. A simple rational family at p=5

For every odd K >= 7, one may take the exact rational coefficients

    p = 5,       y = 1-2^(-13) = 8191/8192,
    x = 2^(-8K-20).                                    (9)

Indeed beta=1/2, C_beta=8/(15pi)>2/15, and

    delta = 1-y^2 = 2^(-12)-2^(-26) < 2^(-12).

The integral lower bound (6), with h=K-6, gives

    F(y^2) < 1-(2/15)2^(11K-74) <= -1/15,              (10)

because K>=7. Set b_K=binom(5/2,K). Starting with |b_4|=5/128 and using

    |b_(j+1)|/|b_j| = (j-5/2)/(j+1) >= 1/4, j>=4,

shows b_K >= 10*4^(-K) for odd K>=7. Since y^2>1/4 and binom(5/2,2)=15/8, equations (3) and (10) give

    d_K < -(1/15)*4 b_K*(15/8)*y^2
          < -b_K/8 <= -(5/4)4^(-K) < -4^(-K).

Now r=(1-y)/2=2^(-14), and x in (9) is smaller than r/2. The entire tail in (8) is strictly less than

    256 r^(-K-2) x^(K+2) = (1/16)4^(-K) x^K.

Consequently

    D_5(x,y) < -(15/16)4^(-K) x^K < 0.                 (11)

This corollary provides exact rational coefficients for an elementary infinite family covering every odd K>=7. Its p=5 scope is narrower than the all-p theorem above, and is stated separately for that reason.

## Scope

For each fixed p in (4,6), no odd-frequency support {0,2,K} with K>=7 can satisfy the constant-one real majorant inequality for every coefficient triple. The result includes the previously certified K=7,9,11 and excludes every larger odd K as well. It makes no claim of positivity for the distinct unrestricted supports {0,1,3} and {0,2,5}. It does not replace the separate stronger quantifier, valid at sufficiently large K, that one coefficient triple works simultaneously for every p in (4,6).
