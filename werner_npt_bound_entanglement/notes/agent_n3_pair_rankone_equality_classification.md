# Complete equality classification for the three-site rank-one pair-sector bound

## Status

This note proves two exact results at the boundary of the sharp qutrit
rank-one inequality
\[
 \left\|\Pi _2(|x\rangle\langle y|)\right\|_2^2
 \leq \frac49\|x\|^2\|y\|^2.                         \tag{1}
\]

First, it classifies every nonzero equality pair \((x,y)\), without a
reality or symmetry assumption.  Up to interchanging \(x\) and \(y\),
there are only two mechanisms:

1. \(x\) is a product vector and \(y\) is tangent to the product-vector
   variety at \(x\);
2. \(x\) and \(y\) have a common local factor, and on the other two
   sites their \(2\times2\) coefficient matrices \(X,Y\) obey the one
   polarized-determinant equation
   \[
     \operatorname{Tr}(X^{-1}Y)=0.                    \tag{2}
   \]

The apparent full-local-rank \(W\) mechanism is case 1 with the product
vector on the \(y\)-side.  There is no third equality orbit.

Second, the product-saturation spectral gap proved previously extends
to case 2.  If \(x,y\) are unit vectors, equality holds in (1), and
\[
 E=\Pi _2(|x\rangle\langle y|),
\]
then
\[
 \boxed{s_2(E)\leq\frac29.}                            \tag{3}
\]
In case 2 one has the stronger oriented operator inequality
\[
 \boxed{
 E^\dagger E\preceq
 \frac4{81}I+\frac{12}{81}|y\rangle\langle y|.}        \tag{4}
\]
Together with the earlier product-left certificate and its adjoint,
this proves (3) on the complete equality locus.

This does not yet prove the unrestricted rank-two pair-sector theorem:
a quantitative stability statement away from the equality locus is
still needed.  It does remove all unclassified rank-one saturation
types from that problem.

The independent symbolic checker is
`verification/verify_n3_pair_rankone_equality_classification.py`.

## 1. Equality as a local-parity condition

Let \(F_i\) swap the \(i\)-th local factors of two replicas and put
\[
 A_i=\frac{I-F_i}{2},\qquad S_i=\frac{I+F_i}{2}.
\]
For unit \(x,y\), the exact rank-one slack identity is
\[
\begin{aligned}
4-9\|\Pi _2(|x\rangle\langle y|)\|_2^2
={}&4\sum_{i<j}\|A_iA_j(x\otimes y)\|^2\\
 &+8\|A_1A_2A_3(x\otimes y)\|^2.                       \tag{5}
\end{aligned}
\]
The last term is redundant once the first three vanish, but it is
useful for displaying the parity.  Equality is therefore equivalent
to
\[
 A_iA_j(x\otimes y)=0\qquad(i<j).                      \tag{6}
\]

Decompose \(x\otimes y\) into the eight simultaneous local-swap
sectors.  Equation (6) says that sectors with two or three
antisymmetric sites vanish.  Consequently
\[
 x\otimes y+y\otimes x
 \in\bigotimes_{i=1}^3\operatorname{Sym}^2 H_i,        \tag{7}
\]
whereas
\[
 x\otimes y-y\otimes x
 \in\bigoplus_{i=1}^3
 \left(\bigwedge\nolimits^2H_i\right)
 \otimes\!\!\bigotimes_{j\ne i}\operatorname{Sym}^2H_j.
                                                               \tag{8}
\]
Equation (7) is the simultaneous polarized-minor equation.  Equation
(8) additionally removes the three-local-exterior component.

## 2. A polarized-minor lemma

For matrices \(X,Y\in M_{m,n}(\mathbb C)\), write
\[
\begin{aligned}
 {\cal B}(X,Y)_{ab;\mu\nu}
={}&X_{a\mu}Y_{b\nu}+Y_{a\mu}X_{b\nu}\\
 &-X_{a\nu}Y_{b\mu}-Y_{a\nu}X_{b\mu}.                 \tag{9}
\end{aligned}
\]
This is the coefficient of \(t\) in every \(2\times2\) minor of
\(X+tY\).

### Lemma 2.1

Suppose \(X\ne0\) and \({\cal B}(X,Y)=0\).

* If \(\operatorname{rank}X\ge3\), then \(Y=0\).
* If \(\operatorname{rank}X=2\), then \(Y\) has the same row and
  column supports as \(X\), and, on these two-dimensional supports,
  \[
    \operatorname{Tr}(X^{-1}Y)=0.                      \tag{10}
  \]
* If \(\operatorname{rank}X=1\), say \(X=u v^{\mathsf T}\), then
  \[
    Y=u w^{\mathsf T}+zv^{\mathsf T}                   \tag{11}
  \]
  for some \(w,z\).  Thus \(Y\) is tangent to the rank-one matrix
  variety at \(X\).

