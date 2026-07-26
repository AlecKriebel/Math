# Hostile clean-room audit of `Q2-E2-A2-B1-D1-N1`

## Verdict

**PASS, with a mandatory scope correction.**

The frozen row is excluded in the sense relevant to the Keller
counterexample program:

\[
\boxed{\text{every Keller map in the row is a polynomial automorphism}.}
\]

There is no omitted frozen coefficient pivot, intrinsic target chart,
all-vertical incidence, marked-pair type, companion point, or projective
boundary in the route reconstructed below.  The two previously unattached
outer `CO` strata have complete, division-free \(E_7/E_6/E_5\) exclusions.
Of the 45 frozen coefficient pivots, exactly 30 can reach a rank-two row;
`C_30`--`C_44` are empty here because their guards leave only the third
target component of \(H_4\) nonzero.

The stronger sentence

\[
\text{“no map in the whole row has nonzero constant Jacobian”}
\]

is **not** certified and must not be used.  In each of the three `C0`
strata, \(G=(H_3)_3=0\), and the valid terminal is the banked
quadratic-component theorem: Keller implies automorphism.  It is not a
contradiction to \(\det JF\in\mathbb C^\times\).  Thus a bridge or closure
note that states blanket nonexistence while including `C0` fails this audit
as written, even though the frozen-row exclusion remains valid after
weakening the conclusion.

No proposed bridge, root `explore_*` file,
`marked_h_distinct/co_closure/`, or
`marked_h_distinct/endpoint_closure/` was consulted.  The reconstruction
uses only the frozen global taxonomy, the frozen marked-companion taxonomy
and certificate, the pre-freeze verticality/top-obstruction and
marked-equal packages, and the permitted `quartic_survivor_search`
`CTAU`/endpoint package.

## 1. Exact theorem being attached

Write
\[
F=F_0+LX+H_2+H_3+H_4,\qquad
E_j=[w^j]\det\!\left(L+wJH_2+w^2JH_3+w^3JH_4\right),
\]
with
\[
L=(\ell_{ij})=
\begin{pmatrix}
\ell_0&\ell_1&\ell_2\\
\ell_3&\ell_4&\ell_5\\
\ell_6&\ell_7&\ell_8
\end{pmatrix}.
\]
For a Keller map,
\[
E_9=\cdots=E_1=0,\qquad \det L\ne0.                  \tag{1}
\]

The bridge proves the following disjunction for every point of the frozen
row.

1. Its cubic normal component vanishes, so the third component of \(F\)
   has degree at most two and the quadratic-component theorem makes \(F\)
   an automorphism.
2. Its cubic normal component is nonzero.  It enters one of the audited
   marked-equal packages or one of the ten nonzero marked-distinct strata,
   where the lower identities force \(\det L=0\), contradicting (1).

This is exactly the exclusion needed for a counterexample row and no
stronger.

## 2. Frozen 45-pivot route

The following is the explicit route from the frozen coefficient partition.
On `C_i`, every preceding coefficient is zero and the displayed coefficient
is nonzero.  For `C_0`--`C_29`, extract the intrinsic gcd and apply the
ordered intrinsic-minor router in Section 3.  For `C_30`--`C_44`, the guard
forces \(H_{4,1}=H_{4,2}=0\), so \(\operatorname{rank}JH_4\le1\); those
pivots have empty intersection with this rank-two row.

