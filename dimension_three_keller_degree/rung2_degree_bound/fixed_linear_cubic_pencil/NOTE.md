# Exclusion of the fixed-linear primitive cubic-pencil quartic row

**First repository release timestamp (UTC):** `2026-07-25T23:14:47Z`

**Status.** This is a self-contained research-program note for the certified
exclusion of frozen row `Q2-E1-A3-B1-D1-N1`. It is **not peer reviewed**.
The proof and its verification software were produced with substantial AI
assistance; see [AI_DISCLOSURE.md](AI_DISCLOSURE.md). Exact computer
algebra checks identities and case coverage encoded in the repository. Such
checks are evidence, not peer review and not a substitute for a reader's
verification of the mathematical argument or the cited literature.

No claim of worldwide priority is made. In particular, the source search
recorded in this project is not a proof of novelty. The theorem below is a
structural exclusion inside one frozen quartic leading-form row, not a proof
of the three-dimensional Jacobian Conjecture in degree four.

## Abstract

Let \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) be a
degree-four Keller map. We prove that \(F\) is an automorphism when the
canonical invariant tuple of its quartic homogeneous part is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
=(2,1,3,1,1,1).
\]
Equivalently, after invariant gcd and relative-closure constructions, the
leading part is a fixed linear divisor times a primitive cubic pencil. The
proof first gives a coefficient-independent normalization
\(H_4=h(p,q,0)\), then splits intrinsically according to whether restriction
of the cubic pencil to \(h=0\) has rank two or one. The horizontal branch is
settled by a homogeneous first-integral valuation. On the vertical branch
the same valuation leaves only a triple vertical member and two cubic
companion types. Weighted Jacobian identities then eliminate every root,
collision, and lower-jet branch. The last branch, where a binary quadratic
\(W_0\) is nonzero, is forced by the degree-six identity onto the exact
nonminimal boundary. The proof retains arbitrary quadratic and cubic lower
jets throughout.

## 1. Statement, conventions, and frozen context

A polynomial map is **Keller** if its Jacobian determinant is a nonzero
constant. After translating source and target, write
\[
F=LX+H_2+H_3+H_4,                                    \tag{1}
\]
where \(L\in\operatorname{GL}_3(\mathbb C)\), each \(H_i\) is homogeneous
of degree \(i\), and \(H_4\ne0\).

For a rank-two leading part, let
\[
h=\gcd(H_{4,1},H_{4,2},H_{4,3}),\qquad e=\deg h,
\]
and put \(G=H_4/h\). Define
\[
K_G=\mathbb C(G_i/G_j:G_j\ne0)
\subset M=\mathbb C(\mathbb P^2),
\]
and let \(E_G\) be the relative algebraic closure of \(K_G\) in \(M\).
The curve with function field \(E_G\) is rational, so
\[
E_G=\mathbb C(p/q)
\]
for coprime homogeneous forms \(p,q\) of a common least degree \(a\).
If the reduced projective image of \(G\) has degree \(\delta\), and
\(\nu=[E_G:K_G]\), the induced map from the pencil line is represented by
a basepoint-free binary triple \(A\) of degree
\[
b=\delta\nu,\qquad e+ab=4.                            \tag{2}
\]
This defines the invariant tuple used below.

### Theorem 1 (fixed-linear primitive cubic-pencil exclusion)

Let \(F\) be as in (1), of exact total degree four, and suppose
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
=(2,1,3,1,1,1).                                      \tag{3}
\]
If \(F\) is Keller, then \(F\) is a polynomial automorphism.

Equivalently, no degree-four Keller counterexample belongs to frozen row
`Q2-E1-A3-B1-D1-N1`.

The frozen denominator has fourteen disjoint inclusive leading-form rows.
At the time of this release the internal certification ledger reads
\[
3/14\text{ certified excluded},\qquad
5/14\text{ provisional},\qquad
6/14\text{ open}.                                    \tag{4}
\]
This bookkeeping is useful context only. Theorem 1 does not exclude the
other eleven rows and does not raise the universal total-degree floor above
four.

## 2. Canonical normalization

### Proposition 2

