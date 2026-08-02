# Milestone 5G: the arbitrary-chain JC root reversal

## Scope and conventions

This note extends the four-leaf root move `Omega` without changing the
network class or the semi-directed convention.  Tree-edge directions are
forgotten, arrowheads entering reticulations are retained, and only the
degree-two artifact created by forgetting the global root is suppressed.

Fix an integer \(k\geq2\).  Let \(S\) be the root, let \(V,X\) be
reticulations, and use the arcs

\[
S\to U,\quad S\to X,\quad U\to V,
\]
\[
U\to P_1\to\cdots\to P_k\to V,
\qquad V\to Q\to X.
\]

Attach one labelled leaf at each of
\(P_1,\ldots,P_k,Q,X\).  In the source their labels, in that order, are

\[
1,2,\ldots,k,k+1,k+2,
\]

and in the target they are

\[
k,k-1,\ldots,1,k+2,k+1.
\]

Call this pair \(\Omega_k\), and call the parameterized local operation
`Omega_chain`.

## Primary theorem

**PROVED.** For every \(k\geq2\), the two members of \(\Omega_k\) are
leaf-labelled binary strongly tree-child level-2 networks on
\(n=k+2\) leaves.  Their root-suppressed blob is the theta graph with three
\(U\)-to-\(V\) paths of lengths

\[
1,\quad k+1,\quad3.
\]

Its three cycle lengths are

\[
4,\quad k+2,\quad k+4,
\]

so the blob is triangle-free.

**PROVED.** The source and target are nonisomorphic as leaf-labelled
semi-directed networks.  The labelled pendant neighbors force any underlying
graph isomorphism to send

\[
P_i\mapsto P_{k+1-i},\qquad Q\leftrightarrow X,qquad U\leftrightarrow V.
\]

This reflection sends the source reticulation set \(\{V,X\}\) to
\(\{U,Q\}\), whereas the target reticulation set is still \(\{V,X\}\).
It therefore fails to preserve reticulation arrowheads.  Since there is no
triangle, this failure cannot be a triangle redirection.

**PROVED.** Under JC, both complete models have dimension

\[
\boxed{2k+5=2n+1}.
\]

Their irreducible Zariski closures are equal, and their open stochastic
images contain a common regular relatively open neighborhood of that full
dimension.  Thus `Omega` is not a four-port anomaly: it is one local move
schema supporting an arbitrary ordered chain of labelled descendant blocks.

No equality of the complete open stochastic images is claimed.

## Exact all-\(k\) correspondence

Write the source edge parameters as follows:

\[
\begin{array}{c|c}
\text{arc}&\text{parameter}\\ \hline
U\to V&A\\
U\to P_1&B\\
P_i\to P_{i+1}&C_i\quad(1\leq i<k)\\
P_k\to V&D\\
S\to U&E\\
S\to X&s\\
V\to Q&t\\
Q\to X&F\\
P_i\to i&p_i\\
Q\to(k+1)&R\\
X\to(k+2)&w.
\end{array}
\]

Fix the source gauge

\[
s=t=w=\lambda_V=\lambda_X=\frac12
\]

and put

\[
G=E+2F,\qquad H=AF+2E.
\]

