# Working theorem: the binary fixed-cubic line stratum

**Status.** Exact working theorem; independent hostile audit passed at
2026-07-25T06:55:00Z.  The orbit tree is specialization-safe and no
Keller-compatible leaf survives.  This has not been peer reviewed.

**Recorded.** 2026-07-25T06:10:20Z.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}
\]
have total degree four, where \(H_i\) is homogeneous of degree \(i\), and
suppose that source and target coordinates have put the top part in the form
\[
 H_4=h(p,q)(p,q,0)^T,\qquad 0\ne h\in\mathbb C[p,q]_3.                 \tag{1}
\]
This is the binary locus in taxonomy row
\((e,a,b,\delta,\nu)=(3,1,1,1,1)\).

### Theorem

If (1) is Keller, then \(F\) is a polynomial automorphism. Consequently no
degree-four Keller counterexample occurs in the binary fixed-cubic line
stratum.

Together with `WORKING_FIXED_CUBIC_LINE_ROW.md`, this closes the whole
fixed-cubic line row. The present note proves only the binary half and does
not alter the status of that other file.

## 2. The two top determinant identities

Write
\[
 P=ph,\quad Q=qh,\quad W=(H_3)_3,\quad
 U=(H_3)_1,\quad V=(H_3)_2,\quad T=(H_2)_3
\]
and
\[
 D=J_{p,q}(P,Q).
\]
Euler's identity gives
\[
 \det D=4h^2,\qquad
 \operatorname{adj}D=4hI_2-(p,q)^T\nabla h.                          \tag{2}
\]
For
\[
 {\cal J}(z)=L_0+zJH_2+z^2JH_3+z^3JH_4,\qquad
 E_j=[z^j]\det{\cal J}(z),
\]
the Keller condition is \(E_j=0\) for \(j>0\). Direct block expansion gives
\[
 E_8=4h^2W_r.                                                        \tag{3}
\]
Thus \(W\) is binary. Put
\[
 a=J(Q,W),\qquad b=J(P,W),\qquad c=J(P,Q)=4h^2.
\]
Then
\[
 \boxed{aU_r-bV_r+cT_r=0.}                                          \tag{4}
\]
Equivalently,
\[
 \nabla W\,\operatorname{adj}D\,(U_r,V_r)^T=4h^2T_r.                 \tag{5}
\]
These identities are checked both from the full \(3\times3\) determinant and
from the independent \(2\times2\) block formulas.

For later use, let \(B=J_{p,q}(U,V)\), let \(A\) be the \(p,q\) Jacobian of
the first two entries of \(H_2\), and put
\[
 u=(U_r,V_r)^T,\quad v=((H_2)_{1,r},(H_2)_{2,r})^T,\quad
 w=\nabla W,\quad t=\nabla T,\quad \tau=T_r.
\]
The next identity used in every elimination is
\[
\boxed{
E_6=4h^2(L_0)_{33}
 +\operatorname{tr}(\operatorname{adj}B\,D)\tau
 -w\operatorname{adj}D\,v
 -w\operatorname{adj}B\,u
 -t\operatorname{adj}D\,u.}                                        \tag{6}
\]
No coefficient is divided by a moduli parameter in the branch proof.

## 3. Three coordinate exits and their degree cost

The following elementary lemmas account for almost every nonzero tangent.
They are stated with degree bounds because the final exit uses the established
plane lower bound \(100\).

### 3.1 Quadratic component

If \(f=Q+\ell\) has degree at most two and \(df\) is nowhere zero, then \(f\)
is a coordinate with a coordinate map and inverse of degree at most two.
Indeed, if \(H\) is the Hessian of \(Q\) and \(b=d\ell\), the affine equation
\(Hx=-b\) is insoluble. Hence some \(v\in\ker H\) has \(b(v)\ne0\), so
\(D_vf\) is a nonzero constant and \(f\) is triangular in the \(v\)-direction.

This treats \(W=0\).

### 3.2 Pure-cube component

