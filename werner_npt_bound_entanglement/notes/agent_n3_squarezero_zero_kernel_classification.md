# The square-zero zero kernel is one crossed-Hodge equality

## Status

This note does **not** prove zero rigidity.  It makes the equality
problem strictly smaller and gives an exact obstruction to proving it
from abstract two-qubit positivity.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad
 {\mathsf A}_i=\frac{I-F_i}{2},\qquad
 R=\sum_{1\leq i<j\leq3}{\mathsf A}_i{\mathsf A}_j .
\tag{1}
\]
For orthogonal isometries \(U=(u_0,u_1)\) and \(W=(w_0,w_1)\),
let \(H\) be the crossed endpoint Gram on
\(\operatorname{Hom}(\operatorname{ran}W,\operatorname{ran}U)\).

The main reductions are:

1. the logical partial transpose has the stronger exact floor
   \[
   \boxed{\qquad H^{\Gamma_2}=\frac14I_4+K,\qquad
   K=(U\otimes W)^\dagger R(U\otimes W)\succeq0;\qquad}
   \tag{2}
   \]
2. after putting a nonzero kernel matrix into singular-value
   coordinates, \(\det H=0\) becomes the single scalar equality
   \[
   \boxed{
   |K_{01,10}|^2
   =
   \left(\frac14+K_{00,00}\right)
   \left(\frac14+K_{11,11}\right);}
   \tag{3}
   \]
3. consequently zero rigidity is exactly strictness, on the
   full-local-support locus, of one crossed-Hodge Cauchy inequality
   displayed in (12) below.

There is one further exact consequence on the balanced branch.  If
the kernel matrix is proportional to a unitary, then the sharp
rank-one product margin alone upgrades to the full quantitative
two-by-two bound
\[
 \boxed{\qquad
 \langle\operatorname{vec}X,H\operatorname{vec}X\rangle
 \geq\frac14\bigl(s_1(X)-s_2(X)\bigr)^2 .
 \qquad}                                                  \tag{B}
\]
Thus every balanced abstract zero already has feature concurrence
exactly \(1/2\).  No physical Hodge input is needed for this
particular implication.

The abstract conditions in (2), rank three, and the sharp product
margin do not force a balanced kernel.  An exact counterexample is
\[
 b=\frac45|00\rangle+\frac35|11\rangle,\qquad
 H_{\rm abs}=\frac{25}{36}(I_4-|b\rangle\langle b|).
\tag{4}
\]
It has an invertible unequal-Schmidt kernel, is positive of rank three,
has product margin \(1/4\), and obeys
\[
 H_{\rm abs}^{\Gamma_2}=\frac14I_4+
 \begin{pmatrix}
 0&0&0&0\\
 0&4/9&-1/3&0\\
 0&-1/3&4/9&0\\
 0&0&0&7/36
 \end{pmatrix},
\tag{5}
\]
where the displayed correction is positive semidefinite.  Thus a
proof must use the common physical origin of \(K\) in (2).

There is also a useful concurrence obstruction.  If
\[
 {\cal C}(K)
 =
 \inf_{K=\sum_\mu|\operatorname{vec}M_\mu\rangle
                    \langle\operatorname{vec}M_\mu|}
 2\sum_\mu|\det M_\mu|
\tag{6}
\]
is homogeneous two-qubit concurrence and
\(\operatorname{vec}B\in\ker H\), then
\[
 \boxed{\qquad
 {\cal C}(K)\geq
 \frac{\|B\|_2^2}{4|\det B|}
 \geq\frac12 .
 \qquad}
\tag{7}
\]
Therefore the still-conjectural physical bound
\({\cal C}(K)\leq1/2\) would force every zero-kernel matrix to be a
scalar multiple of a unitary.  Equality in an optimal pure-column
decomposition then imposes the explicit common-kernel equations
\[
 M_\mu\overline{M_\mu}
 =-|\det M_\mu|I_2
\tag{8}
\]
after logical unitaries put the kernel at
\(\operatorname{vec}I_2\).

