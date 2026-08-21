# Binary fixed-quadratic line double-cover frontier

**Status:** stabilizer quotient, the abstract Hilbert--Burch split, the
complete exact-\(\delta=1\) lower exclusion, and the exact-\(\delta=2\)
Hilbert--Burch stratification are proved.  The active frontier is the
\(\delta=2\), \(\{1,1\}\) \(E_6/E_5\) elimination.  All three
\(\{2,0\}\) loci have provisional full exclusions with independent
SymPy and PARI/GP certificates; hostile mathematical replay is still
pending, so the umbrella is not yet promoted.  On \(\{1,1\}\), the
two exact-\(\delta=2\) \(h=p^2\) incidences now also have provisional
full exclusions, including every \(E_6\) survivor and its \(E_5/E_4\)
obstruction.  The \(h=pq\) doubled-contribution leaf is also
provisionally excluded at \(E_6\), as is its two-simple-contribution
companion.  The doubled-\(p\), doubled-\((p+q)\), two-fixed-root, and
two ramification-contact \(h=p(p+q)\) leaves are likewise
provisionally excluded.  The squarefree-interior doubled-fixed-root
and two-fixed-root leaves are also provisionally excluded.  The other
squarefree-interior fixed-root/contact leaf is now provisionally
excluded through \(E_6/E_5\).  The other three \(\{1,1\}\) incidence
leaves and the separate power fibre remain.  Nothing in this note calls
a partial weighted-identity survivor a Keller map.

**Opened:** 2026-07-25T10:01:53Z.

This note is not peer reviewed.  Its exact checks are evidence about the
encoded algebra, not peer review.

## 1. Scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}
\]
have degree four, with \(H_i\) homogeneous of degree \(i\), and suppose
its top homogeneous part is in the unresolved
binary part of the fixed-quadratic line double-cover row:
\[
H_4=h(p,q)(p^2,q^2,0)^T,\qquad
0\ne h=Ap^2+Bpq+Cq^2.                              \tag{1}
\]
The purpose of this directory is to classify the joint leading orbits and
then eliminate them with the lower Keller identities.
All weighted identities are coefficients of
\[
\det(L_0+zJH_2+z^2JH_3+z^3JH_4).
\]

## 2. Full stabilizer of the squaring cover

The reduced cover
\[
[p:q]\longmapsto[p^2:q^2]                            \tag{2}
\]
has the unique pencil base point \([0:0:1]\) and two ramification members
\(p=0\) and \(q=0\).  A source transformation that stabilizes (2), up to a
target projectivity, must preserve the base point and hence the pencil
\(\langle p,q\rangle\).  Write its induced pencil matrix as
\[
G=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]
The span of \((ap+bq)^2,(cp+dq)^2\) must equal
\(\langle p^2,q^2\rangle\).  Each square therefore has zero \(pq\)
coefficient:
\[
ab=cd=0.
\]
Together with \(\det G\ne0\), this says that \(G\) is diagonal or
anti-diagonal.  Conversely every such matrix is a stabilizer, after a
diagonal target rescaling and, in the anti-diagonal case, a target swap.

This is the full stabilizer, not merely a convenient subgroup.  In the
third source coordinate one may still make
\[
r\longmapsto\gamma r+\ell(p,q),\qquad \gamma\ne0,
\]
but this acts trivially on the binary form \(h\).  Target changes invisible
on the image line also act trivially on \(h\).

For a diagonal pencil change
\((p,q)\mapsto(\alpha p,\beta q)\), followed by the target normalization
\(\operatorname{diag}(\alpha^{-2},\beta^{-2})\), the fixed divisor changes
by
\[
[A:B:C]\longmapsto
[A\alpha^2:B\alpha\beta:C\beta^2].                  \tag{3}
\]
There is also the swap \(A\leftrightarrow C\), and a common nonzero scalar
is immaterial.

## 3. Complete orbit list

### Proposition

The nonzero binary quadratics in (1), modulo the full joint stabilizer, have
the following complete and disjoint set of orbit types:
\[
\begin{array}{c|c|c}
\text{stratum}&\text{representative}&\text{modulus}\\ \hline
\text{branch square}&p^2&\text{none}\\
\text{two branch roots}&pq&\text{none}\\
\text{one branch root}&p(p+q)&\text{none}\\
\text{no branch root}&p^2+\eta pq+q^2&
  \kappa=\eta^2\in\mathbb A^1 .
\end{array}                                           \tag{4}
\]

Thus the orbit space is set-theoretically one affine parameter together
with three isolated boundary orbit types.  Its maximal parameter count is
one.  The value \(\kappa=4\) is the doubled nonbranch root
\((p\pm q)^2\), whereas the isolated representative \(p^2\) is the doubled
branch root; they are not equivalent.

### Proof

The zero pattern of \((A,C)\) is invariant under (3), up to exchange.

- If \(AC\ne0\), choose
  \(t=\alpha/\beta\) with \(t^2=C/A\), then rescale the whole form.  This
  gives \(p^2+\eta pq+q^2\), where
  \[
  \eta^2=\frac{B^2}{AC}=\kappa.                     \tag{5}
  \]
  Replacing \(t\) by \(-t\) changes \(\eta\) to \(-\eta\), so precisely
  \(\kappa\), not a choice of square root, is invariant.  Conversely equal
  values of \(\kappa\) give the same orbit over \(\mathbb C\).
- If exactly one of \(A,C\) is nonzero and \(B=0\), the form is equivalent
  to \(p^2\).
- If exactly one of \(A,C\) is nonzero and \(B\ne0\), diagonal scaling
  makes its two coefficients equal, giving \(p(p+q)\).
- If \(A=C=0\), then \(B\ne0\) and the form is \(pq\).

These cases exhaust every nonzero coefficient triple and are disjoint by
their incidence and multiplicity along the two ramification members.
\(\square\)

The generic member of the one-parameter stratum has only the swap as an
effective finite stabilizer.  The representative \(p^2+\eta pq+q^2\) is
squarefree exactly when \(\kappa\ne4\).  At \(\kappa=0\) it has the extra
sign symmetry \(p\mapsto-p\).  The three boundary strata are
zero-dimensional; \(p^2\) and \(pq\) retain positive-dimensional torus
stabilizers, while \(p(p+q)\) has trivial effective stabilizer.

## 4. Exact \(E_8\) and \(E_7\) identities

Put
\[
P=hp^2,\quad Q=hq^2,\quad
U=(H_3)_1,\quad V=(H_3)_2,\quad R=(H_3)_3,\quad
T=(H_2)_3.
\]
For
\[
\mathcal J(z)=L_0+zJH_2+z^2JH_3+z^3JH_4,\qquad
E_j=[z^j]\det\mathcal J(z),
\]
direct expansion gives
\[
J_{p,q}(P,Q)=8h^2pq.                                \tag{6}
\]
Consequently
\[
\boxed{E_8=8h^2pq\,R_r.}                             \tag{7}
\]
Since the polynomial ring is a domain, \(E_8=0\) makes \(R\) a binary
cubic.

After imposing \(R_r=0\), row-multilinearity of the determinant gives
\[
\begin{aligned}
E_7
 &=\operatorname{Jac}(P,V,R)
   +\operatorname{Jac}(U,Q,R)
   +\operatorname{Jac}(P,Q,T)\\
 &=\boxed{J(Q,R)U_r-J(P,R)V_r+8h^2pq\,T_r}.          \tag{8}
\end{aligned}
\]
Here \(J\) is the binary Jacobian in \(p,q\).

