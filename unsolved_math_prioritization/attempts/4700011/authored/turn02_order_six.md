# Turn 2: a complete order-six classification by tropical obstructions

Problem 4700011, Gasull Problem 11. Authored 2026-10-07.

## Result and boundary of the claim

This turn gives a proof candidate classifying the entire **order-six** family with arbitrary nonnegative real coefficients. It is a partial result toward the arbitrary-order problem, not a resolution of Problem 11. No novelty claim is made; independent mathematical review and a later-literature comparison remain appropriate.

Turn 1 is unchanged. We use its proved surjectivity reduction, exclusion of the increasing branch, palindromic-coefficient condition, and order-three classification. The new ingredients here are a tropical necessary condition, explicit infinite-order tangent/derivative certificates, and an elementary boundary-return proof for the order-two parameter.

**Theorem.** A globally periodic order-six recurrence in the specified nonnegative linear-fractional family is, as a function of its six independent initial variables, one of

\[
\begin{aligned}
x_{n+6}&=x_n,\\
x_{n+6}&=a^2/x_n,\\
x_{n+6}&=b x_{n+3}/x_n,\\
x_{n+6}&=(b^2+b x_{n+3})/x_n,\\
x_{n+6}&=(b^2+b x_{n+2}+b x_{n+4})/x_n,
\end{aligned}
\qquad a,b>0.
\]

Their least common global periods are respectively 6, 12, 18, 15, and 16. Thus no additional example occurs in order six.

The proof's finite certificates use only exact integer arithmetic and polynomial identities. Each certificate specifies a point, an iterate, and the complete deterministic calculation required to verify the obstruction. The accompanying `verify_turn02.py` reproduces the return matrices and all comparisons; `turn02_verification.json` contains the full winning-index lists and matrices.

## 1. Reduction to eight support patterns

Turn 1 reduces every candidate other than \(x_{n+6}=x_n\) to

\[
\tag{1}
x_{n+6}=\frac{a_0+b(x_{n+1}+x_{n+5})
+c(x_{n+2}+x_{n+4})+d x_{n+3}}{x_n},
\qquad a_0,b,c,d\geq0,
\]

where not all four coefficients vanish. We will eliminate the five variable-support patterns

\[
\{b\},\quad\{b,c\},\quad\{b,d\},\quad\{c,d\},\quad\{b,c,d\}.
\]

Here a displayed coefficient is strictly positive and an omitted coefficient is zero. Each elimination allows either \(a_0=0\) or \(a_0>0\). The only supports left will be the empty set, \(\{c\}\), and \(\{d\}\), which reduce to the classical families.

## 2. Tropicalization preserves a common finite order

For a recurrence

\[
x_{n+k}=\frac{a_0+\sum_{j\in S}a_j x_{n+j}}{x_n},\qquad a_j>0\ (j\in S),
\]

let \(\epsilon\) record whether \(a_0>0\). Define the piecewise-linear map

\[
\tag{2}
T(z_0,\ldots,z_{k-1})=
\left(z_1,\ldots,z_{k-1},
\max\big(\{z_j:j\in S\}\cup\{0:\epsilon=1\}\big)-z_0\right).
\]

The maximum is over a nonempty set.

**Lemma 1.** If the positive rational shift map \(F\) satisfies \(F^p=\mathrm{id}\), then \(T^p=\mathrm{id}\) on \(\mathbb R^k\).

*Proof.* Conjugate \(F\) by coordinatewise exponentiation and logarithm at scale \(R>0\):

\[
F_R(z)=R^{-1}\log F(e^{Rz}).
\]

Each \(F_R\) has the same finite-order identity. Its last coordinate is

\[
R^{-1}\log\left(a_0+\sum_{j\in S}a_j e^{Rz_j}\right)-z_0.
\]

The log-sum-exp estimate implies convergence to (2), uniformly on compact sets (indeed the error bound is independent of \(z\)). For each fixed finite number of iterates, the same compact-uniform convergence holds for compositions, because the limit is continuous and all images of a fixed compact set remain in a common compact set. Therefore \(F_R^p=\mathrm{id}\) passes to the limit and gives \(T^p=\mathrm{id}\). \(\square\)

Consequently a single rigorous obstruction for \(T\) eliminates every rational recurrence with that same support, independently of its positive coefficient values.

## 3. Two ways to certify infinite order

**Lemma 2 (strict-cycle derivative).** Suppose \(T^r(z)=z\) and the maximum defining every step along this orbit is attained at a unique entry. If the return derivative \(M=D(T^r)(z)\) has infinite order, then \(T\) has no common finite order.