On the target, again set
\(s'=t'=w'=\lambda'_V=\lambda'_X=1/2\), reverse all middle-path and
pendant parameters,

\[
C'_i=C_{k-i},\qquad p'_i=p_{k+1-i},
\]

and define

\[
\begin{aligned}
A'&=\frac{2F(4-A)}G,&
B'&=\frac D{4-A},&
D'&=\frac{2BH}G,\\
E'&=\frac{4ER(4-A)}H,&
F'&=\frac{2ARG}H,&
R'&=\frac G8.
\end{aligned}
\]

**PROVED.** This rational correspondence makes every Fourier coordinate
equal for every \(k\geq2\).

## Length-independent Fourier proof

Let the characters on the long path be
\(g_1,\ldots,g_k\), and let \(q,x\) be those at \(Q,X\).  Put

\[
L=g_1\oplus\cdots\oplus g_k=q\oplus x
\]

and, for \(i\geq2\), put

\[
s_i=g_i\oplus\cdots\oplus g_k.
\]

The three possible middle-path monomials are

\[
\begin{aligned}
X_D&=\prod_{i=2}^k C_{i-1}^{[s_i\ne0]},\\
X_0&=\prod_{i=2}^k C_{i-1}^{[s_i\oplus q\ne0]},\\
X_1&=\prod_{i=2}^k C_{i-1}^{[s_i\oplus L\ne0]}.
\end{aligned}
\]

Reversing the long path sends the target triple to

\[
(X'_D,X'_0,X'_1)=(X_1,X_0,X_D).
\]

After omitting the common long-pendant factor, every zero-sum assignment is
in exactly one of five JC cases.  Direct contraction of the source gives

\[
\begin{array}{c|l}
\text{case}&\widehat p/\prod_i p_i^{[g_i\ne0]}\\ \hline
q=x=0&X_D\\
x=0,\ q\ne0&\displaystyle {R(ABX_D+DX_0)\over4}\\
q=0,\ x\ne0&\displaystyle {ABFX_D+2BEX_D+DFX_1\over16}\\
q=x\ne0&\displaystyle {R(AEX_D+BDEX_0+8FX_D)\over32}\\
q,x,L\ne0&\displaystyle
 {R(ABEX_D+2ABFX_D+BDEX_0+2DFX_1)\over32}.
\end{array}
\]

**EXACTLY COMPUTED.** Substitution of the displayed target map, together
with \((q',x')=(x,q)\) and
\((X'_D,X'_0,X'_1)=(X_1,X_0,X_D)\), reduces each of these five identities
to zero.  These five cases exhaust \(\mathbb Z_2^2\), so this is an exact
all-\(k\) proof rather than extrapolation from finitely many chain lengths.

As independent checks, the verifier contracts all \(64,256,1024\) zero-sum
coordinates symbolically for \(k=2,3,4\), respectively.

## Exact dimension bound

First set all pendant multipliers to one.  For arbitrary, ungauged local
parameters write

\[
a=A,\quad b=B,\quad d=D,\quad e=E,\quad s=x_{SX},
\quad t=x_{VQ},\quad f=F
\]

and let \(\lambda,\mu\) be the inheritance probabilities at \(V,X\).
Define

\[
\alpha=t\lambda ba,\qquad
\beta=t(1-\lambda)d,\qquad
\gamma=\mu esb,\qquad
\delta=(1-\mu)f.
\]

**PROVED.** The complete core tensor depends only on

\[
b,\alpha,\beta,\gamma,\delta,C_1,\ldots,C_{k-1}.
\]

Indeed, in the same five cases its nontrivial coefficients reduce to

\[
\begin{array}{c|l}
x=0&\alpha X_D+\beta X_0\\
q=0&(\gamma+\delta\alpha)X_D+\delta\beta X_1\\
L=0&(\delta+\alpha\gamma/b^2)X_D+\gamma\beta X_0\\
q,x,L\ne0&
\alpha(\delta+\gamma/b)X_D+\gamma\beta X_0+\delta\beta X_1.
\end{array}
\]

The zero case is \(X_D\).  Hence the core rank is at most
\((k-1)+5=k+4\).

Restoring the \(k+2\) pendant parameters can add at most \(k+2\) tangent
directions.  One is already a core direction, because every displayed-tree
monomial satisfies the exact Euler identity

\[
e\,\partial_e\widehat p+f\,\partial_f\widehat p
=w\,\partial_w\widehat p
=[x\ne0]\widehat p.
\]

Therefore

\[
\dim \mathcal M_{\Omega_k}\leq(k+4)+(k+2)-1=2k+5.
\]

## Exact all-\(k\) lower rank

For two consecutive long-path leaves, marginalize all other long-path
leaves.  The resulting four-port tensor is the original \(\Omega_2\) gauge.
For the pair \((P_i,P_{i+1})\), put

\[
L_i=\prod_{j<i}C_j,\qquad
R_i=\prod_{j>i}C_j.
\]

Its six effective core parameters are

\[
bL_i,\quad \alpha L_i,\quad \beta R_i,
\quad\gamma L_i,\quad\delta,\quad C_i.
\]

The six assignments recorded in the certificate have Jacobian determinant

\[
\Delta=
{\alpha\gamma^2(c-1)(c+1)\over b^4}\,P(b,\alpha,\beta,c),
\]

where the verifier records the explicit polynomial \(P\).

Use the rational source point

\[
A=\frac12,\quad B=\frac14,\quad C_i=D=E=\frac12,
\quad F=\frac1{20},\quad R=\frac1{10},\quad p_i=\frac12,
\]

together with the fixed gauge.  At its \(i\)-th adjacent quartet,

\[
L_i=2^{-\ell},\qquad R_i=2^{-r}
\]

for nonnegative integers \(\ell,r\).  Clearing the positive powers of two
from the only nontrivial determinant factor gives

\[
5-196\,2^{2r}-80\,2^\ell
+448\,2^{\ell+r}+64\,2^{2\ell}.
\]

**PROVED.** This integer is odd, hence nonzero.  Thus every adjacent quartet
is regular at the stated rational point.  The first quartet recovers
\(b,\alpha,\gamma,\delta\); all adjacent quartets recover every \(C_i\),
and then \(\beta\) is recovered from any \(\beta R_i\).  Their pendant
coordinates recover all \(p_i\) and \(R\), while \(w=1/2\) is fixed.
Consequently the source gauge has rank at least

\[
(k+4)+(k+1)=2k+5.
\]

Combined with the upper bound, this proves exact dimension \(2k+5\) for
every \(k\).

**EXACTLY COMPUTED.** For \(k=3\), direct differentiation of all 256
coordinates gives the explicit rank-eleven minor

\[
-\frac{81}{755578637259143234191360000000}\ne0.
\]

## Stochastic interior and closure equality

At the rational source point above, the target parameters are

\[
A'=\frac7{12},\quad B'=\frac17,\quad D'=\frac{41}{48},
\quad E'=\frac{28}{41},\quad F'=\frac{12}{205},
\quad R'=\frac3{40},
\]

and every reversed middle or pendant parameter is \(1/2\).

**EXACTLY COMPUTED.** Every source and target value is strictly between zero
and one, all denominators are positive, and all 256 five-leaf coordinates
agree exactly.

**PROVED.** Rational continuity preserves strict stochasticity on a
neighborhood.  The source gauge has full model rank, and its target image has
the identical tensor, so the target Jacobian has the same full rank there.
The inverse-function theorem gives a common regular relatively open
\((2k+5)\)-dimensional neighborhood.  Irreducibility of parameter-space
closures and equal dimension then give equality of the two Zariski closures.

## Root locality

**PROVED.** Restoring an incoming parent port destroys every
`Omega_chain`.  Marginalize to source labels \(1,2,k+1\) together with the
incoming outgroup.  On the target these same labels occupy the reflected two
long-path positions and \(X\).  Suppressing the zero-character intervening
segments reduces exactly to the strict incoming-port certificate for
\(\Omega_2\), with some edge variables replaced by positive products.  The
source invariant remains zero and the target factor remains strictly
positive throughout the complete open JC cube.

Thus `Omega_chain` is an arbitrary-size but root-local move schema.  It does
not create independently stackable non-triangle bits in separate blobs.

## Classification consequence and status

**PROVED.** Any finite JC move system for arbitrary root subdivisions must
state `Omega` as a path-parameterized rule, not as one isolated four-port
replacement.  This does not imply unbounded primitive move complexity: the
whole family has one uniform graph rule and one uniform rational map.

**UNRESOLVED.** Completeness of
`{C_root,R3,T,Theta,Omega_chain}` for every arbitrary root blob is not yet
claimed here.  A bounded-deck census has isolated `Omega_chain` as the only
new five-port collision not already generated by contextual `C_root`; that
census is the next certificate.

No external literature is used during discovery.

## Replay

Run

```sh
PYTHONPATH=src .venv/bin/python src/verify_jc_omega_chain.py
```

The script writes `certificates/jc_omega_chain.json` and independently
checks the universal five-case identity, the effective rank factorization,
the dyadic nonvanishing argument, three complete symbolic contractions, and
the exact five-leaf common rank certificate.
