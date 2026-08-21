# Arbitrary qutrit graph-orbit codes: exact reductions and obstructions

## Scope

For a qutrit graph \(A\), a nonzero syndrome \(s\), and the signed coset
integers
\[
 K_{a,b}(A,s)=
 \sum_{\substack{t\in\mathbb F_3^n\\s\cdot t=-b}}
 (-1)^{n-w_a(t)}2^{w_a(t)},                                  \tag{1}
\]
where
\[
 w_a(t)=\#\{i:(t_i,(At)_i+a s_i)\ne(0,0)\},
\]
the graph-orbit endpoint problem is
\[
 2K_{0,0}+K_r\ge0,\qquad
 r\in\{(1,0),(0,1),(1,1),(1,2)\}.                            \tag{2}
\]
This note reduces all four inequalities, over the universe of all
graphs, to one Fourier-dominance assertion.  It then gives two exact
forms of that assertion:

- an alternating cut-rank polynomial with a one-vertex extension;
- a sum of quadratic Gauss sums over \(\mathbb F_3\).

Neither form has yielded an all-\(n\) proof.  A naive vertex-deletion
inequality is disproved by an exact three-vertex local contribution.
No graph-code counterexample was found.

New exact finite information is also obtained: every graph-orbit code
through \(n=5\) satisfies (2).  The five-site result is a finite
certificate, not an inference about arbitrary length.

## Research log

- **2026-07-28 15:18 PDT.** Reduced arbitrary fixed logical Weyl lines
  to pairs of orthogonal stabilizer states and proved that every such
  pair is locally Clifford-equivalent to
  \(\{|G_A\rangle,Z^s|G_A\rangle\}\).
- **2026-07-28 15:29 PDT.** Derived the Fourier DC-dominance and
  alternating cut-rank formulas.
- **2026-07-28 15:38 PDT.** Expressed the syndrome term as a cut-rank
  polynomial of the graph obtained by adjoining one apex with
  neighborhood \(s\).
- **2026-07-28 15:46 PDT.** Found an exact five-chirp identity for the
  local radial weight and hence a quadratic Gauss-sum representation.
- **2026-07-28 15:51 PDT.** Exhaustively checked every graph and
  syndrome through \(n=5\) by an exact ternary Fourier transform.
- **2026-07-28 16:01 PDT.** Isolated the negative deletion-pair
  obstruction and completed this checkpoint.

## 1. One logical line suffices over the universe of all graphs

The reduction uses only finite-dimensional linear algebra.  It is useful
beyond this particular endpoint.

### Lemma 1.1 (subspace transversal)

Let \(E_1,\ldots,E_n\) be subspaces of an \(n\)-dimensional vector space
\(W\).  Suppose
\[
 \dim\left(\sum_{i\in S}E_i\right)\ge |S|
 \quad\text{for every }S\subseteq[n].                         \tag{3}
\]
Then there are \(e_i\in E_i\) such that \(e_1,\ldots,e_n\) form a basis
of \(W\).

#### Proof

Induct on \(n\).  If a nonempty proper set \(S\) is tight in (3), apply
the induction hypothesis to \((E_i)_{i\in S}\) inside
\(\sum_{i\in S}E_i\).  In the quotient by this \(|S|\)-dimensional
space, the remaining subspaces still satisfy (3), because for
\(T\subseteq S^c\),
\[
 \dim\frac{\sum_{i\in S\cup T}E_i}{\sum_{i\in S}E_i}
 \ge |S|+|T|-|S|=|T|.
\]
Choose the remaining representatives in the quotient and lift them.

If there is no nonempty proper tight set, choose any nonzero
\(e_n\in E_n\) and pass to \(W/\langle e_n\rangle\).  For every
\(S\subseteq[n-1]\),
\[
 \dim\left(\sum_{i\in S}E_i+\langle e_n\rangle\right)
 /\langle e_n\rangle
 \ge |S|,
\]
because every nonempty such \(S\) has
\(\dim\sum_{i\in S}E_i\ge|S|+1\).  Induction in the quotient and then
adjoining \(e_n\) completes the proof. \(\square\)

### Lemma 1.2 (local graph form for a stabilizer pair)

Let \(L\subseteq(\mathbb F_3^2)^n\) be Lagrangian for the coordinatewise
symplectic form.  There is a block-diagonal local symplectic
transformation taking \(L\) to
\[
 L_A=\{(t,At):t\in\mathbb F_3^n\},                            \tag{4}
\]
where \(A\) is symmetric with zero diagonal.