Hypothesis (3) permits independent invertible source and target changes
after which
\[
H_4=(hp,hq,0)^T,                                     \tag{5}
\]
where \(h\) is linear, \(p,q\) are coprime nonproportional cubics, and
\[
\mathbb C(p/q)\text{ is relatively algebraically closed in }
\mathbb C(\mathbb P^2).                              \tag{6}
\]
The target normalization is covered by three intrinsic rank-two charts and
does not divide by a frozen coefficient pivot.

### Proof

The construction preceding (2) gives an exact polynomial factorization
\[
H_4=hA(p,q).                                         \tag{7}
\]
Here is the specialized argument. The curve with function field \(E_G\) is
dominated by \(\mathbb P^2\); restricting to a general source line shows
that it is dominated by \(\mathbb P^1\), hence is rational. The primitive
triple \(G\) and the substituted triple \(A(p,q)\) define the same
projective rational map. The latter is primitive because \(p,q\) are
coprime and \(A\) is basepoint-free. Two primitive triples over the UFD
\(\mathbb C[x,y,z]\) defining the same projective map differ by a nonzero
constant. Absorbing that constant into \(A\) proves (7).

In (3), \(b=1\), so
\[
A(u,v)=\mathbf a\,u+\mathbf b\,v
\]
for two linearly independent vectors \(\mathbf a,\mathbf b\in\mathbb C^3\);
their independence is exactly basepoint freeness. Complete them to a target
basis and apply its inverse. This sends \(A(u,v)\) to \((u,v,0)^T\), giving
(5).

Explicitly, if
\[
\Delta_{01}=a_0b_1-a_1b_0,\quad
\Delta_{02}=a_0b_2-a_2b_0,\quad
\Delta_{12}=a_1b_2-a_2b_1,
\]
then at least one \(\Delta_{ij}\) is nonzero. On that chart, adjoining the
unused standard basis vector produces a target matrix whose determinant is,
up to sign, \(\Delta_{ij}\). These three charts cover the rank-two
condition and refer to no first-nonzero coefficient \(c_i\) of \(H_4\).

Finally, \(a=3\) is the least pencil degree by construction of the relative
closure. Thus (6) is an invariant hypothesis, not a genericity assumption.
All lower jets and invertible linear parts are carried bijectively to
arbitrary lower jets and invertible linear parts. \(\square\)

## 3. Weighted identities and homogeneous first integrals

Put
\[
P=hp,\qquad Q=hq,\qquad
D(R)=\operatorname{Jac}(P,Q,R).
\]
Use the weighted determinant
\[
\mathcal J(\tau)=L+\tau JH_2+\tau^2JH_3+\tau^3JH_4,
\qquad E_j=[\tau^j]\det\mathcal J(\tau).              \tag{8}
\]
The Keller condition says \(E_j=0\) for \(j>0\).

Let
\[
G_3=(H_3)_3,\qquad G_2=(H_2)_3.
\]
Since the third row of \(JH_4\) is zero, the weight-eight identity is
\[
E_8=D(G_3)=0.                                        \tag{9}
\]
If \(G_3=0\), the third row of \(JH_3\) is also zero and the weight-seven
identity becomes
\[
E_7=D(G_2)=0.                                        \tag{10}
\]

We use the following descent in both the horizontal and vertical branches.

### Lemma 3 (homogeneous first-integral descent)

If \(0\ne R\in\mathbb C[x,y,z]\) is homogeneous of degree \(d\) and
\(D(R)=0\), then
\[
\frac{R^4}{P^d}=\mathcal R(q/p)
\quad\text{for some }\mathcal R\in\mathbb C(t).       \tag{11}
\]

### Proof

The functions \(P,Q\) are algebraically independent: \(Q/P=q/p\) is
nonconstant on \(\mathbb P^2\), while \(P\), of positive homogeneous
degree, supplies the independent scaling parameter. In characteristic zero,
\(dP\wedge dQ\wedge dR=0\) therefore makes \(R\) algebraic over
\(\mathbb C(P,Q)=\mathbb C(q/p,P)\).

