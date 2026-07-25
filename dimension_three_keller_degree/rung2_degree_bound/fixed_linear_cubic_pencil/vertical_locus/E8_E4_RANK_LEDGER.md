# Rank ledger for the triple-vertical \(E_8\)--\(E_4\) frontier

**Status:** active exact reduction, not a full-row exclusion.  The complete
nonvertical-companion exclusion and the zero-\(\ell\), nontriple part of
the vertical companion have passed independent hostile audits.

**Recorded:** 2026-07-25T12:35:00Z.

This ledger uses
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=(U,V,R)^T,\qquad
H_2=(A,B,W)^T,                                         \tag{1}
\]
and writes
\[
q_0=q|_{z=0},\quad A_0=A|_{z=0},\quad
B_0=B|_{z=0},\quad W_0=W|_{z=0}.
\]
The binary bracket is
\[
\{f,g\}=f_xg_y-f_yg_x.
\]

## 1. Legal gauges and the complete \(E_7\) families

The target stabilizer may add the third component to either of the first
two components.  These are legal row operations: they preserve \(H_4\),
but they change the corresponding lower jets and must be applied to all
degrees simultaneously.

### Vertical companion \(R=z^3\)

The exact identity
\[
E_7=z^3\{q,4zW-3U\}=0
\]
and the degree-three kernel theorem give
\[
U=\frac43zW+a q+bz^3.                                  \tag{2}
\]
Adding the third target component to the first kills \(b\).  Adding it to
the second kills the \(z^3\)-coefficient of \(V\).  Thus the complete
gauged \(E_7\) family is
\[
\boxed{
R=z^3,\qquad U=\frac43zW+a q,\qquad
[z^3]V=0.}                                             \tag{3}
\]
The invariant first split is \(a=0\) versus \(a\ne0\).

### Nonvertical companion \(R=q\)

Here
\[
E_7=\{q,4z^4W-4z^3V+qU\}=0.                            \tag{4}
\]
The degree-six first-integral space is exactly
\[
\operatorname{Sym}^2\langle z^3,q\rangle
=\langle z^6,z^3q,q^2\rangle.                          \tag{5}
\]
Indeed the divisor descent for a degree-six first integral has
\(z\)-orders \(0,3,6\); every finite zero order is divisible by four, so
the divisor is a product of two cubic pencil fibres.  Equations
(4)--(5) give
\[
U=cq+dz^3,\qquad
V=zW+eq+fz^3.                                          \tag{6}
\]
Target shears kill \(c,e\), leaving the complete gauged family
\[
\boxed{
R=q,\qquad U=dz^3,\qquad V=zW+fz^3.}                   \tag{7}
\]

Thus \(E_8\)--\(E_7\) have been solved without dividing by a parameter.

## 2. Rank divisors visible on \(z=0\)

The root multiplicity of \(q_0\) is invariant under the leading
stabilizer.  Its three strata are
\[
q_0\sim xy(x-y),\qquad q_0\sim x^2y,\qquad q_0\sim x^3.
\tag{8}
\]
For binary forms of degrees three and two,
\[
\{q_0,K_0\}=0
\]
forces \(K_0=0\), except on the triple-root stratum
\(q_0=L^3\), where \(K_0\in\mathbb C L^2\).  This elementary kernel jump
is the first exceptional divisor.

### 2.1 Vertical companion, \(a\ne0\)

The restriction of \(E_6\) is
\[
\boxed{E_6|_{z=0}=-a\,q_0\{q_0,W_0\}.}                 \tag{9}
\]
Consequently:

- on the squarefree and double-root strata, \(W_0=0\);
- on the triple-root stratum \(q_0=L^3\),
  \(W_0=\gamma L^2\).

On either nontriple stratum write
\[
W=z\ell+\omega z^2,\qquad \ell\in\mathbb C[x,y]_1.
\tag{10}
\]
The complete restriction of \(E_5\) is
\[
\boxed{
\ell\{q_0,V_0\}=q_0\{q_0,\bar L_3\},}                  \tag{11}
\]
where \(\bar L_3\) is the \(x,y\)-part of the third row of the linear
matrix.

The exact binary ranks in (11) are:

