# A Catalan determinant divisor for the Teufl Wagner forest transfer matrix

## Statement and scope

Let \(n\geq1\), let \(A=(a_{ij})_{1\leq i,j\leq n}\) be a matrix of independent commuting indeterminates, and set
\[
R_{\mathbb Z}=\mathbb Z[a_{ij}:1\leq i,j\leq n],
\qquad C_n=\frac1{n+1}\binom{2n}{n}.
\]
Let \(X=\{x_1,\ldots,x_n\}\) and \(Y=\{y_1,\ldots,y_n\}\) be disjoint labelled copies of \([n]\). The rows and columns below are indexed by **all** set partitions, in the same order after identifying either copy with \([n]\).

For each partition \(P\) of \(X\), choose one fixed unweighted tree on each block, including the empty tree on a singleton, and let \(F_P\) be their union. For a set
\[
E\subseteq\{x_i y_j:1\leq i,j\leq n\},
\qquad a_E=\prod_{x_i y_j\in E}a_{ij},
\]
call \(E\) admissible for \((P,Q)\) if the graph on \(X\sqcup Y\) with edge set \(F_P\cup E\) is a forest, every component meets \(Y\), and the nonempty intersections of its components with \(Y\) are exactly the blocks of \(Q\). Define
\[
T(P,Q)=\sum_{E\text{ admissible for }(P,Q)}a_E.
\tag{1}
\]
Each interlayer edge set is counted once. In particular, (1) does not sum over possible choices of trees inside the blocks of \(P\).

**Theorem.** For the matrix \(T=(T(P,Q))\),
\[
(\det A)^{C_n}\mid\det T
\qquad\text{in }R_{\mathbb Z}.
\tag{2}
\]
There is no symmetry, positivity, or planarity assumption on \(A\), on the chosen block trees, or on the admitted forests. This proves the stated divisibility in Problem 1 of Elmar Teufl and Stephan Wagner, “A determinant related to set partitions,” *Oberwolfach Reports* 23/2018, pp. 1457–1458. It makes no assertion that this is the exact exponent of \(\det A\), that the remaining factor is irreducible, or that the method is new.

The proof constructs a constant quotient of the partition space of dimension \(C_n\), and computes the determinant of the induced transfer operator exactly as \((\det A)^{C_n}\). All signs and normalizations used in that calculation are fixed below.

## 1  Exterior algebra and forest products

Work first over a characteristic-zero field. For every vertex \(v\), introduce two odd generators \(\xi_v,\bar\xi_v\). Thus any two generators anticommute, and their squares vanish. For an unordered edge \(uv\), put
\[
q_{uv}=(\xi_u-\xi_v)(\bar\xi_u-\bar\xi_v).
\tag{3}
\]
Reversing the edge orientation changes both factors' signs and leaves \(q_{uv}\) unchanged. The elements \(q_{uv}\) have even degree, commute with each other, and satisfy \(q_{uv}^2=0\).

For a finite graph \(H\), write \(q_H=\prod_{e\in E(H)}q_e\); the edge ordering is immaterial.

**Lemma 1.** If \(H\) contains a cycle, then \(q_H=0\). If \(H\) is a forest, \(q_H\) depends only on its partition into connected components.

**Proof.** Orient the edges and let \(u_e\) be the coefficient vector of the corresponding difference of vertex variables. If there are \(s\) edges, moving all barred factors to the right gives
\[
q_H=(-1)^{s(s-1)/2}
 \left(\bigwedge_e\xi(u_e)\right)
 \left(\bigwedge_e\bar\xi(u_e)\right).
\tag{4}
\]
Along a cycle the oriented edge vectors are linearly dependent, so the first wedge vanishes.

For a tree on a vertex set \(B\), its oriented edge vectors are a \(\mathbb Z\)-basis of the lattice
\[
U_{B,\mathbb Z}=
\left\{(c_v)_{v\in B}\in\mathbb Z^B:\sum_{v\in B}c_v=0\right\}.
\]
Indeed, relative to any root \(b\in B\), each vector \(e_v-e_b\) is an integral sum of oriented edge vectors along the unique path from \(b\) to \(v\). The tree has exactly \(|B|-1\) edges, so its edge vectors form an integral basis. Two such bases differ by a matrix of determinant \(+1\) or \(-1\). The same basis change occurs in the two wedges in (4), multiplying their product by the square of that determinant, which is \(1\). This proves tree independence on a block. Taking the product over the blocks proves the forest assertion. Singleton blocks contribute \(1\). ∎

