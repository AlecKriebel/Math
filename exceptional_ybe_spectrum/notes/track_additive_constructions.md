# Track: additive, colored, and ancilla constructions

**Last updated:** 2026-07-28 21:55 PDT

**Scope:** exact construction mechanisms that could produce local dimension
\(d\equiv2\pmod4\), especially \(d=6\).

**Status labels used below:** `PROVED`, `EXACT_COMPUTATION`, and
`OPEN WITHIN THIS TRACK`.

## Executive result

There is a useful reduced construction target which does not assume the
published five-Pauli-word form:

> A \(12\times12\) unitary Hecke operator on
> \(\mathbb C^2\otimes\mathbb C^3\otimes\mathbb C^2\), satisfying a
> heterogeneous shifted Yang--Baxter equation on a \(72\)-dimensional
> space and having \((-1)\)-multiplicity \(6\), blocks into a
> \(36\times36\) solution at local dimension \(6\).

This is an exact equivalence within the spectator-form ansatz and is a
substantially smaller search problem than an unrestricted \(36\times36\)
matrix.

Three broad ways of extending the known qubit constructions do **not**
reach \(d=6\):

1. scalar-natural colored direct sums \(V=A\oplus B\);
2. a qutrit middle factor which merely controls three ordinary qubit
   operators;
3. replacing a qubit/Clifford factor by a unital representation on a
   qutrit.

The no-go statements below are explicitly restricted to those ansatz
classes. They are not nonexistence results for arbitrary \(d=6\) matrices.
A remaining viable target is a genuinely qutrit-mixing heterogeneous
operator \(K\), with operator-valued rather than scalar color couplings.

## 1. Heterogeneous blocking lemma (`PROVED`)

Let \(A\) and \(B\) be finite-dimensional Hilbert spaces of dimensions
\(a\) and \(b\). Put \(V=A\otimes B\), and on each site swap the factors so
that the chain order is
\[
  B_1,A_1,B_2,A_2,B_3,A_3,\ldots .
\]
Let
\[
  K\in\operatorname{End}(A\otimes B\otimes A).
\]
Define the two-site operator, in the swapped coordinates, by
\[
  \widetilde R_{(B_1A_1)(B_2A_2)}
  =I_{B_1}\otimes K_{A_1B_2A_2}.
\]
On three local sites, after factoring out the global spectator \(B_1\),
the two adjacent copies are
\[
  K_1=K\otimes I_{B\otimes A},
  \qquad
  K_2=I_{A\otimes B}\otimes K
\]
on
\[
  A_1\otimes B_2\otimes A_2\otimes B_3\otimes A_3.
\]
Consequently
\[
  \widetilde R_1\widetilde R_2\widetilde R_1
  =\widetilde R_2\widetilde R_1\widetilde R_2
\]
if and only if
\[
  (K\otimes I_{B\otimes A})
  (I_{A\otimes B}\otimes K)
  (K\otimes I_{B\otimes A})
  =
  (I_{A\otimes B}\otimes K)
  (K\otimes I_{B\otimes A})
  (I_{A\otimes B}\otimes K).
  \tag{HB}
\]
Conjugating back by the sitewise swaps gives an ordinary Yang--Baxter
operator on \(V\otimes V\). Far commutativity is automatic because
generators two or more sites apart have disjoint active factors.

Unitarity and the Hecke relation pass in both directions:
\[
  \widetilde R^*\widetilde R=I
  \Longleftrightarrow K^*K=I,
  \qquad
  (\widetilde R+I)(\widetilde R-qI)=0
  \Longleftrightarrow (K+I)(K-qI)=0.
\]
If \(P_K\) is the \((-1)\)-spectral projection of \(K\), then the
\((-1)\)-projection of \(\widetilde R\) is \(I_B\otimes P_K\). Hence
\[
  \operatorname{rank}P_{\widetilde R}=b\,\operatorname{rank}P_K.
\]
The exceptional half-rank condition for local dimension \(d=ab\) is
therefore exactly
\[
  \operatorname{rank}P_K=\frac{a^2b}{2}.
  \tag{HR}
\]

For \(a=2,b=3\), equation (HB) acts on dimension
\[
  a^3b^2=72,
\]
while \(K\) is \(12\times12\) and (HR) asks for rank \(6\). Thus this gives
the reduced \(d=6\) search target stated above. More generally, taking
\(a=2\) and \(b=2m+1\) targets every \(d=4m+2\).

