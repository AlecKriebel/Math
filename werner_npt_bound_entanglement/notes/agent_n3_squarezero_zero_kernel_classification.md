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

There is also a new converse on the diagonal-collapse boundary.  If
either matched Hodge feature vanishes,
\[
 {\cal T}(u_0,w_0)=0
 \quad\hbox{or}\quad
 {\cal T}(u_1,w_1)=0,
\]
then every determinant-zero kernel is balanced.  In fact both
matched features vanish.  The key input is the sharp restricted
spectral estimate
\[
 \left\|
 P_{\{x,y\}^{\perp}}
 L^{\otimes3}(|x\rangle\langle y|)
 P_{\{x,y\}^{\perp}}
 \right\|_{\rm op}\leq\frac14
\]
for every orthonormal rank-one equality pair
\({\cal T}(x,y)=0\).  This removes the complete diagonal-feature
collapse locus from the unequal-kernel problem.  A hypothetical
unequal-kernel zero must therefore have both matched features
nonzero.

Two proposed extensions beyond this boundary have now been disposed
of exactly.

First, the tempting estimate
\[
 \left\|
 P_{\{x,y\}^{\perp}}
 L^{\otimes3}(|x\rangle\langle y|)
 P_{\{x,y\}^{\perp}}
 \right\|_{\rm op}
 \stackrel{?}{\leq}Q_3(|x\rangle\langle y|)
\tag{R1}
\]
for arbitrary orthonormal \(x,y\) is false.  Section 9 gives a
one-parameter exact counterfamily.  On that family the more
permissive interpolation
\[
 \left\|P_{\{x,y\}^{\perp}}
 L^{\otimes3}(|x\rangle\langle y|)
 P_{\{x,y\}^{\perp}}\right\|_{\rm op}
 \stackrel{?}{\leq}
 \frac14+\frac12\|{\cal T}(x,y)\|
\tag{R2}
\]
is instead an equality.  Inequality (R2) remains conjectural.

Second, an attempted reduction of the determinant-zero kernel
equations to ordinary orthogonality of four Hodge feature vectors
was an index error and is explicitly retracted in Section 10.  The
correct irreducible equations are the \(2\times2\) matrix equation
\[
 \frac14D+\sum_\mu M_\mu D\overline{M_\mu}=0,
 \qquad D=\operatorname{diag}(s,t),
\tag{R3}
\]
or its four scalar entries.  In particular, the two off-diagonal
entries of (R3) do not say that either crossed feature vector is
orthogonal to \(s{\cal T}(u_0,w_0)+t{\cal T}(u_1,w_1)\).

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

## 8. Diagonal feature collapse forces a balanced kernel

We first isolate the spectral fact used in the kernel argument.

### Lemma 8.1 (restricted endpoint norm at rank-one equality)

Let \(x,y\in(\mathbb C^3)^{\otimes3}\) be orthonormal and suppose
\[
 {\cal T}(x,y)=0.
\tag{33}
\]
Put
\[
 A=L^{\otimes3}(|x\rangle\langle y|),\qquad
 P=I-|x\rangle\langle x|-|y\rangle\langle y|.
\]
Then
\[
 \boxed{\qquad \|PAP\|_{\rm op}\leq\frac14.\qquad}
\tag{34}
\]

#### Proof

The complete rank-one equality classification leaves, up to
interchanging \(x,y\), two cases.

In the product--tangent case, local unitaries and phases give
\[
\begin{aligned}
 x&=|000\rangle,\\
 y&=b|100\rangle+c|010\rangle+d|001\rangle,\\
 b,c,d&\geq0,\qquad b^2+c^2+d^2=1.
\end{aligned}
\tag{35}
\]
The scalar term in the general tangent vector is absent because
\(x\perp y\).  Write
\[
 Z=\operatorname{diag}(1,-1,-1),\qquad
 f=|0\rangle\langle1|.
\]
Since
\[
 L(|0\rangle\langle0|)=\frac12Z,\qquad L(f)=f,
\]
one has
\[
 4A=
 b\,f\otimes Z\otimes Z+
 c\,Z\otimes f\otimes Z+
 d\,Z\otimes Z\otimes f=:D.
\tag{36}
\]

Decompose the physical space according to the set of sites carrying
the local symbol \(2\).  The operator \(D\) preserves every such
summand.  On a nonempty-symbol-\(2\) summand at most two binary sites
remain.  Direct decomposition by binary Hamming weight then gives
\[
 \|D\|\leq\sqrt{\sum_{i\ {\rm remaining}}b_i^2}\leq1,
\tag{37}
\]
where \((b_1,b_2,b_3)=(b,c,d)\).