| \(q_0\) | \(\ell\)-orbit | solutions for \((V_0,\bar L_3)\) |
|---|---|---|
| \(xy(x-y)\) | \(\ell\ne0\), including root collisions | \(V_0\in\mathbb Cq_0,\ \bar L_3=0\) |
| \(xy(x-y)\) | \(\ell=0\) | \(V_0\) arbitrary, \(\bar L_3=0\) |
| \(x^2y\) | \(\ell\) not a root line | \(V_0\in\mathbb Cq_0,\ \bar L_3=0\) |
| \(x^2y\) | \(\ell=x\) | \(\langle(q_0,0),(\frac23xy^2,y)\rangle\) |
| \(x^2y\) | \(\ell=y\) | \(\langle(q_0,0),(\frac13x^3,x)\rangle\) |
| \(x^2y\) | \(\ell=0\) | \(V_0\) arbitrary, \(\bar L_3=0\) |

Thus the only \(E_5\) rank drops on the nontriple locus are the two
root-line collisions in the double-root stratum and \(\ell=0\).
There is no hidden squarefree resultant divisor: a collision with any of
its three roots retains the generic rank.

On the generic \(\ell\ne0\) rows of the table, write
\(V_0=\kappa q_0\).  The restriction of \(E_4\) then becomes
\[
\boxed{\{q_0,\kappa A_0-aB_0\}=0.}                     \tag{12}
\]
Since \(q_0\) is not a cube, this is exactly
\[
\boxed{\kappa A_0=aB_0.}                               \tag{13}
\]
The branches \(\ell=0\), the two double-root collisions, and the
triple-root stratum remain separate exceptional leaves; (13) is not
extended across them.

### 2.2 Vertical companion, \(a=0\)

No condition survives from \(E_6|_{z=0}\).  The next exact restriction is
\[
\boxed{
4W_0\{V_0,W_0\}+3q_0\{W_0,A_0\}=0.}                   \tag{14}
\]
This is a genuinely different rank family.  In particular \(W_0=0\)
makes (14) identically zero.  It is recorded as an open exceptional
family rather than being folded into the \(a\ne0\) solve.

### 2.3 Nonvertical companion

For the complete gauge (7),
\[
\boxed{
E_6|_{z=0}=-q_0\{A_0,q_0\}.}                           \tag{15}
\]
On the nontriple root strata this forces \(A_0=0\).  Then
\[
\boxed{
E_5|_{z=0}=-q_0\{\bar L_1,q_0\}}                       \tag{16}
\]
forces the \(x,y\)-part \(\bar L_1\) of the first linear row to vanish.
Finally
\[
\boxed{
E_4|_{z=0}=A_1\{B_0,q_0\},}                            \tag{17}
\]
where \(A=zA_1+\alpha z^2\) and \(A_1\) is linear in \(x,y\).  Hence the
exact \(E_4\) partition is
\[
\boxed{
A=\alpha z^2
\quad\text{or}\quad
B_0=0.}                                                \tag{18}
\]
The triple-root stratum is a rank drop: (15) permits
\(A_0\in\mathbb C L^2\), and neither (16) nor (18) may be imported into
it without a separate solve.

### Constant-minor closure of the nontriple leaves

Both leaves in (18) can be completed without dividing by any remaining
modulus.

If \(A=\alpha z^2\), the full \(E_6,E_5\) coefficient matrix has a
constant \(7\times7\) pivot minor
\[
-524288=-2^{19}.                                       \tag{19}
\]
It forces
\[
B_0=0,\qquad
B=z(\ell_{31}x+\ell_{32}y+\beta z),\qquad
\bar L_2=0,                                             \tag{20}
\]
where \((\ell_{31},\ell_{32})=\bar L_3\).  Since (16) already gave
\(\bar L_1=0\), the first two rows of \(L\) are both multiples of \(dz\).

On the other leaf \(B_0=0\), allow
\[
A=z(a_1x+a_2y+\alpha z).
\]
The full \(E_6,E_5\) matrix has the constant \(6\times6\) pivot minor
\[
-2048=-2^{11}.                                         \tag{21}
\]
It forces \(a_1=a_2=0\) and then exactly (20).  Thus this leaf returns to
the first one and also makes \(L\) singular.