Write the \(r\)-dependent derivatives as
\[
\begin{aligned}
U_r&=u_2r^2+r\,u_1(p,q)+u_0(p,q),\\
V_r&=v_2r^2+r\,v_1(p,q)+v_0(p,q),\\
T_r&=t_1r+t_0(p,q),
\end{aligned}
\]
where the subscripts also indicate degrees in \(p,q\).  Equation (8)
splits into coefficient matrices with respectively
\[
2,\qquad5,\qquad8                                    \tag{9}
\]
unknown coefficients at \(r^2,r^1,r^0\).

## 5. First exact kernel split

The accompanying exact verifier reconstructs (7)--(8) from the full
\(3\times3\) determinant and obtains:

| fixed divisor and cubic | \((r^2,r^1,r^0)\) ranks | nullities |
|---|---:|---:|
| \(h=pq,\ R=p^3+q^3\) | \((2,5,8)\) | \((0,0,0)\) |
| \(h=p(p+q),\ R=p^3+p^2q+q^3\) | \((2,5,8)\) | \((0,0,0)\) |
| \(h=p^2+q^2,\ R=p^3+2p^2q+3pq^2+4q^3\) | \((2,5,8)\) | \((0,0,0)\) |
| \(h=p^2+q^2,\ R=p^3+p^2q+q^3\) | \((2,5,7)\) | \((0,0,1)\) |
| \(h=p^2+q^2,\ R=p^3+q^3\) | \((2,5,6)\) | \((0,0,2)\) |
| \(h=p^2,\ R=p^3+p^2q+pq^2+q^3\) | \((2,5,7)\) | \((0,0,1)\) |
| \(h=(p+q)^2,\ R=p^3+p^2q+pq^2+2q^3\) | \((2,5,7)\) | \((0,0,1)\) |

The first three rows are transverse squarefree samples and show that the
generic orbit has no \(E_7\) tangent.  The next two rows are also transverse
(\(\gcd(h,R)=1\)) but have special Hilbert--Burch splittings.  Thus common
root degree alone does **not** classify this double-cover row.  The final
two rows represent the two geometrically different doubled-root positions
and each has one \(r^0\) tangent.

The table is only a sample of the exhaustive determinantal and
Hilbert--Burch classification below.  Its nonzero-kernel rows are
top-identity survivors, not Keller maps.

## 6. Exact determinantal equations

Write
\[
R=ap^3+bp^2q+cpq^2+dq^3.
\]
Let \(\mathcal M_0(h,R)\) be the square coefficient matrix of the
\(r^0\) equation in (8):
\[
\mathcal M_0:
S_2\oplus S_2\oplus S_1\longrightarrow S_7,\qquad
(u,v,t)\longmapsto J(Q,R)u-J(P,R)v+J(P,Q)t.          \tag{10}
\]
Exact determinant calculation over the full coefficient rings gives
\[
\begin{array}{c|l}
h&\det\mathcal M_0\\ \hline
p^2&0,\\
pq&373248\,a^3d^3,\\
p(p+q)&124416\,d^3(3a-4b)(a-b+c-d)^2,\\
p^2+\eta pq+q^2&
-41472(\eta^2-4)(4c-3d\eta)(3a\eta-4b)\Phi^2,
\end{array}                                           \tag{11}
\]
where
\[
\begin{aligned}
\Phi={}&a^2-ab\eta+ac\eta^2-2ac-ad\eta^3+3ad\eta+b^2\\
&-bc\eta+bd\eta^2-2bd+c^2-cd\eta+d^2\\
={}&\operatorname{Res}_p(p^2+\eta p+1,\,
                         ap^3+bp^2+cp+d).
\end{aligned}                                         \tag{12}
\]

Thus (11) is the complete first rank-drop divisor, including every value
of the orbit modulus \(\kappa=\eta^2\).  In the interior chart its four
geometric sources are:

- the doubled fixed root \(\eta^2=4\);
- contact at the ramification member \(p=0\),
  \(4c-3d\eta=0\);
- contact at \(q=0\), \(3a\eta-4b=0\); and
- a common fixed root, \(\Phi=0\).

The two contact factors explain why \(\gcd(h,R)\) alone missed transverse
rank drops.  In the one-branch chart the analogous factors are
\(d\), \(3a-4b\), and \(a-b+c-d\).

## 7. Hilbert--Burch split with a common \(P,Q\) factor

Set
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q),\qquad g=\gcd(\alpha,\beta,\gamma),
\]
and put \(\delta=\deg g\).  Assume first that \(\alpha,\beta\) are
constant-linearly independent.  After division by \(g\), their degrees
are
\[
(\deg\alpha_0,\deg\beta_0,\deg\gamma_0)=(d_0,d_0,d_0+1),
\qquad d_0=5-\delta.                                  \tag{13}
\]
Constant independence excludes \(\delta=5\), so \(d_0\ge1\).
Consequently the reduced ideal is proper.  Its gcd is one, so no
height-one prime contains it; in \(\mathbb C[p,q]\) its height is exactly
two.  Hilbert--Burch therefore makes its binary syzygy module free of
rank two.  If its minimal total syzygy degrees are \(e_1,e_2\),
Hilbert--Burch gives
\[
e_1+e_2=3d_0+1.                                       \tag{14}
\]

If \(R=0\), the third component of the full map has degree at most two.
The banked quadratic-component coordinate lemma followed by the plane
low-degree exit makes the Keller map an automorphism.  We therefore
assume \(R\ne0\) throughout the remaining Hilbert--Burch and
power-fibre analysis.

The gradient columns
\[
(P_p,Q_p,R_p)^T,\qquad(P_q,Q_q,R_q)^T
\]
are independent syzygies of total degree \(d_0+3\), since
\(\gamma\ne0\).  A syzygy of total degree below \(d_0+1\) is impossible;
at total degree \(d_0\) it would be a constant relation between
\(\alpha_0,\beta_0\).  Hence, with
\[
k_i=d_0+3-e_i,
\]
one has
\[
0\le k_i\le2.
\]
For the missing sum, choose a minimal Hilbert--Burch basis \(N_1,N_2\)
and write the two gradient columns as
\[
(\nabla_p,\nabla_q)=(N_1,N_2)C.
\]
Their wedge is
\[
\nabla_p\wedge\nabla_q=(\alpha,\beta,\gamma)
 =g(\alpha_0,\beta_0,\gamma_0),
\]
while \(N_1\wedge N_2\) is a nonzero scalar multiple of the reduced
row.  Hence \(\det C\) is a nonzero scalar multiple of \(g\).  Row \(i\)
of \(C\) has degree \(k_i\), and therefore
\[
k_1+k_2=\deg\det C=\deg g=\delta.                    \tag{15}
\]
This argument never assumes that \(P,Q\) are coprime; their common factor
\(h\) causes no gap.

The complete nonexceptional split is therefore
\[
\begin{array}{c|c|c}
\delta&\{k_1,k_2\}&
\dim\ker(\mathcal M_2,\mathcal M_1,\mathcal M_0)\\ \hline
0&\{0,0\}&(0,0,0)\\
1&\{1,0\}&(0,0,1)\\
2&\{1,1\}&(0,0,2)\\
2&\{2,0\}&(0,1,2)\\
3&\{2,1\}&(0,1,3)\\
4&\{2,2\}&(0,2,4).
\end{array}                                           \tag{16}
\]
Here \(\mathcal M_2,\mathcal M_1,\mathcal M_0\) have respectively
\((2,5,8)\) columns.  A \(k=1\) basis column contributes one constant
\(r^0\) tangent; a \(k=2\) column contributes two linear \(r^0\) tangents
and one \(r^1\) tangent.  This proves the table from syzygy degrees rather
than from sampled ranks.

