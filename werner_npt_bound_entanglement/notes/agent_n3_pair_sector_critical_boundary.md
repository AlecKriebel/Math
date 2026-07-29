# The qutrit pair sector: exact critical equations and the full-support remainder

## Status

This note does **not** prove the sharp pair-sector inequality
\[
 \|\Pi _2C\|_2^2\leq\frac23\|C\|_2^2,
 \qquad \operatorname{rank}C\leq2.                       \tag{1}
\]
It gives the complete Euler system at an interior rank-two maximum,
derives all rank-preserving linear-filter Hessian inequalities, and
reduces a hypothetical value above \(2/3\) to one full-rank direction
of a \(3\times3\) local-filter compression.  The reduction is exact.

Numerical critical iteration is recorded only as discovery evidence.
It repeatedly reaches \(2/3\), and every generic limiting equality
point examined has singular one-site supports on both singular planes.

## 1. Critical points on the rank-two variety

Let \({\cal P}=\Pi _2\) be the orthogonal projection onto the sector
with exactly two traceless qutrit factors.  Normalize
\(\|C\|_2=1\), put
\[
 D={\cal P}C,\qquad f=\|D\|_2^2,                          \tag{2}
\]
and write a full-rank singular-value decomposition
\[
 C=U\Sigma V^\dagger,\qquad
 U^\dagger U=V^\dagger V=I_2,\qquad
 \Sigma=\operatorname{diag}(s_1,s_2)>0.                 \tag{3}
\]
Let \(P_U=UU^\dagger\) and \(P_V=VV^\dagger\).

### Proposition 1.1 (complete first-order system)

If \(C\) is a local maximum of
\(\|{\cal P}C\|_2^2/\|C\|_2^2\) on the smooth rank-two
stratum, then
\[
 \boxed{
 \begin{aligned}
 U^\dagger DV&=f\Sigma,\\
 (I-P_U)DV&=0,\\
 U^\dagger D(I-P_V)&=0.
 \end{aligned}}                                          \tag{4}
\]
Equivalently,
\[
 \boxed{\qquad
 D=fC+R,\qquad U^\dagger R=0,\qquad RV=0.
 \qquad}                                                  \tag{5}
\]
In particular,
\[
 D^\dagger C=fC^\dagger C,\qquad
 DC^\dagger=fCC^\dagger,                                \tag{6}
\]
and
\[
 \boxed{\qquad \|R\|_2^2=f(1-f).\qquad}                 \tag{7}
\]

#### Proof

The tangent space of the rank-two determinantal variety at \(C\) is
\[
 T_C=\{Z:(I-P_U)Z(I-P_V)=0\}.                            \tag{8}
\]
For
\[
 F(X)=\frac{\|{\cal P}X\|_2^2}{\|X\|_2^2},
\]
the first variation at the normalization in (2) is
\[
 \frac12\,dF_C[Z]
 =\operatorname{Re}\langle Z,D-fC\rangle.                \tag{9}
\]
Thus \(D-fC\) lies in the normal space
\[
 T_C^\perp=(I-P_U)M_{27}(I-P_V).
\]
This is exactly (4)--(5), and (6) follows immediately.

Since \({\cal P}\) is an orthogonal projection,
\[
 \langle C,D\rangle=\langle {\cal P}C,{\cal P}C\rangle=f.
\]
Consequently
\[
 \|D-fC\|_2^2=f-2f^2+f^2=f(1-f),
\]
which proves (7). \(\square\)

The decomposition (5) is block diagonal between the two singular
planes and their orthogonal complements.  Hence the singular values
of \(D\) consist of
\[
 fs_1,\quad fs_2,\quad\hbox{and the singular values of }R. \tag{10}
\]
This is the exact fixed-point system used by alternating
pair-projection/rank-two-truncation iteration.

## 2. Fixed-plane and filter Hessians

### Proposition 2.1 (fixed-plane compression)

At a local maximum as above, for every \(M\in M_2(\mathbb C)\),
\[
 \boxed{\qquad
 \|{\cal P}(UMV^\dagger)\|_2^2
 \leq f\|M\|_2^2.
 \qquad}                                                  \tag{11}
\]
Moreover, \(\Sigma\) is an eigenvector with eigenvalue \(f\) of this
four-dimensional compressed quadratic form.

#### Proof

The line \(C+tUMV^\dagger\) remains in the rank-two variety.  Equation
(9) kills its linear term.  The quadratic coefficient in the
Rayleigh quotient is
\[
 \|{\cal P}(UMV^\dagger)\|_2^2-f\|M\|_2^2,
\]
which must be nonpositive.  Taking \(M=\Sigma\) gives equality.
\(\square\)

### Proposition 2.2 (rank-preserving local-filter Hessians)

Let \(A\in M_3(\mathbb C)\) act on any one left qutrit and let
\(B\in M_3(\mathbb C)\) act on any one right qutrit.  Then
\[
 \boxed{
 \begin{aligned}
 \|{\cal P}(A_iC)\|_2^2&\leq f\|A_iC\|_2^2,\\
 \|{\cal P}(CB_i)\|_2^2&\leq f\|CB_i\|_2^2.
 \end{aligned}}                                          \tag{12}
\]