#### Proof

Invertible row and column changes preserve (9), so take
\[
 X=\begin{pmatrix}I_r&0\\0&0\end{pmatrix}.             \tag{12}
\]
If \(r=1\), the equation with row pair \((1,b)\) and column pair
\((1,\nu)\), where \(b,\nu>1\), says \(Y_{b\nu}=0\).  This is exactly
(11).

If \(r=2\), equations using one index outside the leading \(2\times2\)
block kill every entry of \(Y\) outside that block.  The sole equation
inside it is
\[
 Y_{11}+Y_{22}=0,                                      \tag{13}
\]
which is (10).

If \(r\ge3\), the same outside-index equations kill all entries outside
the leading block.  Inside it, choosing three distinct indices first
kills every off-diagonal entry and then gives
\[
 Y_{ii}+Y_{jj}=0\qquad(i\ne j).
\]
Three such equations force every diagonal entry to vanish.  Hence
\(Y=0\). \(\square\)

## 3. Complete classification

Let \(r_i\) be the rank of the \(i:(jk)\) flattening of \(x\).
Equation (7), applied to each flattening, and Lemma 2.1 imply
\[
 r_i\le2\qquad(i=1,2,3),                               \tag{14}
\]
because \(y\ne0\).  Exactly one of the \(r_i\)'s cannot equal two:
if the other two are one, then \(x\) is a product vector and the
remaining rank is also one.  There are therefore three cases.

### 3.1 Multilinear rank \((1,1,1)\)

Put \(x=|000\rangle\) by local changes of basis.  The rank-one part of
Lemma 2.1 at all three cuts says that a coefficient of \(y\) can be
nonzero only if at most one local index is nonzero.  Hence
\[
 y=a|000\rangle+|b_1\,00\rangle+|0\,b_2\,0\rangle
   +|00\,b_3\rangle, \qquad b_i\perp|0\rangle.          \tag{15}
\]
This is precisely the tangent space to the product-vector variety at
\(x\).  Conversely (15) plainly has no sector with two local exterior
factors, so it gives equality.

### 3.2 Multilinear rank \((1,2,2)\)

After permuting sites, write
\[
 x=|0\rangle\otimes \operatorname{vec}X,\qquad
 \operatorname{rank}X=2.                              \tag{16}
\]
The rank-one equation at the first cut initially permits
\[
 y=|0\rangle\otimes\operatorname{vec}Y
   +|b\rangle\otimes\operatorname{vec}X.               \tag{17}
\]
The column-support conclusion at either rank-two cut forces
\(|b\rangle\) to be proportional to \(|0\rangle\).  Absorbing that
part into \(Y\), one obtains
\[
 y=|0\rangle\otimes\operatorname{vec}Y.                \tag{18}
\]
The remaining polarized-minor equation is exactly (10).  The
three-local-exterior sector vanishes automatically because the first
local factor is common.  This is case 2 in the statement.

### 3.3 Multilinear rank \((2,2,2)\)

All vectors now lie in intrinsic two-dimensional local supports.  By
the rank-two part of Lemma 2.1, for each site there is a unique
traceless \(2\times2\) matrix \(M_i\) such that
\[
 y=M_1^{(1)}x=M_2^{(2)}x=M_3^{(3)}x.                   \tag{19}
\]
Since a traceless \(2\times2\) matrix obeys
\[
 M_i^2=-\det(M_i)I,
\]
commuting two different local actions in (19) gives
\[
 \det M_1=\det M_2=\det M_3.                           \tag{20}
\]

If this common determinant is nonzero, local changes of basis and a
common scaling put every \(M_i\) in the form
\(\operatorname{diag}(1,-1)\).  Equation (19) then forces
\[
 x=p|000\rangle+q|111\rangle,\qquad
 y=p|000\rangle-q|111\rangle.                          \tag{21}
\]
Full local rank gives \(pq\ne0\).  But the
\(\bigwedge^2H_1\otimes\bigwedge^2H_2\otimes
\bigwedge^2H_3\) component of \(x\otimes y\) is then a nonzero
multiple of
\[
 |000\rangle\otimes|111\rangle
 -|111\rangle\otimes|000\rangle,
\]
contradicting (8).

The common determinant must therefore be zero.  Since \(y\ne0\), all
\(M_i\) are nonzero nilpotents.  Independent local changes of basis
put each one in the form
\[
 N=|0\rangle\langle1|.
\]
Solving \(N_1x=N_2x=N_3x\) coefficient by coefficient gives
\[
 x=p|000\rangle+q(|100\rangle+|010\rangle+|001\rangle),
 \qquad y=q|000\rangle,                                \tag{22}
\]
with \(q\ne0\).  Thus \(y\) is product and \(x\) is tangent at \(y\):
this is case 1 after interchanging the two vectors.