If \(R\ne0\) and \(\alpha,\beta\) are constant-linearly dependent, then
\[
J(\lambda P+\mu Q,R)=0
\]
for some constants not both zero.  Unique factorization and
\(\gcd(4,3)=1\) give
\[
\lambda P+\mu Q=L^4,\qquad R=L^3.                    \tag{17}
\]
Explicitly, for \(S=\lambda P+\mu Q\), Euler's identities and
\(J(S,R)=0\) make \(S^3/R^4\) a nonzero scalar.  Thus
\(S=a\ell^4,R=b\ell^3\); replacing \(\ell\) by \(b^{1/3}\ell\) and
rescaling \((\lambda,\mu)\) gives the simultaneous normalization in
(17).
In the present row,
\(\lambda P+\mu Q=h(\lambda p^2+\mu q^2)\).  Therefore \(h=L^2\);
because the second factor has no \(pq\) term, \(L\) is \(p\) or \(q\).
Up to the swap, the unique power-fibre exception is
\[
h=p^2,\qquad P=p^4,\qquad R=p^3.                     \tag{18}
\]
Its three block ranks are \((1,2,3)\), not one of the
nonexceptional rows in (16).

The independent hostile reconstruction
`audit_abstract_hb_e6_hostile/REPORT.md` supplies the expanded
height-two, scalar-normalization, and weighted-degree audit and should be
read as the adversarial companion to this compressed proof.

## 8. The signed \(E_6\) identity

Let \(D\) be the \(2\times2\) binary Jacobian matrix of \((P,Q)\),
let \(B\) be that of \((U,V)\), and write
\[
u=(U_r,V_r)^T,\quad
v=((H_2)_{1,r},(H_2)_{2,r})^T,\quad
w=\nabla R,\quad t=\nabla T,\quad \tau=T_r.
\]
Direct block expansion gives
\[
\boxed{
E_6=(\det D)(L_0)_{33}
+\operatorname{tr}(\operatorname{adj}B\,D)\tau
-w\operatorname{adj}D\,v
-t\operatorname{adj}D\,u
-w\operatorname{adj}B\,u.}                          \tag{19}
\]
Equivalently, if \(A_1,A_2\) are the first two components of \(H_2\),
\[
\boxed{
E_6=\alpha(A_1)_r+\beta(A_2)_r+\gamma(L_0)_{33}+T_6,}
                                                               \tag{20}
\]
where
\[
T_6=\det(dP,dV,dT)+\det(dU,dQ,dT)+\det(dU,dV,dR).     \tag{21}
\]
The exact verifier checks (19) as an abstract \(3\times3\) identity.

### The open nonsplitting stratum

If \(\det\mathcal M_0\ne0\), equation \(E_7=0\) gives
\[
U_r=V_r=T_r=0.
\]
Then \(T_6=0\).  Moreover
\[
w\operatorname{adj}D=(-\alpha,-\beta),
\]
so (20), split into its \(r^1\) and \(r^0\) parts, is exactly the
\(\mathcal M_2\) and \(\mathcal M_1\) syzygy problem.  Both are injective
when \(\mathcal M_0\) is injective.  Consequently
\[
(A_1)_r=(A_2)_r=0,\qquad(L_0)_{33}=0.                \tag{22}
\]
All nonlinear homogeneous pieces are now binary.  Postcomposing by
\(L_0^{-1}\) gives \(X+N(p,q)\); its first two coordinates form a plane
Keller map of degree at most four, hence an automorphism by the established
plane degree bound, and the third coordinate is a triangular shear.
Therefore
\[
\boxed{\det\mathcal M_0\ne0\quad\Longrightarrow\quad
       F\text{ is a polynomial automorphism}.}        \tag{23}
\]
Every counterexample in the binary fixed-quadratic row must lie on the
explicit divisor (11).

### A top-three survivor, not a Keller map

On the power fibre (18), take
\[
H_4=(p^4,p^2q^2,0),\qquad H_3=(0,0,p^3),\qquad H_2=0,
\]
and
\[
L_0=\begin{pmatrix}1&0&0\\0&0&1\\0&1&0\end{pmatrix}.
\]
Then \(\det L_0=-1\) and exact expansion gives
\[
E_8=E_7=E_6=0,\qquad E_3=-4p^3\ne0.                 \tag{24}
\]
Equivalently,
\[
F=(p+p^4,\ r+p^2q^2,\ q+p^3)
\]
is a concrete top-three-identity survivor and explicitly is **not** a
Keller map.  This witnesses that lower elimination is genuinely needed.

## 9. First \(E_6\) contact certificates on \(\delta=1\)

Suppose the nonexceptional Hilbert--Burch shape is
\(\{k_1,k_2\}=\{1,0\}\), and let \(N=(u,v,t)\) be its unique
degree-one tangent column.  The only possible \(r\)-dependence in
\((U,V,T)\) is then
\[
(U_r,V_r,T_r)=\kappa N.
\]
The \(r\)-coefficient of the curvature term \(T_6\) in (21) is a binary
quintic \(K_N\).  In that coefficient the two scalar \(r\)-terms in
\((A_1)_r,(A_2)_r\) enter through \((\alpha,\beta)\), while the
\(\gamma(L_0)_{33}\) term has no \(r\).  A necessary condition for a
nonzero contact parameter is therefore
\[
K_N\in\langle\alpha,\beta\rangle_{\mathbb C}.        \tag{25}
\]
The following literal \(3\times3\) minors give exact certificates on the
first four determinant components.

For \(h=pq\) and
\[
R=bp^2q+cpq^2+dq^3
\]
(the component \(a=0\)), one may take
\[
N=(3p^2,q^2,2bp+cq),\qquad
K_N=2pq^2(7bp^2+3cpq-9dq^2).
\]
Two contact minors are
\[
70b^3,\qquad 6c(54bd+5c^2).                          \tag{26}
\]
Thus contact first forces \(b=0\), then \(c=0\), routing to the deeper
stratum \(R=dq^3\).

For \(h=p(p+q)\), the component \(d=0\) has
\[
N=(p^2,q(2p+3q),bp+2cq).
\]
Off its intersection \(3a-4b=0\), successive exact minors
\[
-14c^2(3a-4b),\qquad 30b^3\big|_{c=0},\qquad
486a^3\big|_{b=c=0}                                  \tag{27}
\]
exclude nonzero contact.  On the other two components, \(3a=4b\) and
\(a-b+c-d=0\), the selected minors are respectively
\[
1944d^3,\qquad486d^3,                                \tag{28}
\]
so their open parts also route to the \(d=0\) intersection.

The branch-square chart behaves differently.  For \(h=p^2\), a cleared
Hilbert--Burch column is
\[
\begin{aligned}
N={}&(12dp^2,\,-2cpq+6dq^2,\\
&\quad (9da-cb)p+2(3db-c^2)q).
\end{aligned}
\]
Two contact minors are
\[
15552cd^4,\qquad -576d^2(27ad^2-10c^3).              \tag{29}
\]
On \(d\ne0\), contact therefore forces \(c=a=0\), leaving
\[
R=bp^2q+dq^3,\qquad bd\ne0.                          \tag{30}
\]
Here the normalized tangent
\[
N=(2p^2,q^2,bq)
\]
really survives (25), since
\[
K_N=4pq^2(bp^2-3dq^2)=-2J(Q,R).
\]
Indeed, for every \(\kappa\),
\[
\begin{aligned}
H_4&=(p^4,p^2q^2,0),\\
H_3&=(2\kappa rp^2,\ \kappa rq^2,\ bp^2q+dq^3),\\
H_2&=(\kappa^2r^2,\ 0,\ \kappa bqr)
\end{aligned}                                        \tag{31}
\]
with the invertible linear part used in (24) satisfies
\[
E_8=E_7=E_6=0,\qquad
E_5=-4p^3(bp^2+3dq^2)\ne0.                           \tag{32}
\]
Thus (31) is another exact top-three survivor, not a Keller map.  It also
shows that \(E_6\) does not by itself exclude the entire \(\delta=1\)
rank-drop divisor.