*Proof.* Strict comparisons make every map along the orbit linear in a neighborhood of the relevant point, so \(T^r\) is differentiable at \(z\). If \(T^p=\mathrm{id}\), then \((T^r)^p=\mathrm{id}\). Since \(z\) is fixed by \(T^r\), differentiation gives \(M^p=I\), a contradiction. \(\square\)

**Lemma 3 (tangent return).** Let \(T^r(z)=z\), permitting ties. The one-sided tangent return

\[
\mathcal R(w)=\lim_{s\downarrow0}\frac{T^r(z+s w)-z}{s}
\]

is a positively homogeneous, piecewise-linear map. If \(T\) has common finite order \(p\), then \(\mathcal R^p=\mathrm{id}\). Thus an unbounded orbit or a nonzero expanding eigenray of \(\mathcal R\) disproves common finite order.

*Proof.* A finite composition of finite-piece piecewise-linear maps has finitely many linear pieces. At a fixed base point, for any fixed direction \(w\), its directional expansion is exact for all sufficiently small positive \(s\). To compute a finite number of successive returns, choose \(s\) small enough for each of the finitely many encountered directions. This proves that the tangent map of \((T^r)^p\) equals \(\mathcal R^p\). If \(T^p=\mathrm{id}\), the former map is the identity. \(\square\)

At a tied maximum, the tangent maximum is taken only over entries tied for the base maximum. A zero constant contributes tangent value zero when it is tied for that maximum. Entries strictly below the base maximum do not enter the tangent comparison.

## 4. Elimination of support \(\{b\}\) by an exact tangent drift

Here \(S=\{1,5\}\), with or without a constant. The point

\[
z=(0,0,1,0,1,0)
\]

returns after five steps. At the first step the winners are indices 1 and 5 (and also the constant, if present); the next four winners are uniquely 1, 5, 1, 5.

For a tangent vector \(w=(u,v,w_2,s,w_4,t)\), direct composition gives

\[
\tag{3}
\mathcal R(u,v,w_2,s,w_4,t)
=(t,\ m-u,\ w_2-v,\ -v,\ w_4-s,\ -s),
\]

where \(m=\max(v,t)\) without a constant and \(m=\max(v,t,0)\) with one.

Put

\[
w_*=(0,0,0,-1,0,0),\qquad
\Delta=(0,0,-1,0,1,0).
\]

In both constant cases, the three consecutive tangent states are

\[
\begin{aligned}
\mathcal R(w_*)&=(0,0,0,0,1,1),\\
\mathcal R^2(w_*)&=(1,1,0,0,1,0),\\
\mathcal R^3(w_*)&=(0,0,-1,-1,1,0)=w_*+\Delta.
\end{aligned}
\]

Formula (3) also gives \(\mathcal R(w+n\Delta)=\mathcal R(w)+n\Delta\), because only coordinates 2 and 4 change and neither enters \(m\). Hence

\[
\mathcal R^{3n}(w_*)=w_*+n\Delta\quad(n\geq0).
\]

This is an unbounded orbit. Lemmas 1 and 3 eliminate \(\{b\}\), for arbitrary positive \(b\) and either constant status.

## 5. Elimination of supports \(\{b,c\}\) and \(\{c,d\}\)

Let \(\alpha\) be the unique real root greater than 1 of

\[
\tag{4}\alpha^3-\alpha^2-1=0.
\]

It lies between 1 and \(3/2\); the polynomial is strictly increasing on \([1,\infty)\).

For both support patterns the point

\[
z=(0,0,1,1,0,0)
\]

returns after four steps. Every base maximum in these four steps equals 1, so adding the zero constant does not affect the tangent return.

### Support \(\{b,c\}\): \(S=\{1,2,4,5\}\)

Use the direction

\[
w_{bc}=(\alpha-1,0,-1,0,\alpha^2-\alpha,0).
\]

The base winning sets through the four steps are

\[
\{2\},\quad\{1,2,5\},\quad\{1,4,5\},\quad\{4\}.
\]

Choose winners \((2,2,1,4)\). The tangent gaps against other tied entries are respectively \(1,\alpha,\alpha,0\), so these choices are valid, including the harmless remaining tie. After four tangent steps the vector is

\[
(\alpha^2-\alpha,0,-\alpha,0,1,0)=\alpha w_{bc},
\]

where the final identity uses (4). Positive homogeneity now gives \(\mathcal R^n(w_{bc})=\alpha^n w_{bc}\), an unbounded ray.

### Support \(\{c,d\}\): \(S=\{2,3,4\}\)

Use

\[
w_{cd}=(0,\alpha-1,0,-1,0,\alpha^2-\alpha).
\]

The base winning sets are

\[
\{2,3\},\quad\{2\},\quad\{4\},\quad\{3,4\}.
\]