It remains to treat the all-binary summand.  There \(D\) lowers
Hamming weight by one.  The weight-one-to-zero block is killed by the
left projection \(P\), and the weight-three-to-two block has norm
\(\sqrt{b^2+c^2+d^2}=1\).  In the single-excitation basis and the
complementary double-excitation basis, the remaining block is, up to
irrelevant row and column signs,
\[
 M=
 \begin{pmatrix}
 0&d&c\\
 d&0&b\\
 c&b&0
 \end{pmatrix}.
\tag{38}
\]
Let \(v=(b,c,d)^{\mathsf T}\).  A direct multiplication gives
\[
 MM^\dagger-I=vv^\dagger
 -2\operatorname{diag}(b^2,c^2,d^2).
\tag{39}
\]
Therefore, for every \(z\perp v\),
\[
 z^\dagger MM^\dagger z
 =
 \|z\|^2-2\sum_i b_i^2|z_i|^2
 \leq\|z\|^2.
\tag{40}
\]
The left projection \(P\) on the single-excitation space is exactly
the projection onto \(v^\perp\).  Equations (37)--(40) prove
\(\|PDP\|\leq1\), hence (34), in the first case.  Interchanging
\(x,y\) replaces \(A\) by its adjoint and changes nothing.

In the common-local-factor case, local unitaries give
\[
 x=|0\rangle\otimes\xi,\qquad
 y=|0\rangle\otimes\eta,
\tag{41}
\]
where, on two qutrits,
\[
\begin{aligned}
 \xi&=a|00\rangle+b|11\rangle,\\
 \eta&=az|00\rangle+s|01\rangle+t|10\rangle-bz|11\rangle,\\
 a,b&\geq0,\quad a^2+b^2=1,\quad
 |z|^2+|s|^2+|t|^2=1.
\end{aligned}
\tag{42}
\]
The polarized determinant equation is already incorporated in this
form.  Orthogonality adds
\[
 (a^2-b^2)z=0.
\tag{43}
\]
Put
\[
 A_2=L^{\otimes2}(|\xi\rangle\langle\eta|).
\]
We claim
\[
 \|A_2\|_{\rm op}\leq\frac12.
\tag{44}
\]

For completeness, here is a direct block proof.  In a suitable
computational-basis ordering, \(2A_2\) is the orthogonal direct sum
of a zero scalar, two \(2\times2\) blocks, and the \(4\times4\)
block
\[
 M=
 \begin{pmatrix}
 0&a\bar s&a\bar t&-2ab\bar z\\
 -b\bar t&0&0&-a\bar t\\
 -b\bar s&0&0&-a\bar s\\
 2ab\bar z&b\bar s&b\bar t&0
 \end{pmatrix}.
\tag{45}
\]
The two small blocks are, up to interchanging \(s,t\),
\[
 \begin{pmatrix}
 -a^2\bar z&-a\bar t\\
 -b\bar s&b^2\bar z
 \end{pmatrix}.
\tag{46}
\]
Their squared Frobenius norms are at most
\[
 (a^4+b^4)|z|^2+a^2|t|^2+b^2|s|^2\leq1,
\tag{47}
\]
and similarly for the other block.

By (43), either \(z=0\) or \(a=b=1/\sqrt2\).  If \(z=0\),
the block (45) splits, after grouping its first and fourth
coordinates, into two rank-one blocks.  Their norms are
\[
 \|(a,b)\|\,\|(s,t)\|=1,\qquad
 \|(b,a)\|\,\|(t,s)\|=1.
\tag{48}
\]
If \(a=b=1/\sqrt2\), use the symmetric and antisymmetric
combinations \(e_+,e_-\) of the first and fourth coordinates.
Then the line \(\mathbb Ce_+\) is mapped into the orthogonal space
\(\mathbb Ce_-\oplus\mathbb C^2\) by a column of squared norm
\[
 |z|^2+|s|^2+|t|^2=1,
\]
while \(\mathbb Ce_-\oplus\mathbb C^2\) is mapped back to
\(\mathbb Ce_+\) by a row of the same squared norm.  Thus
\(\|M\|\leq1\).  Equations (47)--(48) prove (44).

Finally,
\[
 A=L(|0\rangle\langle0|)\otimes A_2,
\]
and \(\|L(|0\rangle\langle0|)\|_{\rm op}=1/2\).
Therefore \(\|A\|\leq1/4\), which is stronger than (34).
This completes the second case and the proof. \(\square\)