### Interior ramification contact

Put
\[
h=p^2+\eta pq+q^2,\qquad
R=ap^3+\frac34a\eta p^2q+cpq^2+dq^3.                \tag{33}
\]
This is the component \(3a\eta-4b=0\).  A cleared tangent column is
\[
\begin{aligned}
N={}&(2(3\eta^2-8)p^2+4\eta pq,\\
&-16p^2-20\eta pq+2(\eta^2-16)q^2,\\
&(3\eta^2a-16c)p+2(\eta c-12d)q).
\end{aligned}
\]
The leading contact equation first gives
\[
7a\eta^3-48a\eta+48c\eta-64d=0.                    \tag{34}
\]
Away from the opposite contact component \(4c-3d\eta=0\), the trailing
coefficient fixes the \(\alpha\)-multiplier.  Three remaining literal
wedges give, in the chart \(a=1,c=t\), two univariate resultants whose
greatest common divisor is exactly \(\eta^2\).  In the chart \(a=0,c=1\),
two wedges are
\[
192\eta(7\eta^2-48),\qquad
48\eta^2(13\eta^2-120).                              \tag{35}
\]
Thus every exact-\(\delta=1\) contact on (33) has
\[
\eta=0,\qquad b=d=0.
\]
Conversely, for
\[
h=p^2+q^2,\qquad R=ap^3+cpq^2,\qquad c(a-c)\ne0,     \tag{36}
\]
the normalized column
\[
N=(p^2,p^2+2q^2,cp)
\]
satisfies \(K_N=-2\beta\).  The inequality in (36) removes the opposite
ramification contact and common-root intersection, so this is genuinely
the exact-\(\delta=1\) stratum.  A sparse completion is
\[
\begin{aligned}
H_4&=((p^2+q^2)p^2,(p^2+q^2)q^2,0),\\
H_3&=(\kappa rp^2,\ \kappa r(p^2+2q^2),\ ap^3+cpq^2),\\
H_2&=(0,\ \kappa^2r^2,\ \kappa cpr).
\end{aligned}                                        \tag{37}
\]
It has \(E_8=E_7=E_6=0\), while
\[
E_5=-2p\{(-3a+4c)p^3q+cpq^3+
             2\kappa(p^2+q^2)^2\}\ne0.              \tag{38}
\]
The opposite contact component gives the swapped family.

### Common and doubled roots

The common-root component has a short evaluation proof.  Write
\[
\begin{aligned}
L&=p-sq,\quad M=sp-q,\quad h=LM,\\
R&=L(Ap^2+Bpq+Cq^2).
\end{aligned}
\]
For \(s\ne0,\ s^2\ne1\), its tangent is
\[
N=L^{-1}(s\partial_p+\partial_q)(P,Q,R).
\]
After dividing \(\alpha,\beta,K_N\) by \(L\), evaluation at \(q=0\) and
\(p=0\), away from the two ramification-contact intersections, forces
both contact multipliers to equal \(-2s\).  Evaluation at \(p=sq\) then
gives
\[
14s(s^2-1)^2(A s^2+B s+C)=0.                        \tag{39}
\]
The last factor vanishes exactly when \(L^2\mid R\), a deeper
intersection.  Hence the exact-\(\delta=1\) common-root open stratum has
no nonzero \(E_6\) contact.

Finally, on the doubled nonbranch root \(h=(p+q)^2\), both
\(\alpha,\beta\) are divisible by \(p+q\), whereas the tangent curvature
has remainder
\[
K_N\bmod(p+q)=-324q^5(a-b+c-d)^3.                   \tag{40}
\]
The factor \(a-b+c-d\) says precisely that \(p+q\mid R\), again the
deeper common-root intersection.  Thus the exact-\(\delta=1\) open part
is obstructed.

Combining (26)--(40) gives the exact-\(\delta=1\) contact classification,
up to the stabilizer and the swap:
\[
\boxed{
\begin{array}{ll}
h=p^2,&R=bp^2q+dq^3,\quad bd\ne0,\\[2pt]
h=p^2+q^2,&R=ap^3+cpq^2,\quad c(a-c)\ne0.
\end{array}}                                        \tag{41}
\]
Every other exact-\(\delta=1\) determinant component either has zero
\(E_7\) contact parameter or is routed to \(\delta\ge2\).  Statement
(41) classifies survival only through \(E_6\); the displayed sparse
completions fail \(E_5\), and no member is asserted to be Keller.

## 10. Full lower exclusion of both exact-\(\delta=1\) survivors

The sparse \(E_5\) failures above are not used for exclusion.  Retain
every binary coefficient of \(H_3,H_2\) and all nine entries
\(\ell_{ij}\) of the linear part \(L\), and solve \(E_6,E_5\) exactly.
The complete derivation is in `DELTA1_EXCLUSION_NOTE.md`.

For the branch-square family in (41), write \(\kappa\ne0\) for the
contact parameter and \(v_2\) for the \(pq^2\)-coefficient of the binary
part of \(V\).  The full \(E_6,E_5\) solution gives
\[
\ell_{13}=\kappa(x_0-v_2^2),\quad
\ell_{23}=\kappa y_0,\quad
\ell_{31}=t_0v_2,\quad \ell_{33}=\kappa t_0.
\]
Set
\[
M_0=\kappa\ell_{11}-v_2\ell_{13},\qquad
M_3=\kappa\ell_{21}-v_2\ell_{23}.
\]
With every other free coefficient still present,
\[
E_4=2bM_3p^4+(bM_0+6dM_3)p^2q^2-3dM_0q^4.         \tag{42}
\]
Since \(bd\ne0\), \(E_4=0\) gives \(M_0=M_3=0\), and
\[
L(\kappa,0,-v_2)^T=0.                               \tag{43}
\]
This contradicts \(\det L\ne0\).

For the interior family in (41), let \(u_1\) be the \(p^2q\)-coefficient
of the binary part of \(U\).  The full solution gives
\[
\ell_{13}=\kappa x_2,\quad
\ell_{23}=\kappa(y_2-u_1^2),\quad
\ell_{32}=t_2u_1,\quad \ell_{33}=\kappa t_2.
\]
Put
\[
M_1=\kappa\ell_{12}-u_1\ell_{13},\qquad
M_4=\kappa\ell_{22}-u_1\ell_{23}.
\]
Then
\[
\begin{aligned}
E_4={}&[3aM_1+(-3a+4c)M_4]p^4\\
&+[(6a-c)M_1+cM_4]p^2q^2+2cM_1q^4.                \tag{44}
\end{aligned}
\]
Because \(c\ne0\), it follows that \(M_1=M_4=0\), and
\[
L(0,\kappa,-u_1)^T=0.                               \tag{45}
\]

Thus
\[
\boxed{\text{no Keller counterexample in the binary fixed-quadratic row has }
       \delta=1.}                                    \tag{46}
\]
The divisor mutations \(b=0,d=0,c=0,a-c=0\) have respectively the
deeper block ranks recorded in the standalone note.  The case
\(\kappa=0\) is the already proved all-binary plane exit, so no divisor
was divided away in deriving (43) or (45).