Finally, a simpler attempt to dominate the crossed coherence by the
two off-diagonal feature norms is false on an exact physical
spin-flip zero.  In that example the proposed inequality fails by a
factor four even though the true crossed inequality is an equality.

The dependency-free exact checker is
`verification/verify_n3_squarezero_zero_kernel_classification.py`.

## 1. The \(I/4\) logical floor

Put
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right).
\]
On a simultaneous swap sector with \(r\) antisymmetric signs, direct
evaluation gives
\[
 Y-\frac14I+\frac18F_1F_2F_3
 =
 \begin{cases}
 0,&r=0,1,\\
 1,&r=2,\\
 3,&r=3.
 \end{cases}
\]
The right side is exactly \(R\), since a sector with two minus signs
is selected by one pair \({\mathsf A}_i{\mathsf A}_j\), while a
sector with three minus signs is selected by all three pairs.  Hence
\[
 \boxed{\qquad
 Y=\frac14I-\frac18F_1F_2F_3+R.
 \qquad}
\tag{9}
\]

The already established crossed-Gram identity is
\[
 (H^{\Gamma_2})_{ab,cd}
 =
 \langle u_a\otimes w_b,Y(u_c\otimes w_d)\rangle .
\tag{10}
\]
The compression of the total swap vanishes:
\[
\begin{aligned}
 &\langle u_a\otimes w_b,
 F_1F_2F_3(u_c\otimes w_d)\rangle\\
 &\qquad
 =\langle u_a,w_d\rangle\langle w_b,u_c\rangle=0,
\end{aligned}
\]
because \(U^\dagger W=0\).  Compressing (9) proves (2).

Define the direct-sum Hodge feature
\[
 {\cal T}(x,y)
 =
 \bigl(
 {\mathsf A}_1{\mathsf A}_2(x\otimes y),\
 {\mathsf A}_1{\mathsf A}_3(x\otimes y),\
 {\mathsf A}_2{\mathsf A}_3(x\otimes y)
 \bigr).
\tag{11}
\]
Then \(K\) is its Gram matrix:
\[
 K_{ab,cd}
 =\langle{\cal T}(u_a,w_b),{\cal T}(u_c,w_d)\rangle .
\]

## 2. Lossless scalar reduction

Every square-zero rank-two operator has the form
\[
 C=UBW^\dagger,\qquad U^\dagger W=0.
\]
Take a singular-value decomposition \(B=A\Sigma D^\dagger\) and
absorb the two logical unitaries into \(U'=UA\), \(W'=WD\).
Thus it is enough to consider
\[
 C=s|u_0\rangle\langle w_0|
   +t|u_1\rangle\langle w_1|,
\qquad s,t\geq0,
\]
after allowing an arbitrary relative phase in one of the four frame
vectors.

By (2) and logical index crossing,
\[
\begin{aligned}
 H_{00,00}
 &=\frac14+\|{\cal T}(u_0,w_0)\|^2,\\
 H_{11,11}
 &=\frac14+\|{\cal T}(u_1,w_1)\|^2,\\
 H_{00,11}
 &=\langle{\cal T}(u_0,w_1),{\cal T}(u_1,w_0)\rangle .
\end{aligned}
\]
Consequently positivity for every \(s,t\) and every relative phase is
equivalent to
\[
\boxed{
\begin{aligned}
 &|\langle{\cal T}(u_0,w_1),{\cal T}(u_1,w_0)\rangle|^2\\
 &\quad\leq
 \left(\frac14+\|{\cal T}(u_0,w_0)\|^2\right)
 \left(\frac14+\|{\cal T}(u_1,w_1)\|^2\right).
\end{aligned}}
\tag{12}
\]
This is a single scalar inequality on an orthonormal four-frame.  It
is losslessly equivalent to the complete square-zero theorem: every
logical matrix is diagonal after changing the two frame bases.

