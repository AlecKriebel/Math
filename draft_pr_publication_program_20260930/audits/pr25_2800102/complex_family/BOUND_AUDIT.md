# Audit of the square complex decrement bound used by the real comparison

Read scope: Abreu-Patil 2609.07802v1, printed pp. 6-18, including the
actual recurrence, generating function, singular expansion, transfer
argument, leading constants, coefficient bounds, and Theorem 1 proof.
This is verification of an external result, not a new contribution.

Let Y_n=E Tr(XX*)^(1/2), C_n=Y_n/n^(3/2), and
D_n=C_n-C_(n+1). This document uses q_d only for the auxiliary scalar
in that paper, not for the moment divided by sqrt(pi).

## Independent recurrence and generating-function bridge

The sealed reconstruction proves, for all n>=1,

`Y_(n+1)=(2+3/(4n^2))Y_n-Y_(n-1)`, with Y_0=0.

Its finite Laguerre connection calculation also gives, as a formal series
and analytically for |z|<1,

`sum_{n>=1} Y_n z^n = sqrt(pi)/2 z(1-z)^(-5/2) F(z)`,
`F(z)=2F1(-1/2,-1/2;1;z)`.

The squared connection coefficients are nonnegative. This checks every
factor in the paper's equations (2.10), (2.11), and (3.1), including the
distinction between the density's mass n and a probability density's mass 1.

## Leading asymptotic constant actually required

The standard integer-excess hypergeometric expansion gives, t=1-z,

`F(1-t)=4/pi-t/pi-t^2/(8pi) log t`
`+t^2(8log2-5)/(16pi)+O(t^3 log t)`.

Here c-a-b=2, the principal branch is analytic away from [1,infinity),
and the expansion converges for 0<|t|<1 with |arg t|<pi. The paper
explicitly checks the resulting Delta-domain hypothesis before using
singularity transfer. Truncation after index J has coefficient remainder
`O(n^(-J+1/2) log n)` for Y_n, hence `O(log n/n^(J+1))` for C_n.
These hypotheses are essential: a mere real-axis O estimate would not
justify coefficient extraction.

For the first three singular terms, the independent arithmetic is

`c_0=2/pi`, `c_1=-5/(2pi)`,
`c_2=(log2/4+11/32)/pi`, `d_2=-1/(16pi)`.

The needed gamma quotient terms are

`Gamma(n+5/2)/Gamma(n+1)=n^(3/2)[1+15/(8n)+65/(128n^2)+O(n^-3)]`,
`Gamma(n+3/2)/Gamma(n+1)=n^(1/2)[1+3/(8n)+O(n^-2)]`.

The three contributions to C_n at order n^-2 are
`65/(48pi)`, `-15/(8pi)`, and `(ell_n+11/2)/(16pi)`, where
ell_n=log n+gamma+6log2. Their constant sum is `-17/(96pi)`.
The n^-1 terms cancel exactly. This reproduces

`C_n=8/(3pi)+(ell_n-17/6)/(16pi n^2)+O(log n/n^4)`.

The error improvement to n^-4 is supported by the paper's explicit
recurrence argument: applying the centered second difference to
`n^(3/2-j)(A_j log n+B_j)` has leading multiplier j(j-2), with
logarithmic cross term 2(1-j)A_j. Only indices j,j-2,... contribute.
At every odd index the multiplier is nonzero, so all odd coefficients
vanish inductively. Arbitrary-order transfer supplies the required
remainder before these formal comparisons are made. Taking consecutive
differences bounds both remainders separately; cancellation of errors is
not assumed. Therefore

`D_n=(ell_n-10/3)/(8pi n^3)+O(log n/n^4)`.

This audit uses the standard hypergeometric expansion, gamma asymptotics,
and Delta-domain transfer theorem as established analytic tools; it checks
their parameter/branch hypotheses and application here rather than
reproving those general theorems.

## All-dimensional upper bound, not an asymptotic extrapolation

Define `q_d=(d+2)^(3/2)-2(d+1)^(3/2)+d^(3/2)-3/(4sqrt(d+1))`.
Strict convexity of t^(-1/2), against the triangular weight 1-|t|,
gives q_d>0. The exact recurrence gives

`E_d-E_(d-1)=8pi q_(d-1)Y_d-log(d/(d-1))`, d>=2,
`E_n=8pi[n(n+1)]^(3/2)D_n-log n`.

The generating coefficients and Gauss sum F(1)=4/pi give

`C_d < (8/(3pi))(d+1/2)Gamma(d+1/2)/(d^(3/2)Gamma(d))`
`< (8/(3pi))(d+1/2)/d`.

The last inequality follows from strict Cauchy-Schwarz in the gamma
integral; it is valid already at d=1.

For `t=1/(d+1)`, the scalar bound in Lemma 6 is equivalent to

`64/(3t^4)[(1+t)^(3/2)+(1-t)^(3/2)-2-3t^2/4]`
`< -log(1-t)/[t(1+t/2)]`.

Its left coefficients are `lambda_j=(128/3) binom(3/2,2j+4)`.
The right coefficients are
`a_m=sum_{r=0}^m (-1/2)^r/(m+1-r)`.
The required initial comparisons are
`a_0=lambda_0=1`, `a_2=1/3>7/24=lambda_1`, and
`a_4=19/120>33/256=lambda_2`. Odd a_m are nonnegative.
For j>=3, lambda_3=143/2048<1/12 and the ratio comparison has
positive cross-multiplication residue `24j^2+77j+50`. Thus
`lambda_j<1/[3(j+1)]`. The paper's integral formula proves
`a_(2j)>1/[3(j+1)]`. Both series converge for 0<t<1, so this is a
universal coefficient comparison.

Important boundary wording repair: Lemma 6 states d>=2, but its proof
proves the scalar inequality for EVERY 0<t<1, hence also d=1. Theorem
1 uses q_1 when d=2. Apply the actual stronger proof at t=1/2 to supply
this boundary. No finite evidence or unproved extension is needed.

These estimates imply E_d-E_(d-1)<0 for every d>=2. The asymptotic
formula above gives `E_n -> C_0=gamma+6log2-10/3`. Hence E_n>C_0.
The scalar positivity C_0>0 follows from gamma>0 and log2>2/3.
This proves the positive lower bound for D_n, and gives C_n>8/(3pi).

Retaining the positive fourth-order term in q_(d-1) gives
`q_(d-1)>3/(64d^(5/2))`; with Y_d>(8/(3pi))d^(3/2), it gives
`8pi q_(d-1)Y_d>1/d`. Summing the exact E differences from d=n+1
to infinity therefore gives

`E_n-C_0 < sum_{d=n+1}^infinity [log(d/(d-1))-1/d]`
`=H_n-log n-gamma`.

Substituting the definition of E_n proves exactly the real paper's input:

`0 < D_n < [H_n+6log2-10/3]/[8pi(n(n+1))^(3/2)]`, for every n>=1.

There is no circular use of the real result. Positivity of the complex
decrement was independently proved in the seal, and the quantitative
argument also supplies it. The standard asymptotic constant identifies
the E limit; coefficient inequalities turn that limit into a bound for
all n. Finite numerical fitting plays no role.

## Limits of this certification

The square bound dependency passes an analytic audit with the above
explicit boundary repair. This does not certify the real-complex LOE
correction or Abel diagonal completion. It does not audit Abreu-Patil's
Corollary 2, applications, or every asymptotic coefficient, which are
unneeded by the source-only package and the real square bound. It is not
a claim that the original attempt already carried out this fuller audit.