## 11. Exact \(\delta=2\) Hilbert--Burch stratification

The local valuation table and all maximal-minor certificates are frozen
in `DELTA2_HB_STRATIFICATION.md`.  At exact \(\delta=2\), both abstract
Hilbert--Burch shapes really occur:
\[
\{1,1\}\longleftrightarrow(2,5,6),\qquad
\{2,0\}\longleftrightarrow(2,4,6).                  \tag{47}
\]
Every exact-\(\delta=2\) point on the three boundary fixed-divisor
orbits \(p^2,pq,p(p+q)\) has shape \(\{1,1\}\).  In the interior, the
complete \(\{2,0\}\) list, up to stabilizer and swap, is:

1. two ramification contacts at orbit modulus \(\kappa=16\);
2. one fixed-root incidence plus one ramification contact at
   \(\kappa=16/3\); and
3. on the doubled nonbranch orbit \(\kappa=4\), the codimension-one
   coefficient locus
   \[
   h=(p+q)^2,\quad
   R=ap^3+bp^2q+\frac32d\,pq^2+dq^3,\quad
   6a-5b+3d=0,                                     \tag{48}
   \]
   on the exact open
   \((3a-2b)(2a-2b+d)\ne0\).

A mandatory rational regression for the first row is
\[
\begin{aligned}
h&=p^2+4pq+q^2,\\
R&=p^3+3p^2q+6pq^2+2q^3.
\end{aligned}                                      \tag{49}
\]
It has
\[
g=2pq,\qquad \operatorname{Res}(h,R)=-18,
\qquad\operatorname{rank}(\mathcal M_2,\mathcal M_1,\mathcal M_0)
=(2,4,6),
\]
and literal \(\mathcal M_1\)-kernel
\[
(-5,-1,1,5,3)^T.                                   \tag{50}
\]
Thus the \(\{2,0\}\) row cannot be discarded before solving \(E_6\).

## 12. Provisional exclusion of the \(\kappa=16\), \(\{2,0\}\) row

The full-coefficient proof is frozen in
`DELTA2_KAPPA16_EXCLUSION.md`; hostile mathematical audit is pending.
For
\[
h=p^2+4pq+q^2,\qquad
R=ap^3+3ap^2q+3dpq^2+dq^3,\qquad a+d\ne0,
\]
the complete \(E_7\) family has its \(r^1\) tangent killed by
\[
[r^3]E_6=12k^2\{(a+2d)(p^3+3p^2q)
 +(2a+d)(3pq^2+q^3)\}.
\]
The remaining \(E_6\) equations reduce all nonlinear \(r\)-dependence to
\[
(A_{1,r},A_{2,r},\ell_{33})
=\lambda(5p+q,-p-5q,3(a-d)).
\]
If \(\lambda=0\), \(E_5\) makes the third column of the linear part zero.
If \(\lambda(a-d)\ne0\), triangularizing the third component gives a
degree-at-most-four plane Keller map over \(\mathbb C(w)\); the banked
plane-field and birational Keller exit makes the three-variable map an
automorphism.  In the only remaining branch \(a=d\ne0,\lambda\ne0\), the
complete \(E_5\) solve gives
\[
[r]E_4=72a\lambda^2(p+q)^3\ne0.
\]
Subject to hostile replay, this excludes the complete
\(\kappa=16,\{2,0\}\) row.

## 13. Provisional exclusion of the \(\kappa=16/3\), \(\{2,0\}\) row

The full proof and exact-open conditions are frozen in
`DELTA2_KAPPA16OVER3_EXCLUSION.md`.  A rational representative is
\[
h=(p+q)(3p+q),\qquad
R=(p+q)(ap^2+2bpq+bq^2),
\qquad b(a-b)(a+3b)\ne0.                           \tag{51}
\]
The genuine \(r^1\) Hilbert--Burch column is
\[
(4p+q,-3q,a-b).
\]
The \(r^3\) coefficient of \(E_6\) kills its quadratic-in-\(r\)
integral.  An endpoint-safe treatment of \([r]E_6\), including
\(a=-2b\), then kills every remaining nonlinear \(r\)-coefficient.
The constant \(E_6\) equation leaves
\[
(A_{1,r},A_{2,r},\ell_{33})
=\lambda(4p+q,-3q,a-b).                            \tag{52}
\]
At \(\lambda=0\), \(E_5\) gives a zero third column.  At
\(\lambda\ne0\), the exact open set has \(a-b\ne0\), so the
degree-at-most-four plane-field and birational Keller exit proves
automorphy.  Subject to hostile replay, this excludes the complete
\(\kappa=16/3,\{2,0\}\) row.

## 14. Provisional exclusion of the \(\kappa=4\), \(\{2,0\}\) row

The full proof is frozen in `DELTA2_KAPPA4_EXCLUSION.md`.  Its normal
form is
\[
\begin{aligned}
h&=(p+q)^2,\\
R&=ap^3+bp^2q+\frac32d\,pq^2+dq^3,\qquad
d=\frac{5b-6a}{3},\\
&\hspace{95pt}b(3a-2b)\ne0.
\end{aligned}                                      \tag{53}
\]
The genuine \(r^1\) column is
\[
(6p+4q,-2q,6a-b).
\]
Again \([r^3]E_6\) kills its quadratic-in-\(r\) integral, and an
endpoint-safe \([r]E_6\) solve, including \(6a+11b=0\), kills all
remaining nonlinear \(r\)-terms.  The constant equation leaves
\[
(A_{1,r},A_{2,r},\ell_{33})
=\lambda(6p+4q,-2q,6a-b).                          \tag{54}
\]
The branches \(\lambda=0\) and
\(\lambda(6a-b)\ne0\) end respectively in a zero third column and the
same plane-field automorphism exit.  On the sole residual divisor
\(a=b/6,\lambda\ne0\), the complete \(E_5\) solve gives
\[
[r]E_4=6b\lambda^2(p+2q)^3\ne0.                    \tag{55}
\]

Together with the exhaustive list in Section 11, these three candidate
theorems give the provisional umbrella
`DELTA2_K20_UMBRELLA.md`:
\[
\boxed{\text{every exact-\(\delta=2\) counterexample in this row,
if any, has HB shape \(\{1,1\}\).}}                 \tag{56}
\]
This is only a shape exclusion.  It does not close exact
\(\delta=2\), \(\delta\ge3\), or the constant-dependent power fibre.

## 15. First provisional \(\{1,1\}\) exclusion

The complete signed-minor and lower-identity proof is frozen in
`DELTA2_11_P2_SIMPLE_FIXED_EXCLUSION.md`.  It treats
\[
h=p^2,\qquad
R=p(Ap^2+Bpq+Cq^2),\qquad BC\ne0.                 \tag{57}
\]
The lifted \(E_6\) contact equation is linear in
\((s^2,st,t^2,x_5,y_5)\).  On
\(\Delta=4AC-B^2\ne0\), its rank-four kernel has Veronese obstruction
\[
3C^2(256AC+11B^2).                                \tag{58}
\]
The \(\Delta=0\) endpoint is recomputed with a fresh tangent basis and
has obstruction \(225B^2\), so it is not lost by division.