This lemma only covers solutions which acquire the displayed spectator
form after a sitewise factor swap. It does not assert that every ordinary
solution has that form.

## 2. Identity amplification is multiplicative (`PROVED`)

If \(R_0\) is an exceptional solution on a local space \(U\) of dimension
\(d_0\), and \(W\) has dimension \(m\), then after the canonical factor
reordering
\[
  R=R_0\otimes I_{W\otimes W}
\]
is an exceptional solution on \(U\otimes W\). Its \((-1)\)-rank is
\[
  \frac{d_0^2}{2}m^2=\frac{(d_0m)^2}{2}.
\]
Starting with \(d_0=4\), this produces exactly \(d=4m\). Plain identity
ancillas cannot produce \(d=6\).

Likewise, homogeneous \((3,2)\)-blocking over a space \(W\) naturally has
local dimension \((\dim W)^2\). The heterogeneous lemma above is the
relevant relaxation when one seeks \(2\cdot3\).

### 2.1 Pure tensor products of two-eigenvalue factors

There is also a spectral obstruction to replacing the identity ancilla by
another nontrivial two-eigenvalue braid operator. Let \(X\) and \(Y\) be
normal braid operators, each with exactly two nonzero eigenvalues. After
the standard factor reordering, \(X\otimes Y\) is again a normal braid
operator. If the projective eigenvalue ratios of \(X,Y\) are respectively
\(r,s\ne1\), the projective spectrum of the tensor product is
\[
  \{1,r,s,rs\}.
\]
For this set to have only two elements, necessarily \(r=s=-1\): indeed
\(r\) and \(s\) must be the same nontrivial element \(t\) of a two-element
set containing \(1\), and closure under the product \(rs=t^2\) forces
\(t^2=1\).

The resulting tensor product has projective eigenvalue ratio \(-1\),
whereas the exceptional ratio is
\[
  \frac{q}{-1}=-q\ne-1.
\]
Thus a pure tensor product of two non-scalar two-eigenvalue unitary braid
operators cannot land in the exceptional class. Within this ansatz, one
factor must be scalar, returning to identity/phase amplification.

## 3. Scalar-natural colored direct sums (`PROVED` no-go)

This subsection completely analyzes a standard colored-gluing ansatz, not
arbitrary block matrices.

Let \(V=A\oplus B\). Assume:

- \(R\) preserves \(A\otimes A\), \(B\otimes B\), and
  \((A\otimes B)\oplus(B\otimes A)\);
- \(R|_{A\otimes A}=T\) and \(R|_{B\otimes B}=S\);
- after identifying \(B\otimes A\) with \(A\otimes B\) by the tensor flip,
  the mixed block is scalar on the internal factors and is represented by
  \[
    C=\begin{pmatrix}c&t\\s&u\end{pmatrix}.
    \tag{C}
  \]

Thus (C) is the most general mixed action which treats all vectors inside
each color naturally and uses only scalar coefficients.

### 3.1 Full mixed-color braid equations

Suppose first that \(T\) is a non-scalar Hecke operator, so
\[
  T^2=(q-1)T+qI
\]
and \(I,T\) are linearly independent. On the color orbit
\[
  AAB,\quad ABA,\quad BAA,
\]
preserving the relative order of the two \(A\)-vectors identifies the two
braid generators with
\[
  R_1=
  \begin{pmatrix}
    T&0&0\\
    0&c&t\\
    0&s&u
  \end{pmatrix},
  \qquad
  R_2=
  \begin{pmatrix}
    c&t&0\\
    s&u&0\\
    0&0&T
  \end{pmatrix}.
\]
Reducing \(R_1R_2R_1-R_2R_1R_2\) in the basis \(I,T\) gives exactly the
following nonzero candidate entries:
\[
\begin{array}{c|cc}
 (i,j)&[I]&[T]\\ \hline
 (0,0)&c(q-st)&c(q-1-c)\\
 (0,1)&-ctu&0\\
 (1,0)&-csu&0\\
 (1,1)&-cu(u-c)&0\\
 (1,2)&ctu&0\\
 (2,1)&csu&0\\
 (2,2)&-u(q-st)&-u(q-1-u).
\end{array}
\tag{MC}
\]
The \(BBA,BAB,ABB\) orbit gives the same equations with the two colors and
the two diagonal coefficients interchanged. The monochromatic orbits are
exactly the Yang--Baxter equations for \(T\) and \(S\). Thus (MC), its
color-reversal, and the two monochromatic equations are the full YBE in
this ansatz.