### Theorem 8.2 (diagonal-collapse balance)

Suppose \(\det H=0\), put its entangled kernel in singular-value
coordinates
\[
 B=\operatorname{diag}(s,t),\qquad s,t>0,
\tag{49}
\]
and assume
\[
 {\cal T}(u_0,w_0)=0
\quad\hbox{or}\quad
 {\cal T}(u_1,w_1)=0.
\tag{50}
\]
Then
\[
 \boxed{\qquad s=t,\qquad
 {\cal T}(u_0,w_0)={\cal T}(u_1,w_1)=0.\qquad}
\tag{51}
\]

#### Proof

It is enough to treat the first alternative in (50).  The
\(00,11\) principal block of \(H\) is positive and annihilates
\((s,t)^{\mathsf T}\).  Since the first diagonal feature vanishes,
\[
 H_{00,00}=\frac14.
\]
The two kernel equations therefore give
\[
 H_{00,11}=-\frac{s}{4t},\qquad
 H_{11,11}=\frac{s^2}{4t^2}.
\tag{52}
\]
But
\[
 H_{11,11}
 =\frac14+\|{\cal T}(u_1,w_1)\|^2\geq\frac14,
\]
so \(s\geq t\).

Let
\[
 A=L^{\otimes3}(|u_0\rangle\langle w_0|).
\]
All four frame vectors are orthonormal, so \(u_1,w_1\) belong to
\(\{u_0,w_0\}^{\perp}\).  Self-adjointness of \(L^{\otimes3}\),
Lemma 8.1, and (52) give
\[
 \frac{s}{4t}
 =|H_{00,11}|
 =|\langle u_1,Aw_1\rangle|
 \leq\frac14.
\tag{53}
\]
Thus \(s\leq t\), and hence \(s=t\).  Substitution into (52) gives
\(H_{11,11}=1/4\), so
\({\cal T}(u_1,w_1)=0\).  Interchanging the labels proves the other
alternative. \(\square\)

The theorem is a genuine physical restriction which the abstract
unequal-kernel example (16) does not satisfy.  It also shows exactly
where the remaining unequal-kernel problem lives: every matched
rank-one transition has a strictly positive Hodge feature.

## 9. Exact failure of the unrestricted spectral extension

Lemma 8.1 uses the full equality hypothesis
\({\cal T}(x,y)=0\).  It cannot be extended to arbitrary orthonormal
pairs by replacing its right side \(1/4\) with the rank-one energy
\(Q_3(|x\rangle\langle y|)\).

Let \(a,b>0\), \(a^2+b^2=1\), and \(a^2>1/2\).  On two qutrits put
\[
 \xi=a|00\rangle+b|11\rangle,\qquad
 \eta=b|00\rangle-a|11\rangle,
\tag{54}
\]
and on three qutrits put
\[
 x=|0\rangle\otimes\xi,\qquad
 y=|0\rangle\otimes\eta.
\tag{55}
\]
The vectors \(x,y\) are orthonormal.  Write
\[
 E=|x\rangle\langle y|,\qquad
 E_2=|\xi\rangle\langle\eta|.
\]
Both one-site partial traces of \(E_2\) equal
\[
 ab\,\operatorname{diag}(1,-1,0),
\]
and \(\operatorname{Tr}E_2=0\).  Therefore
\[
 Q_2(E_2)=1-2a^2b^2
\]
and tensor factorization gives
\[
 \boxed{\qquad
 Q_3(E)=\frac12(1-2a^2b^2).
 \qquad}                                                 \tag{56}
\]

Now put
\[
 A=L^{\otimes3}(E),\qquad
 P=I-|x\rangle\langle x|-|y\rangle\langle y|.
\]
Since
\[
 L(|0\rangle\langle0|)
 =\frac12\operatorname{diag}(1,-1,-1),
\]
one has
\[
 A=L(|0\rangle\langle0|)\otimes L^{\otimes2}(E_2).
\tag{57}
\]
In the two-site computational basis, the only nonzero part relevant
to the operator norm consists of
\[
\begin{aligned}
 \langle00|L^{\otimes2}(E_2)|11\rangle&=-a^2,\\
 \langle11|L^{\otimes2}(E_2)|00\rangle&=b^2,
\end{aligned}
\tag{58}
\]
together with four diagonal entries of modulus \(ab/2\).
Consequently the nonzero singular values of
\(L^{\otimes2}(E_2)\) are
\[
 a^2,\quad b^2,\quad
 \frac{ab}{2},\frac{ab}{2},\frac{ab}{2},\frac{ab}{2}.
\tag{59}
\]
Thus \(\|A\|_{\rm op}=a^2/2\).