For a set partition \(P\) of a finite vertex set, write \(f_P\) for this common block-forest product. In particular, \(f_P=q_{F_P}\) for the fixed forest in (1).

## 2  Integration gives exactly the stated transfer matrix

Order the odd generators with all \(X\) pairs first and then all \(Y\) pairs, and within \(X\) use
\[
\Omega_X=\xi_{x_1}\bar\xi_{x_1}\cdots\xi_{x_n}\bar\xi_{x_n}.
\]
Define \(\mathcal I_X\) to extract the coefficient of \(\Omega_X\), placing this factor to the left of the remaining \(Y\) generators. This is algebraic coefficient extraction; no analytic integral is involved. Define
\[
G_A f=\mathcal I_X\left[
 \exp\left(\sum_{i,j}a_{ij}q_{x_i y_j}\right)f
\right].
\tag{5}
\]
All exponential series in this proof terminate because their arguments have positive exterior degree.

**Lemma 2.** For every partition \(P\) of \(X\),
\[
G_Af_P=\sum_Q T(P,Q)f_Q.
\tag{6}
\]

**Proof.** Since the \(q_{x_i y_j}\) commute and square to zero,
\[
\exp\left(\sum_{i,j}a_{ij}q_{x_i y_j}\right)
=\prod_{i,j}(1+a_{ij}q_{x_i y_j})
=\sum_E a_Eq_E.
\tag{7}
\]
There is one summand for each edge subset \(E\), with coefficient exactly \(a_E\). Multiplication by \(f_P\) gives the edge product of \(F_P\cup E\).

If this graph contains a cycle, the product is zero by Lemma 1. If it is a forest with a component consisting of \(k\) vertices of \(X\) and no vertex of \(Y\), that component's factor has degree \(2(k-1)\). It cannot supply all \(2k\) odd generators on those vertices, so its contribution to \(\mathcal I_X\) is zero.

In every remaining case, choose one \(Y\) root in each component. By Lemma 1, replace the component's tree product by that of the star at this root, without changing the exterior element. Every \(X\) vertex is now a leaf. For an \(X\) leaf \(x\) with root \(y\), the coefficient of \(\xi_x\bar\xi_x\) in
\[
q_{xy}=\xi_x\bar\xi_x-\xi_x\bar\xi_y
       -\xi_y\bar\xi_x+\xi_y\bar\xi_y
\]
is \(+1\). No other factor contains either generator at \(x\), so both must be taken from this first term. The pairs have even degree and commute, giving coefficient \(+1\) for all \(X\) pairs in the prescribed order. The remaining factors are the stars on the component intersections with \(Y\), whose product is \(f_Q\). Precisely the edge sets in (1) therefore survive, each with weight \(a_E\) and with no additional multiplicity or sign. ∎

Only the fixed internal trees stipulated in (1) were used in this expansion. The temporary replacement by stars is an identity of exterior elements for an already selected graph; it does not introduce additional summands.

## 3  A constant invariant quotient of the partition space

Let
\[
U=\left\{u=(u_1,\ldots,u_n)\in\mathbb Q^n:
                  \sum_i u_i=0\right\},\qquad m=n-1,
\]
and regard its elements as row coefficient vectors. On one layer set
\[
\xi(u)=\sum_i u_i\xi_i,\qquad
\bar\xi(u)=\sum_i u_i\bar\xi_i.
\]
Let \(V=\mathbb Q^2\) be the standard representation of \(\mathrm{SL}_2\). The difference algebra on the layer is
\[
\mathcal E=\Lambda(U\otimes V),
\]
where the two generators associated with \(u\) are \(\xi(u)\) and \(\bar\xi(u)\). Put
\[
W=\mathcal E^{\mathrm{SL}_2}.
\tag{8}
\]
The group acts simultaneously on all these pairs. Each \(q_{ij}\), and hence each \(f_P\), is invariant.

