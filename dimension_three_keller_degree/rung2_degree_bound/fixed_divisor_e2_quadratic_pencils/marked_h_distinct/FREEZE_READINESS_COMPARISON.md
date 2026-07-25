# Comparison and freeze readiness for marked companion moduli

**Reviewed (UTC):** 2026-07-25.

## Verdict

The clean-room reconstruction in
`../audit_marked_orbit_reconstruction/REPORT.md` agrees exactly with the
independent scope failure and stabilizer quotient derived in this
directory:
\[
\boxed{3+\mathbb P^1(\mathbb C)+3}.
\]

There is no discrepancy to reconcile.  The quotient taxonomy is ready to
be frozen as an **internal parameterized stratification** of
`Q2-E2-A2-B1-D1-N1`, using the stable IDs assigned by the clean-room
report.  It does not change the denominator of the inclusive frozen
taxonomy.

The exclusion row is emphatically **not** ready for promotion.  The
existing calculations cover six endpoint slices and the \(E_7/E_6\)
stage of the middle \(\tau\)-family only.  No \(E_5\) work should resume
until the parent freeze incorporates the full quotient.

This comparison is not peer reviewed and was materially AI-assisted.
Exact checks certify encoded algebra, not peer review.

## 1. Independence and agreement

The clean-room agent completed and checkpointed its classification before
reading this directory or the earlier readiness report.  It independently
recovered:

1. the three marked pairs
   \[
   (s,h)=(x^2,yz),\quad
   (x^2,x^2+yz),\quad
   (x^2,y^2+xz);
   \]
2. residual companion actions consisting respectively of a torus, the
   identity, and a torus;
3. companion orbit spaces \(3,\mathbb P^1,3\);
4. the fact that source translations do not move the projective normal
   companion.

Its dependency-free checker reconstructs ranks, discriminants, unique
double members, and residual stabilizer images.  Independently, the
SymPy/PARI pair in this directory verifies the two exact counterexamples
that broke the six-endpoint proposal:
\[
\begin{aligned}
h=yz,\quad &G=x(x^2+yz),\\
h=x^2+yz,\quad &G=xyz.
\end{aligned}
\]
Their quadratic quotients have ranks distinct from both previously
computed endpoints.  Thus the clean-room orbit result and the algebraic
counterexamples cross-check one another by different mechanisms.

## 2. Stable-name map for the existing slice algebra

| Existing slice label | Clean-room stable ID | Companion parameter |
|---|---|---|
| RT-reducible/H | `Q2-E2-A2-B1-D1-N1-MD-P21-HR2-CH` | \(r=h=yz\) |
| RT-reducible/S | `Q2-E2-A2-B1-D1-N1-MD-P21-HR2-CS` | \(r=s=x^2\) |
| RT-smooth/H | `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CH` | \(\tau=0,\ r=h\) |
| RT-smooth/S | `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CS` | \(\tau=\infty,\ r=s\) |
| RO-smooth/H | `Q2-E2-A2-B1-D1-N1-MD-P3-HSM-CH` | \(r=h=y^2+xz\) |
| RO-smooth/S | `Q2-E2-A2-B1-D1-N1-MD-P3-HSM-CS` | \(r=s=x^2\) |

The omitted frozen companion strata are:

- `Q2-E2-A2-B1-D1-N1-MD-P21-HR2-CO`,
  represented by \(r=x^2+yz\);
- `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CT`,
  the intrinsic value \(\tau=-1\), where \(r=yz\);
- `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CTAU` with a required
  `tau=<value>` field for every
  \(\tau\in\mathbb C\setminus\{0,-1\}\);
- `Q2-E2-A2-B1-D1-N1-MD-P3-HSM-CO`,
  represented by \(r=x^2+y^2+xz\).

The zero-normal `-C0` branches remain terminal through the separately
certified quadratic-component exit.

## 3. Correct projective parameter for the middle family

For
\[
s=x^2,\qquad t=yz,\qquad h=s+t=x^2+yz,
\]
use homogeneous companion coordinates
\[
\boxed{
[u:v]\in\mathbb P^1,\qquad
r_{[u:v]}=u\,h+v\,s,\qquad
R_{[u:v]}=x\,r_{[u:v]}.
}                                                     \tag{1}
\]
This representation is polynomial and retains the point at infinity.
On the affine chart \(u=1\), put
\[
\tau=v/u,\qquad r_\tau=h+\tau s.                     \tag{2}
\]
The stable boundaries are
\[
\begin{array}{c|c|c}
\text{ID suffix}&[u:v]&\tau\\ \hline
\mathrm{CH}&[1:0]&0\\
\mathrm{CT}&[1:-1]&-1\\
\mathrm{CS}&[0:1]&\infty\\
\mathrm{CTAU}&uv(u+v)\ne0&
  \tau\in\mathbb C\setminus\{0,-1\}.
\end{array}                                           \tag{3}
\]