The quotient \(\Theta=R^4/P^d\) has homogeneous degree zero and lies in
\(M=\mathbb C(\mathbb P^2)\). Choose a scaling coordinate \(t\), so
\(\mathbb C(x,y,z)=M(t)\), \(P=t^4P_0\), and \(R=t^dR_0\). Then \(P\) is
transcendental over \(M\). Clear denominators in an algebraic relation for
\(\Theta\) over \(\mathbb C(q/p)(P)\) and collect powers of \(P\). Its
transcendence over \(M\), which contains \(\Theta\), makes each coefficient
vanish; hence \(\Theta\) is algebraic over \(\mathbb C(q/p)\). Relative
algebraic closure (6) gives \(\Theta\in\mathbb C(q/p)\), proving (11).
\(\square\)

## 4. The intrinsic horizontal/vertical split

Let \(\mathcal P=\langle p,q\rangle\) and restrict it to the fixed line:
\[
\rho_h:\mathcal P\longrightarrow\mathbb C[x,y,z]_3/(h).
\]
There are only three formal ranks.

- If \(\operatorname{rank}\rho_h=2\), no pencil member is divisible by
  \(h\). This is the **horizontal** branch.
- If \(\operatorname{rank}\rho_h=1\), its one-dimensional kernel is a
  unique projective member divisible by \(h\). This is the **vertical**
  branch.
- Rank zero would make \(h\mid p\) and \(h\mid q\), contradicting
  coprimality.

Thus the first two branches are disjoint and exhaustive. The split is
unchanged by a \(\operatorname{GL}_2\)-change of pencil generators.

### 4.1 Horizontal branch

On the horizontal branch, \(h\) divides neither \(p\) nor
\(q-\lambda p\) for any \(\lambda\in\mathbb C\). Factor the numerator and
denominator of \(\mathcal R\) in (11). The valuation along \(h=0\) is then
\[
v_h(\mathcal R(q/p))=0.
\]
Since \(v_h(P)=1\), (11) gives
\[
4v_h(R)=d.                                           \tag{12}
\]
There is no nonzero homogeneous first integral of degree two or three.
Applying this first to (9) and then to (10) yields
\[
G_3=G_2=0.                                           \tag{13}
\]
The third component of the full map is consequently a nonzero linear form.
After linear source and target changes,
\[
F=(F_1,F_2,z).
\]
Each restriction \(z=c\) is a plane Keller map of degree at most four and
therefore an automorphism by the bounded plane theorem stated in Section 5.
Fibrewise injectivity and the injective-étale theorem make \(F\) an
automorphism.

### 4.2 Vertical branch

Set \(h=z\) and choose the unique vertical member as the first generator:
\[
p=z^m r,\qquad 1\le m\le3,\qquad z\nmid rq.           \tag{14}
\]
The integer \(m=v_z(p)\) is intrinsic. A second vertical member cannot
arise without making \(z\) divide both generators.

## 5. The quadratic-component exit and the plane theorem used

We isolate the only external low-degree input.

### Lemma 4 (quadratic-component exit)

Let \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) be Keller of
degree at most four. If a nonzero target-linear combination of its
components has degree at most two, then \(F\) is an automorphism.

### Proof

Call that combination \(f\). Since \(JF\) is invertible everywhere,
\(\nabla f\) never vanishes. Write \(\nabla f=HX+b\), where \(H\) is the
constant symmetric Hessian. If \(b\in\operatorname{im}H\), the equation
\(HX=-b\) would give a critical point. Thus
\[
b\notin\operatorname{im}H=(\ker H)^\perp.
\]
Choose \(v\in\ker H\) with \(b^Tv\ne0\). In linear coordinates with \(v\)
as the third direction,
\[
f=g(y_1,y_2)+\beta y_3,\qquad \beta\ne0.
\]
Hence \(T=(y_1,y_2,f)\) is a triangular polynomial automorphism and
\[
\deg T,\deg T^{-1}\le2.
\]
After the target change selecting \(f\), set \(G=F\circ T^{-1}\). Then
\[
G=(G_1,G_2,x_3),\qquad \deg G\le8.
\]
Every fibre \(x_3=c\) is a plane étale polynomial map of maximum component
degree at most eight.