This proves the classification.

## 4. Canonical form for the common-factor case

It remains to prove the spectral certificate.  Local unitaries put
the case (16)--(18) in the form
\[
\begin{aligned}
 x&=|0\rangle\otimes
    (a|00\rangle+b|11\rangle),\\
 y&=|0\rangle\otimes
    (az|00\rangle+s|01\rangle+t|10\rangle-bz|11\rangle),
                                                               \tag{23}\\
 a,b&\ge0,\qquad a^2+b^2=1,\qquad
 |z|^2+|s|^2+|t|^2=1.
\end{aligned}
\]
The form of \(y\) is exactly the polarized determinant equation
\[
 aY_{11}+bY_{00}=0.                                    \tag{24}
\]

On the last two sites, decompose
\[
 |\operatorname{vec}X\rangle\langle\operatorname{vec}Y|
 =Z_0+Z_1+Z_2
\]
by local traceless degree.  Put \(A=Z_2\), \(B=Z_1\).  Since
\[
 |0\rangle\langle0|=\frac13I+q,
\]
where \(q\) is traceless, the operator
\[
 E=\Pi _2(|x\rangle\langle y|)
\]
is block diagonal in the first local computational basis:
\[
 E=E_0\oplus E_1\oplus E_1,\qquad
 E_0=\frac{A+2B}{3},\quad E_1=\frac{A-B}{3}.            \tag{25}
\]

Thus (4) is equivalent to
\[
\begin{aligned}
 (9E_0)^\dagger(9E_0)&\preceq4I_9+12|Y\rangle\langle Y|,\\
 (9E_1)^\dagger(9E_1)&\preceq4I_9.                    \tag{26}
\end{aligned}
\]

## 5. The distinguished first block

Set
\[
 H_0=4I_9+12|Y\rangle\langle Y|-(9E_0)^\dagger(9E_0).
\]
It splits into blocks on the index sets
\[
 (00,01,10,11),\qquad(02,12),\qquad(20,21),\qquad(22).
                                                               \tag{27}
\]
On the first block, define
\[
 \eta=(az,s,t,-bz)^{\mathsf T},\qquad
 w=(b,0,0,a)^{\mathsf T}.
\]
Then
\[
 H_0^{(4)}
 =4(I-|\eta\rangle\langle\eta|)-|w\rangle\langle w|.   \tag{28}
\]
Here \(\|\eta\|=\|w\|=1\) and
\(\langle w,\eta\rangle=0\), so its spectrum is
\[
 \{0,3,4,4\}.                                          \tag{29}
\]

The \((02,12)\) block is
\[
\begin{pmatrix}
4-b^2(b^2|z|^2+|s|^2)&
ab(a s\bar z-bz\bar t)\\
ab(a z\bar s-bt\bar z)&
4-a^2(a^2|z|^2+|t|^2)
\end{pmatrix},                                         \tag{30}
\]
and the other \(2\times2\) block is obtained by interchanging \(s,t\).
Each diagonal entry in (30) is at least \(3\), while
\[
 |ab(a s\bar z-bz\bar t)|
 \le ab|z|\sqrt{|s|^2+|t|^2}\le\frac14.                \tag{31}
\]
Thus both blocks are positive.  The last scalar is
\[
 4-(a^2-b^2)^2|z|^2\ge3.                               \tag{32}
\]
This proves the first line of (26).

## 6. The repeated block

Put
\[
 H_1=4I_9-(9E_1)^\dagger(9E_1).
\]
It has the same block pattern (27).  The two \(2\times2\) blocks of
\(9E_1\) are, up to interchanging \(s,t\),
\[
 \begin{pmatrix}
 -\bar z&-2a\bar t\\
 -2b\bar s&\bar z
 \end{pmatrix}.                                        \tag{33}
\]
Their squared Frobenius norms obey
\[
 2|z|^2+4a^2|t|^2+4b^2|s|^2\le4,                      \tag{34}
\]
so their operator norms are at most \(2\).  The last scalar has
absolute value at most one.

Only the leading \(4\times4\) block remains.  Apply orthogonal changes
of basis to its first and last pairs of coordinates and put
\[
 d=a^2-b^2,\qquad k=2ab,\qquad d^2+k^2=1.
\]
The block becomes
\[
 K=
\begin{pmatrix}
d\bar z&k\bar z&k\bar s&k\bar t\\
-2k\bar z&0&d\bar s&d\bar t\\
-2\bar t&0&-d\bar z&0\\
-2\bar s&0&0&-d\bar z
\end{pmatrix}.                                         \tag{35}
\]
We prove \(K^\dagger K\preceq4I\).