Now suppose \(\det H=0\).  Strict block positivity implies that
\(H\succeq0\), has rank three, and its kernel is entangled.  Put the
invertible kernel matrix into the form
\[
 B=\operatorname{diag}(s,t),\qquad s,t>0.
\]
The principal submatrix of \(H\) on \(00,11\) is positive and
annihilates \((s,t)\).  Its determinant therefore vanishes, which is
exactly (3), equivalently equality in (12).

Conversely, equality in (12), followed by the adverse relative phase
and the ratio
\[
 \frac{s}{t}
 =
 \sqrt{\frac{H_{11,11}}{H_{00,00}}},
\]
produces a nonzero kernel vector with both Schmidt coefficients
positive.  Hence the proposed zero-rigidity statement is exactly:

> equality in (12) forces at least one of the six one-site plane
> marginals to be singular.

This replaces a \(4\times4\) determinant equality by one complex
transition equality.

## 3. Abstract rank-three normal form

For completeness, the entire abstract two-qubit equality locus can
be written explicitly.  Let
\[
 b=s|00\rangle+t|11\rangle,\qquad r=s/t>0.
\]
A positive two-qubit matrix has rank three and kernel \(\mathbb Cb\)
if and only if it has the form
\[
 H=
 \begin{pmatrix}
 a&x&y&-ra\\
 \overline x&b_0&z&-r\overline x\\
 \overline y&\overline z&c&-r\overline y\\
 -ra&-rx&-ry&r^2a
 \end{pmatrix},
\tag{13}
\]
where
\[
 \begin{pmatrix}
 a&x&y\\
 \overline x&b_0&z\\
 \overline y&\overline z&c
 \end{pmatrix}\succ0.
\tag{14}
\]
Indeed, \(Hb=0\) says that the last column is \(-r\) times the
first, and Hermiticity gives the same row relation.  Rank three and
positivity are then exactly (14).

Partial transpose gives
\[
 H^{\Gamma_2}=
 \begin{pmatrix}
 a&\overline x&y&z\\
 x&b_0&-ra&-r\overline x\\
 \overline y&-ra&c&-ry\\
 \overline z&-rx&-r\overline y&r^2a
 \end{pmatrix}.
\tag{15}
\]
The physical crossed Gram lies in the much smaller sublocus on which
\(H^{\Gamma_2}-I/4\) is the common compression (2).

## 4. Exact abstract obstruction

More generally, take real \(s\geq t>0\) with \(s^2+t^2=1\), put
\[
 b=s|00\rangle+t|11\rangle,\qquad
 H_{s,t}=\frac1{4t^2}(I-|b\rangle\langle b|).
\tag{16}
\]
Then \(H_{s,t}\succeq0\), has rank three, and has kernel
\(\mathbb Cb\).

For a unit product vector \(p\),
\[
 |\langle b,p\rangle|^2\leq s^2.
\]
This is the operator-norm bound for the coefficient matrix
\(\operatorname{diag}(s,t)\).  Therefore
\[
 \langle p,H_{s,t}p\rangle
 \geq\frac{1-s^2}{4t^2}=\frac14.
\tag{17}
\]

The eigenvalues of \((|b\rangle\langle b|)^{\Gamma_2}\) are
\[
 s^2,\quad t^2,\quad st,\quad-st.
\]
Hence
\[
 H_{s,t}^{\Gamma_2}\succeq\frac14I.
\tag{18}
\]
If \(s\ne t\), its kernel is not maximally entangled.  The rational
choice \(s=4/5,t=3/5\) gives exactly (4)--(5).  The correction in
(5) has eigenvalues
\[
 0,\quad\frac19,\quad\frac7{36},\quad\frac79.
\tag{19}
\]

Thus neither positivity, rank three, the sharp product margin, nor
the \(I/4\) partial-transpose floor can prove kernel balance or zero
rigidity.

## 5. Concurrence lower bound at a zero

We use one elementary pure-column inequality.  For any
\(B,M\in M_2(\mathbb C)\),
\[
\boxed{
\left\langle\operatorname{vec}B,
 (|\operatorname{vec}M\rangle\langle\operatorname{vec}M|)^{\Gamma_2}
 \operatorname{vec}B\right\rangle
\geq-2|\det B\,\det M|.}
\tag{20}
\]
To prove it, use local unitaries to put
\(B=\operatorname{diag}(s,t)\), \(s,t\geq0\), and write
\[
 M=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]
