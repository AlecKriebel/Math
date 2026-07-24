# Working theorem: the quartic conductor equation

**Status:** proved and independently adversarially audited under the stated
coprime-leading hypothesis.  The audit found and corrected an overclaim about
finite boundary branches; see Section 3.  This is not peer reviewed, and the
completed source-specific priority search is not a guarantee of worldwide
priority.

**Recorded:** 2026-07-24T23:23:52Z.

This note concerns total polynomial degree \(4\).  The symbol \(\delta\)
always denotes generic field degree, never polynomial degree.

## 1. Coprime-leading setup

Let
\[
F:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
be a Keller map of total degree \(4\).  Choose a generic target line
\(\ell\), target coordinates \((G_1,G_2,t)\) in which
\(\ell=\{G_1=a,G_2=b\}\), and set
\[
C=F^{-1}(\ell).
\]
The generic-line argument in `WORKING_LINE_SECTION.md` makes \(C\) a smooth
integral affine curve.

Homogenize \(G_1-a\) and \(G_2-b\) to quartics
\(\widetilde G_1,\widetilde G_2\) in
\(\mathbb P^3=\operatorname{Proj}\mathbb C[X_0,X_1,X_2,X_3]\).  Suppose
their leading quartics are coprime.  Then
\[
X=V(\widetilde G_1,\widetilde G_2)
\]
is the integral projective closure of \(C\), a complete intersection of type
\((4,4)\).  In particular,
\[
\deg X=16,\qquad p_a(X)=33,\qquad \omega_X\simeq\mathcal O_X(4).
\tag{1}
\]

Indeed, coprimality of the leading quartics prevents a curve component from
lying in \(X_0=0\).  Every one-dimensional component therefore meets the
affine chart, where the generic-line fibre is integral; the regular
sequence has no additional projective curve component.

Let
\[
\nu:\bar C\longrightarrow X
\]
be the normalization, let
\[
E=\operatorname{div}(\nu^*X_0),
\]
and write \(g=g(\bar C)\).  Thus \(\deg E=16\).

Define the normalization conductor
\[
\mathfrak c
=\operatorname{Ann}_{\mathcal O_X}
  \bigl(\nu_*\mathcal O_{\bar C}/\mathcal O_X\bigr)
\]
and the effective conductor divisor \(A=\sum c_p p\) by
\[
\mathfrak c\mathcal O_{\bar C}=\mathcal O_{\bar C}(-A).
\]
The divisor \(A\) is the conductor or adjoint divisor of the normalization.
It is not the ramification divisor of \(\bar C\to\mathbb P^1\).

## 2. Exact conductor equation

### Theorem 1

As divisors on \(\bar C\),
\[
\boxed{\operatorname{div}(dt)+A=4E.}
\tag{2}
\]

### Proof

The curve \(X\) is Gorenstein.  Finite duality for the normalization gives
\[
\nu_*\omega_{\bar C}
\simeq
\mathcal H om_X(\nu_*\mathcal O_{\bar C},\omega_X)
\simeq
\mathfrak c\otimes\omega_X.
\]
Equivalently,
\[
\nu^*\omega_X\simeq\omega_{\bar C}(A).
\tag{3}
\]

On the affine chart \(X_0=1\), the adjunction residue trivializing
\(\omega_X\simeq\mathcal O_X(4)\) is the differential \(\eta\) characterized
by
\[
dG_1\wedge dG_2\wedge\eta
=dX_1\wedge dX_2\wedge dX_3.
\]
The Keller identity gives
\[
dG_1\wedge dG_2\wedge dt
=J\,dX_1\wedge dX_2\wedge dX_3,
\qquad J\in\mathbb C^\times.
\]
Hence \(\eta=J^{-1}dt\) on \(C\).  Under (3), the homogeneous section
\(X_0^4\) of \(\omega_X\simeq\mathcal O_X(4)\) therefore corresponds, up to
the nonzero scalar \(J^{-1}\), to \(dt\).  Its pullback has divisor \(4E\).
Viewing \(dt\) as a section of \(\omega_{\bar C}(A)\) adds the conductor
divisor to its ordinary canonical divisor, proving (2). \(\square\)

The degree check fixes the sign:
\[
\deg A
=64-(2g-2)
=66-2g
=2(33-g).
\tag{4}
\]

## 3. Branch-by-branch form

Let \(p\in\bar C\setminus C\), put
\[
m_p=\operatorname{ord}_p(X_0),
\]
and let \(e_p\) be the local degree of
\(\bar t:\bar C\to\mathbb P^1\).

If \(p\) maps to a finite value, then in a uniformizer \(u\),
\[
t-t(p)=u^{e_p}\cdot(\text{unit}),
\qquad
\operatorname{ord}_p(dt)=e_p-1,
\]
so (2) gives
\[
\boxed{c_p=4m_p-e_p+1.}
\tag{5}
\]
If \(p\) lies over target infinity, then
\[
t=u^{-e_p}\cdot(\text{unit}),
\qquad
\operatorname{ord}_p(dt)=-e_p-1,
\]
and
\[
\boxed{c_p=4m_p+e_p+1.}
\tag{6}
\]

The infinity exponent in (6) is always positive.  The finite exponent in
(5), however, can vanish: effectivity gives only
\[
e_p\le 4m_p+1,
\]
with equality exactly when \(c_p=0\).  Thus (5) alone does **not** imply that
every finite boundary point is singular.

This correction is forced even for local complete intersections with coprime
leading equations.  In coordinates \((w,x,y,z)\) near
\([0:0:0:1]\), take
\[
f=xz^3-w^4,\qquad g=yz^3+x^4,\qquad T=wx^2z.
\]
The branch
\[
w\longmapsto (w,w^4,-w^{16},1)
\]
is smooth, has \(m=1\), and the affine function \(t=T/w^4\) has local degree
\(e=5\).  Formula (5) gives \(c=0\).  This is not asserted to be a Keller
triple; it is an exact counterexample to the discarded positivity inference.

At a singular point \(Q\in X\), the completed local ring is one-dimensional
and Gorenstein.  Local conductor duality gives
\[
\boxed{\sum_{p\mapsto Q}c_p=2\delta_Q.}
\tag{7}
\]
In particular the sum is even at each individual projective singular point,
not merely globally.  The Gorenstein hypothesis is essential: this parity
law is false for general non-Gorenstein curve singularities.

## 4. Exact data in generic degree three

Assume now that \(F\) is a counterexample of generic degree
\(\delta=3\).  Let \(S_F\) be the reduced nonproperness hypersurface and
\[
s=\deg S_F.
\]

Every finite deleted branch now has \(e_p\le2\), while \(m_p\ge1\).
Consequently (5)--(6) are positive on every boundary branch.  Hence every
point of \(X\cap\{X_0=0\}\) is singular on \(X\).  A unibranch singular
support has \(m_p\ge2\), and at a multibranch support the sum of the
\(m_p\)'s is at least \(2\).  Since \(\sum m_p=16\), there are at most eight
boundary singular support points.
For a generic line:

- let \(n_2\) be the number of its \(s\) intersections with \(S_F\) having
  missing-sheet defect \(2\);
- among these, let \(b\) be the number of split defects, with two deleted
  branches of local degree \(1\);
- let \(\tau=n_2-b\) be the number of unsplit defects, with one deleted
  branch of local degree \(2\);
- let \(q\in\{1,2,3\}\) be the number of branches over target infinity.

Then
\[
K=s+n_2,\qquad r=s+b+q.
\]
Substitution in the exact generic-line identity
\[
K=2g-2+3+r
\]
gives
\[
\boxed{\tau=2g+q+1.}
\tag{8}
\]
Thus all discrete possibilities are parameterized by
\[
\begin{aligned}
&2\le s\le15,\qquad q\in\{1,2,3\},\\
&0\le g\le
  \left\lfloor\frac{s-q-1}{2}\right\rfloor,\\
&0\le b\le s-(2g+q+1),
\end{aligned}
\tag{9}
\]
with
\[
n_2=2g+q+1+b,\quad
K=s+2g+q+1+b,\quad
r=s+b+q.
\tag{10}
\]
The projective degree separately requires \(r\le16\).

The conductor exponents modulo \(2\) are now explicit:

- a finite deleted \(e=1\) branch has \(c_p=4m_p\), even;
- a finite deleted \(e=2\) branch has \(c_p=4m_p-1\), odd;
- over target infinity the partitions are
  \([3]\), \([2,1]\), or \([1,1,1]\); only the \(e=2\) branch in the middle
  partition has odd \(c_p\).

Combining this list with (7) gives:

### Corollary 2

At each projective singular support, the number of finite unsplit
transposition branches, together with the \(e=2\) infinity branch when
\(q=2\), is even.

The extremal case is rigid.  Writing
\(\Delta_\infty=\sum_{Q\in X\setminus C}\delta_Q\), one has
\[
(s,\delta)=(2,3)
\quad\Longrightarrow\quad
q=1,\quad g=0,\quad b=0,\quad\tau=2,\quad
\Delta_\infty=33.
\tag{11}
\]
The two finite local-degree-two branches are the only odd-conductor
branches.  By Corollary 2 they must lie over the same projective singular
point, even though their target limits are the two distinct intersections
\(\ell\cap S_F\).

## 5. Clean common-factor linkage variant

The conductor equation above requires the integral complete-intersection
case.  A separate, conditional calculation is available when the two
leading quartics share a squarefree factor \(Q\) of degree \(h\).

Write the leading forms as \(Qa,Qb\).  Suppose that for every irreducible
factor \(q\mid Q\),
\[
aG_{2,3}-bG_{1,3}\not\equiv0\pmod q,
\tag{12}
\]
after removing \(q\) locally.  Then the infinity component is generically
reduced and the residual curve is the plane divisor
\[
Z=V(X_0,Q).
\]
Direct \((4,4)\) linkage gives
\[
\deg X=16-h,\qquad
p_a(X)=\frac{h^2-11h+66}{2}.
\tag{13}
\]
For \(h=1,2,3,4\), the arithmetic genera are respectively
\[
28,\quad24,\quad21,\quad19.
\]

If \(Q\) has a repeated factor, or if (12) fails on a factor of degree \(d\),
the infinity component has extra cycle multiplicity or normal thickening.
Then it need not be a plane divisor, (13) is invalid, and one must use the
general linkage formula instead.  This failure mode is part of the
statement, not a technicality.

## 6. Next work

1. Do not promote the common-factor genus formula without checking (12)
   factor by factor.
2. Add local semigroup restrictions strong enough to use the exact conductor
   exponents, rather than parity alone.