Vistoli states on journal p. 80 that an étale polynomial self-map of
\(\mathbb A^2\), over the algebraically closed characteristic-zero field
fixed on p. 79, is an isomorphism when its degree is at most \(12\). He
attributes this bounded theorem to Moh and notes that Moh proves the result
through degree \(100\), while \(12\) is all Vistoli uses. Thus every fibre
of \(G\) is an automorphism. This makes \(G\) injective: equal images have
equal third coordinates and then equal first two coordinates on that fibre.
The injective-étale theorem quoted by Vistoli (or Ax--Grothendieck together
with étaleness) now makes \(G\), and hence \(F\), an automorphism.
\(\square\)

This is an application of Moh's bounded plane theorem in the exact
degree-\(\le12\) form quoted by Vistoli. It does not assume the unresolved
plane Jacobian Conjecture.

## 6. The top vertical multiplicity lemma

### Lemma 5

In (14), equation (9) has the following complete consequences:
\[
\begin{array}{c|c}
m&\text{homogeneous cubic kernel}\\ \hline
1&0\\
2&0\\
3&\langle z^3,q\rangle .
\end{array}                                           \tag{15}
\]

### Proof

Apply Lemma 3 to a nonzero cubic \(R\), and let
\(\eta=\operatorname{ord}_\infty\mathcal R\), with the valuation
convention that a polynomial of degree \(n\) has order \(-n\) at infinity.
If a prime \(f\) occurs in \(p\) with multiplicity \(a\), valuation of
(11) gives
\[
4v_f(R)-3\bigl(a+\mathbf1_{f=z}\bigr)=a\eta.          \tag{16}
\]

For \(m=1\), the \(z\)-equation gives
\(\eta\equiv2\pmod4\). Every prime in the quadratic \(r\) has multiplicity
\(a=1\) or \(2\), while its equation requires
\(a(3+\eta)\equiv0\pmod4\). But \(3+\eta\equiv1\pmod4\), a contradiction.

For \(m=2\), the \(z\)-equation is
\[
4v_z(R)=9+2\eta,
\]
whose two sides have opposite parity.

For \(m=3\),
\[
4v_z(R)=12+3\eta.
\]
Since \(0\le v_z(R)\le3\), the only possibilities are
\[
(v_z(R),\eta)=(3,0)\quad\text{or}\quad(0,-4).         \tag{17}
\]
The first gives \(R\in\mathbb Cz^3\). In the second case
\(\mathcal R\) has no finite pole, because such a pole would give a
negative valuation along a component of a finite pencil fibre while the
left side of (11) has nonnegative valuation there. Thus \(\mathcal R\) is
a degree-four polynomial. If one of its roots had multiplicity \(n<4\),
then every component of the corresponding cubic pencil member, of
multiplicity \(a\in\{1,2,3\}\), would satisfy \(4\mid na\). This is
impossible for a divisor of total degree three. Hence
\(\mathcal R=c(t-\lambda)^4\), and unique factorization in (11) gives
\(R\sim q-\lambda z^3\). This proves (15). \(\square\)

For \(m=1,2\), equation (9) therefore gives \(G_3=0\). For \(m=3\), it
gives
\[
G_3=0,\qquad G_3\sim z^3,\qquad\text{or}\qquad G_3\sim q. \tag{18}
\]
The zero case is settled by Lemma 4. If
\(G_3=\alpha z^3+\beta q\ne0\), then \(\beta=0\) gives the **vertical
companion** \(G_3=z^3\), whereas \(\beta\ne0\) permits replacement of
\(q\) by \(G_3\) and gives the **nonvertical companion** \(G_3=q\).
These orbits cannot merge because the unique vertical member is divisible
by \(z\), while \(q\) is not.

## 7. Complete companion gauges and root atlas

Write
\[
H_3=(U,V,G_3)^T,\qquad H_2=(A,B,W)^T,
\]
and put \(\{f,g\}=f_xg_y-f_yg_x\).

For the nonvertical companion \(G_3=q\), the complete weight-seven solve,
modulo legal target shears, is
\[
U=dz^3,\qquad V=zW+fz^3.                              \tag{19}
\]