The left side of (20) is
\[
 s^2|a|^2+t^2|d|^2+2st\operatorname{Re}(b\overline c).
\]
Now
\[
\begin{aligned}
 &s^2|a|^2+t^2|d|^2
 +2st\operatorname{Re}(b\overline c)
 +2st|\det M|\\
 &\geq
 2st\bigl(|ad|-|bc|+|ad-bc|\bigr)\\
 &\geq0,
\end{aligned}
\]
by arithmetic--geometric mean and the reverse triangle inequality.
This proves (20).

Apply (20) term by term to any pure-column decomposition of \(K\).
Taking the infimum in (6) gives
\[
 \langle\operatorname{vec}B,K^{\Gamma_2}\operatorname{vec}B\rangle
 \geq-|\det B|{\cal C}(K).
\tag{21}
\]
If \(\operatorname{vec}B\in\ker H\), equation (2) gives
\[
 0=\frac14\|B\|_2^2+
 \langle\operatorname{vec}B,K^{\Gamma_2}\operatorname{vec}B\rangle.
\]
Combining this with (21) proves the first inequality in (7).  The
second is
\[
 \|B\|_2^2\geq2|\det B|,
\]
with equality exactly when the two singular values of \(B\) agree.

Finally, suppose \({\cal C}(K)=1/2\), \(B\) is balanced, and an
optimal decomposition in (6) is chosen.  The pure-state spectral
bound
\[
 (|\operatorname{vec}M\rangle\langle\operatorname{vec}M|)^{\Gamma_2}
 +|\det M|I_4\succeq0
\tag{22}
\]
gives
\[
 H=
 \sum_\mu\left[
 (|\operatorname{vec}M_\mu\rangle
   \langle\operatorname{vec}M_\mu|)^{\Gamma_2}
 +|\det M_\mu|I_4
 \right],
\tag{23}
\]
because \(\sum_\mu|\det M_\mu|=1/4\).
Every summand in (23) is positive and their sum annihilates the kernel
vector, so every summand annihilates it separately.  After logical
unitaries put \(B=I_2\), direct vectorization of that kernel equation
is precisely (8) for each term with nonzero determinant.

This supplies a concrete equality system for a future physical
Hodge-decomposition proof.

## 6. A complete quantitative theorem for a balanced kernel

The following elementary \(2\times2\) lemma turns out to be exactly
adapted to the sharp product margin.

### Lemma 6.1 (rank-one scalar remainder)

For every \(X\in M_2(\mathbb C)\), choose either eigenvalue
\(\lambda\) and put
\[
 R=X-\lambda I_2.
\]
Then \(\operatorname{rank}R\leq1\) and
\[
 \boxed{\qquad
 \bigl(s_1(X)-s_2(X)\bigr)^2\leq\|R\|_2^2.
 \qquad}                                                  \tag{24}
\]
If \(X\) is not scalar, equality holds precisely when its two
eigenvalues lie on one closed ray from the origin (zero is allowed).

#### Proof

Put \(r=\operatorname{Tr}R\).  Since \(\det R=0\), the second
eigenvalue of \(X\) is
\[
 \mu=\lambda+r,
\]
and
\[
 \det X=\lambda\mu.
\]
For a \(2\times2\) matrix,
\[
 \bigl(s_1(X)-s_2(X)\bigr)^2
 =\|X\|_2^2-2|\det X|.
\]
Expanding \(X=\lambda I+R\) therefore gives the exact identity
\[
\begin{aligned}
 &\|R\|_2^2-\bigl(s_1(X)-s_2(X)\bigr)^2\\
 &\qquad
 =2\left(
 |\lambda|\,|\mu|-\operatorname{Re}(\overline\lambda\mu)
 \right)\geq0.                                          \tag{25}
\end{aligned}
\]
The last term vanishes exactly when \(\lambda\) and \(\mu\) have the
same phase, with either one allowed to vanish.  This proves both
claims. \(\square\)

