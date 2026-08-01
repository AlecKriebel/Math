# Mixed-* rank-one consistency eliminates the cloud obstruction block

## Status

This note identifies the first exact relation coupling the holomorphic
five-replica lift to the mixed-conjugate support lift.  It also settles that
relation completely in the local cloud-obstruction block

\[
[4,1]\otimes[4,1]\otimes[3,2].
\]

The main conclusions are:

1. The first coupling is the quadratic star-identity
   \[
   |m\rangle\langle m|
   =\bigl(|h\rangle\langle h|\bigr)^{\Gamma_1},
   \qquad
   h=w\otimes w\otimes z,
   \quad
   m=\bar w\otimes w\otimes z.
   \tag{1}
   \]
2. For a pure holomorphic lift, positivity of the right side of (1) is
   equivalent to the first catalecticant of \(h\) having rank one.  On the
   pair-symmetric source this is exactly the Veronese--Segre condition
   \(h=w\otimes w\otimes z\).
3. The cloud vectors have exact first-catalecticant ranks
   \[
   \operatorname{rank}_{12:345}\xi=7,
   \qquad
   \operatorname{rank}_{12:345}\zeta=11,
   \tag{2}
   \]
   and share an explicit negative \(2\times2\) partial-transpose principal
   minor.
4. More strongly, the binary highest-weight carrier of the first-Pluecker
   source in the displayed local type is seven-dimensional and supports
   **no nonzero PPT operator**.  Thus no negative PPT pseudomoment survives
   inside this carrier.  This is proved by a dependency-free 49-pivot
   rational certificate.

This is an exact elimination of the known rank-seven obstruction, not a proof
of DTH.  The same PPT/mixed-support calculation must still be performed in all
other local carriers and in cross-carrier operator spaces, or replaced by a
global argument.

The independently established mixed-support injectivity theorem in
agent_dth_ppt_block.md is stronger on this same carrier:

\[
\widehat{\mathcal C}_{\rm supp}\rho^{\Gamma_1}=0
\quad\Longrightarrow\quad
\rho=0
\]

without positivity or PPT.  The present result is complementary: it identifies
the lowest rank-one consistency degree, gives explicit catalecticant and NPT
certificates for \(\xi,\zeta\), and proves that the PPT part of the corrected
lift already excludes the carrier.  Neither theorem excludes cancellation by
off-diagonal operator coherences joining different carriers.

The checker is
`verification/agent_dth_mixed_consistency.py`.

## 1. Holomorphic and mixed lifts

Let

\[
V=(\mathbb C^3)^{\otimes3},
\qquad
A=\wedge^2V.
\]

Choose orthonormal bases of \(A\) and \(V\), and write

\[
w=\sum_\alpha w_\alpha e_\alpha,
\qquad
z=\sum_k z_k f_k.
\]

The holomorphic and mixed lifts have coordinates

\[
h_{\alpha\beta k}=w_\alpha w_\beta z_k,
\qquad
m_{\bar\alpha\beta k}=\bar w_\alpha w_\beta z_k.
\tag{3}
\]

Identify the conjugate basis of \(\bar A\) with the chosen basis of \(A\)
only for the purpose of writing matrix entries.  Put

\[
\rho_h=|h\rangle\langle h|.
\]

Partial transpose on the first bivector slot gives

\[
\begin{aligned}
(\rho_h^{\Gamma_1})_{\alpha\beta k,\gamma\delta l}
&=(\rho_h)_{\gamma\beta k,\alpha\delta l}\\
&=w_\gamma w_\beta z_k
  \bar w_\alpha\bar w_\delta\bar z_l\\
&=m_{\bar\alpha\beta k}
  \overline{m_{\bar\gamma\delta l}}.
\end{aligned}
\]

Therefore

\[
\boxed{
\rho_h^{\Gamma_1}=|m\rangle\langle m|.
}
\tag{4}
\]

The vector \(m\) is not determined by \(h\): replacing

\[
w\mapsto e^{i\theta}w,
\qquad
z\mapsto e^{-2i\theta}z
\]

