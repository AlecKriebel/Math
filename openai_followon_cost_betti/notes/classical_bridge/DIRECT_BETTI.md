# Direct computation of the group's L2-Betti numbers

2026-10-06, approximately 21:39 America/Los_Angeles.

This is an additional mechanism, independent of both upstream cost bounds.
It computes the invariant of the explicitly presented group; it supplies
no positive cost gap. The original relation-level target therefore still
depends on validation of the Bernoulli cost lower bound.

## Claim and precise presentation

Let

\[
 A=F(a,b_1,\ldots,b_{99}),\quad
 u_0=1,\quad u_i=u_{i-1}ab_i,\quad w=u_{99}a,
 \quad J=\langle b_1,\ldots,b_{99},w\rangle\leq A.
\]

Set \(\Gamma=A*_J(J\times\langle t\rangle)\), where \(t\) has infinite
order. The elementary embedding checks from `REPORT.md` identify A and
\(J\times\langle t\rangle\) with subgroups of \(\Gamma\). The universal
property of the amalgam gives the equivalent presentation

\[
 \Gamma=\langle a,b_1,\ldots,b_{99},t\mid
 r_i=t b_i t^{-1}b_i^{-1}\ (1\leq i\leq99),\quad
 r_w=twt^{-1}w^{-1}\rangle.
\tag{1}
\]

Indeed commuting with the displayed generators of J is equivalent to
commuting with every element of J. There are 101 generators and exactly
100 relators in (1). The claim is

\[
                 \beta_n^{(2)}(\Gamma)=0\qquad(n\geq0).
\tag{2}
\]

For the original target, only the n=0,1 part is needed. The all-degree
claim is included because the argument also proves the presentation
complex is a finite two-dimensional classifying space.

## 1. The relevant free basis and operator

The elements \(a,u_1,\ldots,u_{99}\) form a free basis of A. This can be
verified without assuming independence of a list of words: the inverse
basis substitution is

\[
                 b_i=a^{-1}u_{i-1}^{-1}u_i\quad(1\leq i\leq99).
\tag{3}
\]

Substituting the definitions of u_i proves (3); substituting (3) back
recovers each u_i successively. The two homomorphisms between the free
groups on the old and new abstract bases are inverse. Hence
\(F=\langle u_1,\ldots,u_{99}\rangle\) is a freely embedded subgroup of A
of rank 99, and also embeds in \(\Gamma\).

Put

\[
                         S=\sum_{j=0}^{99}u_j
                           =1+u_1+\cdots+u_{99}\in\mathbb C F.
\tag{4}
\]

Both left and right convolution by S are injective on \(\ell^2(F)\),
and hence on \(\ell^2(\Gamma)\). A self-contained proof follows.

Construct a bipartite graph with vertex set \(F_L\sqcup F_R\) and edges
\(g_L\)--\((g u_i)_R\), for \(g\in F\), \(0\leq i\leq99\).
It is connected and 100-regular: the label-zero matching connects the
two copies, and two-edge paths implement multiplication by each
\(u_i^{\pm1}\). It has no cycle. In fact a nonbacktracking closed walk
would give a word

\[
 u_{i_1}u_{j_1}^{-1}\cdots u_{i_k}u_{j_k}^{-1}=1
\]

whose consecutive edge labels are distinct. Delete the factors with
index zero. There are no two consecutive zero labels. Deleting one
zero brings together factors of the same sign, which cannot cancel;
adjacent opposite-sign factors left in the word have distinct indices.
At least one nonidentity factor remains. Thus the result is a nonempty
freely reduced word, contradicting the free-basis property. The graph
is consequently the infinite 100-regular tree.

**Regular-tree lemma.** Adjacency on the infinite d-regular tree has
trivial kernel on \(\ell^2\), for every integer \(d\geq2\).

Root the tree at o, set \(q=d-1\), and let
\(E_n=\sum_{\operatorname{dist}(o,v)=n}|f(v)|^2\). If Af=0, then
at every vertex v of depth n>=1,

\[
 \sum_{z\text{ child of }v}f(z)=-f(\operatorname{parent}(v)),\qquad
 \sum_{z\text{ child of }v}|f(z)|^2
 \geq\frac{|f(\operatorname{parent}(v))|^2}{q}.
\]

Summing over depth n>=2 counts every depth n+1 vertex once and every
depth n-1 parent exactly q times. Hence \(E_{n+1}\geq E_{n-1}\).
Both sequences \(E_1,E_3,\ldots\) and \(E_2,E_4,\ldots\) are
nonnegative and nondecreasing. Since \(\sum_n E_n<\infty\), both
sequences vanish identically. The equation at a neighbor of o now
forces f(o)=0. This proves the lemma. Adjacency is bounded, since
\(\|Af\|_2\leq d\|f\|_2\), so the pointwise equations apply to
the Hilbert-space operator without a domain issue.