Consequently, any two orthogonal stabilizer states having the same
Lagrangian label space are locally Clifford-equivalent, up to phases,
to
\[
 |G_A\rangle,\qquad Z^s|G_A\rangle                           \tag{5}
\]
for some \(s\ne0\).

#### Proof

Choose a generator matrix of \(L\).  At coordinate \(i\), its two
columns span a subspace \(E_i\) of the dual of the generator-row space.
For \(S\subseteq[n]\), the dimension of \(\sum_{i\in S}E_i\) is the
dimension of the projection of \(L\) to the sites in \(S\).  The kernel
of that projection is an isotropic subspace supported on \(S^c\), hence
has dimension at most \(|S^c|\).  Since \(\dim L=n\),
\[
 \dim\sum_{i\in S}E_i\ge n-|S^c|=|S|.                        \tag{6}
\]

Lemma 1.1 selects one linear combination from each local column pair so
that the \(n\) selected columns are independent.  A local symplectic
change makes each selected combination the local \(X\)-column.  Row
reduction then puts the generator in the form
\[
 [\,I\mid A\,].
\]
Isotropy gives \(A=A^\mathsf T\).  The local shear
\((x_i,z_i)\mapsto(x_i,z_i-A_{ii}x_i)\) removes the diagonal without
altering any off-diagonal entry.  This proves (4).

For completeness, every one-site symplectic matrix used here is
implemented by a qutrit Clifford: the Fourier transform implements
\((x,z)\mapsto(-z,x)\), the quadratic phase gate implements a shear, and
the permutation \(|j\rangle\mapsto|rj\rangle\), \(r\in\mathbb F_3^\times\),
implements a nonzero scaling.  Gaussian elimination in
\(\operatorname{SL}(2,\mathbb F_3)\) writes every local symplectic matrix
as a product of these operations.

After fixing one stabilizer character to \(+1\) by a Pauli correction,
the second state's character is a nonzero linear functional of \(t\),
say \(s\cdot t\).  It is therefore \(Z^s|G_A\rangle\); nonzeroness of
\(s\) is equivalent to orthogonality. \(\square\)

Every fixed logical-Weyl eigenplane in a graph-orbit code is the span of
two distinct eigenstates of one physical Pauli normalizing the code.
Adjoining that Pauli label to the common codimension-one stabilizer label
space gives a Lagrangian shared by the two states; only their characters
differ.  Thus they are two orthogonal stabilizer states of the type in
Lemma 1.2.
The endpoint superoperator is covariant under local unitaries.  Hence:

### Corollary 1.3

To prove all four inequalities (2) for every graph and syndrome at a
fixed length, it is enough to prove the single line
\[
 2K_{0,0}(A,s)+K_{0,1}(A,s)\ge0                              \tag{7}
\]
for every graph \(A\) and every \(s\ne0\) at that length.

This reduction is over the complete universe of graphs.  For one fixed
graph, the local Clifford in Lemma 1.2 generally changes the graph.

## 2. Exact Fourier dominance

Put
\[
 \eta(x,z)=
 \begin{cases}
 -1,&(x,z)=(0,0),\\
 2,&(x,z)\ne(0,0),
 \end{cases}
\qquad
 f_A(t)=\prod_{i=1}^n\eta(t_i,(At)_i).                       \tag{8}
\]
Define the ternary Fourier coefficient
\[
 F_A(s)=\sum_{t\in\mathbb F_3^n}f_A(t)\omega^{s\cdot t}.      \tag{9}
\]
Since \(f_A(-t)=f_A(t)\), every \(F_A(s)\) is real.

Let \(H_b=\sum_{s\cdot t=-b}f_A(t)\).  Then \(H_1=H_2\), and character
orthogonality gives
\[
 F_A(0)=H_0+2H_1,\qquad F_A(s)=H_0-H_1.                      \tag{10}
\]
Thus
\[
 \boxed{
 2K_{0,0}+K_{0,1}=F_A(0)+F_A(s),}                            \tag{11}
\]
and also
\[
 \boxed{
 3K_{0,1}=F_A(0)-F_A(s).}                                   \tag{12}
\]