Thus the only nonzero \(E_6\) contact lies on
\(256AC+11B^2=0\), a single stabilizer orbit represented by
\[
R=p(-11p^2+16pq+q^2).                              \tag{59}
\]
Its mandatory tangent and quadratic \(r\)-coefficients are
\[
\begin{aligned}
(U_r,V_r,T_r)&=k(4p^2,6pq+q^2,15p+30q),\\
([r^2]H_{2,1},[r^2]H_{2,2})&=(6k^2,9k^2).
\end{aligned}                                      \tag{60}
\]
After the complete rank-six \(E_6\) solve with all lower coefficients
and all entries of the linear part retained,
\[
[r^2]E_5
=-24k^3(72p^3+7p^2q-11pq^2+q^3),                 \tag{61}
\]
so \(k\ne0\) is impossible.  The \(k=0\) branch is the established
all-binary automorphism exit.  Subject to hostile replay, this excludes
the complete incidence (57), not the other \(\{1,1\}\) mechanisms.

## 16. Second provisional \(\{1,1\}\) exclusion

The complete proof is frozen in
`DELTA2_11_P2_BRANCH_CONTACT_EXCLUSION.md`.  It treats the other
exact-\(\delta=2\) branch-square incidence
\[
h=p^2,\qquad R=Ap^3+Cpq^2+Dq^3,\qquad D\ne0.      \tag{62}
\]
With \(\Lambda=27AD^2+4C^3\), the generic lifted contact determinant is
\[
-71663616C^2D^6\Lambda^3.                         \tag{63}
\]
The \(\Lambda=0,C\ne0\) chart is recomputed from a fresh basis and has
determinant \(-12288C^2\).  At \(C=0,A\ne0\), the rank-four contact
kernel misses the Veronese cone by
\[
\frac{81}{16}A^2D^2.
\]
The unique actual contact occurs at \(A=C=0\), namely
\[
R=Dq^3,\qquad
(U_r,V_r,T_r)=k(2p^2,q^2,0),\qquad(x_5,y_5)=(k^2,0).
                                                               \tag{64}
\]
The full lower solve first forces a rank-five \(E_5\) compatibility
\(3Dkv_0^2=0\).  After solving \(E_5\), \(E_4\) has the exact form
\[
E_4=D(6M_3p^2q^2-3M_0q^4),\qquad
L(k,0,-v_2)^T=(M_0,M_3,0)^T.                      \tag{65}
\]
Thus \(E_4=0\) makes the linear part singular.  Subject to hostile
replay, both \(h=p^2\) exact-\(\delta=2,\{1,1\}\) leaves are now
excluded.

The remaining thirteen leaves and every routed mutation are listed in
`DELTA2_11_LEAF_REGISTRY.md`.  The active next leaf is
\[
h=pq,\qquad R=p^2(Ap+Bq),\qquad AB\ne0,
\]
chosen because its lifted contact matrix is pivot-generic and has
maximal rank at rational regressions.

## 17. Third provisional \(\{1,1\}\) exclusion

For
\[
h=pq,\qquad R=p^2(Ap+Bq),\qquad AB\ne0,            \tag{66}
\]
the complete lifted \(E_6\) contact determinant is
\[
-2332800000A^3B^8.                                \tag{67}
\]
It forces both \(E_7\) tangent parameters and both quadratic
\(r\)-coefficients of \(H_2\) to vanish.  The remaining constant
\(E_6\) block has decisive determinant
\[
-3240A^3B,                                         \tag{68}
\]
so all nonlinear terms are binary and the established plane-field
exit proves automorphy.  The coefficient mutations \(A=0,B=0\) route
to \(\delta\ge3\).  The full provisional proof is
`DELTA2_11_PQ_DOUBLE_EXCLUSION.md`.

The leaf registry now has three provisional closures and twelve open
leaves.  The active next leaf is the remaining two-simple-contribution
family
\[
h=pq,\qquad R=pq(Ap+Bq),\qquad AB\ne0.
\]

## 18. Fourth provisional \(\{1,1\}\) exclusion

For the remaining \(h=pq\) leaf
\[
R=pq(Ap+Bq),\qquad AB\ne0,                         \tag{69}
\]
the lifted contact matrix has rank four with kernel
\[
(X,Y,Z,x_5,y_5)=(1,7/5,1,0,0).
\]
Its Veronese obstruction is \(24/25\), so no actual tangent survives.
The constant \(E_6\) block has decisive determinant \(8A^2B^2\);
all nonlinear terms are binary and the plane-field exit applies.
Both coefficient boundaries have \(\delta=3\).  The full proof is
`DELTA2_11_PQ_TWO_SIMPLE_EXCLUSION.md`.

Thus all exact-\(\delta=2,\{1,1\}\) leaves on \(h=pq\) are
provisionally excluded.  The registry now has four provisional
closures and eleven open leaves.

## 19. Fifth provisional \(\{1,1\}\) exclusion

On
\[
h=p(p+q),\qquad R=p^2(Ap+Bq),
\]
the exact open is \(B(A-B)(3A-4B)\ne0\).  The three boundary divisors
have gcd degree three and are explicitly routed; \(A=0\) remains in
the exact open.  The lifted contact and constant \(E_6\) determinants
are respectively
\[
\begin{aligned}
&-6220800B^5(A-B)^2(3A-4B),\\
&-1080B(A-B)^2(3A-4B).
\end{aligned}                                      \tag{70}
\]
Both are nonzero, giving the all-binary automorphism exit.  The proof
is `DELTA2_11_PELL_DOUBLE_P_EXCLUSION.md`.

## 20. Sixth provisional \(\{1,1\}\) exclusion

On
\[
h=p(p+q),\qquad R=(p+q)^2(Ap+Bq),
\]
the exact open is \(B(5A+4B)\ne0\).  The two boundary divisors have
gcd degree three.  Away from the internal pivot \(A=B\), two lifted
contact minors are
\[
\begin{aligned}
M_0={}&-466560000B^3(A-B)^6
       (5A^2+26AB+23B^2),\\
M_1={}&-311040000B^3(A-B)^6
       (2A+7B)(5A+4B).
\end{aligned}                                      \tag{71}
\]
They cannot vanish simultaneously on the exact open: \(M_1=0\)
would force \(2A+7B=0\), where the last factor of \(M_0\) is
\(-27B^2/4\).  At \(A=B\), a fresh tangent chart has contact
determinant \(276480\).  Thus every contact variable vanishes on the
whole exact open.  The remaining constant \(E_6\) block has determinant
\[
-648B^3(5A+4B),                                    \tag{72}
\]
so the all-binary automorphism exit applies.  This proof treats the
marked row independently and does not assume that interchanging
\(p\) and \(p+q\) preserves it.  The complete proof is
`DELTA2_11_PELL_DOUBLE_L_EXCLUSION.md`.

## 21. Seventh provisional \(\{1,1\}\) exclusion

For
\[
h=p(p+q),\qquad R=p(p+q)(Ap+Bq),
\]
the exact open is \(B(A-B)(A+4B)\ne0\).  Fresh recomputation on the
three excluded boundary divisors gives gcds
\[
p^2(p+q),\qquad p(p+q)^2,\qquad pq(p+q),
\]
respectively, so each routes to \(\delta=3\).  A polynomial basis of
the two \(E_7\) tangents is
\[
\begin{aligned}
N_1={}&(5Bp^2,-Bq(6p+q),3Bp(A-B)),\\
N_2={}&(-(A+4B)p^2,q(6Ap+5Aq-4Bq),3Bq(A-B)).
\end{aligned}                                      \tag{73}
\]
The lifted contact map has rank four.  Its kernel is spanned by
\[
\bigl(-(5A^2+4AB-4B^2),-B(7A-2B),-5B^2,0,
36B^2(A-B)^2\bigr),
\]
whose Veronese obstruction is
\[
24B^2(A-B)^2.                                      \tag{74}
\]
Thus no nonzero actual tangent survives.  The constant \(E_6\)
determinant is \(8B^2(A-B)(A+4B)\), yielding the all-binary
automorphism exit.  The complete proof is
`DELTA2_11_PELL_TWO_FIXED_EXCLUSION.md`.

