# The qutrit pair sector: a sharp rank-one SOS and the shifted Gram frontier

## Status

This note does **not** prove the unrestricted pair-sector inequality
\[
 \|\Pi_2C\|_2^2\leq\frac23\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
 \tag{1}
\]
It proves the sharp rank-one bound, polarizes it exactly, and reduces
(1) to one \(2\times2\) shifted Gram determinant involving only the
two common singular planes.

The independent exact checker is
`verification/verify_n3_pair_sector_shifted_gram.py`.

## 1. Notation

On a local qutrit operator space, let
\[
 {\cal P}_i(C)=\frac13I_i\otimes\operatorname{Tr}_iC,
 \qquad {\cal Q}_i=I-{\cal P}_i.
 \tag{2}
\]
The exact degree-two projection on \(M_3^{\otimes3}\) is
\[
 \Pi_2
 ={\cal Q}_1{\cal Q}_2{\cal P}_3
  +{\cal Q}_1{\cal P}_2{\cal Q}_3
  +{\cal P}_1{\cal Q}_2{\cal Q}_3.
 \tag{3}
\]

On two replicas of the physical qutrit triple, let \(F_i\) swap the
two copies of site \(i\).  For vectors \(x,y\), put
\[
 r_S(x,y)
 =
 \langle x\otimes y|
 \prod_{i\in S}F_i
 |x\otimes y\rangle.
 \tag{4}
\]
The swap trick identifies this with
\(\operatorname{Tr}(\rho_S^x\rho_S^y)\), with the standard harmless
choice of whether \(S\) or its complement labels the reduced
operator.  In particular every \(r_S\) is nonnegative.

## 2. Sharp rank-one theorem

### Theorem 2.1

For arbitrary \(x,y\in(\mathbb C^3)^{\otimes3}\),
\[
 \boxed{
 \left\|\Pi_2(|x\rangle\langle y|)\right\|_2^2
 \leq
 \frac49\|x\|^2\|y\|^2.}
 \tag{5}
\]
The constant \(4/9\) is sharp.

#### Proof

Let \(C=|x\rangle\langle y|\).  Directly expanding the three
orthogonal summands in (3), or equivalently using the partial-trace
formula for their squared norms, gives
\[
 \|\Pi_2C\|_2^2
 =
 \frac13\sum_i r_i
 -\frac29\sum_{i<j}r_{ij}
 +\frac19r_{123}.
 \tag{6}
\]
Write \(r_\varnothing=\|x\|^2\|y\|^2\).  Since the local swaps
commute and \(I-F_i\succeq0\), the following is a sum of nonnegative
squared norms:
\[
 \begin{aligned}
 &4r_\varnothing-9\|\Pi_2C\|_2^2\\
 &\quad=
 \sum_{i<j}
 \langle x\otimes y|
 (I-F_i)(I-F_j)
 |x\otimes y\rangle\\
 &\qquad\quad+
 \langle x\otimes y|
 (I-F_1)(I-F_2)(I-F_3)
 |x\otimes y\rangle
 \geq0.
 \end{aligned}
 \tag{7}
\]
Expansion of the right side gives
\[
 4r_\varnothing-3\sum_i r_i
 +2\sum_{i<j}r_{ij}-r_{123},
 \]
which is exactly the left side by (6).

For sharpness take \(x=y=|000\rangle\).  Locally,
\(|0\rangle\langle0|\) has identity-sector squared mass \(1/3\)
and traceless-sector squared mass \(2/3\).  The probability of exactly
one identity sector is therefore
\[
 3\left(\frac13\right)\left(\frac23\right)^2=\frac49.
 \tag{8}
\]
\(\square\)

Equation (7) also gives an exact equality criterion: the two-replica
product \(x\otimes y\) must have no local-swap sector containing two
or three antisymmetric sites.

## 3. Partial transpose and the exterior slack

Under vectorization, \({\cal P}_i\) is the rank-one maximally
entangled projector \(P_i\).  Partial transpose on the second replica
gives
\[
 P_i^\Gamma=\frac13F_i,\qquad
 (I-P_i)^\Gamma=I-\frac13F_i.
 \tag{9}
\]
Thus \(\Pi_2^\Gamma\) is diagonal in the joint local-swap parity
decomposition.  If \(q\) of the three local swaps have eigenvalue
\(-1\), its eigenvalues are
\[
 \begin{array}{c|cccc}
 q&0&1&2&3\\ \hline
 \Pi_2^\Gamma&4/9&4/9&0&-16/9.
 \end{array}
 \tag{10}
\]

Define
\[
 W=\frac23I-\Pi_2.
 \tag{11}
\]
Then
\[
 \boxed{
 W^\Gamma
 =\frac29I+\frac49\Pi_{q=2}^-+\frac{20}{9}\Pi_{q=3}^-
 \succeq0,}
 \tag{12}
\]
where \(\Pi_{q=k}^-\) projects onto the sum of local-swap sectors with
exactly \(k\) antisymmetric sites.