For explicit convolution conventions, set

\[
 (Tf)(g)=\sum_{i=0}^{99}f(gu_i),\qquad
 (T^*f)(g)=\sum_{i=0}^{99}f(gu_i^{-1}).
\]

Tree adjacency is \(\begin{pmatrix}0&T\\T^*&0\end{pmatrix}\), so
both T and T* are injective. Right convolution by S on coefficient
functions is \(fS=T^*f\). Left convolution is conjugate to T by the
unitary map \((If)(g)=f(g^{-1})\), and is also injective. Their
adjoints are injective as well.

Right convolution preserves each **left** coset \(gF\) of F in Gamma.
The orthogonal sum decomposition over these cosets identifies it with a
direct sum of copies of the same operator on \(\ell^2(F)\). Hence it
is injective on \(\ell^2(\Gamma)\). Left convolution similarly uses
**right** cosets \(Fg\). No ambient torsion-free hypothesis is hidden
in this transfer.

Finally, right multiplication by t-1 is injective on
\(\ell^2(\Gamma)\). A vector f satisfying f(t-1)=0 has coefficients
constant along each infinite orbit of right multiplication by t.
Square summability forces each such constant to vanish. This uses
the verified infinite order of t, not a conjecture about Gamma.

The special operator proof was independently found by the root agent
and the `special_s_injectivity` child. The child's complete conventions
and boundary checks appear in `special_s/PROOF.md`.

## 2. Cellular boundary calculation, with multiplication order fixed

Take the usual presentation complex K for (1), with one vertex, 101
oriented one-cells, and 100 two-cells. Its universal cover has cellular
chains which are free **left** Gamma-modules, written with coefficients
to the left of the chosen lifted cells. Thus the completed chain spaces
and operators are

\[
 \ell^2(\Gamma)^{100}\xrightarrow{d_2}
 \ell^2(\Gamma)^{101}\xrightarrow{d_1}\ell^2(\Gamma),
 \qquad d_1(f)=\sum_x f_x(x-1).
\tag{5}
\]

The multiplication appearing in coordinate formulas is **right**
convolution. This is compatible with left Gamma equivariance.

The lifted path for a word contributes its prefix before each positive
letter to the corresponding edge, and minus its prefix after each
negative letter. Equivalently these are left Fox derivatives
\(D_x(vz)=D_x(v)+vD_x(z)\),
\(D_x(x^{-1})=-x^{-1}\). Consequently, with
\(P_i=u_{i-1}a\),

\[
                    D_a w=S,\qquad D_{b_i}w=P_i.
\]

Evaluated in Gamma, the commutator rows are

\[
\begin{array}{c|ccc}
 &a&b_i&t\\ \hline
 r_j&0&\delta_{ij}(t-1)&1-b_j\\
 r_w&(t-1)S&(t-1)P_i&1-w.
\end{array}
\tag{6}
\]

For example \(D_x(twt^{-1}w^{-1})=tD_xw-D_xw\) for
x=a or b_i, since the evaluated relator is one; for the t-column,
\(D_t r_w=1-twt^{-1}=1-w\). Thus for a two-chain
\(q=(q_1,\ldots,q_{99},q_w)\), formula (6) reads exactly

\[
\begin{split}
 (d_2q)_a&=q_w(t-1)S,\\
 (d_2q)_{b_i}&=q_i(t-1)+q_w(t-1)P_i,\\
 (d_2q)_t&=\sum_{i=1}^{99}q_i(1-b_i)+q_w(1-w).
\end{split}
\tag{7}
\]

These formulas can also be checked by the fundamental telescoping
identity

\[
       S(a-1)+\sum_iP_i(b_i-1)=w-1.
\]

The corresponding d1d2 row is
\((t-1)(w-1)+(1-w)(t-1)=tw-wt=0\). The b_i rows
likewise give \(tb_i-b_it=0\). In particular, the factor order
in (7) is not left unspecified or silently commuted.

If d2q=0, its a-coordinate gives q_w(t-1)S=0. Injectivity of
right convolution by S gives q_w(t-1)=0, and injectivity of
right convolution by t-1 gives q_w=0. The b_i coordinates now
give q_i(t-1)=0, hence every q_i=0. Therefore

\[
                            \ker d_2=\{0\}.
\tag{8}
\]

Changing to opposite module conventions replaces the operators by
appropriately transposed/involuted ones; the displayed convention is
fixed throughout, so no such conversion is needed in this proof.

## 3. Degree-one von Neumann dimension argument