## 22. Eighth provisional \(\{1,1\}\) exclusion

For
\[
h=p(p+q),\qquad R=p(4Tp^2+3Tpq+Cq^2),
\qquad C(C+T)\ne0,
\]
the excluded boundaries \(C=0,C=-T\) are recomputed as
\(\delta=3\).  Off the two internal divisors, the lifted contact
determinant is
\[
27648C^5(C+T)^2(12C+7T)(16C-9T)^3.               \tag{75}
\]
At the tangent-basis pivot \(16C=9T\), a fresh normalized chart has
contact determinant \(422400000\).  At the genuine rank-drop divisor
\(12C=-7T\), a fresh normalized chart has rank four and kernel
\[
\left(-\frac{2354}{3},\frac{3773}{24},
      -\frac{539}{48},0,1\right),
\]
whose Veronese obstruction is \(3053435/192\).  Thus no actual contact
survives anywhere on the exact open.  The constant \(E_6\) determinant
is \(72C^2(C+T)^2\), yielding the all-binary automorphism exit.  The
complete proof is `DELTA2_11_PELL_P_CONTACT_EXCLUSION.md`.

## 23. Ninth provisional \(\{1,1\}\) exclusion

For
\[
h=p(p+q),\quad
R=(p+q)(-4Bp^2+Bpq+Cq^2),\quad C(5B-C)\ne0,
\]
the excluded boundaries \(C=0,C=5B\) are recomputed as
\(\delta=3\).  Off the internal divisors, the contact determinant is
\[
-746496C^3(B+16C)^3(5B-4C)(5B-C)^4.              \tag{76}
\]
The fresh \(B=-16C\) pivot chart has full determinant \(6967296\).
On the fresh \(5B=4C\) rank-drop chart, the one-dimensional kernel is
\[
\left(-840,-\frac{945}{2},-\frac{945}{4},0,1\right)
\]
and misses the Veronese cone by \(99225/4\).  The constant \(E_6\)
determinant is \(-648C^3(5B-C)\), yielding the all-binary
automorphism exit.  The complete independent proof is
`DELTA2_11_PELL_L_CONTACT_EXCLUSION.md`.

Thus every exact-\(\delta=2,\{1,1\}\) leaf on the one-branch fixed
divisor \(h=p(p+q)\) is provisionally excluded.

## 24. Tenth provisional \(\{1,1\}\) exclusion

On the squarefree-interior chart
\[
L=p-wq,\quad M=wp-q,\quad h=LM,\quad
R=L^2(Ap+Bq),
\]
the exact open removes \(w=0,w^2=1\), the other fixed-root evaluation,
and both branch contacts.  On the generic pivot \(Aw+B\ne0\), four
selected contact minors reduce to residual cubics \(Q_1,\dots,Q_4\)
in \(A/B\).  Four exact pairwise resultants have monic gcd
\[
w^3(w^2-1)^{12}.                                  \tag{77}
\]
Thus they have no common zero on the interior open; the missing
projective endpoint \(B=0\) has residual gcd \(w^2\).

The internal pivot \(Aw+B=0\) is the genuine triple-root case
\(R=L^3\), not a mutation.  In a fresh tangent chart its contact
determinant is
\[
48977602560w^5(w-1)^6(w+1)^6
\,(w^2-3)^4(3w^2-1),                              \tag{78}
\]
nonzero after excluding the two branch-contact divisors.  The constant
\(E_6\) block is full rank on the entire exact open, giving the
all-binary automorphism exit.  The proof is
`DELTA2_11_INTERIOR_DOUBLE_FIXED_EXCLUSION.md`.

## 25. Eleventh provisional \(\{1,1\}\) exclusion

For the squarefree-interior two-fixed-root family
\[
h=(p-wq)(wp-q),\qquad R=h(Ap+Bq),
\]
the exact open removes both fixed-root evaluations and both branch
contacts.  The lifted contact map has rank four.  Its complete kernel
has Veronese obstruction
\[
24(A+Bw)^2(w-1)^2(w+1)^2(Aw+B)^2,                \tag{79}
\]
which is nonzero throughout that open.  The constant \(E_6\) block is
also full rank, so the all-binary automorphism exit applies.  All four
deeper-incidence boundary gcds are explicitly routed.  The complete
proof is `DELTA2_11_INTERIOR_TWO_FIXED_EXCLUSION.md`.

## 26. Twelfth provisional \(\{1,1\}\) exclusion

On the squarefree-interior fixed-root/contact chart
\[
\begin{aligned}
L&=p-wq,\qquad M=wp-q,\qquad h=LM,\\
R&=L\{Ap^2+(1-3w^2)Tpq+4wTq^2\},
\end{aligned}
\]
the exact open removes the other fixed-root incidence, a doubled
chosen root, the second branch contact, and the exceptional
\(\kappa=16/3\) modulus.  The generic lifted contact determinant has
the two internal factors
\[
\begin{aligned}
D&=-16Aw+T(9w^4-6w^2+1),\\
H&=12Aw^3-4Aw+T(7w^6+9w^4-3w^2-5).
\end{aligned}
\]
Fresh \(D=0\) and \(H=0\) tangent bases cover their singular generic
denominators.  The \(H=0\) rank-four kernel has Veronese obstruction
with primitive numerator
\[
V(u)=515u^4-548u^3+162u^2-324u+243,\qquad u=w^2.
\]
This is a genuine \(E_6\) survivor.  Over the exact field
\(\mathbb Q[w]/(V(w^2))\), a denominator-cleared tangent gives
\[
[r^2p^3]E_5=-96w^5(u+1)^2F_0^3JG_0N_XC(u).
\]
Every displayed factor is invertible; in particular
\[
\operatorname{Res}(V,C)
=2^{81}3^{20}5^2\cdot1291\ne0.
\]
The coefficient is top-only by a mixed-determinant support argument
for the weight partitions \((3,2,0),(3,1,1),(2,2,1)\).

The four residual singular-basis fields
\[
w^2+1,\quad5w^2-3,\quad11w^2-9,\quad J(w^2)
\]
were recomputed independently.  Two contact maps have full rank; the
other two have rank-four kernels missing the Veronese cone.  The
uniform constant \(E_6\) block is full rank, so the all-binary exit
applies.  The complete proof is
`DELTA2_11_INTERIOR_FIXED_CONTACT_EXCLUSION.md`.

## 27. Thirteenth provisional \(\{1,1\}\) exclusion

For the squarefree-interior two-contact family
\[
\begin{aligned}
h&=(p-wq)(wp-q),\\
R&=4wap^3-3(1+w^2)ap^2q
   -3(1+w^2)pq^2+4wq^3,
\end{aligned}
\]
the exact open removes both fixed-root evaluations and the two
exceptional \(\kappa=16\) factors.  The residual stabilizer identifies
\(a\) with \(a^{-1}\), \(w\) with \(w^{-1}\), and
\((w,a)\) with \((-w,-a)\); \(u=w^2\), modulo inversion, is the
four-point cross-ratio.

On the generic \(E_7\) basis, the six contact minors stratify through
two linear factors \(K_1,K_2\).  Their simultaneous vanishing gives
two primitive irreducible sextics; fresh exact-field contact kernels
have rank four and miss the Veronese cone.  The reciprocal octics and
the residual quartic \(5w^4-6w^2+5\) are exactly fixed-root incidence
boundaries, verified over their coefficient fields rather than
discarded as denominator factors.