We prove the spanning statement and dimension directly, without requiring an external invariant-basis theorem.

### 3.1  A weight-space calculation

Consider a tensor power of the standard complex representation, or an exterior power of a direct sum of copies of it. With the natural Hermitian inner product, let \(E,F,H\) be the usual infinitesimal operators, normalized by
\[
[E,F]=H,\qquad E^*=F,
\]
with weights \(+1\) and \(-1\) on the two standard basis vectors. The identities extend to tensor and exterior powers by the induced derivation actions. Write \(M_k\) for the weight-\(k\) subspace of any such module.

**Lemma 3.** Its invariant dimension is
\[
\dim M^{\mathrm{SL}_2}=\dim M_0-\dim M_2.
\tag{9}
\]

**Proof.** If \(v\in M_0\) and \(Ev=0\), then
\[
\|Fv\|^2=\langle v,EFv\rangle
=\langle v,(FE+H)v\rangle=0.
\]
Thus \(v\) is killed by \(E,F,H\). Being killed by \(E\) and \(F\) is equivalent to being fixed by their exponentials, the upper and lower unipotent one-parameter subgroups; those subgroups generate \(\mathrm{SL}_2\). Conversely, an invariant vector has weight zero and is killed by \(E\). Hence the invariant subspace is \(\ker(E:M_0\to M_2)\).

This map is surjective. A vector \(w\in M_2\) orthogonal to its image has \(Fw=0\), and hence
\[
2\|w\|^2=\langle w,[E,F]w\rangle
=\|Fw\|^2-\|Ew\|^2=-\|Ew\|^2.
\]
It follows that \(w=0\). Rank-nullity proves (9). The operators defining the kernels have rational matrices, so the dimensions are unchanged over \(\mathbb Q\). ∎

### 3.2  Generation by quadratic invariants

For \(u,v\in U\), put
\[
b(u,v)=\xi(u)\bar\xi(v)+\xi(v)\bar\xi(u).
\tag{10}
\]
This is the exterior image of the alternating invariant tensor in \(V\otimes V\), and is therefore invariant.

**Lemma 4.** The algebra \(W\) is generated by the elements (10).

**Proof.** First consider \(V^{\otimes2r}\). By (9), its invariant dimension is
\[
\binom{2r}{r}-\binom{2r}{r+1}
=\frac1{r+1}\binom{2r}{r}=C_r.
\tag{11}
\]
For every noncrossing perfect matching of the ordered positions \(1,\ldots,2r\), put a copy of
\[
\varepsilon=e_+\otimes e_- - e_-\otimes e_+
\]
in the two positions of each pair. The resulting tensor is invariant. There are \(C_r\) such matchings: record a plus sign at each left endpoint and a minus sign at each right endpoint. This gives a Dyck word, from which the unique noncrossing matching is recovered by the stack rule. The reflection of a word at its first prefix with more minus than plus signs counts the excluded words as \(\binom{2r}{r+1}\), proving the count.

Order tensor words lexicographically with \(e_+>e_-\). The leading word of a matching tensor has \(e_+\) at all left endpoints and \(e_-\) at all right endpoints, with coefficient \(1\). Every other term reverses at least one pair, and at the first changed position replaces \(e_+\) by \(e_-\), making it smaller. Distinct noncrossing matchings have distinct Dyck leading words, so these tensors are linearly independent. By (11), they form a basis of the invariant tensors. Thus all invariant tensors are spanned by paired copies of \(\varepsilon\). In odd degree there are no invariants because the central element \(-I\) acts as \(-1\).

Now take an invariant element of \(\Lambda^{2r}(U\otimes V)\). Normalized antisymmetrization embeds the exterior power equivariantly into \((U\otimes V)^{\otimes2r}\), with exterior projection as a left inverse. Rearranging ordinary tensor factors identifies the invariant tensor space with
\[
U^{\otimes2r}\otimes(V^{\otimes2r})^{\mathrm{SL}_2}.
\]
It is spanned by tensors paired in the \(V\) slots. Exterior projection of each is, up to the sign from rearranging slots, a product of expressions
\[
\xi(u)\bar\xi(v)-\bar\xi(u)\xi(v)=b(u,v).
\]
These products therefore span the exterior invariants. ∎