For the vertical companion \(G_3=z^3\),
\[
E_7=z^3\{q,4zW-3U\}=0,
\]
and the complete legal gauge is
\[
U=\frac43zW+\sigma q,\qquad [z^3]V=0.                \tag{20}
\]
The removable \(z^3\)-coefficients of \(q\) and \(V\) are killed by target
shears that only rename unrestricted lower jets. The split
\(\sigma=0\) or \(\sigma\ne0\) is invariant and exhaustive.

Because \(z\nmid q\), the binary cubic
\[
q_0=q|_{z=0}
\]
is nonzero and has root partition \(1+1+1\), \(2+1\), or \(3\). The first
two have representatives \(xy(x-y)\) and \(x^2y\). On the triple-root
locus, write
\[
q=x^3+z(A_1x^2+B_1xy+C_1y^2)+z^2(D_1x+E_1y)+F_1z^3.
\]
The full parabolic stabilizer gives the three minimal charts
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2+\beta z^3,\\
q_B&=x^3+xyz+\beta z^3,\\
q_E&=x^3+yz^2.
\end{aligned}                                        \tag{21}
\]
If \(C_1=B_1=E_1=0\), then \(q\in\mathbb C[x,z]_3\), so
\((z^3,q)\) is nonminimal. For the vertical companion, the \(\beta z^3\)
term in (21) is removable; for the nonvertical companion it is retained.
Thus (21), together with the nontriple representatives, retains every
continuous modulus and has exactly one omitted locus: the invariant
nonminimal boundary.

## 8. The fifteen terminal groups

The following predicates are disjoint and exhaustive. “SF,” “D,” and “T”
mean squarefree, double-plus-simple, and triple binary root type.

| ID | Exact predicate | Exit |
|---|---|---|
| H | horizontal restriction rank \(2\) | valuation (12), then plane fibres |
| Z1 | vertical \(m=1\) | \(G_3=0\), Lemma 4 |
| Z2 | vertical \(m=2\) | \(G_3=0\), Lemma 4 |
| Z3 | \(m=3,\ G_3=0\) | Lemma 4 |
| N1 | \(G_3=q,\ q_0\) SF | nonvertical nontriple obstruction |
| N2 | \(G_3=q,\ q_0\) D | nonvertical nontriple obstruction |
| N3 | \(G_3=q,\ q_0\) T | three-chart nonvertical obstruction |
| V1 | \(G_3=z^3,\ \sigma\ne0,\ q_0\) SF, \(\ell=0\) | zero-\(\ell\) obstruction |
| V2 | same, \(\ell\ne0\) | nonzero-\(\ell\) obstruction |
| V3 | \(G_3=z^3,\ \sigma\ne0,\ q_0\) D, \(\ell=0\) | zero-\(\ell\) obstruction |
| V4 | same, \(\ell\ne0\) | nonzero-\(\ell\), including both collisions |
| V5 | \(G_3=z^3,\ \sigma\ne0,\ q_0\) T, \(\gamma\ne0\) | direct \(E_6\) contradiction |
| V6 | same, \(\gamma=0\) | \(E_6\) forces \(\ell=0\), then \(E_5,E_4\) |
| V7 | \(G_3=z^3,\ \sigma=0,\ W_0=0\) | five-chart \(E_6,E_5,E_4\) obstruction |
| V8 | \(G_3=z^3,\ \sigma=0,\ W_0\ne0\) | \(E_6\) forces the nonminimal boundary |

Here \(W_0=W|_{z=0}\). When \(\sigma\ne0\), restriction of \(E_6\) gives
\[
-\sigma q_0\{q_0,W_0\}=0.                            \tag{22}
\]
For SF or D, the degree-two bracket kernel is zero, so
\[
W=z\ell+\omega z^2,\qquad \ell\in\mathbb C[x,y]_1.
\]
For T, (22) gives \(W_0=\gamma x^2\). These statements prove that the
predicates in the table cover every vertical companion. We now record
enough of each elimination to make its mathematical content inspectable.

### 8.1 Nonvertical companion: N1--N3