Choose winners \((2,2,4,3)\). The only nontrivial tangent gaps are 1 and \(\alpha\), both positive. The four-step tangent image is

\[
(0,\alpha^2-\alpha,0,-\alpha,0,1)=\alpha w_{cd}.
\]

Again this is an unbounded eigenray. Lemmas 1 and 3 exclude both patterns, with or without \(a_0\).

## 6. Strict-cycle certificates for the last two patterns

The following four certificates eliminate \(\{b,d\}\) and \(\{b,c,d\}\). All indices are zero-based state coordinates; the initial state is \((z_0,\ldots,z_5)\).

To verify any certificate, start with its listed state and \(M=I_6\). At each step compute the largest of the supported coordinates, and zero if the constant is present. The largest is unique. If coordinate \(j\) wins, update

\[
(z_0,\ldots,z_5)\longmapsto(z_1,\ldots,z_5,z_j-z_0),
\]

and update the matrix by shifting its first five rows and making its last row \(M_j-M_0\). If the constant wins, the new last coordinate is \(-z_0\) and the new last matrix row is \(-M_0\). After the listed number of steps, the state returns to its initial value. Every winning margin is at least 1. Thus the final matrix is a genuine return derivative.

### Certificate A: \(S=\{1,3,5\}\), no constant

Initial state \((4,5,-8,-6,9,8)\), return time 99. The return matrix is

\[
M_A=\begin{pmatrix}
3&3&0&1&-1&-1\\
-2&-2&0&-1&1&1\\
-1&-1&1&0&1&0\\
1&1&0&1&-1&0\\
-1&-1&1&0&2&1\\
-2&-3&0&-1&1&2
\end{pmatrix}.
\]

Its characteristic polynomial is

\[
(t-1)^3(t^3-4t^2+3t-1).
\]

The cubic is negative at 3 and positive at 4, so \(M_A\) has an eigenvalue greater than 3. It cannot have finite order.

### Certificate B: \(S=\{1,3,5\}\), constant present

Initial state \((8,-1,3,1,-4,2)\), return time 47. The return matrix is

\[
M_B=\begin{pmatrix}
0&-2&1&1&0&1\\
-1&0&1&2&0&1\\
1&3&-1&-1&-1&-1\\
-2&-5&3&3&1&2\\
1&3&-2&-1&0&-1\\
0&-1&0&-1&0&1
\end{pmatrix}.
\]

Its characteristic polynomial is

\[
(t-1)^3(t^3+7t-1).
\]

The cubic changes sign between 0 and 1, producing an eigenvalue of modulus strictly less than 1. Again finite order is impossible.

### Certificate C: \(S=\{1,2,3,4,5\}\), no constant

Initial state \((4,3,-1,10,-4,-5)\), return time 65. The return matrix has the compact form

\[
M_C=I+uv^{\mathsf T},\qquad
u=(1,1,0,0,1,-1)^{\mathsf T},\quad
v=(0,0,-1,-1,-1,-1)^{\mathsf T}.
\]

Both vectors are nonzero and \(v^{\mathsf T}u=0\). Consequently

\[
M_C^n=I+nuv^{\mathsf T}\ne I\quad(n\geq1).
\]

### Certificate D: \(S=\{1,2,3,4,5\}\), constant present

Initial state \((1,8,2,-6,2,6)\), return time 65. Here

\[
M_D=I+uv^{\mathsf T},\qquad
u=(0,0,1,0,-1,-1)^{\mathsf T},\quad
v=(2,-1,0,-1,0,0)^{\mathsf T}.
\]

Again \(uv^{\mathsf T}\ne0\) and \(v^{\mathsf T}u=0\), so \(M_D\) has infinite order.

For C and D, the exact matrices, rather than only their characteristic polynomials \((t-1)^6\), matter: a nontrivial unipotent matrix is not finite-order in characteristic zero.

All four checks are reproduced by the verifier, with the full winning-index lists saved in its output. Lemmas 1 and 2 finish the support exclusions.

## 7. An elementary order-two boundary argument

The remaining support \(\{d\}\) in (1) gives three independent interlaced copies of

\[
u_{n+2}=\frac{a_0+d u_{n+1}}{u_n},\qquad d>0.
\]

After rescaling \(u_n=d y_n\), this is

\[
\tag{5}y_{n+2}=\frac{A+y_{n+1}}{y_n},\qquad A=a_0/d^2\geq0.
\]

**Lemma 4.** Equation (5) is globally periodic if and only if \(A\in\{0,1\}\).

*Proof.* If \(A=0\) or \(A=1\), exact substitution gives periods 6 and 5, respectively, as also verified in Turn 1.