The stronger two-sided assertion
\[
 \boxed{|F_A(s)|\le F_A(0)}                                  \tag{13}
\]
is therefore equivalent to (7) together with \(K_{0,1}\ge0\).
Every exact search performed here satisfies (13).

## 3. The alternating cut-rank formula

For \(R\subseteq[n]\), write \(C=R^c\) and
\[
 c_R=\operatorname {rank}_{\mathbb F_3}A_{R,C}.              \tag{14}
\]
Let
\[
 d_R=
 \mathbf1_{\{s_C\in\operatorname {row}(A_{R,C})\}}.           \tag{15}
\]

### Lemma 3.1

The fixed-line numerator has the exact form
\[
 \boxed{
 \frac{2K_{0,0}+K_{0,1}}{3^n2^n}
 =
 \sum_{R\subseteq[n]}
 \left(-\frac12\right)^{|R|}
 3^{-c_R}(1+d_R).}                                          \tag{16}
\]

#### Proof

Expand each local factor as
\[
 \eta(t_i,(At)_i)=
 2-3\mathbf1_{\{t_i=0,\ (At)_i=0\}}.                         \tag{17}
\]
For a fixed \(R\), impose the identity conditions at every \(i\in R\).
The remaining variables \(t_C\) obey
\[
 A_{R,C}t_C=0,\qquad s_C\cdot t_C=-b.                        \tag{18}
\]

For \(b=0\), the solution space has dimension
\[
 |C|-\operatorname {rank}
 \begin{bmatrix}A_{R,C}\\s_C^\mathsf T\end{bmatrix}.
\]
For \(b=1\), (18) is consistent exactly when
\(s_C\notin\operatorname {row}(A_{R,C})\).  If (15) holds, the
\(b=1\) count is zero and twice the homogeneous count is
\[
 2\cdot3^{|C|-c_R}.
\]
If (15) fails, all three counts entering \(2K_{0,0}+K_{0,1}\) equal
\(3^{|C|-c_R-1}\), and their sum is \(3^{|C|-c_R}\).
Multiplication by the subset coefficient
\((-3)^{|R|}2^{n-|R|}\) and extraction of \(3^n2^n\) gives (16).
\(\square\)

The summand is positive before the alternating factor.  Its exponent is
the graph cut-rank, a symmetric submodular function.  This is the exact
deletion/contraction target.

## 4. The apex extension

Adjoin a vertex \(*\) whose weighted neighborhood is \(s\):
\[
 A^+=
 \begin{bmatrix}
 A&s\\s^\mathsf T&0
 \end{bmatrix}.                                              \tag{19}
\]
For \(R\subseteq[n]\), let
\[
 r_R=\operatorname {cutrk}_{A^+}(R\cup\{*\})
 =\operatorname {rank}
 \begin{bmatrix}A_{R,C}\\s_C^\mathsf T\end{bmatrix}.          \tag{20}
\]
Thus \(r_R=c_R\) when \(d_R=1\), and \(r_R=c_R+1\) otherwise.  The
pointwise identity
\[
 3^{-c_R}(1+d_R)
 =\frac12\,3^{-c_R}+\frac32\,3^{-r_R}                        \tag{21}
\]
gives:

### Proposition 4.1 (one-vertex-extension formula)

Define
\[
 B_A(z)=\sum_{R\subseteq[n]}z^{|R|}3^{-c_R},\qquad
 H_{A,s}(z)=\sum_{R\subseteq[n]}z^{|R|}3^{-r_R}.              \tag{22}
\]
Then
\[
 \boxed{
 \frac{2K_{0,0}+K_{0,1}}{3^n2^n}
 =\frac12B_A(-1/2)+\frac32H_{A,s}(-1/2).}                    \tag{23}
\]

The first polynomial is a rank-one graph-state purity polynomial.  More
generally,
\[
 \mathcal B_A(z_1,\ldots,z_n)
 =\sum_R3^{-c_R}\prod_{i\in R}z_i                            \tag{24}
\]
is nonnegative on the full cube \([-1,1]^n\).  To see this directly,
first note that the reduced graph-state purity across the cut
\(R:R^c\) is exactly \(3^{-c_R}\).  Indeed, in the stabilizer expansion,
the terms supported trivially on \(R\) have
\[
 t_R=0,\qquad A_{R,R^c}t_{R^c}=0.
\]
There are \(3^{|R^c|-c_R}\) such orthogonal Pauli terms, so direct
Hilbert--Schmidt normalization gives
\(\operatorname{Tr}(\rho_{R^c}^2)=3^{-c_R}\).