With gauge (19), for a noncube \(q_0\), the restrictions of
\(E_6,E_5,E_4\) successively give
\[
A_0=0,\qquad \overline L_1=0,\qquad
A=\alpha z^2\ \text{or}\ B_0=0.                      \tag{23}
\]
The two full coefficient systems have constant pivot minors
\[
-2^{19}\quad\text{and}\quad -2^{11},                 \tag{24}
\]
uniformly for \(q_0=xy(x-y)\) and \(q_0=x^2y\), and force
\[
B=z(\ell_{31}x+\ell_{32}y+\beta z),\qquad
\overline L_2=0,\qquad
\overline L_3=(\ell_{31},\ell_{32}).
\]
The first two rows of \(L\) are then multiples of \(z\), so
\(\det L=0\).

On the triple-root charts (21), the combined full \(E_6,E_5\) systems have
constant \(14\times14\) minors
\[
-2^{24}3^8,\qquad -2^{18}3^6,\qquad -2^{20}3^7,
\]
and give the same dependent-row conclusion. The first two minors retain
the modulus \(\beta\), and the first retains \(\alpha\). Hence N1--N3 are
empty without a generic-rank specialization.

### 8.2 Vertical companion with \(\sigma\ne0\): V1--V6

For SF or D and \(\ell\ne0\), the complete binary \(E_5\) kernel is
\[
V_0=\kappa q_0,\qquad \overline L_3=0,
\]
except on the two D collision lines, where the explicitly larger kernels
are retained. Raw \(E_6\) coefficients are
\[
\begin{array}{c|cc}
\text{SF}&[x^4yz]E_6=\sigma u&[xy^4z]E_6=-\sigma v\\
\text{D, noncollision}&[x^4yz]E_6=\sigma u&
[x^3y^2z]E_6=-2\sigma v,
\end{array}                                          \tag{25}
\]
for \(\ell=ux+vy\). On the two collision kernels \(\ell=cx\) and
\(\ell=cy\), the decisive coefficients are respectively
\(\sigma c\) and \(-2\sigma c\). Thus every \(\ell\ne0\) branch is empty.

If \(\ell=0\), so \(W=\omega z^2\), the complete degree-six solution on
both nontriple root types is
\[
V=kq+\frac z\sigma(A-a_5z^2)
  -\frac4{3\sigma}z^2(\ell_{31}x+\ell_{32}y).         \tag{26}
\]
Constant pivots \(2^5 3^{11}\sigma^8\) and
\(-2^4 3^5\sigma^5\) prove completeness of the \(E_6,E_5\) solves.
The latter gives \(\ell_{31}=\ell_{32}=0\), and \(E_4\) gives
\[
\ell_{21}=\frac{k}{\sigma}\ell_{11},\qquad
\ell_{22}=\frac{k}{\sigma}\ell_{12}.
\]
Therefore \(\det L=0\). This closes V1 and V3.

For the triple-root type, write
\[
W=\gamma x^2+z(ux+vy+\omega z).
\]
If \(\gamma\ne0\), the three charts \(q_C,q_B,q_E\) give respectively
\[
\begin{aligned}
[x^4yz]E_6&=4\gamma\sigma,\\
[x^5z]E_6&=\sigma(2\gamma-3v),\quad
-\tfrac16[x^3yz^2]E_6+[xy^2z^3]E_6
  =-\tfrac{\sigma}{3}(\gamma+v),\\
\tfrac23[x^4z^2]E_6+[xyz^4]E_6&=\tfrac{10}{3}\gamma\sigma .
\end{aligned}                                        \tag{27}
\]
Each chart is impossible, proving V5.

If \(\gamma=0\), all three charts first give
\([x^5z]E_6=-3\sigma v\), hence \(v=0\). Three displayed
chartwise linear combinations then equal nonzero constants times
\(\sigma u\), so \(u=0\). With \(W=\omega z^2\), the complete
\(E_6,E_5,E_4\) solution is again (26) followed by the dependent-row
relations above. Its chartwise pivots are powers of \(2,3,\sigma\) and
contain neither \(\alpha\) nor \(\omega\). This proves V6.

### 8.3 The branch \(\sigma=0,W_0=0\): V7