If
\[
 f=L^3+Q+\ell
\]
has nowhere-zero differential, then \(f\) is a coordinate with coordinate
map and inverse of degree at most three.

Let \(H\) be the Hessian of \(Q\), \(b=d\ell\), and \(K=\ker H\). If some
\(v\in K\cap\ker L\) has \(b(v)\ne0\), then again \(D_vf\) is a nonzero
constant. Otherwise \(b|_K=\lambda L|_K\). If \(L|_K\ne0\), choose
\(s\in\mathbb C\) with \(\lambda+3s^2=0\), solve
\[
 Hx=-b-3s^2L,
\]
and adjust by \(K\) so that \(L(x)=s\). This is a critical point. If
\(L|_K=0\), then \(b,L\in\operatorname{im}H\); solvability reduces to
\(s=A+Bs^2\), which always has a complex solution, again a critical point.
Thus a submersion must have the constant-derivative direction.

This treats every pure cube \(W=L^3\), including all aligned power strata.

### 3.3 Matched linear factor

Suppose
\[
 f=W(p,q)+T_0(p,q)+r\tau(p,q)+\ell(p,q,r),\qquad
 0\ne\tau\in\mathbb C[p,q]_1.                                      \tag{7}
\]
Then a nowhere-critical \(f\) is a coordinate. Choose affine coordinates
\((x,y)\) with the coefficient of \(r\) equal to \(y+c\), so
\[
 f=(y+c)r+g(x,y).
\]
At \(y=-c\), a zero of \(g_x(x,-c)\) would give a critical point after a
choice of \(r\). Hence \(g_x(x,-c)=\beta\in\mathbb C^\times\). Therefore
\[
 g=\beta x+s(y)+(y+c)k(x,y),\qquad \deg k\le2.
\]
After \(r'=r+k\), the coordinates \((f,y,r')\) have inverse degree at most
six. Thus composing a degree-four Keller map with this inverse has plane
degree at most \(24<100\).

In each of these exits, setting the coordinate component equal to the third
coordinate leaves a plane Keller map over a characteristic-zero function
field. The established plane degree bound makes it birational, and the
birational Keller theorem makes the original map an automorphism.

There is one additional routine exit. If every nonlinear homogeneous piece
is binary, apply \(L_0^{-1}\) on the target to obtain \(X+N(p,q)\), shear off
the third component, and use the degree-four plane result.

## 4. The root-order formula

Assume \(W\ne0\), and let \(\ell\) be a linear factor with
\[
 \ell^m\Vert h,\qquad \ell^n\Vert W.
\]
Then
\[
\boxed{
\operatorname{ord}_{\ell}\gcd(a,b,c)
=\min(2m,m+n-1).}                                                    \tag{8}
\]

To prove it, choose \(p=\ell\) and a transverse coordinate \(q\). Write
\[
 h=p^mH,\qquad W=p^nG
\]
with \(H,G\) units at \(p=0\). Homogeneity gives
\[
 H(0,q)=H_0q^{3-m},\qquad G(0,q)=G_0q^{3-n}.
\]
The leading coefficient of \(a=J(qh,W)\) at order \(m+n-1\) is
\[
 (3m-4n)H_0G_0q^{5-m-n},
\]
which is nonzero for \(1\le m\le3\), \(0\le n\le3\). Since
\(\operatorname{ord}_\ell(c)=2m\), (8) follows. The only cancellation in
the analogous leading term of \(b\) is \(m=n=3\); there \(a\) still has
order five, so the same formula holds. In particular \(n=0\) contributes
\(m-1\).

Define the common-root index
\[
 \rho(h,W)=
 \sum_{\ell\mid h}\min(2m_\ell,m_\ell+n_\ell-1)
 =\deg\gcd(a,b,c).                                                   \tag{9}
\]
This \(\rho\) is local notation and is not the \(\delta=1\) in the taxonomy
row label.

## 5. Exhaustive stabilizer quotient