The table (MC) is independently replayed by
`scripts/verify_track_additive_scalar_gluing.py`.

### 3.2 Unitarity rules out nontrivial gluing

Assume \(q=e^{i\pi/3}\), and assume \(R\) is unitary and satisfies the
Hecke polynomial.

If \(c\ne0\), the \((0,0)\) entry of (MC) forces
\[
  c=q-1,\qquad st=q.
\]
Thus \(s,t,c\) are all nonzero, and the off-diagonal equations force
\(u=0\). But the two columns of the unitary matrix (C) would then have
inner product \(\overline c\,t\ne0\), a contradiction.

If \(c=0,u\ne0\), the \((2,2)\) equation gives the color-reversed
contradiction. If \(c=u=0\), then
\[
  C^2=st\,I,
\]
whereas the Hecke relation would have a nonzero off-diagonal term
\((q-1)C\), impossible because \(q\ne1\) and \(C\) is invertible.
Therefore a non-scalar \(T\) cannot occur.

It remains to check that taking both \(T\) and \(S\) scalar does not hide a
colored solution. Write \(T=xI,S=yI\), with
\(x,y\in\{-1,q\}\). If either \(c\) or \(u\) vanishes, unitarity of the
\(2\times2\) matrix (C) forces both to vanish, which is incompatible with
its Hecke polynomial as above. Hence \(c,u\ne0\). The mixed equations force
\(s=t=0\), then the \(AAB\) orbit forces \(c=u=x\), and the \(BBA\) orbit
forces \(c=u=y\). Thus \(x=y\) and the entire operator is scalar.

We have proved:

> **Scalar-cross gluing no-go.** The scalar-natural colored direct-sum
> ansatz above has no non-scalar unitary Hecke Yang--Baxter operator at
> \(q=e^{i\pi/3}\). In particular, it cannot adjoin a two-dimensional
> colored sector to the known four-dimensional solution.

This does not rule out operator-valued mixed blocks.

## 4. Controlled qutrit middle factor (`PROVED` no-go)

The heterogeneous \(12\times12\) target can still be simplified in a way
that is tempting but too restrictive. Let \(A=\mathbb C^2\) and let
\(B=\mathbb C^b\) have an orthonormal basis \(e_1,\ldots,e_b\). Suppose
\(K\) does not mix these middle colors:
\[
  K(x\otimes e_r\otimes y)
  =
  e_r\text{-controlled application of }L_r(x\otimes y),
  \qquad
  L_r\in\operatorname{End}(A\otimes A).
  \tag{CTRL}
\]
Equivalently, after moving the middle factor aside,
\[
  K=\bigoplus_{r=1}^b L_r.
\]

Restricting (HB) to the sector \(B_2=e_r,B_3=e_s\) gives
\[
  (L_r)_{12}(L_s)_{23}(L_r)_{12}
  =
  (L_s)_{23}(L_r)_{12}(L_s)_{23}
  \quad\text{on }A^{\otimes3}.
  \tag{MB}
\]
In particular, \(r=s\) says that every \(L_r\) is an ordinary
two-dimensional unitary Hecke Yang--Baxter operator.

Let \(k_r\in\{0,1,2,3,4\}\) be its \((-1)\)-multiplicity. If \(k_r=0\) or
\(4\), then \(L_r\) is respectively \(qI\) or \(-I\). If
\(L_r=\lambda I\), equation (MB) and invertibility give
\[
  \lambda^2L_s=\lambda L_s^2
  \quad\Longrightarrow\quad
  L_s=\lambda I
\]
for every \(s\). Such a family has total \((-1)\)-rank \(0\) or \(4b\),
not the required \(2b\).

Otherwise \(k_r\in\{1,2,3\}\). The established emptiness of the ordinary
exceptional class in base dimension two rules out \(k_r=2\). Hence every
\(k_r\) is odd. When \(b\) is odd,
\[
  \operatorname{rank}P_K=\sum_{r=1}^b k_r
\]
is odd, whereas the exceptional condition (HR) requires
\[
  \operatorname{rank}P_K=2b,
\]
which is even. Contradiction.

Therefore:

> **Controlled-middle no-go.** For every odd \(b\), no operator of the
> controlled form (CTRL) can solve the heterogeneous half-rank problem
> with \(A=\mathbb C^2\). In particular, a \(2\oplus1\) block extension of
> the published \(8\times8\) active operator cannot yield \(d=6\).

