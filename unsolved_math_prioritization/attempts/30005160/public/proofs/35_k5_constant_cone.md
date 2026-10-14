# Proof 35  The constant dominant coefficient cone on zero two five

Included dependencies: [Dominant constant coefficient boxes on odd frequency bands](21_dominant_odd_bands.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Statement and exact scope

Put q=p/2 in (2,3). For nonnegative A,B,C with A>=B+C, the full real coefficient box on frequencies {0,2,5} satisfies

    ||a+b z^2+c z^5||_p <= ||A+B z^2+C z^5||_p

whenever |a|<=A, |b|<=B, and |c|<=C. More quantitatively, for A>0 define

    D = E|A+B z^2+C z^5|^(2q) - E|A-B z^2+C z^5|^(2q),
    L = 4 binom(q,5) binom(q,2) A^(2q-7) B^5 C^2,
    beta = q-2 in (0,1).

Then

    D >= L * B(3-beta,2 beta)/B(3-beta,beta) >= 0.             (1)

Here B(u,v)=integral_0^1 t^(u-1)(1-t)^(v-1) dt is the positive beta integral. Its ratio in (1) also equals

    2 Gamma(2 beta) / [Gamma(beta) Gamma(3+beta)].

In particular D>0 when A,B,C are positive. Coordinate-zero cases follow by continuity; A=0 forces all three bounds to vanish. This is a prescribed-box theorem on the constant-dominant cone, not an unrestricted theorem for this support. The earlier frequency-5-dominant cone C>=A+B remains a separate accepted result.

## 1. Exact resonant expansion

By homogeneity take A=1, and write x=B/A, y=C/A, so x+y<=1. The binomial expansion of (1+xz^2+yz^5)^q is absolutely uniformly convergent, including at x+y=1, because sum_j |binom(q,j)| is finite. The product with its conjugate is therefore integrable term by term.

Write (q)_j=q(q-1)...(q-j+1), with (q)_0=1. A sign-sensitive resonance has oriented multiplicities

    (r+5k,s) and (r,s+2k),

where r,s>=0, k is a positive odd integer, and the coordinates count x and y. Indeed 2(u-u')+5(v-v')=0, and the x sign differs precisely for odd k. Including both orientations, its contribution to D is

    4 (q)_(r+s+5k) (q)_(r+s+2k)
      x^(2r+5k) y^(2s+2k)
      / [(r+5k)! s! r! (s+2k)!].                         (2)

The r=s=0,k=1 term is L=4 binom(q,5)binom(q,2)x^5 y^2>0. It is the unique positive term: every other sign-sensitive term has block indices of opposite parity and both indices are at least 3. For j>=3, sign((q)_j)=(-1)^(j-3), so their products are negative.

Put k=2h+1, R=r+5h, S=s+2h, N=R+S. The remaining terms have N>=1 and

    0<=h<=H=min(floor(R/5),floor(S/2)).

After dividing D by L, the exact series is

    D/L = 1 - sum_(N>=1) sum_(R+S=N) c_(R,S) x^(2R)y^(2S),             (3)

where

    c_(R,S) = 240 sum_(h=0)^H T_h,
    T_h = (3-beta)_(N+3h)^+ beta (1-beta)_(N-3h-1)^+
          / [(R+5h+5)! (S-2h)! (R-5h)! (S+2h+2)!].                 (4)

The superscript + denotes a rising factorial; all factors in (4) are positive. The index N-3h-1 is nonnegative: for h>=1, N>=7h, and for h=0, N>=1. Formula (4) is exact, not an upper estimate of a factorial product. It follows directly from

    |(q)_(N+3h+5)/(q)_5| = (3-beta)_(N+3h)^+,
    |(q)_(N-3h+2)/(q)_2| = beta (1-beta)_(N-3h-1)^+.

## 2. Coefficient domination, including higher circuit multiples

Define the boundary coefficient

    a_N = 2 (3-beta)_N^+ beta (1-beta)_(N-1)^+ / [N!(N+2)!].          (5)

We prove the following inequality for every integer N>=1 and R+S=N:

    c_(R,S) <= a_N binom(2N,2R).                                  (6)

First, T_h is nonincreasing in h. For h+1<=H, the quotient T_(h+1)/T_h is

    product_(i=0)^2 [(N+3h+3-beta+i)/(N-3h-3-beta+i)]
    * product_(j=0)^4 [(R-5h-j)/(R+5h+6+j)]
    * [(S-2h)(S-2h-1)/((S+2h+3)(S+2h+4))].                       (7)

The quotient in each factor of the first product is increasing in beta, because its numerator exceeds its denominator. Therefore the first product is at most its value at beta=1, namely

    (N+3h+2)(N+3h+3)(N+3h+4)
    / [(N-3h-4)(N-3h-3)(N-3h-2)].

All these denominators are positive because h+1<=H implies N>=7h+7. Also S>=2h+2 implies R<=N-2h-2. For j=0,1,2, monotonicity in R gives

    (R-5h-j)/(R+5h+6+j)
    <= (N-7h-2-j)/(N+3h+4+j)
    <= (N-3h-2-j)/(N+3h+4-j).

Multiplying these three inequalities cancels the first product's upper bound exactly. Each unused factor in (7) is at most 1. Hence T_(h+1)<=T_h and sum_h T_h<=(H+1)T_0.

After using Vandermonde's inequality binom(N,R)^2<=binom(2N,2R), we obtain

    c_(R,S) / [a_N binom(2N,2R)] <= (H+1)P,
    P = 120(N+1)(N+2)
        / [(R+1)(R+2)(R+3)(R+4)(R+5)(S+1)(S+2)].                  (8)

If R=0, then H=0 and P=1. If S=0, then H=0 and

    P=60/[(N+3)(N+4)(N+5)]<=1.

If R,S>=1, then H+1<=(R+5)/5. Moreover RS>=N-1, N>=2, and consequently

    (R+1)(R+2)(S+1)(S+2)
      = (RS+N+1)(RS+2N+4) >= 6N(N+1).

Since (R+3)(R+4)>=20, equation (8) gives

    (H+1)P <= 24(N+1)(N+2) / [120N(N+1)]
           = (N+2)/(5N) <= 2/5 < 1.

This proves (6), including N=1 and every h>0 term.

## 3. Summation by a positive beta integral

For x,y>=0 with x+y<=1, equation (6) implies

    sum_(R+S=N) c_(R,S)x^(2R)y^(2S)
    <= a_N sum_(R+S=N) binom(2N,2R)x^(2R)y^(2S)
    <= a_N (x+y)^(2N) <= a_N.                                    (9)

To evaluate the sum, define for 0<=t<=1

    F(t) = [1/B(3-beta,beta)]
           * integral_0^1 u^(2-beta)(1-u)^(beta-1)(1-tu)^beta du.

The binomial expansion of (1-tu)^beta has constant term 1 and strictly negative coefficients thereafter. Termwise integration for t<1 yields

    F(t)=1-sum_(N>=1) a_N t^N.

This identity can alternatively be checked directly by integrating u^N: the ratio of beta integrals is (3-beta)_N^+/(3)_N^+, and |binom(beta,N)|=beta(1-beta)_(N-1)^+/N!. At t=1, monotone convergence of the nonnegative series 1-(1-tu)^beta or dominated convergence of the integral gives

    1-sum_(N>=1) a_N = F(1)
      = B(3-beta,2 beta)/B(3-beta,beta) > 0.                        (10)

Equations (3), (9), and (10) prove (1) for positive x,y. Continuity covers either zero. Restoring A by homogeneity gives the stated power A^(2q-7).

## 4. Full real coefficient box and stopping scope

At fixed magnitudes, a global sign sets the constant coefficient positive, and z -> -z independently sets the frequency-5 coefficient positive while leaving frequency 2 unchanged. Thus the two norms in D exhaust all real sign vertices. Convexity of the Lp norm then gives the complete prescribed-box theorem.

Combining with the accepted frequency-5-dominant theorem leaves precisely the positive-amplitude region

    A < B+C and C < A+B.

This contains the entire frequency-2-dominant cone B>=A+C and the strict triangle region. No result here settles these remaining regions, Q_1, Q_3, or unrestricted MP_p for {0,2,5}. No numerical search is used as proof.