The orthogonal complement of the image of d1 consists of vectors
fixed by translation by every listed generator. Such a vector is
constant on Gamma. Since Gamma is infinite, it must be zero in
\(\ell^2(\Gamma)\). Thus d1 has dense image, of von Neumann
dimension one. The dimension rank formula gives

\[
           \dim_\Gamma\ker d_1=101-1=100,
           \qquad
           \dim_\Gamma\overline{\operatorname{im}d_2}=100-0=100.
\]

Since the second closed submodule is contained in the first, their
quotient has dimension zero. Equivalently the orthogonal complement
has dimension zero and is zero, by faithfulness of the trace. Hence
the reduced first L2 homology vanishes, as does beta_0.

This already computes \(\beta_1^{(2)}(\Gamma)\) without an
asphericity assumption: any presentation complex can be completed to
a classifying space by attaching cells of dimensions >=3, leaving
d1 and d2, and thus degree-one homology, unchanged. Alternatively
the next paragraph proves asphericity directly in this case.

## 4. Asphericity and the all-degree consequence

The injectivity in (8) restricts to injectivity on finitely supported
integral chains. Thus the ordinary cellular H2 of the universal cover
of K is zero. That cover is a simply connected, two-dimensional CW
complex: H1 is zero and all H_n for n>2 are zero. It is therefore
acyclic and simply connected. Hurewicz, successively in each degree,
then gives trivial homotopy groups, and Whitehead gives contractibility.
So K is a finite two-dimensional K(Gamma,1).

Its L2 chain complex stops in degree two. Equation (8) gives beta_2=0,
all higher Betti numbers vanish by dimension, and section 3 gives
beta_0=beta_1=0. This proves (2). The Euler characteristic is indeed
\(1-101+100=0\), consistent with the computation, but it is not the
reason for injectivity.

## 5. Why the proposed Euler/Mayer--Vietoris shortcut alone is insufficient

The graph-of-spaces construction also has Euler characteristic
\(\chi(A)+\chi(J\times\mathbb Z)-\chi(J)=-99+0-(-99)=0\).
For a two-dimensional classifying space and an infinite group this
only yields beta_1=beta_2. It allows both numbers to be positive.

Similarly, vanishing of the Betti numbers of the direct-product vertex
group does not by itself show that the map from the amalgamated
subgroup's degree-one homology to that of A has trivial kernel. Both
J and A have beta_1=99. An operator between modules of equal dimension
can have nonzero kernel and cokernel of equal dimension. A genuine
injectivity mechanism is required; sections 1--2 provide it for this
specific subgroup embedding. No general Mayer--Vietoris assertion
is being used as a substitute for that check.

## Classical sources, validation, and scope

- The von Neumann dimension rank and faithfulness facts are Gaboriau
  2002, Properties 1.2(1),(3), printed p. 106, already inspected in
  the classical audit. All chain modules and operators here are
  bounded and have finite von Neumann dimension.
- Fox calculus is classical: R. H. Fox, *Free differential calculus.
  I. Derivation in the free group ring*, Annals of Mathematics (2)
  **57** (1953), 547--560, DOI
  [10.2307/1969736](https://doi.org/10.2307/1969736). The matrix
  conventions are also described in Fox II, **59** (1954), 196--210,
  section 2, pp. 198--199, and section 7, p. 210. Here the actual
  entries were derived from the lifted attaching loops rather than
  assumed from an uncited formula.
- An alternative input for section 1 is P. A. Linnell, *Zero divisors
  and L2(G)*, C. R. Acad. Sci. Paris Ser. I Math. **315** (1992),
  49--53, Theorem 2, p. 50, specialized to H=1 and a free group.
  The actual statement and its surrounding conventions were visually
  inspected in the
  [author-hosted primary PDF](https://personal.math.vt.edu/linnell/research/zerol2.pdf).
  Linnell--Puls, *Zero Divisors and Lp(G), II*, New York J. Math.
  **7** (2001), 49--58, explicitly reaffirms the free-group L2 result
  on p. 51 and at the start of section 6, p. 53.
  This heavy analytic theorem is **not required** by the final proof
  above, because the particular S has the elementary tree proof.

The direct computation uses only the elementary group presentation
and embedding properties. It does not use either upstream cost
bound, a finite permutation model, a rank estimate, or a planar word
lemma. It proves no cost lower bound. Its operators are injective but
are not asserted to have bounded inverses or positive least singular
values. A priority audit must still determine whether this specific
computation or the all-degree conclusion was already publicly stated;
classical ingredients and a fresh local derivation do not establish
novelty by themselves.

Assigned direct-invariant computation completion estimate: 100% for
the proof presented here; publication package contribution: research
addendum only, no deposit files or metadata. The proof remains subject
to the project's required adversarial and complete-package reviews.