Put \(W=z(ux+vy+\omega z)\). The SF, D, and three minimal T charts form a
complete five-chart atlas. On every chart a constant \(5\times5\) subsystem
of \(E_6\) gives
\[
\begin{aligned}
A_{20}&=\frac29u^2,& A_{11}&=\frac49uv,&
A_{02}&=\frac29v^2,\\
\ell_{31}&=\frac{9A_{10}-4u\omega}{12},&
\ell_{32}&=\frac{9A_{01}-4v\omega}{12}.              \tag{28}
\end{aligned}
\]
The nontriple charts and \(q_C\) force \(u=v=0\) through cubic monomials
of \(E_5\). The \(q_B,q_E\) charts either do the same or leave one
explicit \(u\ne0\) compatibility family. On \(u=v=0\), \(E_5,E_4\)
force
\[
\ell_{11}=\ell_{12}=\ell_{31}=\ell_{32}=0,
\]
so \(\det L=0\). On each exceptional \(u\ne0\) family, two or three raw
\(E_4\) coefficients demand incompatible values of one coefficient of
\(V\). Thus V7 is empty.

## 9. The final \(W_0\ne0\) elimination

This is V8 and is worth giving in full because its conclusion is
reclassification, not singularity of \(L\).

Assume \(\sigma=0\), so \(U=\frac43zW\). Row multilinearity gives the
compact identity
\[
3E_6=z\Phi,\qquad
\Phi=4W\{q,W\}+9z^2\{A,q\}+12z^3\{q,L_3\}.           \tag{29}
\]
The variables \(B,V,L_1,L_2\) cancel or do not occur; they have not been
specialized. The coefficient of the lowest power of \(z\) is
\[
4W_0\{q_0,W_0\}.
\]
Since \(W_0\ne0\), we obtain
\[
\{q_0,W_0\}=0.                                       \tag{30}
\]

If binary forms \(f,g\) of degrees three and two satisfy
\(\{f,g\}=0\), dehomogenization gives
\(2F'G-3FG'=0\). Hence \(F^2/G^3\) is constant, and unique
factorization yields
\[
q_0=\kappa L^3,\qquad W_0=\gamma L^2,\qquad
\kappa\gamma\ne0.                                    \tag{31}
\]
After a binary change take \(L=x\), retaining every coefficient:
\[
\begin{aligned}
q={}&\kappa x^3+z(\alpha x^2+\beta xy+\chi y^2)
 +z^2(\delta x+\epsilon y)+\phi z^3,\\
W={}&\gamma x^2+z(ux+vy)+\omega z^2,\\
A={}&a_{20}x^2+a_{11}xy+a_{02}y^2
 +z(a_{10}x+a_{01}y)+a_{00}z^2.
\end{aligned}                                        \tag{32}
\]
Six raw coefficients of \(\Phi\) suffice. The first four give
\[
\chi=0,\qquad
r=2\beta\gamma-3\kappa v=0,
\]
\[
f=27\kappa a_{02}+2\beta\gamma v-6\kappa v^2=0,
\qquad
h=9a_{02}\beta-2\beta v^2=0.
\]
Put \(g=9a_{02}-v^2\). The division-free combinations
\[
f-vr=3\kappa g,\qquad h-\beta g=-\beta v^2           \tag{33}
\]
give \(g=0\) and \(\beta v^2=0\). Multiplying \(r=0\) by \(v^2\) gives
\(-3\kappa v^3=0\), hence
\[
v=\beta=a_{02}=0.                                    \tag{34}
\]
The remaining two coefficients reduce to
\[
27\kappa a_{11}+8\gamma^2\epsilon=0,\qquad
9a_{11}\epsilon=0.                                   \tag{35}
\]
Multiply the first equation by \(\epsilon\) and subtract three
\(\kappa\) times the second. Then \(8\gamma^2\epsilon^2=0\), so
\[
\epsilon=a_{11}=0.                                   \tag{36}
\]
Equations (32), (34), and (36) give
\[
q=\kappa x^3+\alpha x^2z+\delta xz^2+\phi z^3
\in\operatorname{Sym}^3\langle x,z\rangle.           \tag{37}
\]