Now apply at site \(i\) the map
\[
 \mathcal L_{z_i}(C)=C+z_i\operatorname {Tr}(C)I_3
\]
to a rank-one graph-state projector.  After vectorization, its quadratic
form is the expectation of
\[
 \bigotimes_i(I+z_iF_i)
\]
on two copies of the graph-state vector; every factor is positive
semidefinite for
\(|z_i|\le1\).  Expanding partial traces gives (24).

For clarity, define
\[
 N_{A,s}(z)=
 \sum_{R\subseteq[n]}z^{|R|}
 3^{-\operatorname {rank}[\,A_{R,R^c}\mid s_R\,]}.
\]
Splitting (24) for \(A^+\) according to whether the apex is absent or
present gives
\[
 \mathcal B_{A^+}(z,\ldots,z,x)
 =N_{A,s}(z)+xH_{A,s}(z).
\]
Consequently, at \(z=-1/2\),
\[
 N_{A,s}(z)+xH_{A,s}(z)\ge0\qquad(-1\le x\le1),               \tag{25}
\]
and hence
\[
 N_{A,s}(-1/2)\ge|H_{A,s}(-1/2)|.                            \tag{26}
\]
This is exact but insufficient for (23), which needs
\[
 H_{A,s}(-1/2)\ge-\frac13B_A(-1/2).                          \tag{27}
\]
Already for the one-vertex graph,
\[
 B_A(-1/2)=\frac12,\qquad
 H_{A,s}(-1/2)=-\frac16,\qquad
 N_{A,s}(-1/2)=\frac56.                                     \tag{28}
\]
Thus the general rank-one cube bound (26) loses a factor of five at the
basic equality example.

## 5. A quadratic Gauss-sum representation