There are three binary-cubic types:
\[
 h_s=pq(p-q),\qquad h_d=p^2q,\qquad h_t=p^3.                         \tag{10}
\]
Their projective stabilizers are respectively the finite \(S_3\) permuting
the three marked roots, the diagonal torus fixing the double and simple
roots, and the affine group \(u=q/p\mapsto\alpha u+\beta\).
Multiplying \(W\) by a nonzero scalar is harmless.

The following list is exhaustive modulo these stabilizers. Parameter
restrictions prevent a displayed residual factor from becoming another
marked factor.

| \(h\) | \(\rho\) | representatives for \(W\) |
|---|---:|---|
| \(h_s\) | 0 | no marked root of \(h_s\) divides \(W\) |
| \(h_s\) | 1 | exactly one marked root divides \(W\) simply |
| \(h_s\) | 2 | \(p^2(Ap+q)\), \(pq(Ap+q)\), \(A\ne0,-1\); also \(p^3\) |
| \(h_s\) | 3 | \(p^2q\), \(pq(p-q)\) |
| \(h_d\) | 1 | neither \(p\) nor \(q\) divides \(W\) |
| \(h_d\) | 2 | \(q(p^2+Bpq+q^2)\), \(p(p^2+Bpq+q^2)\) |
| \(h_d\) | 3 | \(q^2(p+q)\), \(pq(p+q)\), \(p^2(p+q)\); also \(q^3\) |
| \(h_d\) | 4 | \(pq^2\), \(p^2q\); also \(p^3\) |
| \(h_t\) | 2 | \(q^3+p^2q+\Lambda p^3\); \(p^3+q^3\); also \(q^3\) |
| \(h_t\) | 3 | \(pq(p-q)\), \(pq^2\) |
| \(h_t\) | 4 | \(p^2(p+q)\) |
| \(h_t\) | 5 | \(p^3\) |

For the first \(h_d,\rho=2\) family, \(B=0\) is the
\(\{2,0\}\)-splitting point. The values \(B=\pm2\) are pivot charts, not
omitted orbits. In the \(h_t,\rho=2\) family the pivot discriminant is
\[
 27\Lambda^2+4=0.
\]
The family \(p^3+q^3\) is the other \(\{2,0\}\) point. Pure cubes in the
last column of several rows exit by Section 3.2.

Exhaustivity is immediate from (8): record the multiplicity \(n_\ell\) of
each marked root in \(W\), then normalize the residual roots using the
displayed stabilizer. For \(h_t\), this is just the standard affine
classification of a cubic, quadratic, or linear polynomial in \(u=q/p\).
For \(h_d\), diagonal scaling normalizes the two endpoint coefficients of
the residual quadratic. For \(h_s\), only the finite \(S_3\) quotient
remains, which is why the parameters are retained.

## 6. Raw \(E_7\) ranks and converse parameterizations

Split \(u=(U_r,V_r,T_r)\) by powers of \(r\). Exact coefficient extraction
from (4) gives the following nullities:

| common-root stratum | splitting | \((r^2,r^1,r^0)\) nullities | corresponding ranks |
|---|---|---:|---:|
| \(\rho=0\) | none | \((0,0,0)\) | \((2,5,8)\) |
| \(\rho=1\) | \(\{1,0\}\) | \((0,0,1)\) | \((2,5,7)\) |
| \(\rho=2\), generic | \(\{1,1\}\) | \((0,0,2)\) | \((2,5,6)\) |
| \(\rho=2\), special | \(\{2,0\}\) | \((0,1,2)\) | \((2,4,6)\) |
| \(\rho=3\) | \(\{2,1\}\) | \((0,1,3)\) | \((2,4,5)\) |
| \(\rho=4\) | \(\{2,2\}\) | \((0,2,4)\) | \((2,3,4)\) |

The ranks are for matrices with respectively \(2,5,8\) unknown
coefficients. The fail-closed verifier prints an exact nullspace basis for
every representative in Section 5. Thus the displayed parameterizations
are converses: every solution of \(E_7\), including every specialization,
is a unique linear combination of the printed basis after the indicated
finite pivot change.