This norm survives the compression.  Indeed,
\[
 u=|100\rangle,\qquad v=|111\rangle
\]
belong to \(\{x,y\}^{\perp}\), and (57)--(58) give
\[
 |\langle u,Av\rangle|=\frac{a^2}{2}.
\]
It follows that
\[
 \boxed{\qquad
 \|PAP\|_{\rm op}=\frac{a^2}{2}.
 \qquad}                                                 \tag{60}
\]
If \(z=a^2\), then
\[
 \frac z2-Q_3(E)
 =-(z-\tfrac12)(z-1)>0
 \qquad(\tfrac12<z<1).
\tag{61}
\]
This disproves (R1).  For example, at \(a^2=3/4\),
\[
 Q_3(E)=\frac5{16},\qquad
 \|PAP\|_{\rm op}=\frac38.
\tag{62}
\]

The same family identifies a sharp surviving target.  The rank-one
feature identity gives
\[
 \|{\cal T}(x,y)\|^2
 =Q_3(E)-\frac14
 =(a^2-\tfrac12)^2.
\tag{63}
\]
Hence every member with \(a^2\geq1/2\) saturates
\[
 \|PAP\|_{\rm op}
 =
 \frac14+\frac12\|{\cal T}(x,y)\|.
\tag{64}
\]
This is consistent with Lemma 8.1 at feature norm zero, but no proof
of the general inequality (R2) is presently known.  Moreover, scalar
kernel arithmetic shows that (R2) alone would still permit some
unequal singular-value ratios, so additional common-code geometry
would remain necessary.

## 10. Retraction and the corrected smallest kernel equations

An earlier draft inferred ordinary feature-vector orthogonality from
the transverse entries of the determinant-zero kernel equation.
That inference is false because logical partial transpose crosses
the indices.

Choose an orthonormal basis \((e_\mu)\) in the direct-sum Hodge
feature space and write the four feature coordinates as the
\(2\times2\) matrices
\[
 M_\mu=
 \begin{pmatrix}
  a_\mu&b_\mu\\
  c_\mu&d_\mu
 \end{pmatrix},
\qquad
 (M_\mu)_{ij}
 =\langle e_\mu,{\cal T}(u_i,w_j)\rangle.
\tag{65}
\]
Then
\[
 K=\sum_\mu
 |\operatorname{vec}M_\mu\rangle
 \langle\operatorname{vec}M_\mu|.
\]
If the kernel matrix has been put in singular-value coordinates
\[
 D=\operatorname{diag}(s,t),\qquad s,t>0,
\]
the equation \(H\operatorname{vec}D=0\) is exactly
\[
 \boxed{\qquad
 \frac14D+\sum_\mu M_\mu D\overline{M_\mu}=0.
 \qquad}                                                 \tag{66}
\]
Here the final bar is entrywise conjugation, not the adjoint.
Expanding (66) gives the corrected four scalar equations
\[
\begin{aligned}
 \frac{s}{4}
  +\sum_\mu(s|a_\mu|^2+t b_\mu\overline{c_\mu})&=0,\\
 \sum_\mu(s a_\mu\overline{b_\mu}
             +t b_\mu\overline{d_\mu})&=0,\\
 \sum_\mu(s c_\mu\overline{a_\mu}
             +t d_\mu\overline{c_\mu})&=0,\\
 \frac{t}{4}
  +\sum_\mu(s c_\mu\overline{b_\mu}+t|d_\mu|^2)&=0.
\end{aligned}                                            \tag{67}
\]
For example, the first transverse equation in (67) contains
\(b_\mu\overline{d_\mu}\), whereas ordinary orthogonality of
\((b_\mu)_\mu\) to
\((s a_\mu+t d_\mu)_\mu\) contains
\(\overline{b_\mu}d_\mu\).  They are not the same scalar in
general.  Thus no one-dimensional ``longitudinal'' feature reduction
follows from (67).

Equations (66)--(67), the scalar equality (3), and the condition that
all four feature columns arise from one orthonormal physical
four-frame are the smallest currently valid interior problem.  In
particular, after Theorem 8.2 the only unresolved determinant-zero
locus has both matched features nonzero; no valid further collapse
of that locus has yet been proved.