#### Proof

Both \(C+tA_iC=(I+tA_i)C\) and
\(C+tCB_i=C(I+tB_i)\) have rank at most two for every \(t\).
The same second-variation calculation as in Proposition 2.1 proves
(12). \(\square\)

## 3. Exact reduction to a full-rank local-filter direction

Fix a left site \(i\).  On \(M_3\), define the two Hermitian forms
\[
 \begin{aligned}
 {\cal N}_i(A,B)&=\langle A_iC,B_iC\rangle,\\
 {\cal G}_i(A,B)&=
 \langle{\cal P}(A_iC),{\cal P}(B_iC)\rangle.             \tag{13}
 \end{aligned}
\]
The first form is
\[
 {\cal N}_i(A,B)=\operatorname{Tr}
 \bigl(A^\dagger B\,\rho_i^L\bigr),\qquad
 \rho_i^L=\operatorname{Tr}_{\bar i}(CC^\dagger).        \tag{14}
\]
If \(\rho_i^L>0\), this is an inner product on \(M_3\).

Equations (4)--(6) imply the generalized eigenvector identity
\[
 \boxed{\qquad
 {\cal G}_i(A,I)=f\,{\cal N}_i(A,I)
 \quad\hbox{for every }A\in M_3.
 \qquad}                                                  \tag{15}
\]
Proposition 2.2 says
\[
 {\cal G}_i\preceq f{\cal N}_i.                          \tag{16}
\]

Use the established local-support-boundary theorem: if a rank-two
matrix has a left or right one-site support of dimension at most two,
then its three-copy endpoint value is nonnegative.  Since the
degree-two endpoint eigenvalue is \(-1/2\) and every other sector
eigenvalue is at most \(1\), endpoint nonnegativity implies
\[
 \|{\cal P}X\|_2^2\leq\frac23\|X\|_2^2.                 \tag{17}
\]
For every \(A\) of matrix rank at most two, \(A_iC\) has such a
left support.  Therefore
\[
 \boxed{\qquad
 {\cal W}_i(A,A):=
 \frac23{\cal N}_i(A,A)-{\cal G}_i(A,A)\geq0
 \quad\text{when }\operatorname{rank}A\leq2.
 \qquad}                                                  \tag{18}
\]

If an interior critical point had \(f>2/3\), then (15) would give
\[
 {\cal W}_i(I,I)=\left(\frac23-f\right)
 {\cal N}_i(I,I)<0.                                      \tag{19}
\]
Thus each full-support site would produce a Hermitian quadratic form
on \(M_3\) which is nonnegative on the entire rank-at-most-two
determinantal variety but negative in the full-rank identity
direction; the identity is simultaneously its generalized
eigenvector.  The same statement holds at every right site.

Consequently the pair-sector theorem is reduced to the following
strictly smaller critical lemma:

> **Full-support filter lemma.**  A critical pair
> \((C,D={\cal P}C)\) satisfying (4), with all six one-site singular
> plane reductions positive definite, cannot make any of the six
> forms (18) negative at its identity direction.

Proving this lemma excludes all \(f>2/3\) interior maxima.  The
rank-one stratum is already bounded by \(4/9\), and the local-support
boundary is bounded by \(2/3\).

## 4. Exact boundary equality

Let \(E_{01}=|0\rangle\langle1|\) and
\(P_2=|0\rangle\langle0|+|1\rangle\langle1|\).  Then
\[
 C=E_{01}\otimes E_{01}\otimes P_2                       \tag{20}
\]
has rank two and
\[
 {\cal P}C=\frac23E_{01}\otimes E_{01}\otimes I_3.
                                                               \tag{21}
\]
Thus
\[
 \frac{\|{\cal P}C\|_2^2}{\|C\|_2^2}=\frac23.            \tag{22}
\]
Its left and right singular planes have local-support ranks
\((1,1,2)\).  It satisfies (4) exactly with \(f=2/3\).

The dependency-free exact checker
`verification/verify_n3_pair_sector_critical_boundary.py` verifies
(20)--(22), all six local support ranks, and the Euler residual.

## 5. Discovery evidence, not a theorem

Alternating exact-pair-sector projection with rank-two singular
truncation was run from unrestricted complex starts.  Every tested
start converged to \(f=2/3\).  At generic-looking limiting points,
the two nonzero singular values of the associated pair-sector
operator were equal, the normalized sector weights of the rank-two
truncation were
\[
 (w_0,w_1,w_2,w_3)=(0,0,2/3,1/3),
\]
and every one of the six local singular-plane reductions had
numerical rank two.  In contrast, twenty random full-support right
planes gave fixed-plane maxima between approximately \(0.476\) and
\(0.530\).

These observations motivate the full-support filter lemma but are
not used as mathematical evidence.