## 7. Specialization-safe \(E_6\) tree

The matched-factor lemma means that an \(r^0\) tangent with \(T_r\ne0\)
is already an automorphism exit. It remains only to inspect the kernel of
the normal projection and the possible \(r\)-multipliers.

### 7.1 \(\rho\le2\)

For \(\rho=0\), (4) has no tangent. For the split \(\rho=1\) stratum, its
unique nonzero tangent has nonzero normal part. In the double-root
\(\rho=1\) stratum, write
\[
 W=a_0p^3+a_1p^2q+a_2pq^2+a_3q^3,\qquad a_0a_3\ne0.
\]
The possible zero-normal tangent is killed by the branch-safe \(E_6\)
pairing
\[
 162a_3^3\kappa^2.
\]

In every generic \(\{1,1\}\) stratum the normal map is injective. At the
three pivot charts \(B=\pm2\) and \(27\Lambda^2+4=0\), the extra
zero-normal vector is inconsistent at \(E_6\); normalized exact
coefficients include respectively
\[
 \frac92,\qquad \frac{15}{2},\qquad 4.
\]
For the two \(\{2,0\}\) orbits, the \(r^3\)-coefficient of \(E_6\) kills
the \(r\)-multiplier. Every remaining nonzero \(r^0\) multiple has
nonzero normal part.

Raw \(E_6\) ranks in this range are:

| cases | matrix shape, rank |
|---|---|
| split/double \(\rho=1\) | \((12,24),9\); \((13,24),9\) |
| \(s2a,s2b,d2q,d2p,t2g\) | \((13,24),9\), \((11,24),9\), \((12,24),9\), \((12,24),9\), \((13,24),9\) |
| all three pivot charts | rank \(9\) |
| \(d2q\) and \(t2\), full \(\{2,0\}\) | \((19,24),10\) |
| same after the \(r\)-multiplier is zero | \((12,24),9\), \((13,24),9\) |

### 7.2 \(\rho=3\)

For all seven representatives, \([r^3]E_6\) is a nonzero scalar multiple
of the square of the sole \(r\)-multiplier, so that multiplier is zero.
The kernel of the normal map is one-dimensional except for
\[
 (h,W)=(p^3,pq^2),
\]
where it is two-dimensional. Exact \(E_6\) incompatibility kills the
one-dimensional kernel in the first six cases. In the exceptional case it
kills the second vector and leaves only
\[
 N=\left(\frac85p^2,pq,0\right).                                    \tag{11}
\]
A complete \(E_6\) solve has shape \((8,24)\), rank \(8\), and \(E_5\)
contains the constant
\[
 \boxed{\frac{24}{25}}.                                              \tag{12}
\]

The full \(E_6\) shapes/ranks for
\[
s3a,s3b,d3q,d3pq,d3p,t3s,t3d
\]
are respectively
\[
(20,24)/10,\ (18,24)/10,\ (22,24)/10,\ (18,24)/10,\
(16,24)/10,\ (20,24)/10,\ (17,24)/10.
\]
After setting the \(r\)-multiplier to zero they are
\[
(12,24)/9,\ (11,24)/9,\ (13,24)/9,\ (11,24)/9,\
(10,24)/8,\ (12,24)/9,\ (12,24)/9.
\]

### 7.3 \(\rho=4\)

Use the names
\[
d4a=(p^2q,pq^2),\quad d4b=(p^2q,p^2q),\quad
t4=(p^3,p^2(p+q)).
\]
Their full \(E_6\) shapes/ranks are
\[
(20,24)/9,\qquad(14,24)/9,\qquad(16,24)/9,
\]
and their \(r^0\) shapes/ranks are
\[
(12,24)/9,\qquad(9,24)/8,\qquad(10,24)/8.
\]