Suppose \(A>0\) and let \(G_A(x,y)=(y,(A+y)/x)\). Direct substitution shows that \(H=G_A^5\) extends rationally and continuously to every point \((0,y)\) with \(y>0\), with

\[
\tag{6}H(0,y)=(0,Ay).
\]

Here are details ensuring that (6) is a legitimate extension rather than an informal singularity calculation. Writing the successive scalar terms as \(x_0=x,x_1=y\), one obtains

\[
x_2=\frac{A+y}{x},\qquad
x_3=\frac{Ax+A+y}{xy},\qquad
x_4=\frac{Axy+Ax+A+y}{y(A+y)},
\]

and

\[
x_5=\frac{x(A^2y+Axy+Ax+Ay^2+A+y)}{(A+y)(Ax+A+y)}.
\]

After cancellation, the denominator of \(x_6\) is

\[
(Ax+A+y)(Axy+Ax+A+y),
\]

which becomes \((A+y)^2>0\) at \(x=0\). Its numerator at \(x=0\) is \(Ay(A+y)^2\). Thus both coordinates of \(H=(x_5,x_6)\) extend, and (6) follows. Also \(x_5/x\to(Ay+1)/(A+y)>0\).

If \(G_A^p=\mathrm{id}\) on the positive quadrant, then \(H^p=\mathrm{id}\) there. Starting from \((0,y)\), its extended boundary iterates are \((0,A^n y)\), all with positive second coordinate. Continuity of the finitely many compositions therefore extends the identity to that boundary point, giving \(A^p y=y\). Since \(A>0\), this forces \(A=1\). \(\square\)

This argument supplies the order-two coefficient restriction without invoking an external classification theorem or assuming that the tropical period equals the rational map period.

## 8. Completion of the order-six theorem

After Sections 4–6, only three support patterns remain.

1. **Empty variable support:** \(a_0>0\), giving the reciprocal dilation \(x_{n+6}=a_0/x_n\).
2. **Only \(d>0\):** Lemma 4 forces \(a_0=0\) or \(a_0=d^2\), giving the six- and five-period base dilations.
3. **Only \(c>0\):** The even and odd subsequences each obey the order-three recurrence
   \[
   u_{m+3}=\frac{a_0+c u_{m+1}+c u_{m+2}}{u_m}.
   \]
   Its variable-coefficient ratio is 1. Turn 1's proved order-three classification forces \(a_0=c^2\), giving the eight-period base dilation. The homogeneous case is excluded as well by Turn 1's odd-order homogeneous obstruction.

For these interlaced systems, global periodicity of the order-six shift implies global periodicity of each base map: the appropriate power of the shift acts independently on the residue classes, whose initial data can be varied independently. Conversely each displayed classical base identity gives the indicated finite order of the interlaced shift. The least-period multiplication argument from Turn 1 gives 6, 12, 18, 15, and 16.

The increasing branch is already exactly the identity dilation, so the theorem follows.

The same conclusion applies to equations of order \(6\ell\) whose variable support is contained in \(\{\ell,2\ell,3\ell,4\ell,5\ell\}\): they split into \(\ell\) independent order-six subsystems. This is an index-dilation corollary, not a classification of all order-\(6\ell\) equations.

## 9. Failed or insufficient routes, and what remains

The following exploratory observations are deliberately not used as proofs:

- Many long integer tropical orbit periods were found. Any finite list of periods is compatible with their least common multiple, so the observations alone do not exclude a common global period.
- Some strict periodic tropical points have return matrix equal to the identity. That does not itself imply that the whole tropical map has finite order.
- A strict 17-step orbit for support \(\{1,3,5\}\) has a nonidentity return matrix whose sixth power is the identity. Nonidentity alone is therefore not an obstruction; the retained certificates explicitly prove infinite order.
- Eigenvectors of a selected linear branch must satisfy that branch's maximum inequalities. Several expanding spectral candidates failed these inequalities and were discarded. The retained expanding rays include every tied comparison.
- An open-set rigidity argument for finite-order piecewise-linear maps was considered, but is not needed anywhere in the final proof.

The arbitrary-order classification remains unresolved in this work. The new proof handles one previously unaddressed order in the cited 2020 list, not all possible orders or supports. A next substantive turn can investigate whether the tropical drift/expansion certificates extend uniformly to arbitrary support gaps, or carry out the first comparable complete support analysis in order eight. A successful low-order support enumeration is not evidence of a proof for all orders.

## Citation context

The problem's primary statement and its recorded low-order classification are in Armengol Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, Problem 11: https://arxiv.org/abs/2012.02524 . The preceding arguments are independently authored and do not reproduce a source proof. The source's omission of order six is historical context only, not a verified novelty claim or evidence that no later order-six result exists.
