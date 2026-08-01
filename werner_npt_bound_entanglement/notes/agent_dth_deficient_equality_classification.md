# Equality classification on the deficient-local-rank DTH boundary

## Status

The deficient-local-rank Ky--Fan theorem is sharp, but its equality set was
not previously classified.  This note proves:

\[
\boxed{
\begin{gathered}
 \operatorname{rank}\rho_i^z\le2\text{ for some site }i,\\
 \sum_{j=1}^4s_j(D_z)^2={1\over2}\|z\|^2
 \quad\Longrightarrow\quad
 \operatorname{rank}\rho_k^z=1\text{ for some site }k.
\end{gathered}}
\tag{1}
\]

More precisely, after permuting sites,

\[
 z=a\otimes\xi,
 \qquad \operatorname{SchmidtRank}(\xi)\le2.
\tag{2}
\]

Thus every equality point on the already-solved deficient-support boundary
belongs to the one-site-factor equality mechanism found by the direct
physical optimizer.  A hypothetical equality point outside (2) must have
all three one-site marginals positive definite.

This does not exclude a full-local-rank equality point or a strict
violation.  It reduces the stationarity problem to that interior locus.

## 1. The double-Hodge equality spaces

For (X\in M_3(\mathbb C)), put

\[
 \mathscr D_X=\sum_{p,q}X_{pq}A_p\otimes A_q,
 \qquad (A_p)_{ai}=2^{-1/2}\varepsilon_{pai},
\]

and let

\[
 k_2(X)=\lambda_1(\mathscr D_X^\dagger\mathscr D_X)
       +\lambda_2(\mathscr D_X^\dagger\mathscr D_X).
\]

### Lemma 1

For every (X),

\[
 k_2(X)\le {1\over2}\|X\|_2^2,
\tag{3}
\]

and equality holds if and only if

\[
 \operatorname{rank}X\le2.
\tag{4}
\]

If (X\ne0) has rank two, its top right singular space
\(E_X\subset M_3\) has dimension two.  In singular coordinates

\[
 X=\operatorname{diag}(a,b,0),
 \qquad a,b>0,
\]

it is

\[
 \boxed{E_X=\operatorname{span}
 \{E_{22},\ bE_{00}+aE_{11}\}.}
\tag{5}
\]

If (X=uv^\dagger\) has rank one, its top space has dimension four and
is

\[
 \boxed{E_X=\{Z:u^\dagger Z=0,\ Zv=0\}.}
\tag{6}
\]

### Proof

Hodge covariance reduces (X) to

\[
 X=\operatorname{diag}(a,b,c),
 \qquad a,b,c\ge0,
 \qquad s=a^2+b^2+c^2.
\]

On the six off-diagonal matrix units, the singular values of
\(\mathscr D_X\) are

\[
 {a\over2},{a\over2},{b\over2},{b\over2},
 {c\over2},{c\over2}.
\tag{7}
\]

On the three diagonal matrix units, the matrix is

\[
 B={1\over2}
 \begin{pmatrix}
 0&c&b\\ c&0&a\\ b&a&0
 \end{pmatrix},
 \qquad \operatorname{Tr}B^2={s\over2}.
\tag{8}
\]

Two values from (7) have squared sum at most (a^2/2\le s/2),
with equality only at rank one.  Two singular values from (B) have
squared sum at most (s/2), with equality only if the third eigenvalue
vanishes.  Since

\[
 \det B={abc\over4},
\]

that equality requires rank at most two.

For a mixed pair, the principal (2\times2) submatrix containing the
edge (a/2) has eigenvalues (a/2,-a/2).  Interlacing implies that,
after removing an eigenvalue of (B) of largest absolute value, one
remaining squared eigenvalue is at least (a^2/4).  Hence

\[
 \|B\|_{\rm op}^2+{a^2\over4}
 \le \operatorname{Tr}B^2={s\over2}.
\]

Equality again forces the unused eigenvalue of (B) to vanish, hence
\(abc=0).  This proves necessity in (4).  If (c=0), the diagonal block
has eigenvalues

\[
 {\sqrt s\over2},-{\sqrt s\over2},0,
\]

so (3) is an equality.  This proves sufficiency.

The eigenspaces of the explicit blocks give (5).  When (b=c=0), the
top eigenspace is the lower-right (2\times2) matrix space.  Undoing the
singular-coordinate changes gives (6).  \(\square\)

## 2. A common-top-space rigidity lemma

### Lemma 2

Let (X,Y\in M_3\) be nonzero with rank at most two.  Suppose there is a
two-plane

\[
 P\subset E_X\cap E_Y.
\tag{9}
\]

Then exactly the following possibilities can occur.

1. If both (X,Y) have rank two, then (Y\) is proportional to (X).
2. If both have rank one, then they have a common left factor or a common
   right factor.
3. One cannot have one matrix of rank two and the other of rank one.

### Proof

If both matrices have rank two, both top spaces have dimension two, so
\(E_X=E_Y\).  Put (X=\operatorname{diag}(a,b,0)\).  In the projective
line (5),

\[
 \det\left(alpha(bE_{00}+aE_{11})+\beta E_{22}\right)
 =ab\,\alpha^2\beta.
\tag{10}
\]

Thus the line contains one distinguished rank-one point (E_{22}) and
one other rank-at-most-two point (bE_{00}+aE_{11}).  The corresponding
two distinguished points for (Y) must agree with these.  The rank-one
point is the conjugate cofactor line, so (Y) has the same left and right
null lines as (X).  It is therefore an invertible upper (2\times2)
block.

For any invertible (2\times2) block (Y), its second distinguished
top vector is