### Theorem 6.2 (balanced-kernel completion)

Let \(H\) be a Hermitian form on \(M_2(\mathbb C)\) such that
\[
 H\,\operatorname{vec}I_2=0
\tag{26}
\]
and, for every rank-at-most-one \(R\),
\[
 \langle\operatorname{vec}R,H\operatorname{vec}R\rangle
 \geq\frac14\|R\|_2^2.                                  \tag{27}
\]
Then, for every \(X\in M_2(\mathbb C)\),
\[
 \boxed{
 \langle\operatorname{vec}X,H\operatorname{vec}X\rangle
 \geq\frac14\bigl(s_1(X)-s_2(X)\bigr)^2.}               \tag{28}
\]
In particular \(H\succeq0\).  The same conclusion holds when the
kernel matrix is any scalar multiple of a unitary, after a logical
unitary change of coordinates.

#### Proof

Choose an eigenvalue \(\lambda\) of \(X\) and put
\(R=X-\lambda I\).  Equation (26) and Hermiticity give
\[
 \langle\operatorname{vec}X,H\operatorname{vec}X\rangle
 =
 \langle\operatorname{vec}R,H\operatorname{vec}R\rangle.
\]
Apply (27) and then Lemma 6.1.  Logical left and right unitaries
preserve matrix rank, Frobenius norm, and singular values, so they
reduce a unitary kernel matrix to \(I_2\). \(\square\)

For a nonscalar \(X\), equality in (28) requires both:

1. \(R=X-\lambda I\) saturates the rank-one product margin (27);
2. the two eigenvalues of \(X\) lie on one closed ray.

In the physical crossed Gram, the first condition is
\({\cal T}(x,y)=0\) for the rank-one logical transition determined by
\(R\).  The complete rank-one equality classification then puts that
transition on the product--tangent or common-local-factor locus.
The scalar kernel itself does not yield such a transition, so this
observation does not yet prove zero rigidity.

There is also a concise concurrence consequence.  For a physical
balanced zero, Section 5 gives
\({\cal C}(K)\geq1/2\).  The determinant-one filter formula, with
(28) applied after every logical filter, gives the reverse inequality.
Hence
\[
 \boxed{\qquad {\cal C}(K)=\frac12
 \quad\hbox{for every balanced zero.}\qquad}             \tag{29}
\]

## 7. Exact failure of an off-diagonal norm shortcut

A tempting strengthening of (12) is
\[
 K_{01,01}K_{10,10}
 \stackrel{?}{\leq}
 \left(\frac14+K_{00,00}\right)
 \left(\frac14+K_{11,11}\right).                        \tag{30}
\]
Together with ordinary Cauchy--Schwarz, it would prove (12).
It is false even at an exact physical endpoint zero.

For the fully transverse spin-flip frame recorded in
`agent_n3_transverse_anchor_boundary.md`, the crossed endpoint Gram
is
\[
 H=
 \begin{pmatrix}
 1/4&0&0&-1/4\\
 0&3/4&0&0\\
 0&0&3/4&0\\
 -1/4&0&0&1/4
 \end{pmatrix}.
\tag{31}
\]
Therefore
\[
 K=H^{\Gamma_2}-\frac14I_4
 =
 \begin{pmatrix}
 0&0&0&0\\
 0&1/2&-1/4&0\\
 0&-1/4&1/2&0\\
 0&0&0&0
 \end{pmatrix}.                                         \tag{32}
\]
The left side of (30) is \(1/4\), while its right side is
\(1/16\).  Thus (30) fails by the exact factor four.  In contrast,
the actual crossed term obeys
\[
 |K_{01,10}|^2=\frac1{16}
 =
 \left(\frac14+K_{00,00}\right)
 \left(\frac14+K_{11,11}\right),
\]
so the physical target (12) is sharp.  Any proof must control the
crossed coherence itself rather than replace it by the product of the
two off-diagonal feature masses.