Write
\[
 D=d^2,\quad u=|z|^2,\quad p=|s|^2,\quad q=|t|^2,
\quad
 \chi=z^2\bar s\bar t+\bar z^2st.                      \tag{36}
\]
Thus \(u+p+q=1\), \(k^2=1-D\), and
\[
 \chi\ge-2u\sqrt{pq}.                                  \tag{37}
\]
Direct determinant expansion gives
\[
\det(4I-K^\dagger K)
=4D\left\{u\,{\cal A}
+2k(4-Du)(2-k^2u)\chi\right\},                         \tag{38}
\]
where
\[
\begin{aligned}
{\cal A}={}&Dk^4u^3-4k^4u^2+(16-13D)u+4D+20\\
&-4(4-Dk^2u)pq.                                        \tag{39}
\end{aligned}
\]
Since \(\sqrt{pq}\le(1-u)/2\), and the right side decreases as
\(\sqrt{pq}\) increases after using (37), (38)--(39) imply that the
quantity in braces is at least
\[
 u(4-Du)\,G(k,u),                                      \tag{40}
\]
where
\[
\begin{aligned}
G(k,u)
={}&5-4k-k^2\\
 &+(2k^3+2k^2+4k+4)u-k^2(k+1)^2u^2.                  \tag{41}
\end{aligned}
\]
For fixed \(k\in[0,1]\), this is concave in \(u\), and
\[
G(k,0)=(1-k)(k+5)\ge0,\qquad
G(k,1)=9-k^4>0.                                        \tag{42}
\]
Hence the determinant in (38) is strictly positive whenever
\(d\ne0\) and \(z\ne0\).

The parameter space with \(d>0,z\ne0\) is connected, as is the one
with \(d<0,z\ne0\).  On each component the inertia of
\(4I-K^\dagger K\) is constant by (38).  At \(k=0\), \(z=1\), the
matrix \(K\) has singular values \(1,1,1,0\), so the inertia is
positive.  Therefore
\[
 4I-K^\dagger K\succ0
\]
throughout both open components.

The omitted boundary has a direct proof.  If \(d=0\), write an input
as \((P,Q,\xi)\in\mathbb C\oplus\mathbb C\oplus\mathbb C^2\) in the
basis used for (35), and put \(r=(s,t)\), with \(J(s,t)=(t,s)\).
Then
\[
 K(P,Q,\xi)
 =\bigl(zQ+r^{\mathsf T}\xi,\,-2zP,\,-2JrP\bigr).
                                                               \tag{43}
\]
Cauchy--Schwarz gives
\[
 \|K(P,Q,\xi)\|^2
 \le |Q|^2+\|\xi\|^2+4|P|^2
 \le4(|P|^2+|Q|^2+\|\xi\|^2).                          \tag{44}
\]
If \(z=0\), then
\[
 K(P,Q,\xi)
 =\bigl(kr^{\mathsf T}\xi,\,
        dr^{\mathsf T}\xi,\,-2JrP\bigr),               \tag{45}
\]
and the same estimate follows from \(d^2+k^2=\|r\|^2=1\).
This completes the second line of (26), hence proves (4).

## 7. Uniform equality-locus spectral gap

In the common-factor case, (4) implies
\[
 s_2(E)^2\le\frac4{81}.                                \tag{46}
\]
Indeed the rank-one term on the right of (4) can affect at most the
largest eigenvalue.  The product-left case has the same certificate
by the earlier product-saturation theorem.  In the product-right
case, apply that theorem to \(E^\dagger\); singular values are
unchanged.  By the classification these cases exhaust the equality
locus, proving (3).

Moreover equality in (1), (4), and Cauchy--Schwarz gives
\[
 Ey=\frac49x,\qquad E^\dagger x=\frac49y,               \tag{47}
\]
so \(s_1(E)=4/9\).  Thus every rank-one saturation point has the
uniform singular-value pattern
\[
 s_1(E)=\frac49,\qquad s_2(E)\le\frac29.                \tag{48}
\]

For a pair-only dual operator \(D=\tau E\) exposed at rank-one
saturation, the standard normalization
\[
 \|D\|_2^2=3\sum_{i<j}\|B_{ij}\|_2^2
\]
then yields
\[
 s_1(D)^2+s_2(D)^2
 \le\frac53\sum_{i<j}\|B_{ij}\|_2^2,                   \tag{49}
\]
with a strict \(1/3\) margin below the desired constant \(2\).
Any failure of the unrestricted pair-sector theorem must therefore
stay quantitatively away from the complete rank-one equality locus,
not merely away from product saturation.