The positive exterior slack in Theorem 2.1 is
\[
 \boxed{
 S:=
 \left(\frac49I-\Pi_2\right)^\Gamma
 =\frac49\Pi_{q=2}^-+\frac{20}{9}\Pi_{q=3}^- .}
 \tag{13}
\]
Indeed, (7) is exactly
\[
 \langle x\otimes y|S|x\otimes y\rangle
 =\frac49\|x\|^2\|y\|^2
  -\|\Pi_2(|x\rangle\langle y|)\|_2^2.
 \tag{14}
\]
This isolates the missing geometry: only the sectors with at least
two local exterior factors contribute to the rank-one slack.

## 4. The exact shifted \(2\times2\) Gram problem

Let
\[
 C_r=|x_r\rangle\langle y_r|,\qquad r=1,2,
 \tag{15}
\]
where \(x_1,x_2\) are orthonormal and \(y_1,y_2\) are orthonormal.
Define
\[
 G_{rs}=\langle C_r,\Pi_2C_s\rangle_{\rm HS}.
 \tag{16}
\]
Because \(\Pi_2\) is an orthogonal projection, \(G\succeq0\).
Every matrix
\[
 C=\lambda_1C_1+\lambda_2C_2
 \tag{17}
\]
has rank at most two and
\[
 \|C\|_2^2=|\lambda_1|^2+|\lambda_2|^2,\qquad
 \|\Pi_2C\|_2^2=\lambda^\dagger G\lambda.
 \tag{18}
\]
Conversely every rank-two matrix has this form in a singular-value
frame.  Therefore (1) is exactly equivalent to
\[
 \boxed{G\preceq\frac23I_2}
 \tag{19}
\]
for every pair of orthonormal planes and every matching of their
orthonormal frames.

Theorem 2.1 gives the sharp diagonal estimates
\[
 0\leq G_{11},G_{22}\leq\frac49.
 \tag{20}
\]
Thus the whole remaining statement is the single determinant
\[
 \boxed{
 \left(\frac23-G_{11}\right)
 \left(\frac23-G_{22}\right)
 \geq |G_{12}|^2.}
 \tag{21}
\]

The polarization orientation is important.  Equations (9)--(13) give
\[
 \frac23\delta_{rs}-G_{rs}
 =
 \langle x_r\otimes y_s|
 W^\Gamma
 |x_s\otimes y_r\rangle.
 \tag{22}
\]
For \(r\ne s\), the identity part of \(W^\Gamma\) vanishes because
both singular frames are orthonormal.  Hence
\[
 -G_{12}
 =
 \langle x_1\otimes y_2|
 S
 |x_2\otimes y_1\rangle.
 \tag{23}
\]
Combining (14), (21), and (23), the missing inequality is the
crossed exterior Cauchy inequality
\[
 \begin{aligned}
 &\left(\frac29+
 \langle x_1\otimes y_1|S|x_1\otimes y_1\rangle\right)
 \left(\frac29+
 \langle x_2\otimes y_2|S|x_2\otimes y_2\rangle\right)\\
 &\qquad\geq
 \left|
 \langle x_1\otimes y_2|S|x_2\otimes y_1\rangle
 \right|^2.
 \end{aligned}
 \tag{24}
\]
Ordinary Cauchy--Schwarz for \(S\succeq0\) has the crossed diagonal
terms
\(\langle x_1y_2,Sx_1y_2\rangle\) and
\(\langle x_2y_1,Sx_2y_1\rangle\), and therefore does not prove
(24).  The replacement of those crossed norms by the two matched
norms plus \(2/9\) is precisely the common-Pluecker information still
missing.

## 5. Sharp rank-two equality

Let \(E_{01}=|0\rangle\langle1|\) and
\(P_r=|r\rangle\langle r|\).  Take
\[
 C_1=E_{01}\otimes E_{01}\otimes P_0,\qquad
 C_2=E_{01}\otimes E_{01}\otimes P_1.
 \tag{25}
\]
These are matched dyads from orthonormal left and right frames.
Their degree-two projections coincide:
\[
 \Pi_2C_1=\Pi_2C_2
 =\frac13E_{01}\otimes E_{01}\otimes I_3.
 \tag{26}
\]
Consequently
\[
 G=\frac13
 \begin{pmatrix}1&1\\1&1\end{pmatrix},
 \qquad
 \operatorname{spec}(G)=\left\{0,\frac23\right\}.
 \tag{27}
\]
Thus (21), if proved, is sharp, and neither a strict-gap argument nor
an off-diagonal estimate below \(1/3\) can work.

## 6. Remaining exact lemma

The pair-sector frontier is now:

> **Crossed exterior determinant lemma.**  For the exterior-sector
> operator \(S\) in (13) and orthonormal pairs
> \(x_1,x_2\), \(y_1,y_2\), prove (24).

This is strictly smaller than the original partial-trace expression:
the rank-one diagonal problem has been removed completely, the
partial transpose is positive, and only two explicitly weighted
exterior sectors remain.  Any proof must use that all four entries
come from the same two decomposable bivectors; bounding the crossed
pair independently loses exactly the information required at the
sharp family (25).