The local two-dimensional Fourier transform of \(\eta\) is
\[
 \widehat\eta(v)=
 \begin{cases}
 15,&v=0,\\
 -3,&v\ne0.
 \end{cases}                                                  \tag{29}
\]
Put
\[
 g(v)=
 \begin{cases}
 5,&v=0,\\
 -1,&v\ne0.
 \end{cases}
\]
Then \(\widehat\eta=3g\).  Poisson summation on the Lagrangian graph
\[
 L_A=\{(t,At):t\in\mathbb F_3^n\}
\]
therefore rewrites each Fourier coefficient \(F_A(s)\) as
\[
 \boxed{
 F_A(s)=\sum_{v\in d_s+L_A'}\prod_{i=1}^ng(v_i),}             \tag{30}
\]
where \(L_A'\) is a local symplectic rotation of \(L_A\) and \(d_s\) is
the affine coset determined by the character \(s\).  Local symplectic
rotation does not change whether a coordinate is zero.

There is an exact five-chirp identity for \(g\).  Define
\[
 q_1(x,z)=x^2+z^2,\qquad
 q_2(x,z)=x^2+xz-z^2.                                       \tag{31}
\]
Both forms are anisotropic over \(\mathbb F_3\): direct substitution of
\(x/z=0,1,2\), together with the case \(z=0\), shows that neither
vanishes away from \((0,0)\).  Hence, for every nonzero \(v\), each pair
\(\{q_j(v),-q_j(v)\}\) is \(\{1,2\}\).  It follows that
\[
 \boxed{
 g(v)=
 1+\omega^{q_1(v)}+\omega^{-q_1(v)}
  +\omega^{q_2(v)}+\omega^{-q_2(v)}.}                        \tag{32}
\]
At \(v=0\), both sides are \(5\); away from zero, the right side is
\(1+2(\omega+\omega^2)=-1\).

Substitution in (30) gives a sum of \(5^n\) quadratic Gauss sums:
\[
 F_A(s)=
 \sum_{\sigma_i\in\{0,\pm q_1,\pm q_2\}}
 \ \sum_{v\in d_s+L_A'}
 \omega^{\sum_i\sigma_i(v_i)}.                               \tag{33}
\]
After parametrizing the affine Lagrangian, every inner sum is a standard
finite quadratic sum
\[
 \sum_{x\in\mathbb F_3^n}
 \omega^{x^\mathsf TM_\sigma x+\ell_{\sigma,s}^\mathsf Tx+c}. \tag{34}
\]
Its value is zero if the linear term misses the image of the polar
matrix; otherwise completing the square gives a root of unity times an
exact power of \(3\) (and, for odd rank, the one-dimensional quadratic
Gauss factor).

Formula (33) is a compact exact quadratic-form representation.  It is not
termwise positive: an odd-rank pair \(M,-M\) can cancel at zero linear
term and become positive or negative after a linear twist.  A proof must
group different choices of the local anisotropic forms.

## 6. Why the simplest deletion pairing fails

Fix a site \(i\) with \(s_i\ne0\), and pair \(R\not\ni i\) with
\(R\cup\{i\}\) in (16).  Write
\[
 W_R=3^{-c_R}(1+d_R).
\]
Moving one vertex across a cut changes the cut-rank by at most one.
Exact row-space analysis shows that the possible ratios are
\[
 \frac{W_{R\cup\{i\}}}{W_R}
 \in\left\{\frac13,\frac23,1,2,3\right\}.                    \tag{35}
\]
Here is the short analysis.  Put \(D=R^c\setminus\{i\}\) and
\[
 B_0=A_{R,D},\qquad a=A_{R,i},\qquad b=A_{i,D}.
\]
Then the old and new cut matrices are \([B_0\mid a]\) and
\(\begin{bmatrix}B_0\\b\end{bmatrix}\).  Each rank is
\(\operatorname{rank}B_0\) or \(\operatorname{rank}B_0+1\).  Moreover,
if \(d_R=1\), deleting the nonzero coordinate \(s_i\) from the row-space
relation shows \(s_D\in\operatorname{row}B_0\), and hence
\(d_{R\cup\{i\}}=1\).  If \(d_R=0\) and
\(d_{R\cup\{i\}}=1\), the ratio could only acquire the extra factor
two.  The apparent value \(6\) would require
\[
 a\notin\operatorname{col}B_0,\qquad
 b\in\operatorname{row}B_0,\qquad
 s_D\in\operatorname{row}B_0.
\]
Choose \(x_0\) with \(x_0^\mathsf TB_0=s_D\).  Since
\(a\notin\operatorname{col}B_0\), some
\(y\in\ker B_0^\mathsf T\) has \(y^\mathsf Ta\ne0\).
As \(s_i\ne0\), a suitable \(x=x_0+\lambda y\) then satisfies
\[
 x^\mathsf TB_0=s_D,\qquad x^\mathsf Ta=s_i,
\]
contradicting \(d_R=0\).  Substitution in
\[
 \frac{W_{R\cup\{i\}}}{W_R}
 =3^{c_R-c_{R\cup\{i\}}}
  \frac{1+d_{R\cup\{i\}}}{1+d_R}
\]
gives exactly the five values in (35).

The value \(3\) makes the paired bracket
\[
 W_R-\frac12W_{R\cup\{i\}}
\]
negative.

This happens in the smallest nontrivial way.  Take three vertices, with
vertex \(0\) isolated and one edge of weight one between vertices \(1\)
and \(2\):
\[
 A=\begin{bmatrix}0&0&0\\0&0&1\\0&1&0\end{bmatrix},
 \qquad s=(0,0,1).                                          \tag{36}
\]
Choose the active site \(i=2\) and \(R=\{0,1\}\).  Then
\[
 c_R=1,\quad d_R=1,\quad W_R=\frac23,
\]
whereas
\[
 c_{R\cup\{2\}}=0,\quad d_{R\cup\{2\}}=1,\quad
 W_{R\cup\{2\}}=2.
\]
Since \(|R|=2\), this deletion pair contributes
\[
 \frac23-\frac12(2)=-\frac13                               \tag{37}
\]
to the normalized alternating sum.  Other subsets restore the total
nonnegativity.  Thus neither termwise positivity nor one-vertex pairing
can prove (16).

## 7. Exact exhaustive theorem through five sites

The program
```
discovery/exhaust_graph_line01_fft.cpp
```
constructs \(f_A(t)\) from (8) and computes all \(3^n\) Fourier
coefficients simultaneously by an exact ternary transform over
\(\mathbb Z[\omega]\).  It checks both sides of (13).

The complete output is
\[
\begin{array}{c|r|r|r|r}
n&\#\text{ graphs}&\#(A,s\ne0)&
\min(F_A(0)+F_A(s))&\min(F_A(0)-F_A(s))\\ \hline
1&1&2&0&6\\
2&3&24&0&0\\
3&27&702&0&0\\
4&729&58\,320&0&0\\
5&59\,049&14\,289\,858&0&0
\end{array}                                                   \tag{38}
\]
Every operation is an integer addition or multiplication in
\(\mathbb Z[\omega]\).  At \(n=5\), all \(59\,049\) weighted graphs and
all \(242\) nonzero syndromes are included.

Combining (38) with Corollary 1.3 proves:

### Theorem 7.1

For every \(n\le5\), every qutrit graph, every nonzero syndrome, and
every rank-two plane in its three-dimensional graph orbit,
\[
 Q_n(P)\ge0.                                                  \tag{39}
\]

The exhaustive checker also records that every equality in the
\((0,1)\) line through \(n=5\) has an isolated vertex on which the
syndrome is nonzero.  The equality counts for \(n=1,\ldots,5\) are
\[
 2,\quad4,\quad26,\quad248,\quad7562.                         \tag{40}
\]
This equality observation is exact at the listed lengths but is not
used as an all-\(n\) classification.

## 8. Exact all-length tensorized subclasses

There is one safe way to turn the finite theorem into an unbounded-length
statement.  Suppose the graph is a disjoint union
\[
 A=A_{\rm act}\oplus A_{\rm sp},
\qquad s=(s_{\rm act},0).                                    \tag{41}
\]
Every logical plane factors as
\[
 P=P_{\rm act}\otimes |G_{\rm sp}\rangle\langle G_{\rm sp}|.
\]
Since both the Hilbert--Schmidt form and the endpoint map tensorize,
\[
 Q(P)=Q(P_{\rm act})\,
 Q(|G_{\rm sp}\rangle\langle G_{\rm sp}|).                   \tag{42}
\]
The second factor is nonnegative.  Indeed, for any rank-one operator
\(C=|u\rangle\langle v|\),
\[
 Q(C)=
 \langle u\otimes v|
 (I-\tfrac12F)^{\otimes m}
 |u\otimes v\rangle\ge0,                                    \tag{43}
\]
because \(I-\tfrac12F\succeq0\).

Consequently (39) holds at arbitrary total length whenever the syndrome
is supported on a single connected component which is one of:

- an arbitrary graph on at most five vertices, by Theorem 7.1;
- a complete graph of arbitrary order, by the complete-graph theorem;
- a cycle with constant nonzero syndrome, by Theorem 6.1 of
  `agent_path_cycle_graph_codes.md`.

The spectator graph in (41) is completely arbitrary and may have
unbounded size.  This is an all-length tensorized class, not a theorem
for a connected arbitrary graph.

## 9. Search record and current bottleneck

The exact Gray-code evaluator
```
discovery/search_arbitrary_graph_codes_fast.cpp
```
updates \(At\), the syndrome dot product, and all five relevant \(K\)'s
in \(O(n)\) per ternary vector.  It found no negative numerator in:

- \(20\,000\) random graph/syndrome instances at \(n=10\);
- \(1\,000\) random instances at \(n=12\);
- \(72\,900\) exact apex-neighborhood instances at \(n=7\);
- \(218\,700\) exact apex-neighborhood instances at \(n=8\).

These are discovery data only.  The finite exhaustive theorem is (38),
not the random search.

The exact unresolved statement is now the Fourier bound
\[
 |F_A(s)|\le F_A(0)                                         \tag{44}
\]
for every symmetric zero-diagonal \(A\) and every \(s\).  The useful
facts and obstructions are:

1. Isotropy is essential.  Arbitrary injective linear embeddings
   \(t\mapsto(u_1(t),\ldots,u_n(t))\) need not satisfy (44).
2. Rank-one multivariate block positivity yields (26), but not the
   factor \(1/3\) required in (27).
3. The cut-rank summands cannot be paired one vertex at a time, by
   (36)--(37).
4. The quadratic Gauss sums in (33) have both signs after linear
   twisting; positivity is not termwise in the quadratic-form index.
5. Finite scans do not imply (44) at arbitrary length.

Thus no exact arbitrary-graph all-\(n\) theorem and no exact graph
counterexample is claimed here.  The main reusable outputs are the
universal line reduction, the cut-rank/apex identity (23), and the
five-chirp Gauss representation (33).