| pivot | first nonzero coefficient | forced nonzero target row | next route |
|---|---|---:|---|
| `C_0` | \([H_{4,1}]_{x^4}\) | 1 | `M_0,...,M_44` |
| `C_1` | \([H_{4,1}]_{x^3y}\) | 1 | `M_0,...,M_44` |
| `C_2` | \([H_{4,1}]_{x^3z}\) | 1 | `M_0,...,M_44` |
| `C_3` | \([H_{4,1}]_{x^2y^2}\) | 1 | `M_0,...,M_44` |
| `C_4` | \([H_{4,1}]_{x^2yz}\) | 1 | `M_0,...,M_44` |
| `C_5` | \([H_{4,1}]_{x^2z^2}\) | 1 | `M_0,...,M_44` |
| `C_6` | \([H_{4,1}]_{xy^3}\) | 1 | `M_0,...,M_44` |
| `C_7` | \([H_{4,1}]_{xy^2z}\) | 1 | `M_0,...,M_44` |
| `C_8` | \([H_{4,1}]_{xyz^2}\) | 1 | `M_0,...,M_44` |
| `C_9` | \([H_{4,1}]_{xz^3}\) | 1 | `M_0,...,M_44` |
| `C_10` | \([H_{4,1}]_{y^4}\) | 1 | `M_0,...,M_44` |
| `C_11` | \([H_{4,1}]_{y^3z}\) | 1 | `M_0,...,M_44` |
| `C_12` | \([H_{4,1}]_{y^2z^2}\) | 1 | `M_0,...,M_44` |
| `C_13` | \([H_{4,1}]_{yz^3}\) | 1 | `M_0,...,M_44` |
| `C_14` | \([H_{4,1}]_{z^4}\) | 1 | `M_0,...,M_44` |
| `C_15` | \([H_{4,2}]_{x^4}\) | 2 | `M_0,...,M_44` |
| `C_16` | \([H_{4,2}]_{x^3y}\) | 2 | `M_0,...,M_44` |
| `C_17` | \([H_{4,2}]_{x^3z}\) | 2 | `M_0,...,M_44` |
| `C_18` | \([H_{4,2}]_{x^2y^2}\) | 2 | `M_0,...,M_44` |
| `C_19` | \([H_{4,2}]_{x^2yz}\) | 2 | `M_0,...,M_44` |
| `C_20` | \([H_{4,2}]_{x^2z^2}\) | 2 | `M_0,...,M_44` |
| `C_21` | \([H_{4,2}]_{xy^3}\) | 2 | `M_0,...,M_44` |
| `C_22` | \([H_{4,2}]_{xy^2z}\) | 2 | `M_0,...,M_44` |
| `C_23` | \([H_{4,2}]_{xyz^2}\) | 2 | `M_0,...,M_44` |
| `C_24` | \([H_{4,2}]_{xz^3}\) | 2 | `M_0,...,M_44` |
| `C_25` | \([H_{4,2}]_{y^4}\) | 2 | `M_0,...,M_44` |
| `C_26` | \([H_{4,2}]_{y^3z}\) | 2 | `M_0,...,M_44` |
| `C_27` | \([H_{4,2}]_{y^2z^2}\) | 2 | `M_0,...,M_44` |
| `C_28` | \([H_{4,2}]_{yz^3}\) | 2 | `M_0,...,M_44` |
| `C_29` | \([H_{4,2}]_{z^4}\) | 2 | `M_0,...,M_44` |
| `C_30` | \([H_{4,3}]_{x^4}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_31` | \([H_{4,3}]_{x^3y}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_32` | \([H_{4,3}]_{x^3z}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_33` | \([H_{4,3}]_{x^2y^2}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_34` | \([H_{4,3}]_{x^2yz}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_35` | \([H_{4,3}]_{x^2z^2}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_36` | \([H_{4,3}]_{xy^3}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_37` | \([H_{4,3}]_{xy^2z}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_38` | \([H_{4,3}]_{xyz^2}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_39` | \([H_{4,3}]_{xz^3}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_40` | \([H_{4,3}]_{y^4}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_41` | \([H_{4,3}]_{y^3z}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_42` | \([H_{4,3}]_{y^2z^2}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_43` | \([H_{4,3}]_{yz^3}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |
| `C_44` | \([H_{4,3}]_{z^4}\) | 3 | empty: \(\operatorname{rank}JH_4\le1\) |

The 45 guards are disjoint and cover every nonzero \(H_4\).  Their
intersection with this row is the first 30 guards only.  Indeed,
`C_30`--`C_44` make the first two target rows identically zero and the
third nonzero, so the Jacobian has at most one nonzero row.  Conversely,
the first 30 guards leave at least two target components available and
therefore proceed to the intrinsic rank-two test.  After gcd extraction,
the nonzero-row assertion is safe: if \(H_{4,j}=h g_j\ne0\) in the
polynomial domain, then \(g_j\ne0\).

## 3. Intrinsic extraction and the second 45-chart router

On any of the 30 coefficient pivots not already empty in the target row,
exact gcd extraction gives
\[
h=\gcd(H_{4,1},H_{4,2},H_{4,3}),\qquad
H_4=h(g_1,g_2,g_3),\qquad \deg h=\deg g_i=2.       \tag{2}
\]
Write the coefficient matrix of the primitive triple in the order
\[
(x^2,xy,xz,y^2,yz,z^2)
\]
as \(B=(b_{ij})\in\operatorname{Mat}_{3\times6}\).  The frozen tuple
\((2,2,2,1,1,1)\) says precisely that
\[
\operatorname{rank}B=2,\quad
\langle g_1,g_2,g_3\rangle=\langle p,q\rangle,
\quad \gcd(p,q)=1,
\]
and that \(\mathbb C(p/q)\) is the relative closure/minimal pencil field.

For target rows \(r<s\) and quadratic columns \(\alpha<\beta\), put
\[
\Delta_{rs;\alpha\beta}
=b_{r\alpha}b_{s\beta}-b_{r\beta}b_{s\alpha}.       \tag{3}
\]
Order the 45 minors as follows.

| primitive target rows | ordered guards |
|---|---|
| 1,2 | `M_0`=\(\Delta_{12;x^2,xy}\), `M_1`=\(\Delta_{12;x^2,xz}\), `M_2`=\(\Delta_{12;x^2,y^2}\), `M_3`=\(\Delta_{12;x^2,yz}\), `M_4`=\(\Delta_{12;x^2,z^2}\), `M_5`=\(\Delta_{12;xy,xz}\), `M_6`=\(\Delta_{12;xy,y^2}\), `M_7`=\(\Delta_{12;xy,yz}\), `M_8`=\(\Delta_{12;xy,z^2}\), `M_9`=\(\Delta_{12;xz,y^2}\), `M_10`=\(\Delta_{12;xz,yz}\), `M_11`=\(\Delta_{12;xz,z^2}\), `M_12`=\(\Delta_{12;y^2,yz}\), `M_13`=\(\Delta_{12;y^2,z^2}\), `M_14`=\(\Delta_{12;yz,z^2}\) |
| 1,3 | `M_15`=\(\Delta_{13;x^2,xy}\), `M_16`=\(\Delta_{13;x^2,xz}\), `M_17`=\(\Delta_{13;x^2,y^2}\), `M_18`=\(\Delta_{13;x^2,yz}\), `M_19`=\(\Delta_{13;x^2,z^2}\), `M_20`=\(\Delta_{13;xy,xz}\), `M_21`=\(\Delta_{13;xy,y^2}\), `M_22`=\(\Delta_{13;xy,yz}\), `M_23`=\(\Delta_{13;xy,z^2}\), `M_24`=\(\Delta_{13;xz,y^2}\), `M_25`=\(\Delta_{13;xz,yz}\), `M_26`=\(\Delta_{13;xz,z^2}\), `M_27`=\(\Delta_{13;y^2,yz}\), `M_28`=\(\Delta_{13;y^2,z^2}\), `M_29`=\(\Delta_{13;yz,z^2}\) |
| 2,3 | `M_30`=\(\Delta_{23;x^2,xy}\), `M_31`=\(\Delta_{23;x^2,xz}\), `M_32`=\(\Delta_{23;x^2,y^2}\), `M_33`=\(\Delta_{23;x^2,yz}\), `M_34`=\(\Delta_{23;x^2,z^2}\), `M_35`=\(\Delta_{23;xy,xz}\), `M_36`=\(\Delta_{23;xy,y^2}\), `M_37`=\(\Delta_{23;xy,yz}\), `M_38`=\(\Delta_{23;xy,z^2}\), `M_39`=\(\Delta_{23;xz,y^2}\), `M_40`=\(\Delta_{23;xz,yz}\), `M_41`=\(\Delta_{23;xz,z^2}\), `M_42`=\(\Delta_{23;y^2,yz}\), `M_43`=\(\Delta_{23;y^2,z^2}\), `M_44`=\(\Delta_{23;yz,z^2}\) |

The guard for `M_j` is
\[
M_0=\cdots=M_{j-1}=0,\qquad M_j\ne0.                \tag{4}
\]
These guards are disjoint.  They cover because rank \(B=2\).  No rank-two
point is localized at a zero minor.

For the selected rows \(r,s\), let \(t\) be the remaining row and
\(\Delta=\Delta_{rs;\alpha\beta}\).  Define
\[
\lambda_N=b_{t\alpha}b_{s\beta}-b_{t\beta}b_{s\alpha},
\qquad
\mu_N=b_{r\alpha}b_{t\beta}-b_{r\beta}b_{t\alpha}.   \tag{5}
\]
Rank two gives the division-free relation
\[
\Delta g_t-\lambda_Ng_r-\mu_Ng_s=0.                 \tag{6}
\]
The target operation with rows
\[
g_r,\qquad g_s,\qquad
\Delta g_t-\lambda_Ng_r-\mu_Ng_s
\]
has determinant \(\pm\Delta\ne0\).  Hence it is legal and gives
\[
H_4=(hp,hq,0),\qquad (p,q)=(g_r,g_s),                \tag{7}
\]
without using an invalid localization.  Division by \(\Delta\) is optional;
equation (6) is the cleared calculation.

## 4. Ordered intrinsic top route

With
\[
P=hp,\qquad Q=hq,\qquad G=(H_3)_3,
\]
the weight-eight identity is
\[
E_8=\operatorname{Jac}(P,Q,G)=0.                     \tag{8}
\]
The complete ordered route is:

| ordered guard | conclusion | terminal |
|---|---|---|
| \(H_4=0\) | degree at most three | outside \(\mathcal K_4\) |
| \(H_4\ne0,\ \operatorname{rank}JH_4=1\) | frozen row `Q1` | route out |
| rank two, recomputed tuple not \((2,2,2,1,1,1)\) | another frozen row | route out |
| target tuple and some prime of \(h\) horizontal | \(G=0\) by \(4v_f(G)=3v_f(h)\) | automorphism exit |
| all primes vertical; genuine \(h=\ell^2,p=\ell m,\ m\not\sim\ell\) | same-fibre equation \(4N=6\) | \(G=0\), automorphism exit |
| all primes vertical; distinct vertical split members | same-fibre equation \(4N=3\), or nonminimal square ratio | \(G=0\), automorphism exit |
| \(p=h\), pencil has no double line | divisor parity contradiction for \(G\ne0\) | \(G=0\), automorphism exit |
| \(p=h\), unique \(s=\ell^2\), \(G=0\) | third component has degree at most two | automorphism exit |
| \(p=h\), unique \(s=\ell^2\), \(G\ne0\) | \(G=\ell r,\ [r]\in\mathbb P\langle h,s\rangle\) | marked router |

These rows are ordered and disjoint.  The all-vertical shapes exhaust
irreducible \(h\), square \(h\), and split reduced \(h\).  The unique
double-line statement follows because two different double lines would
make the pencil a degree-two composition of a linear pencil, contradicting
minimality.

If \(h=s\), the two canonical pencils and their complete nonzero companion
orbits are:

| pencil | zero companion | triple companion | mixed companion |
|---|---|---|---|
| \(\langle x^2,yz\rangle\) | automorphism exit | \(G=x^3\), audited `ranktwo_triple` | \(G=xyz\), audited mixed package |
| \(\langle x^2,y^2+xz\rangle\) | automorphism exit | \(G=x^3\), audited `rankone_triple` | \(G=x(y^2+xz)\), audited mixed package |

Thus the marked-equal branch is exhaustive and closed.  It is not silently
identified with the marked-distinct branch.

## 5. Disjoint exhaustive marked-distinct table

For \(h\ne s\), use
\[
r=uh+vs,\qquad [u:v]\in\mathbb P^1.                  \tag{9}
\]
The complete route, including the zero affine cone point, is:

| marked pair | suffix | exact guard | terminal evidence |
|---|---|---|---|
| `P21-HR2` | `C0` | \(G=0\) | automorphism exit |
| `P21-HR2` | `CH` | \(G\ne0,\ v=0\) | endpoint \(E_5\) |
| `P21-HR2` | `CS` | \(G\ne0,\ u=0\) | endpoint \(E_5\) |
| `P21-HR2` | `CO` | \(G\ne0,\ uv\ne0\) | new CO \(E_5\) below |
| `P21-HSM` | `C0` | \(G=0\) | automorphism exit |
| `P21-HSM` | `CH` | \(G\ne0,\ v=0\) | endpoint \(E_5\) |
| `P21-HSM` | `CT` | \(G\ne0,\ u+v=0\) | finite-\(k\) \(E_5\) |
| `P21-HSM` | `CS` | \(G\ne0,\ u=0\) | endpoint \(E_5\) |
| `P21-HSM` | `CTAU` | \(G\ne0,\ uv(u+v)\ne0\) | uniform finite-\(k\) \(E_5\) |
| `P3-HSM` | `C0` | \(G=0\) | automorphism exit |
| `P3-HSM` | `CH` | \(G\ne0,\ v=0\) | endpoint \(E_4\) |
| `P3-HSM` | `CS` | \(G\ne0,\ u=0\) | endpoint \(E_5\) |
| `P3-HSM` | `CO` | \(G\ne0,\ uv\ne0\) | new CO \(E_5\) below |

The exact count is
\[
\boxed{3\ \mathrm{C0}+6\ \mathrm{CH/CS}
+1\ \mathrm{CT}+1\ \mathrm{CTAU}+2\ \mathrm{CO}=13}. \tag{10}
\]

For either outer torus quotient, \(v=0\), \(u=0\), and \(uv\ne0\) are
disjoint and cover \(\mathbb P^1\).  In the middle quotient, \(v=0\),
\(u=0\), \(u+v=0\), and \(uv(u+v)\ne0\) are disjoint and cover
\(\mathbb P^1\).  Hence the projective points at zero, minus one, and
infinity are not swallowed by an affine calculation.

## 6. Finite middle chart and its boundaries

On \(u=1\), put \(k=v/u\).  Then
\[
h=x^2+yz,\quad s=x^2,\quad
r=h+ks,\quad
\begin{aligned}
H_4&=(h^2,hx^2,0),\\
H_3&=(Ax^3,Bx^3,x(h+kx^2)),\\
(H_2)_3&=Tx^2.
\end{aligned}                                          \tag{11}
\]
The boundary correspondence is
\[
k=0:\mathrm{CH},\qquad
k=-1:\mathrm{CT},\qquad
k=\infty:\mathrm{CS}.                                  \tag{12}
\]
Thus the permitted finite calculation applies exactly to `CT` and `CTAU`
when \(k\ne0\); it does not claim either missing endpoint.

Its released \(E_7\) chart pivots have extra factors
\[
q=9k^2+6k-1,\qquad \rho=3k-1,
\]
and the exact identity
\[
\frac12q-\frac32(k+1)\rho=1                            \tag{13}
\]
proves that the charts cover every finite \(k\).  The subsequent \(E_6\)
chain is division-free except for the declared guard \(k\ne0\):
\[
\begin{aligned}
b_1&=2\ell_7,&a_1&=-12k\ell_7,&-36k^2\ell_7&=0,\\
b_2&=2\ell_8,&a_2&=-12k\ell_8,& 36k^2\ell_8&=0,
\end{aligned}                                          \tag{14}
\]
together with
\[
a_3=a_5=b_3=b_5=0.
\]
Hence
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0.       \tag{15}
\]
The decisive \(E_5\) coefficients are
\[
\begin{array}{c|l}
x^4y&(3k-1)\ell_1-(6k+2)\ell_4\\
x^4z&-(3k-1)\ell_2+(6k+2)\ell_5\\
x^2y^2z&-\ell_1-(6k+4)\ell_4\\
x^2yz^2&\ell_2+(6k+4)\ell_5\\
y^3z^2&-2\ell_4\\
y^2z^3&2\ell_5 .
\end{array}                                             \tag{16}
\]
They force
\(\ell_1=\ell_2=\ell_4=\ell_5=0\).  Together with (15), the last two
columns of \(L\) vanish.  This covers all `CTAU` values and `CT`, while
`CH` and `CS` remain in the endpoint package exactly as required.

## 7. Six endpoint attachment

The permitted endpoint package supplies complete \(E_7\) normal forms and
constant \(E_6\) pivots.  The following concrete lower equations are enough
to check that every radical component is attached.

### 7.1 The two `P21-CS` endpoints

For \(h=yz\) and \(h=x^2+yz\),
\[
H_3=(Axyz,Bxyz,x^3),\qquad (H_2)_3=Tyz.
\]
The \(E_6\) solve gives
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0.
\]
Then
\[
[x^2y^2z]E_5=-6\ell_4,\qquad
[x^2yz^2]E_5=6\ell_5,
\]
and the \(x^4y,x^4z\) coefficients force
\(\ell_1=\ell_2=0\).  Thus \(\det L=0\).

### 7.2 The two `P21-CH` endpoints

For both rank-two marked pairs,
\[
\begin{aligned}
U&=Ax^3-2Cyh-2Dzh,\\
V&=Bx^3+Cx^2y+Dx^2z,\qquad
W=Tx^2,\qquad R=xh.
\end{aligned}
\]
The \(E_6\) radical is the union
\[
A=0\quad\text{or}\quad C=D=0.
\]
On \(A=0\),
\[
[x^2y^3]E_5=-12C^3,\qquad
[x^2z^3]E_5=12D^3,
\]
so \(C=D=0\).  On that component,
\[
\ell_4=\ell_5=0,\qquad
\ell_1=(6B-8T)\ell_7,\qquad
\ell_2=(6B-8T)\ell_8,
\]
which makes the relevant rows proportional and gives \(\det L=0\).

### 7.3 `P3-CS`

With \(h=y^2+xz\), the \(E_6\) radical has \(D=0\) and
\[
\begin{aligned}
U&=2Azh,\\
V&=Ax^2z+Bxh+\frac23Cyh,\\
W&=Cxy+Sh,\qquad R=x^3.
\end{aligned}
\]
The coefficient
\[
[x^2z^3]E_5=-\frac29C^3
\]
forces \(C=0\).  The remaining equations give
\[
\ell_1=\ell_4=\ell_7=0,\qquad
\ell_2=Aa_3,\qquad \ell_5=Ab_3,
\]
so the second column of \(L\) vanishes.

### 7.4 `P3-CH`

On the \(A=0\) radical component, let \(q_0=a_0-9B^2\).  The equations
\[
Cq_0=0,\qquad
Dq_0+6BC^2=0,\qquad
C(6BD-C^2)=0
\]
force \(C=0\); the remaining three-term chain gives
\[
D\ell_8=0,\qquad D^3=0,
\]
and hence \(D=0\).

On the \(C=D=0\) component,
\[
\begin{gathered}
A\ell_7=A\ell_8=0,\qquad
\ell_1=6B\ell_7,\qquad
\ell_2=6B\ell_8+Ta_3,\\
\ell_4=0,\qquad \ell_5=Tb_3,
\end{gathered}
\]
and
\[
\det L
=T\ell_7(6Bb_3\ell_6+a_3\ell_3-b_3\ell_0).            \tag{17}
\]
If \(A\ne0\), (17) vanishes already at \(E_5\).  If \(A=0\), the genuine
through-\(E_5\) survivor is killed by
\[
[xyz^2]E_4=-8\ell_8^2,\qquad
[x^2yz]E_4=-4\bigl(2(b_0-\ell_6)\ell_8-\ell_7^2\bigr).
\]
Thus \(\ell_8=\ell_7=0\) and again \(\det L=0\).  This preserves the
package's sharp warning that this endpoint does not die uniformly at
\(E_5\).

## 8. Independent derivation of `P21-HR2-CO`

Put
\[
h=yz,\quad s=x^2,\quad
P=h^2,\quad Q=h s,\quad R=x(h+s).
\]
Let \(U=(H_3)_1,V=(H_3)_2,W=(H_2)_3\) be general forms of degrees
\(3,3,2\).  The raw \(E_7\) coefficient map has size \(36\times26\),
rank \(18\), and nullity \(8\).  One exact kernel basis is
\[
\begin{array}{c|ccc}
&U&V&W\\ \hline
1&x^3&0&0\\
2&xh&0&0\\
3&0&x^3&0\\
4&0&xh&0\\
5&0&0&x^2\\
6&2y^2z&x^2y&xy\\
7&2yz^2&x^2z&xz\\
8&0&0&h .
\end{array}                                             \tag{18}
\]
The legal gauge space is
\[
(R,0,0),\quad(0,R,0),\quad
(\partial_iP,\partial_iQ,\partial_iR)\quad(i=x,y,z).    \tag{19}
\]
It has rank five.  Adding
\[
(x^3,0,0),\qquad(0,x^3,0),\qquad(0,0,x^2)
\]
raises the rank to eight, proving the complete quotient
\[
\boxed{(U,V,W)=(Ax^3,Bx^3,Tx^2).}                      \tag{20}
\]
There is no denominator or parameter restriction in (18)--(20).

Write the first two components of \(H_2\) in the order
\((x^2,xy,xz,y^2,yz,z^2)\) with coefficients \(a_i,b_i\).
The twelve nonzero \(E_6\) coefficients are
\[
\begin{array}{c|c@{\qquad}c|c}
x^5y&3a_1&x^5z&-3a_2\\
x^4y^2&6a_3&x^4z^2&-6a_5\\
x^3y^2z&-a_1-6b_1&x^3yz^2&a_2+6b_2\\
x^2y^3z&-2(a_3+6b_3)&x^2yz^3&2(a_5+6b_5)\\
xy^3z^2&-2(b_1-2\ell_7)&xy^2z^3&2(b_2-2\ell_8)\\
y^4z^2&-4b_3&y^2z^4&4b_5 .
\end{array}                                             \tag{21}
\]
They force
\[
a_1=a_2=a_3=a_5=b_1=b_2=b_3=b_5=\ell_7=\ell_8=0.
\]
The reduced \(E_5\) coefficients are
\[
\begin{array}{c|c@{\qquad}c|c}
x^4y&3\ell_1&x^4z&-3\ell_2\\
x^2y^2z&-\ell_1-6\ell_4&
x^2yz^2&\ell_2+6\ell_5\\
y^3z^2&-2\ell_4&y^2z^3&2\ell_5 .
\end{array}                                             \tag{22}
\]
Hence
\[
\ell_1=\ell_2=\ell_4=\ell_5=\ell_7=\ell_8=0,
\]
the last two columns of \(L\) vanish, and \(\det L=0\).

## 9. Independent derivation of `P3-HSM-CO`

Put
\[
h=y^2+xz,\quad s=x^2,\quad
P=h^2,\quad Q=hs,\quad R=x(h+s).
\]
The raw \(36\times26\) \(E_7\) matrix again has rank \(18\) and nullity
\(8\).  An exact kernel basis is
\[
\begin{array}{c|ccc}
&U&V&W\\ \hline
1&x^3&0&0\\
2&xh&0&0\\
3&0&x^3&0\\
4&0&xh&0\\
5&0&0&x^2\\
6&2yh&x^2y&xy\\
7&2zh&x^2z&xz\\
8&-2zh&-x^2z&y^2 .
\end{array}                                             \tag{23}
\]
The same five gauges (19) have rank five.  Adding
\[
(x^3,0,0),\qquad(0,x^3,0),\qquad(2zh,x^2z,xz)
\]
raises the rank to eight.  The complete quotient is therefore
\[
\boxed{
U=Ax^3+2Czh,\qquad
V=Bx^3+Cx^2z,\qquad
W=Cxz.}                                                 \tag{24}
\]
Again, no coefficient has been divided out.

A triangular subset of the exact \(E_6\) coefficients is
\[
\begin{array}{c|l}
x^6&3a_1\\
x^5y&-6(a_2-a_3)\\
x^5z&-a_1+3a_4-6b_1\\
x^4y^2&-a_1-6a_4-6b_1\\
x^3z^3&-2b_4\\
x^2yz^3&8b_5\\
x^3y^3&2(a_2-a_3+6b_2-6b_3)\\
x^4yz&2(6C^2+a_2-a_3-6a_5+6b_2-6b_3)\\
xy^5&4(b_2-b_3-2\ell_8)\\
x^4z^2&-a_4-2b_1-6b_4+4\ell_7 .
\end{array}                                             \tag{25}
\]
It gives, without a case split,
\[
\begin{gathered}
a_1=a_4=b_1=b_4=b_5=\ell_7=\ell_8=0,\\
a_2=a_3,\qquad a_5=C^2,\qquad b_2=b_3.                 \tag{26}
\end{gathered}
\]
The four decisive reduced \(E_5\) coefficients are
\[
\begin{array}{c|l}
x^5&3\ell_1\\
x^3z^2&-2\ell_4\\
x^4y&6(Ca_3-\ell_2)\\
y^5&-4(Cb_3-\ell_5).
\end{array}                                             \tag{27}
\]
Thus
\[
\ell_1=\ell_4=\ell_7=0,\qquad
\ell_2=Ca_3,\qquad \ell_5=Cb_3.
\]
The second column of \(L\) is zero, so \(\det L=0\).  This includes
\(C=0\); no normal-parameter divisor is missing.

## 10. Boundary and localization audit

Every possible degeneration has an ordered destination:

| event | required action |
|---|---|
| all 45 quartic coefficients vanish | degree drops below four |
| primitive component rank drops to one | route to `Q1` |
| gcd degree, minimal pencil degree, image degree, or cover degree changes | recompute the frozen tuple and route to the unique other row |
| a selected intrinsic minor vanishes | proceed to the next `M_j` |
| \(h=s\) | marked-equal package |
| \(h\ne s,\ G=0\) | one of the three `C0` automorphism exits |
| middle \(k\to0\) | `CH` endpoint |
| middle \(k\to-1\) | `CT`, retained in the finite calculation |
| middle \(k\to\infty\) | `CS` endpoint |
| an endpoint \(E_6\) radical drops rank | one of the explicitly treated radical components in Section 7 |
| a CO normal parameter vanishes | retained division-free in (21)--(27) |

Therefore no boundary is disposed of by continuity, genericity, or an
unstated saturation.

## 11. Executable exact replay

Run

```sh
./verify_strict.sh
```

The dependency-free checker implements exact rational sparse-polynomial
arithmetic using only the Python standard library.  It reads no source
package.  It reconstructs:

- all 45 frozen coefficient guards, including the 30 that can reach rank
  two and the 15 that force rank at most one;
- all 45 ordered intrinsic minors;
- the disjoint `4+5+4` projective route;
- both raw CO \(E_7\) matrices, their ranks, eight-vector kernels,
  five legal gauges, and three-vector quotient complements;
- every CO \(E_6/E_5\) equation displayed above;
- the finite-\(k\) `CT`/`CTAU` \(E_6/E_5\) equations and Bezout cover;
- and the terminal distinction
  `3 AUTOMORPHISM_EXIT + 10 DET_L_ZERO`.

The strict replay ends with

```text
AUDIT_BRIDGE_Q2_E2_EXACT_PASS_B625E1
routes: 30 rank-two-possible coefficient pivots; 15 empty rank-one pivots; 45 intrinsic minors; 4+5+4=13 strata
CO E7: rank 18, nullity 8, gauge 5, quotient 3 (both cases)
terminal kinds: 3 AUTOMORPHISM_EXIT; 10 DET_L_ZERO
AUDIT_BRIDGE_Q2_E2_STRICT_PASS_D9347B
```

## Final hostile conclusion

No counterexample or uncovered localization was found.  The exact,
disjoint route is
\[
45\ \text{frozen pivots}
\longrightarrow
\begin{cases}
30\ \text{rank-two-possible pivots}
   \longrightarrow45\ \text{ordered intrinsic minor charts},\\
15\ \text{empty pivots with }\operatorname{rank}JH_4\le1,
\end{cases}
\longrightarrow
\begin{cases}
\text{route out of the row},\\
\text{automorphism exit},\\
\text{marked-equal lower package},\\
\text{one of }4+5+4\text{ marked-distinct strata}.
\end{cases}
\]
All nonzero companion strata force \(\det L=0\); every zero-companion
stratum invokes the quadratic-component automorphism theorem.  With that
scope distinction made explicit,
\[
\boxed{\texttt{Q2-E2-A2-B1-D1-N1 is fully excluded as a counterexample row}.}
\]

The result is AI-assisted exact research, not peer review.