For \(d4a\), \(E_6\) kills both \(r\)-multipliers. On the zero-normal
kernel it kills the second vector; the normalized first vector
\[
\left(\frac52p^2,pq,0\right)
\]
has an \(E_6\) solve of shape \((7,24)\), rank \(7\), followed by the
\(E_5\) constant
\[
\boxed{15}.                                                         \tag{13}
\]

For \(d4b\), let the \(r\)-multiplier coefficients be \(g_0,g_1\). Exact
compatibility gives
\[
3g_0^2-8g_0g_1+8g_1^2=0.                                           \tag{14}
\]
If they vanish, the only zero-normal survivor is
\[
\left(-\frac12p^2,pq,0\right),
\]
and \(E_5\) contains \(3/2\). If they do not vanish, then \(g_1\ne0\).
The source scaling \(r\mapsto c r\) acts on the nonzero multiplier by a
nonzero square and merely rescales the \(r^0\) parameters.  Over
\(\mathbb C\), choose \(c^2\) so that the transformed \(g_1\) is one;
this is a coordinate normalization, not an appeal to homogeneity of
\(E_6\).  Put \(\gamma=g_0\), and define
\[
R_1=\left(-\frac12p,q,0\right),\qquad R_2=(2p,0,1),\qquad
\kappa=1-\frac38\gamma.
\]
The complete compatible derivative is
\[
u=r(\gamma R_1+R_2)+(\alpha p+\beta q)(R_1+\kappa R_2),              \tag{15}
\]
where
\[
3\gamma^2-8\gamma+8=0.
\]
The specialized \(E_6\) matrix has shape \((14,24)\), rank \(8\), and
the printed row reduction parameterizes every solution. Substitution in
\(E_5\) gives
\[
-\frac58\alpha(\gamma-4),\qquad
-\frac58\beta(\gamma-4),\qquad
\boxed{\frac{\gamma+2}{6}}.                                         \tag{16}
\]
The boxed element is nonzero in
\(\mathbb Q[\gamma]/(3\gamma^2-8\gamma+8)\), so this branch is empty.

For \(t4\), \(E_6\) first forces \(g_0=0\). If \(g_1\ne0\), use the same
source scaling to normalize it to one. With
\[
\begin{aligned}
R_2&=(0,p,1),\\
N_1&=(4p^2,-p(3p-q),0),\\
N_3&=(0,p^2,p),\\
N_4&=(-4p^2,3p^2,q),
\end{aligned}
\]
the complete compatible branch is
\[
u=rR_2+\alpha N_1+\beta N_3+\alpha N_4.                              \tag{17}
\]
Its \(E_6\) matrix has shape \((9,24)\), rank \(7\). The exact \(E_5\)
row reduction followed by three \(E_4\) pivots gives
\[
\begin{aligned}
(L_0)_{12}&=2a_5(L_0)_{32},&
(L_0)_{22}&=2a_{11}(L_0)_{32},\\
(L_0)_{13}&=2a_5(L_0)_{33},&
(L_0)_{23}&=2a_{11}(L_0)_{33}.
\end{aligned}
\]
Thus columns two and three of \(L_0\) are proportional and
\(\det L_0=0\), impossible for a Keller map.

If the \(t4\) multipliers vanish, its sole zero-normal survivor \(N_1\)
has \(E_5\) constant \(-12\).

## 8. The lower-syzygy audit

After the whole \(E_7\) tangent vanishes, (6) reduces to the same primitive
syzygy problem one degree lower for
\[
\big((H_2)_{1,r},(H_2)_{2,r},(L_0)_{33}\big).
\]
A nonzero normal constant \((L_0)_{33}\) makes the third component
triangular and exits by Section 3. The exact \(E_7\) bases show that there
are precisely four zero-normal lower leaves:

| \((h,W)\) | lower vector | solved identity | contradiction |
|---|---|---|---:|
| \((p^3,pq^2)\) | \((\frac85p,q,0)\) | \(E_5\to E_4\) | \(-24/5\) |
| \((p^2q,pq^2)\) | \((\frac52p,q,0)\) | \(E_5\to E_4\) | \(-15/2\) |
| \((p^2q,p^2q)\) | \((-\frac12p,q,0)\) | \(E_5\to E_4\) | \(3/2\) |
| \((p^3,p^2(p+q))\) | \((4p,-3p+q,0)\) | \(E_5\to E_4\) | \(-12\) |

The corresponding \(E_5\) matrix shapes/ranks are
\[
(6,19)/6,\qquad(5,19)/5,\qquad(5,19)/5,\qquad(5,19)/5.
\]
This table includes the \(p^3,pq^2\) leaf found during the hostile audit;
omitting it would leave a genuine gap.

When the lower tangent also vanishes, every nonlinear piece is binary and
the plane-plus-shear exit in Section 3 applies.

## 9. Completion and converse statement

Every orbit in Section 5 follows exactly one path:

1. \(W=0\) or \(W\) is a pure cube: coordinate exit.
2. A nonzero \(r^0\) tangent has nonzero normal part: matched-factor exit.
3. A zero-normal tangent: one of the exact \(E_6/E_5\) contradictions.
4. A nonzero \(r\)-multiplier: killed at \(E_6\), or one of the two complete
   algebraic branches (15), (17), both contradictory.
5. The \(E_7\) tangent vanishes: a triangular lower exit, one of the four
   lower constants, or the binary plane-plus-shear exit.

The nullspace bases, ranks, and simultaneous substitutions in the verifier
are converse parameterizations, not candidate-only ansätze. The
discriminant and algebraic branches are checked in their quotient fields,
so no inference depends on dividing by a parameter that might vanish.
No Keller-compatible unresolved leaf survives.

## 10. Exact artifacts and reproduction

The audited working package consists of:

- `WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md`
- `verify_binary_fixed_cubic_complete.py`
- `verify_binary_fixed_cubic_complete_pari.gp`
- `audit_binary_fixed_cubic_hostile/`

Run

```text
/usr/bin/python3 -u verify_binary_fixed_cubic_complete.py
gp -q verify_binary_fixed_cubic_complete_pari.gp
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_orbits_lower_exact.py
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_exceptional_branches_exact.py
./audit_binary_fixed_cubic_hostile/test_fail_closed.sh
```

The promoted SymPy reconstruction reports the raw \(E_7\) bases,
branch-safe compatibility certificates, exceptional constants, and
algebraic \(r\)-branches used in its proof path.  The PARI/GP
reconstruction separately expands the determinants and checks the four
residual \(E_7\) constants, four lower constants, and (15)--(17).  The
two clean-room audit scripts assert every claimed raw \(E_6\) rank,
specialization divisor, zero-normal kernel, lower leaf, and the complete
\(t4\) converse row reduction.  The fault suite rejects optimized Python
and injected false identities.

## 11. Research log

- **2026-07-25T04:55Z:** derived (3)--(6) and the local formula (8).
- **2026-07-25T05:12Z:** completed the stabilizer quotient and raw
  Hilbert--Burch splitting table.
- **2026-07-25T05:34Z:** isolated the pure-cube and matched-factor coordinate
  exits, reducing the computation to zero-normal kernels and
  \(r\)-multipliers.
- **2026-07-25T05:52Z:** closed all \(\rho=2,3\) residual kernels.
- **2026-07-25T06:02Z:** closed both \(\rho=4\) algebraic
  \(r\)-multiplier branches.
- **2026-07-25T06:06Z:** hostile lower-syzygy audit found the additional
  \((p^3,pq^2)\) lower leaf; exact \(E_4\) constant \(-24/5\) closed it.
- **2026-07-25T06:10Z:** both clean fail-closed reconstructions passed; no
  leaf remained.
- **2026-07-25T06:55Z:** hostile audit independently reconstructed every
  orbit, pivot, raw rank, exceptional branch, lower leaf, coordinate exit,
  and the \(t4\) converse.  Verdict: PASS after the executable guard and
  two documentation clarifications.