This argument uses only the already-established \(d=2\) emptiness and
does not classify non-controlled qutrit mixing.

## 5. Qutrit graph-phase/global-flip extension (`PROVED` no-go)

The published active qubit operator arises from a diagonal sign reflection
and an anticommuting global bit flip. There is a natural finite qutrit
generalization which can be exhausted exactly without fixing the mixing
angle.

Use the computational basis
\[
  (a,b,c)\in\mathbb Z_2\times\{0,1,2\}\times\mathbb Z_2
\]
of \(A\otimes B\otimes A\). Let \(\pi\) be any involution of the three
middle symbols (the identity or one of the three transpositions), and
define the permutation reflection
\[
  E(a,b,c)=(a\mathbin{\oplus}1,\pi(b),c\mathbin{\oplus}1).
\]
The outer flips make \(E\) fixed-point-free, so it has six two-element
orbits. Let \(M\) be any diagonal sign reflection satisfying
\[
  M(Ev)=-M(v)
\]
on basis vectors. There are \(2^6=64\) such \(M\) for each \(\pi\), and
\[
  M^2=E^2=I,\qquad ME=-EM,\qquad
  \operatorname{Tr}M=\operatorname{Tr}E=0.
\]
Thus every
\[
  H=xM+yE,\qquad x,y\in\mathbb R,\qquad x^2+y^2=1,
  \tag{GF}
\]
is automatically a traceless Hermitian involution.

The exact verifier exhausts all \(4\cdot64=256\) pairs \((M,E)\) and all
mixing angles at once. For \(x\ne0\), put \(t=y/x\). Expanding the cubic
residual and using \(x^2=1/(1+t^2)\) turns every matrix entry into a cubic
polynomial in \(t\):
\[
  3(A+tB+t^2C+t^3D)
  -(1+t^2)(L_M+tL_E).
  \tag{GF-poly}
\]
For every one of the 256 cases, the exact gcd over \(\mathbb Q[t]\) of
all nonzero entry polynomials in (GF-poly) is \(1\). The endpoint
coefficient matrices for \(x=0\) and \(y=0\) are also nonzero. Hence no
real or complex mixing angle solves the cubic relation.

Therefore the most direct diagonal-phase/product-involution qutrit
analogue of the published two-reflection mechanism cannot produce
\(d=6\). This is an exhaustive result only for (GF): it does not exclude
non-diagonal \(M\), non-product \(E\), or a sum of more than two
reflections. The certificate is
`scripts/verify_track_additive_graph_flip_qutrit.py`.

## 6. Diagonal \(SU(2)\) symmetry (`PROVED` no-go)

A nonabelian symmetry gives a genuinely qutrit-mixing ansatz which can
also be exhausted exactly. Take
\[
  A=V_{1/2}\cong\mathbb C^2,\qquad B=V_1\cong\mathbb C^3
\]
with the usual unitary \(SU(2)\) actions, and require \(K\), equivalently
its \((-1)\)-spectral projection \(P_K\), to commute with the diagonal
\(SU(2)\) action on \(A\otimes B\otimes A\).

Clebsch--Gordan decomposition gives
\[
  V_{1/2}\otimes V_1\otimes V_{1/2}
  \cong V_0\oplus 2V_1\oplus V_2.
\]
An equivariant projection is specified by choices
\[
  p_0,p_2\in\{0,1\},
  \qquad
  r\in\{0,1,2\},
\]
where \(r\) is the projection rank in the multiplicity space of \(V_1\).
Its ordinary rank is
\[
  p_0+3r+5p_2.
\]
Rank six has only two solutions:
\[
  (p_0,r,p_2)=(1,0,1)
  \quad\text{or}\quad
  (0,2,0).
\]
They are complementary, so the corresponding traceless involutions are
\(H\) and \(-H\).

Let \(C\) denote the total-spin Casimir. Its eigenvalues on
\(V_0,V_1,V_2\) are \(0,2,6\). Choosing \(H=-1\) on \(V_0\oplus V_2\) and
\(+1\) on \(2V_1\) gives the exact polynomial
\[
  H=-I+\frac32C-\frac14C^2.
\]
Exact calculation on
\(A\otimes B\otimes A\otimes B\otimes A\) gives
\[
  H_1H_2H_1-H_2H_1H_2-\frac13(H_1-H_2)\ne0;
\]
in the standard product basis its \((1,1)\) entry (zero-based indexing)
is
\[
  \frac{13}{8}.
\]
Replacing \(H\) by \(-H\) negates the residual, so the complementary
choice also fails.