For \(n\geq2\), take the basis \(u_i=e_i-e_n\), \(1\leq i\leq m\), of \(U\). Expansion gives
\[
b(u_i,u_i)=2q_{in},\qquad
b(u_i,u_j)=q_{in}+q_{jn}-q_{ij}\quad(i\ne j).
\tag{12}
\]
Since \(b\) is bilinear, the \(q_{ij}\) generate \(W\). A monomial in them is zero if an edge is repeated, is zero if the distinct edges contain a cycle, and otherwise is \(f_P\) for the component partition of its forest, by Lemma 1. Hence the elements \(f_P\), for all set partitions \(P\), span \(W\).

Let \(\mathcal P_n\) be the set of partitions of \([n]\), and let \(V_n\) be the rational vector space with basis \(\{e_P:P\in\mathcal P_n\}\). We have proved that
\[
\Phi:V_n\longrightarrow W,\qquad e_P\longmapsto f_P
\tag{13}
\]
is a surjection. This map is defined over \(\mathbb Q\) and does not depend on \(A\). Its constancy is important when taking determinants over a polynomial ring.

### 3.3  The Catalan dimension

The central element \(-I\) shows that \(W\) has only even degrees. Write
\[
W=\bigoplus_{r=0}^m W_{2r},\qquad d_r=\dim W_{2r}.
\]
In \(\Lambda^{2r}(U\otimes V)\), a weight-zero monomial uses \(r\) unbarred and \(r\) barred generators, while a weight-two monomial uses \(r+1\) unbarred and \(r-1\) barred generators. Lemma 3 gives
\[
d_r=\binom mr^2-\binom m{r-1}\binom m{r+1},
\tag{14}
\]
where an out-of-range binomial coefficient is zero. Vandermonde's identity gives
\[
\begin{aligned}
d:=\dim W
&=\sum_{r=0}^m\left(\binom mr^2-\binom m{r-1}\binom m{r+1}\right)\\
&=\binom{2m}{m}-\binom{2m}{m-2}\\
&=\frac1{m+2}\binom{2m+2}{m+1}=C_n.
\end{aligned}
\tag{15}
\]
Also \(d_r=d_{m-r}\), so
\[
\sum_{r=0}^m 2r\,d_r=m d.
\tag{16}
\]

### 3.4  The determinant character

Each \(g\in\mathrm{GL}(U)\) acts by substitution on both copies of \(U\), commuting with \(\mathrm{SL}_2\), and hence acts on \(W\). Denote the action by \(\rho(g)\).

**Lemma 5.** For \(m>0\),
\[
\det\rho(g)=(\det g)^d.
\tag{17}
\]

**Proof.** On \(g=\operatorname{diag}(t_1,\ldots,t_m)\), the determinant of the action on \(W\) is a monomial \(\prod_i t_i^{\alpha_i}\). Indeed, the exterior algebra has a monomial weight basis, and the invariant subspace is stable under the diagonal torus and is the direct sum of its weight spaces. Conjugation by permutation matrices shows that all exponents are equal, say to \(\alpha\).

The scalar \(tI\) acts on \(W_{2r}\) as \(t^{2r}\), so (16) makes its determinant \(t^{md}\). The diagonal formula gives \(t^{m\alpha}\). Thus \(\alpha=d\), since \(m>0\). Equation (17) holds on diagonal matrices and hence on diagonalizable matrices. Over \(\mathbb C\), invertible matrices with distinct eigenvalues are Zariski dense. Both sides are polynomial functions of the entries of \(g\), so the identity holds on all of \(\mathrm{GL}(U)\), over \(\mathbb Q\) and every characteristic-zero extension. ∎

## 4  The determinant of the induced Gaussian transfer

Set
\[
R=\mathbb Q[a_{ij}],\qquad K=\mathbb Q(a_{ij}).
\]
Equation (6) and the constant surjection (13) show that \(G_A\) maps \(W_X\otimes R\) into \(W_Y\otimes R\). Identify these two spaces by their common labels. Thus \(G_A\) is a polynomial matrix on the constant \(d\)-dimensional space \(W\), although we will compute its determinant over \(K\).