The two minors are identical on the squarefree and double-root normal
forms and contain no coefficient of the lower \(z\)-jets of \(q\), of
\(W\), or of \(d,f\).  Hence there is no omitted rank divisor inside
either nontriple root stratum.

It follows that
\[
\boxed{\text{the nonvertical companion is impossible whenever }
q_0\text{ is not a cube}.}                              \tag{22}
\]
This is an exact working exclusion; it awaits hostile audit before global
promotion.

The triple-root rank drop has now also been solved.  Its complete minimal
stabilizer atlas is
\[
\boxed{
x^3+y^2z+\alpha xz^2+\beta z^3,\quad
x^3+xyz+\beta z^3,\quad
x^3+yz^2.}                                             \tag{23}
\]
The missing fourth coefficient shape is binary in \(x,z\) and is exactly
the nonminimal boundary.  On the three families in (23), the full
\(E_6,E_5\) systems have literal constant \(14\times14\) minors
\[
-2^{24}3^8,\qquad -2^{18}3^6,\qquad -2^{20}3^7,         \tag{24}
\]
respectively.  Each forces
\[
A=\alpha_0z^2,\quad
B=z(\ell_{31}x+\ell_{32}y+\beta_0z),\quad
\bar L_1=\bar L_2=0.                                   \tag{25}
\]
Thus \(L\) is singular on every triple-root family as well.

Combining (22)--(25),
\[
\boxed{\text{the entire nonvertical companion }G_3=q
\text{ is impossible}.}                               \tag{26}
\]
The detailed classification and certificate are in
`NONVERTICAL_TRIPLE_ROOT_LEMMA.md`.  A dependency-free hostile
reconstruction in `audit_nonvertical_companion/` has now passed.

## 3. Regression guard and current boundary

The exact \(E_5\) survivor
\[
q=x^3+y^3,\quad
R=z^3,\quad
W=z^2,\quad
U=q+\tfrac43z^3,\quad
V=0,\quad
A=0,\quad B=xz,\quad L_0=I                             \tag{19}
\]
lies on the exceptional leaf
\[
a\ne0,\quad q_0\text{ squarefree},\quad \ell=0.
\]
It satisfies \(E_8=\cdots=E_5=0\) and has
\(E_4=9x^2z^2\).  Every future solve must reproduce this leaf and this
nonzero residual.

The current \(E_4\) leaves are therefore:

1. vertical \(a\ne0\), nontriple, generic \(\ell\ne0\), with (13);
2. vertical \(a\ne0\), \(\ell=0\);
3. vertical \(a\ne0\), the two double-root collisions;
4. vertical \(a\ne0\), triple-root \(q_0\);
5. vertical \(a=0\), governed by (14);
The nonvertical leaves are closed.  Only the five vertical-companion
families remain.

Within item 2, the squarefree and double-root strata are excluded by
literal constant minors through total source degrees six, five, and four;
see `VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md` and its independent hostile
audit.  On the triple-root stratum, the complete
\(\gamma=0,\ell=0\) sublocus is also excluded on all three minimal
charts by `VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md` and its independent
hostile audit.  The raw \(E_6\) identities in
`VERTICAL_TRIPLE_GAMMA0_REDUCTION.md` reduce every
\(a\ne0,\gamma=0\) point to that sublocus, while
`VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md` excludes
\(\gamma\ne0\) directly.  Both reductions passed independent hostile
audits.  Hence the complete triple-root part of the \(a\ne0\) vertical
companion is excluded.

On the nontriple strata, `VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md`
and its dependency-free hostile audit exclude every \(\ell\ne0\)
kernel, including all root-line collision kernels; the previously audited
`VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md` excludes \(\ell=0\).
Consequently the complete nontriple part of the \(a\ne0\) vertical
companion is also excluded.

On the separate \(a=0\) family, the full five-chart calculation in
`VERTICAL_A0_W0_ZERO_EXCLUSION.md` excludes \(W_0=0\) through
\(E_6,E_5,E_4\).  A derivation completed independently before comparison,
a second symbolic parameterization, and a PARI/GP exterior reconstruction
all pass; see `audit_vertical_a0_w0_zero/REPORT.md`.  The only remaining
vertical-companion family is therefore
\[
\boxed{a=0,\qquad W_0\ne0.}
\]
It is not called excluded in this ledger until its separate candidate and
hostile audit pass.