The singular generic denominator \(B=0\) has a fresh tangent basis.
Its elimination leaves the routed factors and one primitive
irreducible reciprocal degree-sixteen polynomial \(P_{16}\); the
fresh \(P_{16}\)-field contact map has full rank.  The remaining point
is
\[
w^2=-1,\qquad a=0.
\]
There the contact map has rank three and a unique Veronese lift
\[
(2p^2+q^2,q^2,0),\qquad(x_5,y_5)=(-w,0).
\]
It survives the top-only \(E_5\) test.  Restoring every lower
coefficient, the full \(E_6,E_5,E_4\) solve forces the first column of
the linear part to be \(u_2\) times its third column.  Hence its
constant Jacobian coefficient is zero.  The complete proof is
`DELTA2_11_INTERIOR_TWO_CONTACTS_EXCLUSION.md`.

## 28. Fourteenth provisional \(\{1,1\}\) exclusion

For the doubled-nonbranch simple-fixed family
\[
h=(p+q)^2,\qquad
R=(p+q)(Ap^2+Bpq+Cq^2),
\]
the exact open is
\[
(A-2B)(2B-C)(A-B+C)\ne0.
\]
The generic \(E_7\) tangent basis has internal denominator
\(\Delta=4AC-B^2\).  A rank-six \(E_7\) minor and the lifted contact
determinant are respectively
\[
-768(A-2B)(2B-C)\Delta(A-B+C)^2
\]
and
\[
26542080(A-2B)(2B-C)\Delta^3(A-B+C)^3.
\]
Thus there is no contact survivor for \(\Delta\ne0\).

The divisor \(\Delta=0\) was recomputed from a fresh polynomial
tangent basis.  With \(A=B^2/(4C)\), its contact determinant is
\[
-\frac{3840B(B-8C)(B-2C)^6(2B-C)^4}{C},
\]
and every factor is forced nonzero by the exact open.  Finally, the
uniform constant \(E_6\) determinant is
\[
-512(A-2B)(2B-C)(A-B+C)^2.
\]
The all-binary automorphism exit therefore applies.  The complete
proof is
`DELTA2_11_DOUBLED_NONBRANCH_SIMPLE_FIXED_EXCLUSION.md`.

## 29. Verification boundary

Run

```text
/usr/bin/python3 -u verify_orbits_top_sympy.py
./verify_e7_determinants_pari_strict.sh
/usr/bin/python3 -u verify_e6_delta1_sympy.py
./verify_delta1_lower_exclusion_strict.sh
./verify_delta2_hb_stratification_strict.sh
./verify_delta2_kappa16_exclusion_strict.sh
./verify_delta2_kappa16over3_exclusion_strict.sh
./verify_delta2_kappa4_exclusion_strict.sh
./verify_delta2_11_p2_simple_fixed_strict.sh
./verify_delta2_11_p2_branch_contact_strict.sh
./verify_delta2_11_pq_double_strict.sh
./verify_delta2_11_pq_two_simple_strict.sh
./verify_delta2_11_pell_double_p_strict.sh
./verify_delta2_11_pell_double_l_strict.sh
./verify_delta2_11_pell_two_fixed_strict.sh
./verify_delta2_11_pell_p_contact_strict.sh
./verify_delta2_11_pell_l_contact_strict.sh
./verify_delta2_11_interior_double_fixed_strict.sh
./verify_delta2_11_interior_two_fixed_strict.sh
./verify_delta2_11_interior_fixed_contact_strict.sh
./verify_delta2_11_interior_two_contacts_strict.sh
./verify_delta2_11_doubled_simple_fixed_strict.sh
```

The SymPy script checks the stabilizer coefficient action, the three signed
block identities, exact sample ranks, and the top-three survivor.  The
independent PARI/GP certificate checks every factor in (11), the resultant
(12), and representative ranks for all Hilbert--Burch shapes plus the
power fibre.  The second SymPy script checks the literal contact minors
(26)--(29), the resultants and evaluations (33)--(40), and both full
determinant expansions.  The final strict wrapper independently replays
the complete \(E_6,E_5,E_4\) lower solve in SymPy and PARI/GP, including
mutation guards for \(b,d,c,a-c,\kappa\) and both kernel vectors.  Orbit
completeness and the Hilbert--Burch bounds are mathematical proofs above,
not consequences of sampling.  The last strict wrapper reconstructs the
complete exact-\(\delta=2\) incidence list from local valuations, checks a
decisive maximal minor on every incidence type, and independently replays
the three exceptional \(\{2,0\}\) mechanisms in PARI/GP.  The final three
wrappers start from their full integrated \(E_7\) families and
independently replay the provisional
\(\kappa=16,\kappa=16/3,\kappa=4\) \(E_6,E_5,E_4\) solves in SymPy and
PARI/GP, including every exceptional parameter divisor used above.
The last wrapper independently reconstructs the signed-minor/Veronese
contact divisor, its \(\Delta=0\) chart and boundary mutations, then
replays the full rational-survivor \(E_6/E_5\) obstruction.  The final
wrapper checks the second \(h=p^2\) contact atlas, its unique \(R=Dq^3\)
survivor, and the complete \(E_6/E_5/E_4\) linear-part-kernel
contradiction.  The last wrapper replays the two decisive \(h=pq\)
doubled-contribution \(E_6\) determinants and all exact-open mutations.
The final wrapper checks the two-simple-contribution rank-four kernel,
its Veronese miss, and the constant \(E_6\) determinant.  The last
wrapper replays all three exact-open boundaries and both decisive
\(h=p(p+q)\), doubled-\(p\) determinants.
The final wrapper checks the doubled-\((p+q)\) boundary gcds, the
two-minor contact cover, the fresh \(A=B\) pivot chart, and the
constant \(E_6\) determinant independently in SymPy and PARI/GP.
The last wrapper reconstructs all three two-fixed-root boundary
specializations, its full tangent basis, rank-four kernel and
Veronese miss, and the constant \(E_6\) determinant in both systems.
The final wrapper checks both fixed-\(p\) contact boundaries, the
generic determinant, both fresh internal charts, and the constant
\(E_6\) block independently.
The last wrapper independently replays the fixed-\((p+q)\) companion,
including both routed boundaries, its pivot chart, its genuine
rank-four contact chart, and its constant block.
The final wrapper reconstructs the first squarefree-interior leaf,
including its projective resultant cover, coefficient endpoint, fresh
triple-root pivot, and constant block.
The last wrapper independently checks the squarefree-interior
two-fixed-root leaf, including all four routed boundaries, its full
contact kernel, and its Veronese miss.
The final wrapper checks the squarefree-interior fixed-root/contact
leaf, including its generic contact chart, both internal divisors, the
primitive quartic \(E_6\) survivor and top-only \(E_5\) resultant, all
four singular-basis coefficient fields, and the uniform constant
block in both SymPy and PARI/GP.
The last wrapper checks the squarefree-interior two-contact leaf,
including its stabilizer and cross-ratio identifications, generic and
alternate contact-resultant atlases, every reciprocal algebraic
boundary, the irreducible \(P_{16}\) pivot, and the full lower
singular-linear-part obstruction in both systems.
The final wrapper checks the doubled-nonbranch simple-fixed leaf,
including all three routed gcd mutations, the complete generic
contact chart, the fresh \(\Delta=0\) pivot, and the uniform constant
block independently in SymPy and PARI/GP.