Write the \(X\) generators as column vectors \(\xi,\bar\xi\) and the \(Y\) generators as \(\eta,\bar\eta\). Define
\[
r_i=\sum_j a_{ij},\quad c_j=\sum_i a_{ij},\quad
D=\operatorname{diag}(r_1,\ldots,r_n),\quad
E=\operatorname{diag}(c_1,\ldots,c_n),
\]
and
\[
B=D^{-1}A,\qquad S=E-A^{\mathsf T}D^{-1}A.
\tag{18}
\]
The elements \(r_i\) and \(\det A\) are nonzero in \(K\), so \(D\) and \(B\) are invertible there. For the all-ones column \(\mathbf1\),
\[
B\mathbf1=\mathbf1,\qquad S^{\mathsf T}=S,\qquad S\mathbf1=0.
\tag{19}
\]
The last identity follows from \(A\mathbf1=D\mathbf1\) and \(A^{\mathsf T}\mathbf1=E\mathbf1\). Symmetry gives zero column sums too.

The exponent in (5) has the exact completion
\[
\begin{aligned}
\sum_{i,j}a_{ij}q_{x_i y_j}
&=\xi^{\mathsf T}D\bar\xi-\xi^{\mathsf T}A\bar\eta
  -\eta^{\mathsf T}A^{\mathsf T}\bar\xi+\eta^{\mathsf T}E\bar\eta\\
&=(\xi-B\eta)^{\mathsf T}D(\bar\xi-B\bar\eta)
  +\eta^{\mathsf T}S\bar\eta.
\end{aligned}
\tag{20}
\]
No odd factors were interchanged in this expansion, so no implicit sign adjustment is present.

### 4.1  The lowering operator

Introduce \(n\) new pairs \(z_i,\bar z_i\), ordered before the remaining variables for coefficient extraction. Define
\[
H_D f(\xi,\bar\xi)
=\frac1{\det D}\mathcal I_z\left[
 \exp(z^{\mathsf T}D\bar z)\,
 f(z+\xi,\bar z+\bar\xi)\right].
\tag{21}
\]

**Lemma 6.** The operator \(H_D\) preserves \(W\otimes K\), and its determinant on that space is \(1\).

**Proof.** In the difference algebra all arguments of \(f\) can be written as differences. After substitution they become
\[
(z_i-z_j)+(\xi_i-\xi_j),\qquad
(\bar z_i-\bar z_j)+(\bar\xi_i-\bar\xi_j).
\]
Extracting a \(z\) coefficient therefore leaves a polynomial in differences of the remaining variables. Thus the difference algebra is preserved.

Simultaneous \(\mathrm{SL}_2\) substitution on the \(z\) and \(\xi\) pairs preserves every \(z_i\bar z_i\), the exponential, and the top form \(\prod_i z_i\bar z_i\). The substitution \(z+\xi\) is equivariant. Coefficient extraction is equivariant too, as the projection onto that invariant top \(z\)-degree. Hence \(H_D\) preserves invariants.

The term of \(f(z+\xi,\bar z+\bar\xi)\) using no \(z\) variable is \(f(\xi,\bar\xi)\), and
\[
\mathcal I_z\exp(z^{\mathsf T}D\bar z)
=\mathcal I_z\prod_i(1+r_i z_i\bar z_i)
=\prod_i r_i=\det D.
\tag{22}
\]
Thus the degree-preserving part of (21) is the identity. Every other surviving term uses a positive even number of \(z\) generators from \(f\): the exponential contributes either both \(z_i,\bar z_i\) or neither, so \(f\) must supply both missing generators. Such a term strictly lowers the degree in the remaining variables. The resulting matrix is triangular by degree, with diagonal entries \(1\), proving the determinant claim. ∎

### 4.2  The raising operator

Define
\[
M_Sh=\exp(\eta^{\mathsf T}S\bar\eta)h.
\tag{23}
\]

**Lemma 7.** The operator \(M_S\) preserves \(W\otimes K\), and its determinant on that space is \(1\).