\[
 Y\bigl(\|Y\|_2^2I-Y^\dagger Y\bigr)
 =|\det Y|^2(Y^\dagger)^{-1}.
\tag{11}
\]

Its proportionality to \(\operatorname{diag}(b,a)\) forces

\[
 Y\ \propto\ \operatorname{diag}(b,a)^{-1}
 \ \propto\ \operatorname{diag}(a,b)=X.
\]

If both have rank one, write (X=uv^\dagger) and (Y=cd^\dagger).
Equation (6) identifies their top spaces with tensor-product spaces

\[
 u^\perp\otimes(v^\perp)^*,
 \qquad c^\perp\otimes(d^\perp)^*.
\]

If neither left factors nor right factors agree, both intersections of
the two-dimensional factors are one-dimensional, so
\(\dim(E_X\cap E_Y)=1\).  If a left or right factor agrees, the
intersection has dimension at least two.  This proves the second claim.

Finally, let (X\) have rank two and put it in the coordinates of (5).
If (Y=cd^\dagger\) has rank one and (E_X\subset E_Y\), then both
\(E_{22}\) and (bE_{00}+aE_{11}\) obey (6).  The second condition forces
\(c\) into the (E_{22}\) line, while the first then fails (and likewise
on the right).  This contradiction proves the mixed-rank claim. \(\square\)

## 3. Equality classification for a deficient qutrit site

### Theorem 3

Let (z\in(\mathbb C^3)^{\otimes3}\), and suppose one one-site marginal
has rank at most two.  Then

\[
 \sum_{j=1}^4s_j(D_z)^2\le {1\over2}\|z\|^2.
\tag{12}
\]

If (z\ne0), equality holds if and only if (z) factors at some site as

\[
 z=a\otimes\xi,
 \qquad \operatorname{SchmidtRank}(\xi)\le2.
\tag{13}
\]

### Proof

Use the third site as the deficient one and choose a local basis in which

\[
 z=x_0\otimes|0\rangle+x_1\otimes|1\rangle.
\tag{14}
\]

Put (B_r=\mathscr D_{X_r}\), where (X_r) is the coefficient matrix of
\(x_r\).  The exact last-site Hodge block form gives

\[
 \sum_{j=1}^4s_j(D_z)^2
 =\lambda_1(B_0^\dagger B_0+B_1^\dagger B_1)
  +\lambda_2(B_0^\dagger B_0+B_1^\dagger B_1).
\tag{15}
\]

Ky--Fan subadditivity and Lemma 1 yield

\[
 \begin{aligned}
 \text{left side of (15)}
 &\le k_2(X_0)+k_2(X_1)\\
 &\le {1\over2}(\|X_0\|_2^2+\|X_1\|_2^2)
 ={1\over2}\|z\|^2.
 \end{aligned}
\tag{16}

Suppose equality holds.  Every nonzero (X_r) has rank at most two by
Lemma 1.  Moreover, a rank-two projection maximizing (15) must maximize
both summands separately.  Its range is therefore a two-plane contained
in every nonzero (E_{X_r}).

If only one slice is nonzero, (13) holds at the third site.  If both are
nonzero and have rank two, Lemma 2 makes them proportional, and (13) again
holds at the third site.  The mixed rank case is impossible.  If both have
rank one, Lemma 2 gives a common left or common right factor, so (13) holds
at the first or second site.  In the latter case the complementary tensor
has Schmidt rank at most two because its remaining coefficient matrix has
only the two columns in (14).

Conversely, suppose (13) holds.  Put the factor at the first site and the
rank-at-most-two Schmidt form of the complement in local bases.  Then

\[
 D_z=A_a\otimes D_\xi.
\]

The two nonzero singular values of (A_a) are both (1/\sqrt2), while
Lemma 1 gives two leading squared singular values of (D_\xi) summing to
\(1/2\).  The four leading squared singular values of (D_z) therefore
sum to (1/2\).  This proves the converse and the theorem. \(\square\)

## 4. Consequence for the physical DTH maximizer

Because (D_z) is skew, write its distinct squared singular-pair values
as \(\lambda_1\ge\lambda_2\ge\cdots\).  Equation (12) is

\[
 \lambda_1+\lambda_2\le {1\over4}\|z\|^2.
\]

Theorem 3 proves the exact dichotomy

\[
\boxed{
 \lambda_1+\lambda_2\ge {1\over4}\|z\|^2
 \Longrightarrow
 \begin{cases}
 z=a\otimes\xi,\ \operatorname{SR}(\xi)\le2,
     &\text{if some local marginal is deficient},\\
 \rho_1^z,\rho_2^z,\rho_3^z\succ0,
     &\text{otherwise}.
 \end{cases}}
\tag{17}
\]

The first branch is exactly the physical equality face proved nonnegative
in `agent_dth_physical_pseudomoment_track.md`.  The remaining necessity
problem is now entirely the full-local-rank stationary locus.

The new third-moment filter is compatible with this classification.  On
the factor branch, if the Schmidt coefficients of \(\xi\) are (s,t),

\[
 \operatorname{Tr}(D_z^\dagger D_z)^3
 ={1+s^6+t^6\over128}.
\tag{18}
\]

Thus the moment threshold for a strict violation does not itself remove
the equality face; its role is to constrain the remaining full-rank branch.

## 5. Remaining exact lemma

It is enough to prove either of the following.

1. Every full-local-rank critical point of
   \(\lambda_1(D_z^\dagger D_z)+\lambda_2(D_z^\dagger D_z)\)
   has value strictly below (1/4\); or
2. every global maximizer has at least one deficient one-site marginal.

Theorem 3 would then force the rank-one local factor and close the equality
classification.  It does not yet prove either statement.