Future uniform calculations should store \([u:v]\), not only an affine
symbol.  Computation may use \(u=1\), but every denominator must be
homogenized back and the \(u=0\) chart must be rebuilt separately.
Although \(\tau=-1\) is algebraically generic at \(E_7/E_6\), the divisor
\(u+v=0\) must remain declared because it is an intrinsic rank-two
companion boundary in the frozen orbit taxonomy.

## 4. The \(\tau\) modulus survives \(E_7\) symbolically

Set
\[
H_4=(h^2,hs,0),\qquad
R=x(h+\tau s)
\]
on the finite chart.  The exact raw \(E_7\) matrix has:

\[
\begin{array}{c|c|c}
\tau&\operatorname{rank}E_7&\text{legal normal dimension}\\ \hline
0&14&7\\
\tau\ne0&18&3\\
\infty&16&5.
\end{array}                                           \tag{4}
\]

For every finite \(\tau\ne0\), a complete complement to the five legal
gauges is
\[
\boxed{
U=Ax^3,\qquad V=Bx^3,\qquad W=Tx^2.
}                                                     \tag{5}
\]
The normal-basis minor is the constant \(-4\).

The rank-\(18\) assertion is specialization-safe.  Put
\[
q(\tau)=9\tau^2+6\tau-1.
\]
Two pinned \(18\times18\) minors are
\[
\begin{aligned}
\Delta_{7,q}
  &=-557256278016\,\tau^8q(\tau)^2,\\
\Delta_{7,\ell}
  &=-557256278016\,\tau^8(3\tau-1)^2.
\end{aligned}                                        \tag{6}
\]
Since
\[
\gcd(q(\tau),3\tau-1)=1,
\]
their nonvanishing charts cover all \(\tau\ne0\).  The only common
rank-drop divisor on the finite line is \(\tau=0\), which is the
separately computed `CH` boundary.  In particular \(\tau=-1\) is not an
\(E_7\) rank drop.

Thus \(E_7\) reduces the lower normal space on the punctured chart but
does not identify or constrain distinct nonzero values of \(\tau\).

## 5. The \(\tau\) modulus also survives \(E_6\)

Substitute (5), retain all twelve coefficients in the first two
quadratic components and all nine coefficients of \(L\), and form
\(E_6=0\).  For every \(\tau\ne0\):

- the \(28\times21\) lower-data matrix has rank \(10\);
- its inhomogeneous right side is identically zero;
- therefore there is **no \(E_6\) compatibility equation at all** on
  \(A,B,T,\tau\).

Two pinned rank-\(10\) minors are
\[
\begin{aligned}
\Delta_{6,q}
  &=-331776\,\tau^4q(\tau)^2,\\
\Delta_{6,\ell}
  &=-331776\,\tau^4(3\tau-1)^2.
\end{aligned}                                        \tag{7}
\]
They give the same complete two-chart cover of \(\tau\ne0\).

At \(\tau=0\), the separately computed `CH` normal space has rank
\(14\) at \(E_7\), and its \(E_6\) compatibility ideal is
\[
(AC,AD,AE,AF,CE,DF,E^2,F^2).
\]
At \(\tau=\infty\), the separately computed `CS` normal space has rank
\(16\) at \(E_7\), and its \(E_6\) compatibility ideal is
\[
(C^2,D^2).
\]
Both boundaries survive.

A uniform determinant-one lower witness exists for every finite
\(\tau\): take \(U=V=W=H_2=0\), retain the fixed \(R\), and use
\[
L=
\begin{pmatrix}
0&1&0\\0&0&1\\1&0&0
\end{pmatrix}.
\]
It satisfies \(E_9,E_8,E_7,E_6\).  Hence
\[
\boxed{\text{every }\tau\in\mathbb P^1(\mathbb C)
\text{ survives through }E_6.}
\]

This is checked independently by
`verify_tau_family_sympy.py` and `verify_tau_family_pari.gp`.

## 6. Freeze/readiness decision

### Ready to freeze

- the three marked-pair IDs;
- the two discrete \(3\)-orbit companion quotients;
- the full middle \(\mathbb P^1\) companion quotient;
- special values \(0,-1,\infty\) and the parameterized `CTAU` key;
- homogeneous representation (1) and boundary divisor
  \(uv(u+v)=0\).

### Not ready for exclusion or promotion

- neither open `CO` orbit has an \(E_7/E_6\) package yet;
- the middle family has only been carried through \(E_6\);
- no \(E_5\) taxonomy or specialization-safe lower pivot atlas exists;
- no post-freeze full-row assembly audit exists.

The next uniform computation, only after the parent freeze is recorded,
should take (1) as input.  It should use the finite main chart
\(u=1,\tau\ne0\) with the two pivot charts in (6)--(7), while retaining
the frozen divisor \(\tau+1=0\) for `CT`.  It must rebuild the
\(u=0\) (`CS`) and \(v=0\) (`CH`) boundaries rather than specializing a
localized solve.