**Proof.** The zero row and column sums give
\[
\eta^{\mathsf T}S\bar\eta
=\sum_{i,j<n}S_{ij}(\eta_i-\eta_n)(\bar\eta_j-\bar\eta_n).
\tag{24}
\]
Because \(S\) is symmetric, this is a linear combination of the invariants (10): a diagonal term uses \(\tfrac12b(u,u)\), and each sum of terms at two distinct indices uses \(b(u,v)\). It lies in \(W_2\otimes K\). Multiplication by its exponential preserves \(W\). The exponential is \(1\) plus positive-degree terms, so \(M_S\) is triangular by degree, with diagonal entries \(1\). ∎

### 4.3  The middle substitution and exact factorization

For row coefficient vectors, substitution \(\xi=B\eta\) acts as \(u\mapsto uB\). By \(B\mathbf1=\mathbf1\), this preserves \(U\). Call its restriction \(g_B\). On the one-dimensional quotient by \(U\), the induced map is the identity, since
\[
(uB)\mathbf1=u\mathbf1.
\]
Taking determinants with respect to this invariant hyperplane gives
\[
\det g_B=\det B=\frac{\det A}{\det D}.
\tag{25}
\]

Top coefficient extraction is invariant under the odd translation
\(\xi=z+B\eta,\ \bar\xi=\bar z+B\bar\eta\).
Indeed, translating a monomial cannot increase its degree in the integrated variables. Its full top-degree coefficient can come only from the full product of the original integrated generators, and this contributes the new full product with coefficient \(1\).

Use this change of variables in (20). All exponential arguments are even, so their exponentials commute. For \(f\in W\otimes K\), (5) becomes
\[
\begin{aligned}
G_Af(\eta,\bar\eta)
&=\exp(\eta^{\mathsf T}S\bar\eta)\,
 \mathcal I_z\left[\exp(z^{\mathsf T}D\bar z)
 f(z+B\eta,\bar z+B\bar\eta)\right]\\
&=(\det D)\,M_S\,\rho(g_B)\,H_D f.
\end{aligned}
\tag{26}
\]
This is an equality of operators in the displayed order. In particular, \(H_D\) is formed before substitution by \(B\); no commutation of these two operators is asserted or needed.

For \(n\geq2\), taking determinants and using Lemmas 5–7 gives
\[
\begin{aligned}
\det(G_A|W)
&=(\det D)^d\det M_S\det\rho(g_B)\det H_D\\
&=(\det D)^d\left(\frac{\det A}{\det D}\right)^d\\
&=(\det A)^d=(\det A)^{C_n}.
\end{aligned}
\tag{27}
\]
There is no undetermined sign or constant: (22), the translation coefficient \(1\), and the unit diagonals of \(H_D,M_S\) fix all of them. This equality over \(K\) is a polynomial identity in \(R\), because \(G_A\) already had polynomial entries before the temporary inversion of the row sums. No numerical row-sum restriction remains.

## 5  Lifting the quotient determinant to the full matrix

Extend (13) to \(R\), and define the endomorphism \(L_A\) of \(V_n\otimes R\) by
\[
L_Ae_P=\sum_QT(P,Q)e_Q.
\tag{28}
\]
With column-vector conventions its matrix is \(T^{\mathsf T}\), so \(\det L_A=\det T\). Equation (6) says
\[
\Phi L_A=G_A\Phi.
\tag{29}
\]
Let \(N=\ker(\Phi:V_n\to W)\). Since \(\Phi\) is a constant rational surjection, its kernel after extension of scalars is exactly \(N\otimes R\). By (29), this submodule is \(L_A\)-invariant.

Choose a rational basis of \(N\), a rational basis of \(W\), and arbitrary rational lifts to \(V_n\) of that second basis. Together these form a constant basis of \(V_n\), in which
\[
L_A\sim\begin{pmatrix}
K_A&*\\
0&G_A
\end{pmatrix}
\tag{30}
\]
with \(K_A\) a matrix over \(R\). The change of basis is independent of \(A\), so its denominators are rational constants and introduce no variable denominators. Consequently
\[
\det T=(\det K_A)(\det A)^{C_n}
\quad\text{in }\mathbb Q[a_{ij}].
\tag{31}
\]
The determinant of an empty kernel block is understood as \(1\).