For a cubic pencil containing \(z^3\), condition (37) is exactly the
nonminimal boundary
\[
q\in\operatorname{Sym}^3\langle z,L\rangle.
\]
It therefore has canonical pencil degree \(a=1\), not \(a=3\), and routes
to one of the separate frozen \(e=1,a=1,b=3\) rows. No point of the
minimal row (3) survives. This proves V8.

The fifteen terminal predicates now prove Theorem 1. \(\square\)

## 10. Frozen coefficient pivots and certification boundary

The frozen coefficient partition orders the fifteen quartic monomials
component by component and uses the first nonzero coefficient
\(c_0,\ldots,c_{44}\). Proposition 2 and Sections 3--9 are global on the
invariant row and divide by none of these coefficients. Therefore every
nonempty pivot `C00`--`C29` enters the theorem directly. If the first pivot
were `C30` or later, the first two target components of \(H_4\) would be
zero, so \(\operatorname{rank}JH_4\le1\), contrary to (3). Thus
`C30`--`C44` are empty.

The post-freeze bridge audit expands the proof into 48 disjoint route atoms
mapping uniquely to the fifteen terminal groups above. It checks all 45
pivots, including exact leading-form witnesses for `C00`--`C29`; those
witnesses are not asserted to be Keller maps. This is a coverage
certificate, not an additional mathematical hypothesis.

Detailed derivations are retained in:

- [WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md](WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md);
- [vertical_locus/WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md](vertical_locus/WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md);
- the branch lemmas in [vertical_locus](vertical_locus/);
- [vertical_locus/a0_w0_nonzero_attack/NOTE.md](vertical_locus/a0_w0_nonzero_attack/NOTE.md);
- [../WORKING_QUADRATIC_COMPONENT_EXIT.md](../WORKING_QUADRATIC_COMPONENT_EXIT.md); and
- the final hostile bridge report in
  [../taxonomy_freeze/audit_bridge_q2_e1_a3_b1_d1_n1_v1/REPORT.md](../taxonomy_freeze/audit_bridge_q2_e1_a3_b1_d1_n1_v1/REPORT.md).

The corresponding hostile reports independently reconstruct the encoded
algebra with separate implementations and negative controls. They are not
referee reports and must not be represented as community verification.
Run [verify_all_strict.sh](verify_all_strict.sh) to replay the retained
exact and hostile suites and the final fail-closed bridge wrapper.

## 11. Prior art, attribution, and claims

The only external bounded-degree result used in the proof is the plane
theorem in the degree-\(\le12\) form quoted by Vistoli. Vistoli attributes
it to Moh, whose cited paper is the 1983 paper on configurations of roots.
We do not attribute the present three-dimensional row decomposition to
Moh, and we do not confuse this plane result with the separate unpublished
Moh--Sathaye computer calculation for three-dimensional degree three that
Vistoli discusses elsewhere.

No claim is made that this row theorem is absent from all prior literature.
The project records a source-specific search and exact internal provenance;
that is weaker than a priority determination. The defensible claim here is
only the theorem stated and proved above.  The first repository release
timestamp is `2026-07-25T23:14:47Z`.

## References

1. T.-T. Moh, “On the Jacobian conjecture and the configurations of
   roots,” *Journal für die reine und angewandte Mathematik* **340**
   (1983), 140--212.
   [doi:10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
2. Angelo Vistoli, “The Jacobian conjecture in dimension 3 and degree 3,”
   *Journal of Pure and Applied Algebra* **142** (1999), 79--89.
   [doi:10.1016/S0022-4049(98)00040-1](https://doi.org/10.1016/S0022-4049(98)00040-1).
   The field and degree conventions are on journal p. 79; the two
   unnumbered theorems used here are on p. 80.
3. Hyman Bass, Edwin H. Connell, and David Wright, “The Jacobian
   conjecture: reduction of degree and formal expansion of the inverse,”
   *Bulletin of the American Mathematical Society (N.S.)* **7** (1982),
   287--330.
   [AMS article](https://www.ams.org/bull/1982-07-02/S0273-0979-1982-15032-7/).
4. The Stacks Project, Theorem 41.14.1, Tag
   [025G](https://stacks.math.columbia.edu/tag/025G), for the standard
   fact that an étale universally injective morphism is an open immersion.