Thus no diagonally \(SU(2)\)-equivariant rank-six heterogeneous operator
solves (HB). This is an exhaustive symmetry-class result, not evidence
against nonsymmetric qutrit mixing. The exact certificate is
`scripts/verify_track_additive_su2_ansatz.py`.

### 6.1 Exploratory \(S_4\) symmetry (`NUMERICAL_EVIDENCE`)

A separate reproducible probe used the two- and three-dimensional
irreducible real representations of \(S_4\) for \(A\) and \(B\). Character
decomposition gives
\[
  A\otimes B\otimes A\cong 2V_3\oplus2V_{3'},
\]
so the commutant is \(M_2(\mathbb C)\oplus M_2(\mathbb C)\). Besides the
two central rank-six projections, the half-rank involutions have a
four-real-parameter branch consisting of a traceless multiplicity-space
reflection in each isotypic component.

The two central points fail exactly: in a rational representation basis,
the \((0,1)\) entry of the cubic residual is respectively
\(-5/12\) and \(5/12\). The certificate is
`scripts/verify_track_additive_s4_central.py`.

The deterministic experiment
`scripts/explore_track_additive_s4_symmetry.py` then ran 20 BFGS starts on
the four-parameter branch (seed \(7\)). No zero was found; the best squared
Frobenius norm of the cubic residual was approximately
\[
  64.
\]
This is only negative numerical evidence. It is not an exhaustive
certificate and is not used in any no-go theorem above. The raw output,
software versions, seed, and timestamps are in
`results/track_additive_s4_symmetry.txt`.

## 7. Clifford/quaternion factor substitution (`PROVED` no-go)

Another natural attempt is to retain a qubit formula but replace one
Pauli or quaternionic factor by matrices on \(\mathbb C^3\).

There is an elementary parity obstruction. A unital
\(*\)-representation
\[
  \pi:M_2(\mathbb C)\longrightarrow M_b(\mathbb C)
\]
exists only when \(b\) is even. Indeed, \(\pi(e_{11})\) and
\(\pi(e_{22})\) are complementary projections, while
\(\pi(e_{12})\) is a partial isometry identifying their ranges. Their
ranks are equal, so \(b=2\,\operatorname{rank}\pi(e_{11})\).
Equivalently, every such representation is unitarily equivalent to
\[
  x\longmapsto x\otimes I_{b/2}.
\]

The still weaker requirement of two invertible anticommuting matrices
already forces even dimension:
\[
  XY=-YX
  \quad\Longrightarrow\quad
  \det(XY)=(-1)^b\det(YX),
\]
and invertibility implies \((-1)^b=1\).

Consequences for the present construction track:

- factorwise unital substitution into the Pauli/Clifford active operator
  cannot replace its middle qubit by a qutrit;
- factorwise complex representations of the older quaternionic
  construction have the same obstruction, because the complexified
  quaternion algebra is \(M_2(\mathbb C)\);
- with outer factor dimension \(2\), these substitutions give local
  dimension \(d=2b\) only for even \(b\), hence only \(4\mid d\).

This does not rule out a formula on a qutrit that abandons the qubit
algebra relations.

## 8. Ice-rule / unordered-pair blocks (`PROVED` global ansatz no-go)

A much broader basis-sparse ansatz can also be excluded. Fix an
orthonormal basis \(e_1,\ldots,e_d\) and suppose \(R\) preserves every
subspace
\[
  \mathbb C(e_i\otimes e_i)
  \quad\text{and}\quad
  \operatorname{span}\{e_i\otimes e_j,e_j\otimes e_i\}
  \quad(i<j).
  \tag{ICE}
\]
No uniformity among the \(2\times2\) blocks is assumed.

Let \(\epsilon_i\in\{0,1\}\) record whether the eigenvalue on
\(e_i\otimes e_i\) is \(q\) or \(-1\), and let
\(k_{ij}\in\{0,1,2\}\) be the \((-1)\)-multiplicity of the mixed
\(2\times2\) block. For every pair \(i<j\), the local subspace
\[
  U_{ij}=\operatorname{span}\{e_i,e_j\}
\]
has \(U_{ij}^{\otimes2}\) invariant under \(R\), so restriction gives an
ordinary two-dimensional unitary Hecke Yang--Baxter operator. Its
\((-1)\)-rank is
\[
  \epsilon_i+\epsilon_j+k_{ij}.
  \tag{PAIR}
\]
The established emptiness of the \(d=2\), half-rank exceptional class
rules out the value \(2\) in (PAIR).

If \(\epsilon_i\ne\epsilon_j\), then \(k_{ij}=1\) is ruled out immediately.
For \(k_{ij}=0\) or \(2\), the mixed block is respectively \(qI_2\) or
\(-I_2\). The full restriction to \(U_{ij}^{\otimes2}\) is then diagonal
but not scalar. Yet an invertible diagonal Yang--Baxter operator must be
scalar: writing its entries as \(r_{ab}\), the equation on
\(e_a\otimes e_b\otimes e_c\) gives
\[
  r_{ab}=r_{bc}
\]
for all \(a,b,c\). This is a contradiction. Hence all
\(\epsilon_i\) are equal.

If every \(\epsilon_i=0\), then \(k_{ij}=2\) is forbidden by (PAIR), so
the total \((-1)\)-rank is at most
\[
  \binom d2<\frac{d^2}{2}.
\]
If every \(\epsilon_i=1\), then \(k_{ij}=0\) is forbidden, so the rank is
at least
\[
  d+\binom d2>\frac{d^2}{2}.
\]
Both alternatives contradict the exceptional half-rank condition.

Therefore no solution in the exceptional class has the ice form (ICE), in
any dimension. This rules out all unordered-pair block, six-vertex-style,
and basis-charge-conserving constructions of this precise type. It does
not rule out sparse matrices which couple different unordered pairs.

## 9. Monomial-unitary matrices (`PROVED` global ansatz no-go)

The monomial-unitary search class can be excluded in every dimension,
without a numerical enumeration.

Let \(R\) be a monomial matrix satisfying
\[
  (R+I)(R-qI)=0,\qquad q\ne1.
\]
Decompose the underlying permutation into cycles. On a cycle of length
\(\ell\), the corresponding weighted cyclic block has minimal polynomial
\[
  x^\ell-\gamma
\]
for a nonzero product \(\gamma\) of its weights. Since this polynomial
must divide the quadratic Hecke polynomial, \(\ell\le2\). A two-cycle is
also impossible: \(x^2-\gamma\) has zero linear coefficient, whereas
\[
  (x+1)(x-q)=x^2+(1-q)x-q
\]
has nonzero linear coefficient. Hence every cycle has length one and
\(R\) is diagonal, with every diagonal entry in \(\{-1,q\}\).

Write the entry of \(R\) on the basis vector \(e_i\otimes e_j\) as
\(r_{ij}\ne0\). On \(e_i\otimes e_j\otimes e_k\), the diagonal
Yang--Baxter equation is
\[
  r_{ij}^2r_{jk}=r_{ij}r_{jk}^2,
\]
so
\[
  r_{ij}=r_{jk}
\]
for all \(i,j,k\). These equalities force all \(r_{ij}\) to be the same.
Thus \(R\) is scalar and cannot have both Hecke eigenvalues.

Therefore there are no nontrivial monomial solutions in the exceptional
class in any base dimension. This covers arbitrary unit-modulus monomial
weights, not only signed permutations. It does not exclude sparse
non-monomial matrices.

For comparison, the involution formulation gives an especially short
signed-permutation obstruction: both cubic words are signed permutation
matrices, so the left side of
\[
  3(H_1H_2H_1-H_2H_1H_2)=H_1-H_2
\]
has entries divisible by \(3\), while the right side has entries in
\(\{-2,-1,0,1,2\}\). Hence \(H_1=H_2\), which forces \(H\) to be scalar
and contradicts \(\operatorname{Tr}H=0\).

## 10. Reducing an identity amplification (`PROVED` restricted no-go)

One might start with the \(d=8\) identity amplification of the published
\(d=4\) operator and try to select a six-dimensional local direct summand.
There is a clean obstruction if "direct summand" means a reducing local
sector for the one-leg coefficient algebras.

For a two-site operator \(R\in\operatorname{End}(U\otimes U)\), let its
left and right leg algebras be generated by all slices
\[
  (\operatorname{id}\otimes\omega)(R),
  \qquad
  (\omega\otimes\operatorname{id})(R)
\]
as \(\omega\) ranges over linear functionals on
\(\operatorname{End}(U)\).

For the published \(d=4\) operator, the left slices of \(H\) contain
\[
  ZI,\quad JI,\quad XI,
\]
so they generate \(M_2(\mathbb C)\otimes I_2\). The right slices contain
\[
  ZZ,\quad JJ,\quad ZJ,\quad JZ,\quad XX.
\]
The algebra generated jointly by the two legs is all of \(M_4(\mathbb C)\):
for example,
\[
  (ZI)(ZZ)=IZ,\qquad (JI)(JJ)=-IJ,
\]
and the first- and second-qubit matrix algebras together generate \(M_4\).

After identity amplification by an \(m\)-dimensional ancilla \(W\), the
joint local leg algebra is
\[
  M_4(\mathbb C)\otimes I_W.
\]
Any local projection \(E\) which reduces both leg algebras therefore lies
in their commutant,
\[
  E\in I_4\otimes M_m(\mathbb C).
\]
It follows that
\[
  \operatorname{rank}E\in4\mathbb Z.
\]
In particular, the \(d=8\) identity amplification has no rank-six local
sector which is reducing for all one-leg coefficients.

This is intentionally narrower than ruling out every subspace
\(S\subset\mathbb C^8\) for which \(S\otimes S\) happens to be invariant.
Pairwise invariance alone does not automatically imply that the local
projection commutes with every leg slice, so no broader compression claim
is made here.

## 11. What remains open in this track

The reduced \(d=6\) route is now sharply identified:

\[
\boxed{
\begin{gathered}
K\in U(12),\qquad (K+I)(K-qI)=0,\\
\dim\ker(K+I)=6,\qquad K\text{ satisfies (HB) on dimension }72.
\end{gathered}}
\]

To evade all no-go lemmas above, such a \(K\) must genuinely mix the
three-dimensional middle factor (in every basis relevant to (CTRL)) and
must not arise merely by a unital Pauli/quaternion representation or by a
scalar-natural colored direct sum. An operator-valued colored extension,
a qutrit Weyl/group-algebra construction, or a genuinely heterogeneous
biunitary connection remains possible.

No claim of nonexistence at \(d=6\) follows from this track.

## 12. Reproducibility

Exact certificate:

```text
scripts/verify_track_additive_scalar_gluing.py
scripts/verify_track_additive_graph_flip_qutrit.py
scripts/verify_track_additive_su2_ansatz.py
scripts/verify_track_additive_s4_central.py
scripts/explore_track_additive_s4_symmetry.py
```

Recorded output:

```text
results/track_additive_scalar_gluing.txt
results/track_additive_graph_flip_qutrit.txt
results/track_additive_su2_ansatz.txt
results/track_additive_s4_central.txt
results/track_additive_s4_symmetry.txt
```

Command:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  /Users/alec/Documents/Math-kissing5/exceptional_ybe_spectrum/scripts/verify_track_additive_scalar_gluing.py

/Users/alec/Documents/Math/.venv/bin/python \
  /Users/alec/Documents/Math-kissing5/exceptional_ybe_spectrum/scripts/verify_track_additive_graph_flip_qutrit.py

/Users/alec/Documents/Math/.venv/bin/python \
  /Users/alec/Documents/Math-kissing5/exceptional_ybe_spectrum/scripts/verify_track_additive_su2_ansatz.py

/Users/alec/Documents/Math/.venv/bin/python \
  /Users/alec/Documents/Math-kissing5/exceptional_ybe_spectrum/scripts/verify_track_additive_s4_central.py

/Users/alec/Documents/Math/.venv/bin/python \
  /Users/alec/Documents/Math-kissing5/exceptional_ybe_spectrum/scripts/explore_track_additive_s4_symmetry.py
```

The scripts use exact SymPy arithmetic. The first verifies the table (MC)
and exhausts the controlled-middle parity statement for representative odd
values of \(b\); the written parity proof applies to every odd \(b\). The
second exhausts the qutrit graph-phase/global-flip class by exact
polynomial gcds. The third constructs both possible
\(SU(2)\)-equivariant half-rank involutions (up to sign) through the
Casimir and supplies an exact nonzero entry of the cubic residual. The
fourth rejects the central \(S_4\) projections exactly. The fifth is
explicitly a numerical falsifier of the remaining \(S_4\) branch; it is
retained for provenance and supports no theorem.