By (1), \(\det T\in\mathbb Z[a_{ij}]\). The polynomial \(\det A\) is primitive over \(\mathbb Z\), since its nonzero coefficients are \(+1\) or \(-1\); hence its power is primitive by Gauss's lemma. Multivariate Gauss's lemma upgrades (31) to divisibility over \(\mathbb Z\). Explicitly, write any nonzero rational quotient as \((a/b)h\), where \(h\) is an integral primitive polynomial and \(\gcd(a,b)=1\). The product \((\det A)^{C_n}h\) is primitive, so integrality of \((a/b)(\det A)^{C_n}h\) forces \(b=1\). A zero quotient is already integral.

For \(n=1\), there is one partition and the only admissible interlayer edge set is \(\{x_1y_1\}\). Thus \(T=(a_{11})\), \(\det A=a_{11}\), and \(C_1=1\), proving the remaining case and completing the proof. ∎

## 6  Attribution and source scope

The exterior forest algebra and Gaussian elimination above belong to established work. No novelty claim is made for these tools, for the Catalan-dimensional quotient, or for this reconstruction.

1. **Problem source.** Elmar Teufl and Stephan Wagner, “A determinant related to set partitions,” in *Enumerative Combinatorics*, *Oberwolfach Reports* 23/2018, printed pp. 1457–1458. The generic Bell-state determinant divisibility is Problem 1 on p. 1458. [Report DOI](https://doi.org/10.4171/OWR/2018/23); [public report PDF](https://ems.press/content/serial-article-files/46745).

2. **Forest algebra and elimination.** Sergio Caracciolo, Alan D. Sokal, and Andrea Sportiello, *Grassmann Integral Representation for Spanning Hyperforests*, *Journal of Physics A* **40** (2007), 13799–13835. [DOI 10.1088/1751-8113/40/46/001](https://doi.org/10.1088/1751-8113/40/46/001); [arXiv record](https://arxiv.org/abs/0706.1509); [version 2 PDF](https://arxiv.org/pdf/0706.1509v2). In that version, Section 4, Corollaries 4.3–4.5 (pp. 15–17), gives the forest algebra and exponential forest expansion. Section 5, Lemma 5.1 and Corollary 5.2 (pp. 18–19), gives elimination. The Catalan-basis statement is announced on p. 17 with proof deferred; the associated reference [39] on p. 49 is listed as “in preparation,” so that entry alone is not a completed proof citation.

3. **Detailed basis treatment.** Andrea Sportiello, *Combinatorial methods in Statistical Field Theory: Trees, loops, dimers and orientations vs. Potts and non-linear σ-models*, Scuola Normale Superiore, Tesi di Perfezionamento. [Public thesis PDF](https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf). Chapter 10, Theorem 10.3, printed p. 207, gives the basis theorem. The relevant triangular argument is Lemma 10.6, stated on p. 208 and proved on pp. 211–213. The \(\lambda=0\) case is supported by the normalized forest-polynomial formulation in equation (10.3), p. 196, the polynomial/no-division convention on p. 197, and the \(\lambda\)-independent leading coefficients \(+1\) or \(-1\) in the triangular argument on pp. 211–213. This is not an assertion obtained by naively substituting \(\lambda=0\) into unnormalized scalar products. The nonplanar transfer setting is discussed on p. 195.

These are attributions of prior work, not additional hypotheses: Sections 1–5 establish the forest identities, exact counting, invariant spanning, Catalan dimension, Gaussian determinant, and integral descent within this report. The noncrossing matchings in Lemma 4 are only an invariant-tensor basis argument. They impose no noncrossing or planar restriction on the partitions indexing \(T\) or the forests it counts.

## 7  Reconstruction provenance

This is a newly written reconstruction dated 9 October 2026. It restores the specified proof strategy and theorem; it does not claim byte-for-byte recovery of an earlier report. A checksum or review attached to an earlier file does not certify this file. A checksum of the reconstruction must be calculated from the present bytes, and a fresh assessment must examine the present text.

This reconstruction adds no new approach, enlarges no theorem, and claims neither publication nor a fresh independent acceptance. It does not infer optimality of the determinant exponent. Its output is the self-contained proof above, with explicit attribution and conventions. No third-party source document or dataset is reproduced as part of the report.