leaves \(h\) fixed and multiplies \(m\) by \(e^{-2i\theta}\).  Its rank-one
density is determined, which explains why (4), rather than a linear vector
identity, is the canonical coupling.

There cannot be a nonzero linear coupling between \(h\) and \(m\).  Under the
independent phase change \(w\mapsto e^{i\theta}w\), with \(z\) fixed, the two
lifts have weights \(2\) and \(0\).  Varying \(\theta\) separates the two
summands in any purported linear identity.  In addition, the established
support-span theorem says that physical supported monomials span the complete
first-Pluecker holomorphic source.  Hence a linear equation cannot remove the
cloud direction.  Quadratic degree is the first possible consistency degree.

## 2. Pure PPT is exactly the first catalecticant condition

For arbitrary

\[
h\in A\otimes(A\otimes V),
\]

let

\[
\operatorname{Cat}_1(h):A^*\longrightarrow A\otimes V
\]

be the flattening with entries

\[
[\operatorname{Cat}_1(h)]_{\alpha,(\beta,k)}
=h_{\alpha\beta k}.
\]

### Lemma 2.1

For nonzero \(h\),

\[
\boxed{
(|h\rangle\langle h|)^{\Gamma_1}\succeq0
\iff
\operatorname{rank}\operatorname{Cat}_1(h)=1.
}
\tag{5}

### Proof

Take a singular-value decomposition across

\[
A:(A\otimes V):
\qquad
h=\sum_{r=1}^q s_r a_r\otimes b_r,
\]

where \(s_r>0\) and both displayed families are orthonormal.  Direct
contraction shows that partial transpose exchanges

\[
\bar a_i\otimes b_j
\quad\hbox{and}\quad
\bar a_j\otimes b_i
\]

with coefficient \(s_is_j\).  Consequently

\[
\frac{
\bar a_i\otimes b_j-\bar a_j\otimes b_i
}{\sqrt2}
\]

is an eigenvector with eigenvalue \(-s_is_j\) whenever \(i\ne j\).  Positivity
therefore forces \(q=1\).  Conversely, if \(h=a\otimes b\), then

\[
(|h\rangle\langle h|)^{\Gamma_1}
=|\bar a\rangle\langle\bar a|\otimes|b\rangle\langle b|
\succeq0.
\]

This proves (5). \(\square\)

The condition in (5) is the vanishing of the quadratic minors

\[
\boxed{
h_{\alpha\beta k}h_{\gamma\delta l}
-h_{\gamma\beta k}h_{\alpha\delta l}=0
}
\tag{6}

for all indices.

### Lemma 2.2

If \(h\in\operatorname{Sym}^2(A)\otimes V\) is nonzero, then

\[
\operatorname{rank}\operatorname{Cat}_1(h)=1
\iff
h=w\otimes w\otimes z
\]

for some nonzero (w\in A) and (z\in V).

### Proof

Rank one gives

\[
h_{\alpha\beta k}=a_\alpha q_{\beta k}.
\]

Symmetry in \(\alpha,\beta\) gives

\[
a_\alpha q_{\beta k}=a_\beta q_{\alpha k}.
\]

Choose \(\alpha_0\) with \(a_{\alpha_0}\ne0\).  Then

\[
q_{\beta k}
=a_\beta q_{\alpha_0k}/a_{\alpha_0}
=a_\beta z_k,
\]

which proves the claim with \(w=a\).  The converse is immediate. \(\square\)

Finally, on (h=w^{\otimes2}\otimes z), the first-Pluecker equation is
proportional to

\[
(w\wedge w)\otimes z=0.
\]

For a bivector, this is exactly decomposability.  Indeed, if a coefficient
(w_{ab}\ne0), the four-index Pluecker equations solve every coefficient as

\[
w_{ij}
=\frac{w_{ai}w_{bj}-w_{aj}w_{bi}}{w_{ab}},
\]

so \(w\) is the wedge of two explicitly constructed vectors.  The converse
follows by alternating a repeated vector.  Thus pure PPT, source symmetry,
and the first Pluecker equation recover the physical Veronese--Segre--Pluecker
locus exactly.

## 3. Support at the density level

Let

\[
\widehat{\mathcal C}_{\rm supp}:
\bar A\otimes A\otimes V\longrightarrow A\otimes\bar V
\]

be the mixed-conjugate contraction established in the support-lift audit:

\[
\widehat{\mathcal C}_{\rm supp}
(\bar w\otimes w\otimes z)
=w\otimes(W^\dagger z).
\tag{7}

Combining (4) and (7), the exact density form of physical support is

\[
\boxed{
\widehat{\mathcal C}_{\rm supp}
\rho_h^{\Gamma_1}
\widehat{\mathcal C}_{\rm supp}^\dagger=0.
}
\tag{8}

When \(\rho_h^{\Gamma_1}\succeq0\), (8) is equivalent to annihilation of its
range by \(\widehat{\mathcal C}_{\rm supp}\).  Thus a correctly relaxed
first-level moment problem has the form

\[
\rho\succeq0,
\qquad
\rho^{\Gamma_1}\succeq0,
\qquad
\operatorname{ran}\rho\subseteq
\ker\mathcal A_4\cap\ker\mathcal C_\Omega,
\qquad
\widehat{\mathcal C}_{\rm supp}
\rho^{\Gamma_1}
\widehat{\mathcal C}_{\rm supp}^\dagger=0.
\tag{9}

The scalar condition \(\operatorname{Tr}(J_5\rho)=0\) retains only one trace
of the matrix-valued information in (8).  That is exactly why it admits
\(\zeta\).

## 4. Exact test of \(\xi\) and \(\zeta\)

Use the binary realization from the cloud obstruction.  A product-basis
state on one global replica is written as a three-bit word.  Across the cut
replicas (12:345), define

\[
\begin{aligned}
r_0&=((0,0,0),(0,0,1)),\\
r_1&=((0,0,0),(0,1,0)),\\
c_0&=((0,0,0),(0,0,1),(1,1,0)),\\
c_1&=((0,0,1),(0,0,0),(1,0,1)).
\end{aligned}
\tag{10}

Let \(M_\xi\) be the corresponding coefficient matrix.  Exact collection
gives

\[
M_\xi(r_0,c_1)=M_\xi(r_1,c_0)=0,
\quad
M_\xi(r_1,c_1)=1,
\quad
M_\xi(r_0,c_0)=-2.
\tag{11}

Hence the catalecticant minor on these rows and columns is \(-2\).  On the
partial-transpose basis states ((r_0,c_1),(r_1,c_0)), the principal matrix
is

\[
\begin{pmatrix}0&-2\\-2&0\end{pmatrix},
\]

whose determinant is \(-4\).

For exact arithmetic write the scaled cloud vector

\[
\zeta'=\sqrt{231}\,\xi_++11\xi_-=\sqrt{11}\,\zeta.
\]

The same two crossed coefficients vanish, and the product of the other two
is

\[
p=-165-\frac{33}{4}\sqrt{231}.
\tag{12}

The corresponding partial-transpose principal determinant is

\[
\boxed{
-p^2
=-\frac{687159}{16}-\frac{5445}{2}\sqrt{231}<0.
}
\tag{13}

Exact Gaussian elimination gives

\[
\boxed{
\operatorname{rank}_{12:345}\xi=7,
\qquad
\operatorname{rank}_{12:345}\zeta=11.
}
\tag{14}

The latter does not conflict with the previously reported rank seven across
the different cut (1234:5).

Equations (11)--(13) show explicitly that neither vector can be coupled to a
mixed vector \(m\) through (4): the left side is indefinite, whereas the
right side is positive semidefinite.

## 5. No PPT pseudomoment survives in the whole obstruction block

### Theorem 5.1

Let \(\mathscr K_{[4,1],[4,1],[3,2]}^{\rm bin}\) be the binary
highest-weight carrier of the first-Pluecker source inside the local type

\[
[4,1]\otimes[4,1]\otimes[3,2].
\]

If an operator \(\rho\) is supported on this seven-dimensional carrier and

\[
\rho^{\Gamma_{12}}\succeq0,
\]

then \(\rho=0\).  In particular, this carrier contains no nonzero PPT
pseudomoment, even before the Omega and support equations are imposed.

### Proof

Realize the two \([4,1]\) factors as the sum-zero parts of the point modules
on five symbols, and the \([3,2]\) factor as the incidence kernel in the
two-subset module.  Project the resulting \(4\cdot4\cdot5=80\) seed tensors
onto pair antisymmetry, pair-exchange symmetry, and the kernel of the first
four-replica antisymmetrizer.  Exact elimination gives

\[
\dim\mathscr K_{[4,1],[4,1],[3,2]}^{\rm bin}=7.
\tag{15}

Choose the seven exact rational basis vectors \(k_a\) returned by the
echelon calculation, and write their coefficient matrices across
\(12:345\) as \(M_a\).  Every supported operator has a unique expression

\[
\rho_X=\sum_{a,b=1}^7X_{ab}|k_a\rangle\langle k_b|.
\tag{16}

The seven matrices use 30 row words and 66 column words, hence a product
grid of 1980 coordinates.  Their common union contains exactly 180
coordinates; 1800 coordinates are absent.

For an absent coordinate (p=(i,\alpha)),

\[
(\rho_X^{\Gamma_{12}})_{p,p}
=(\rho_X)_{p,p}=0.
\tag{17}

A positive semidefinite matrix with a zero diagonal entry has a zero row and
column there: positivity of the principal \(2\times2\) matrix on \(p,q\)
gives

\[
0\le
\det\begin{pmatrix}0&T_{pq}\\\overline{T_{pq}}&T_{qq}\end{pmatrix}
=-|T_{pq}|^2,
\]

so (T_{pq}=0).

Thus PPT forces, for every absent (p=(i,\alpha)) and every
(q=(j,\beta)),

\[
0=(\rho_X^{\Gamma_{12}})_{p,q}
=\sum_{a,b=1}^7
X_{ab}M_a(j,\alpha)\overline{M_b(i,\beta)}.
\tag{18}

All \(M_a\) in this realization are rational.  Exact sparse Gaussian
elimination on the coefficient forms in (18) has rank

\[
\boxed{49=\dim M_7(\mathbb C).}
\tag{19}

This is stronger than a Hermitian calculation: the equations annihilate an
arbitrary complex \(7\times7\) matrix \(X\).  Therefore \(X=0\), and (16)
gives \(\rho=0\). \(\square\)

The verifier constructs all modules, projectors, absent coordinates, and 49
pivots from scratch using rational arithmetic.  No numerical eigenvalue sign
is used.

## 6. Consequences and remaining scope

The precise missing relation exposed by the cloud vector is not a higher
Pluecker equation.  It is the lowest quadratic Segre/mixed-star consistency:

\[
\rho^{\Gamma_1}\succeq0,
\]

or, on a pure lift, the quadratic catalecticant minors (6).  In the cloud
binary carrier this one condition removes not only \(\xi\) and \(\zeta\),
but every nonzero pseudomoment supported entirely in that carrier.

This means that a seven-replica Pluecker prolongation should not be launched
to repair this carrier.  The correct next finite calculation is the
mixed-PPT cone (9) in the remaining local carriers **and the off-diagonal
operator spaces coupling them**.  A cross-carrier density can have partial
transpose rows or mixed-support outputs that cancel between its diagonal and
off-diagonal blocks, so carrierwise exclusion alone does not prove the global
relaxation.  If every coupled block is eliminated or the witness is positive
on the surviving cone, the result would prove DTH.  If a negative PPT block
survives, its exact density would identify the next missing matrix-valued
rank-one equation.

Not proved here:

- global positivity of the complete mixed-PPT DTH relaxation;
- exclusion of cross-carrier cancellation;
- DTH;
- square-zero positivity;
- the compatible common-plane/square-zero cross inequality;
- unrestricted three-copy positivity or the all-copy theorem.

Completion estimate for eliminating the known
\([4,1]\otimes[4,1]\otimes[3,2]\) obstruction block: **100%**.
Completion estimate for the full corrected first-level mixed-PPT DTH
decision: **40%**.
