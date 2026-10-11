# Independent complex-family criterion and universal reconstruction

Sealed 2026-10-01T20:55:48Z, before reading the historical review, historical
verification scripts/results, or any sibling/root detailed audit report.
The exact head under audit is `aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95`.
The original SOURCE_AUDIT hash is
`99ae40a387e00e5d2c46ed8db4e479170092b2484cf237f83629ba5e1201ec8e`.

## Acceptance criterion

This is an audit of a source-only, unsolved partial with 0/5 proof attempts,
not an assertion that the campaign solved both directions. A satisfactory
complex component must match CN(0,1), with real and imaginary component
variances 1/2, the square LUE weight exp(-x), shape zero, and
`C(n)=n^(-3/2) E Tr(XX*)^(1/2)`. Its all-dimensional proof must have a valid
moment recurrence and base case; finite checks alone are insufficient.
The literature withdrawal correction and the explicit real proof hold must
remain visible. This family does not grant an independent real universal
theorem or novelty credit. Supporting quantitative decrement bounds must
be checked at their actual proof dependency, not inferred from an abstract.

Falsifiers include a factor sqrt(2) from the complex variance convention,
an extra/missing n in the one-point density, a missing square root of x,
a sign change in the recurrence, an invalid n=1 boundary, and extrapolating
finitely many moments to all n. Fresh controls will explicitly exercise these.

## Reconstruction from the square moment integral, valid for every n

For independent complex entries of density pi^(-1) exp(-|z|^2), the joint
eigenvalue density of XX* is proportional to exp(-sum x_i) times the
squared Vandermonde. Orthogonalizing the Vandermonde with ordinary
Laguerre polynomials of norm one gives the expected counting density

`rho_n(x)=exp(-x) sum_{j=0}^{n-1} L_j(x)^2`, whose integral is n.

Put `Q_n(s)=integral x^s rho_n(x) dx`, with s=1/2 for the target and Q_0=0.
The ordinary and generalized Laguerre generating identities give the finite
connection formula

`L_j(x)=sum_{r=0}^j (-s)_{j-r}/(j-r)! L_r^(s)(x)`.

Generalized Laguerre orthogonality with weight x^s exp(-x), obtainable by
Rodrigues' formula and integration by parts, has squared norm
`Gamma(r+s+1)/r!`. Consequently, coefficientwise as formal power series,

`H(z)=sum_{n>=1} Q_n(s) z^n`
`=Gamma(s+1) z (1-z)^(-s-2) F(z)`,
`F(z)=sum_{m>=0} [(-s)_m/m!]^2 z^m`.

Every coefficient uses finite sums. There is no exchange of a divergent
analytic series or limit. The ratio of adjacent coefficients of F directly
implies its differential equation

`z(1-z)F''+[1+(2s-1)z]F'-s^2 F=0`.

Substitute `H=Gamma(s+1) z(1-z)^(-s-2)F` to obtain

`z^2(1-z)^2 H''+z(-1-2z+3z^2)H'`
`+[1+z^2-s(s+1)z]H=0`.

Extracting the coefficient of z^(n+1), for every integer n>=1, gives

`n^2 Q_{n+1}-(2n^2+s(s+1))Q_n+n^2 Q_{n-1}=0`.

In particular, at s=1/2:

`Q_{n+1}=(2+3/(4n^2))Q_n-Q_{n-1}`,
`Q_0=0`, `Q_1=sqrt(pi)/2`, `Q_2=11 sqrt(pi)/8`.

This proof reconstructs the square recurrence directly from the density and
finite Laguerre connection formula; it does not require Carlson continuation.

## Universal sign and boundary cases

With `C_n=Q_n/n^(3/2)` and delta_n=C_(n+1)-C_n, for n>=2,

`delta_n=(A_n-B_n-1) C_n+B_n delta_(n-1)`,
`A_n=(2+3/(4n^2))(n/(n+1))^(3/2)`,
`B_n=((n-1)/(n+1))^(3/2)>0`.

For 0<=x<=1 define f(x)=(1+x)^(3/2)+(1-x)^(3/2). On 0<x<1,
`f''(x)=3/4 [(1+x)^(-1/2)+(1-x)^(-1/2)]>3/2` by strict
convexity of t^(-1/2). Integrating twice with f(0)=2 and f'(0)=0 gives
`f(x)>2+3x^2/4` for 0<x<1; continuity, or the explicit endpoint value,
gives strictness at x=1. Thus A_n-B_n-1<0. The base increment is strictly
negative because `C_2/C_1=11/(8 sqrt(2))<1`, checked by 121<128.
Positive C_n and induction prove C_(n+1)<C_n for EVERY integer n>=1.

The Baslingker-Dan sentence saying this scalar inequality holds for every
x>=0 overstates its real domain. Its use at x=1/n lies entirely in [0,1]
and is valid. The delta induction is started at n=2; no undefined C_0 is used.

## Independent check of the cited hypergeometric recurrence

For a real shape alpha>=0 and fixed k, let
`F_n=3F2(1-n,1-k,k+2;2,alpha+2;1)` and D=(k-1)(k+2).
For n>=2 its finite contiguous identity is

`a_(n+1) F_(n+1)-(a_(n+1)+a_(n-1)+D)F_n+a_(n-1)F_(n-1)=0`,
`a_n=n(n+alpha)`.

A direct telescoping certificate uses
`g_j=(-n)_j(1-k)_j(k+2)_j/[(2)_j(alpha+2)_j j!]`, 0<=j<=n,
and `q_j=j(j+1)(j+alpha+1)/n`.
The residual with the opposite sign has coefficient

`h_j=[-(n+alpha-1)j^2-(D+3n+alpha+1)j+nD]/n`,

and `h_j g_j=q_(j+1)g_(j+1)-q_j g_j`. Both end terms vanish.
This proves the finite identity for all n>=2, without sampling n.
Multiplication by the Cunden moment prefactor gives the quoted recurrence.
For n=1, use the directly integrated n=1,2 moments. In particular, do not
interpret the square boundary as 0 times a divergent nonterminating 3F2.

Audit completion estimate at this checkpoint: 35%. Strongest verified
mathematical result: universal strict complex square decrease under the
exact original Gaussian convention. Remaining work: quantitative bound
dependency, all 16 input hashes/head/provenance, and fresh plus historical
control reproduction. No new discovery is claimed.
