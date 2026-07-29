# Local \(S_4\) recoupling for the pair-sector wedge, and its exact linear no-go

## Status

This note computes the complete one-site recoupling between:

- the two scalar/traceless replica pairings after right partial
  transpose; and
- the left- and right-replica swap parities in the common-origin
  bivector.

The qutrit exclusion of the four-fold alternating representation is
visible explicitly.  It is nevertheless **not** enough to prove the
pair-sector inequality by positivity of the resulting recoupled
operator.  That operator has the exact expectation value \(-24\) on a
physical three-site qutrit vector lying entirely in the
\([2,2]^{\otimes3}\) block.

This is not a counterexample to the pair-sector theorem.  The negative
vector has Schmidt rank \(64\), rather than one, across the
left-replica-pair : right-replica-pair cut.  Thus the calculation
isolates the information still missing from a purely local
representation-theoretic argument: the global four-fold Segre
condition, equivalently the shared two-plane Pluecker origin.

The dependency-free exact checker is
`verification/verify_n3_local_s4_recoupling_nogo.py`.

## 1. From the wedge mass to a four-species product witness

Let \(\Pi=\Pi_2\) be the exact degree-two projection on
\(M_3^{\otimes3}\), and put
\[
 Y=2I-3\Pi,\qquad {\cal K}=Y^{(1)}Y^{(2)}.
 \tag{1}
\]
For orthonormal singular frames \(u_1,u_2\) and \(v_1,v_2\), write
\[
 E_r=u_r\otimes\overline v_r,\qquad
 z=E_1\otimes E_2.
 \tag{2}
\]
If \(T\) swaps the two complete operator replicas, then
\[
 \omega=\frac{I-T}{\sqrt2}z.
 \tag{3}
\]
The operator \({\cal K}\) commutes with \(T\), and its eigenvalues
according as zero, one, or two exterior factors lie in
\(\operatorname{Ran}\Pi\) are \(4,-2,1\).  Therefore
\[
 \boxed{\quad
 \langle\omega,{\cal K}\omega\rangle
 =6A_0+3A_2-2.
 \quad}
 \tag{4}
\]
Equivalently,
\[
 \langle\omega,{\cal K}\omega\rangle
 =\langle z,(I-T){\cal K}z\rangle.
 \tag{5}
\]

Regroup the four species as
\[
 (L_1,L_2):(R_1,R_2)
 \tag{6}
\]
and partially transpose both right species.  Let
\[
 L=\prod_{i=1}^3(L_{1,i}\ L_{2,i}),\qquad
 R=\prod_{i=1}^3(R_{1,i}\ R_{2,i}).
 \tag{7}
\]
Writing \(\widehat{\cal K}={\cal K}^{\Gamma_R}\), the elementary
order reversal on the transposed side gives
\[
 \boxed{\quad
 {\cal B}:=((I-T){\cal K})^{\Gamma_R}
 =\widehat{\cal K}-L\widehat{\cal K}R.
 \quad}
 \tag{8}
\]
Consequently (4) is exactly
\[
 \langle
 u_1\otimes u_2\otimes v_1\otimes v_2,\,
 {\cal B}\,
 u_1\otimes u_2\otimes v_1\otimes v_2
 \rangle\geq0,
 \tag{9}
\]
with the harmless convention-dependent conjugations absorbed into
the \(v\)'s.  Thus the theorem asks for nonnegativity of \({\cal B}\)
on a four-fold Segre variety.  Positivity of \({\cal B}\) on its whole
linear ambient space would be sufficient, but, as shown below, is
false.

## 2. The complete one-site recoupling table

At one physical site label the four qutrits
\[
 1=L_1,\quad2=L_2,\quad3=R_1,\quad4=R_2.
 \tag{10}
\]
Define the vertical and horizontal commuting transpositions
\[
 f_1=(13),\quad f_2=(24),\qquad
 \ell=(12),\quad r=(34).
 \tag{11}
\]
The normalized scalar projector satisfies
\[
 P^\Gamma=\frac13f.
 \tag{12}
\]
Hence, on one complete operator replica,
\[
 \widehat Y
 =2I-\sum_i f_i
   +\frac23\sum_{i<j}f_if_j
   -\frac13f_1f_2f_3.
 \tag{13}
\]
If \(q\) of the three vertical swaps have eigenvalue \(-1\), its
eigenvalue is
\[
 y_q=\frac23,\ \frac23,\ 2,\ \frac{22}{3}
 \qquad(q=0,1,2,3).
 \tag{14}
\]

The local permutation algebra on \((\mathbb C^3)^{\otimes4}\) has the
four sectors
\[
 [4],\quad[3,1],\quad[2,2],\quad[2,1,1].
 \tag{15}
\]
The alternating sector \([1,1,1,1]\) is absent because
\(\bigwedge^4\mathbb C^3=0\).

For vertical signs \(a,b\) and horizontal signs
\(\sigma,\tau\), set
\[
\begin{aligned}
 V_{ab}&=\frac14(I+af_1)(I+bf_2),\\
 H_{\sigma\tau}&=\frac14(I+\sigma\ell)(I+\tau r).
\end{aligned}
\tag{16}
\]
In every sector in (15), each nonzero character space in (16) has
rank one.  With rows indexed by the listed vertical characters and
columns by the same list of horizontal characters, phases may be
chosen so that the complete recoupling matrices are
\[
\begin{array}{c|c|c}
\lambda&\text{character order}&U_\lambda\\ \hline
[4] &(++) &(1)\\[1mm]
[3,1] &(++,+-,-+)&
\begin{pmatrix}
0&1/\sqrt2&1/\sqrt2\\
1/\sqrt2&1/2&-1/2\\
1/\sqrt2&-1/2&1/2
\end{pmatrix}\\[5mm]
[2,2] &(++,--)&
\begin{pmatrix}
1/2&\sqrt3/2\\
\sqrt3/2&-1/2
\end{pmatrix}\\[5mm]
[2,1,1] &(+-, -+, --)&
\begin{pmatrix}
1/2&-1/2&1/\sqrt2\\
-1/2&1/2&1/\sqrt2\\
1/\sqrt2&1/\sqrt2&0
\end{pmatrix}.
\end{array}
\tag{17}
\]
All four matrices are real orthogonal.  Their squared entries also
follow directly from
\[
 \operatorname{Tr}_\lambda(V_{ab}H_{\sigma\tau})
 =\frac1{16}\sum_{g\in\langle f_1,f_2\rangle}
              \sum_{h\in\langle\ell,r\rangle}
 \chi_{ab}(g)\chi_{\sigma\tau}(h)\chi_\lambda(gh).
 \tag{18}
\]
For comparison, the missing alternating representation would contain
only \((--)\) in both couplings, with recoupling amplitude one.

## 3. The exact global recoupled operator

For a triple of sectors
\(\boldsymbol\lambda=(\lambda_1,\lambda_2,\lambda_3)\), let
\({\cal C}_{\lambda_i}\) be its vertical character list in (17).
In the product vertical basis define
\[
 {\cal H}_{\boldsymbol\lambda}
 \bigl((a_i,b_i)_{i=1}^3\bigr)
 =
 y_{\#\{i:a_i=-1\}}\,
 y_{\#\{i:b_i=-1\}}.
 \tag{19}
\]
This is a diagonal matrix.  If
\[
\begin{aligned}
 \ell_\lambda
 &=U_\lambda
   \operatorname{diag}(\sigma)U_\lambda^{\mathsf T},\\
 r_\lambda
 &=U_\lambda
   \operatorname{diag}(\tau)U_\lambda^{\mathsf T},
\end{aligned}
\tag{20}
\]
then (8) restricts to the explicit finite matrix
\[
 \boxed{\quad
 {\cal B}_{\boldsymbol\lambda}
 =
 {\cal H}_{\boldsymbol\lambda}
 -
 \left(\bigotimes_i\ell_{\lambda_i}\right)
 {\cal H}_{\boldsymbol\lambda}
 \left(\bigotimes_i r_{\lambda_i}\right).
 \quad}
 \tag{21}
\]
Equations (14), (17), and (21) are the requested local-to-global
recoupling formula.  No multiplicity space occurs in it: the same
small matrix is simply repeated on every multiplicity copy.

## 4. Exact negative direction in the sign-free relaxation

Take
\[
 \boldsymbol\lambda=([2,2],[2,2],[2,2]).
 \tag{22}
\]
In this sector the vertical and horizontal character orders are both
\((++,--)\), and
\[
 \ell_{[2,2]}=r_{[2,2]}
 =
 J:=
 \begin{pmatrix}
 -1/2&\sqrt3/2\\
 \sqrt3/2&1/2
 \end{pmatrix}.
 \tag{23}
\]
Because the two vertical signs agree at every site,
\({\cal H}\) depends only on the Hamming weight \(q\), with diagonal
values
\[
 h_q=y_q^2
 =\frac49,\ \frac49,\ 4,\ \frac{484}{9}.
 \tag{24}
\]
Let \(e_0=(1,0)^{\mathsf T}\), the vertical \(++\) vector, and put
\(x=e_0^{\otimes3}\).  Since
\[
 Je_0=-\frac12e_0+\frac{\sqrt3}{2}e_1,
 \tag{25}
\]
the squared amplitudes of \(J^{\otimes3}x\) have the binomial
distribution with weights \(1/4,3/4\).  Therefore
\[
\begin{aligned}
 \langle x,{\cal H}x\rangle&=\frac49,\\
 \langle J^{\otimes3}x,
          {\cal H}J^{\otimes3}x\rangle
 &=
 \frac{10}{64}\frac49
 +\frac{27}{64}4
 +\frac{27}{64}\frac{484}{9}
 =\frac{220}{9}.
\end{aligned}
\tag{26}
\]
Thus
\[
 \boxed{\qquad
 \langle x,{\cal B}_{[2,2]^{\otimes3}}x\rangle=-24.
 \qquad}
 \tag{27}
\]
In particular, removing the forbidden alternating representation is
not enough to make the recoupled operator positive.

There is a completely explicit physical realization of the local
vector \(e_0\).  In the order \(L_1,L_2,R_1,R_2\), put
\[
\begin{aligned}
 \xi=\frac1{2\sqrt3}\bigl(
 &-|1100\rangle+2|1010\rangle-|1001\rangle\\
 &-|0110\rangle+2|0101\rangle-|0011\rangle
 \bigr).
\end{aligned}
\tag{28}
\]
It is fixed by both vertical swaps \((13),(24)\), and the central
\([2,2]\) projector fixes it.  Hence
\(\xi^{\otimes3}\) realizes \(x\) in (27) inside twelve genuine
qutrit tensor factors.  Direct contraction of the 128 permutation
terms in (8) again gives
\[
 \langle\xi^{\otimes3},{\cal B}\xi^{\otimes3}\rangle=-24.
 \tag{29}
\]

## 5. The missing nonlinear constraint

The vector (28) is not admissible common-origin data.  Across
\[
 (L_1L_2):(R_1R_2)
 \tag{30}
\]
its unnormalized coefficient matrix, on the local
\(\{|00\rangle,|01\rangle,|10\rangle,|11\rangle\}\) support, is
\[
 \begin{pmatrix}
 0&0&0&-1\\
 0&2&-1&0\\
 0&-1&2&0\\
 -1&0&0&0
 \end{pmatrix}.
 \tag{31}
\]
Its determinant is \(-3\), so its Schmidt rank is four.  Consequently
\(\xi^{\otimes3}\) has Schmidt rank \(4^3=64\) across (30).

By contrast, the pre-wedge vector in (9) is
\[
 (u_1\otimes u_2)\otimes(v_1\otimes v_2),
 \tag{32}
\]
which has Schmidt rank one across the same cut.  After horizontal
parity resolution, its four components have the correlated form
\[
 u_\sigma\otimes v_\tau,
 \tag{33}
\]
with equal prescribed norms and with \(u_+,u_-\) (and likewise
\(v_+,v_-\)) arising from one common two-plane.

Thus the exact surviving problem is not a missing local \(S_4\)
sector.  It is block positivity of (21) on the four-fold Segre variety,
together with the common-plane Pluecker relations.  Any proof that
keeps only local swap parities, local Hodge complementation, and the
absence of \(\bigwedge^4\mathbb C^3\) necessarily admits the exact
negative relaxation vector (28).

## 6. Exact obstruction to a stronger marginal feature bound

The same recoupling investigation suggests a natural but false
strengthening.  Let
\[
 S=\frac49E_2+\frac{20}{9}E_3
 \tag{34}
\]
be the positive feature part of the partially transposed pair witness,
and let \(K_{\rm f}\) be its compression to the two logical planes.  The
inequality
\[
 \lambda_{\max}(K_{\rm f})
 \stackrel?{\leq}
 \frac29+\lambda_{\min}(\operatorname{Tr}_B K_{\rm f})
 \tag{35}
\]
would imply the desired PPT inequality by the two-dimensional
reduction identity.  It is exact at the canonical nonnormal boundary,
but it is false even on a physical common-origin code.

Take
\[
\begin{aligned}
 U&=(|000\rangle,|222\rangle),\\
 V&=(|000\rangle,|100\rangle).
\end{aligned}
\tag{36}
\]
These are qutrit isometries.  Direct local swap-parity contraction
gives, in the logical order \(00,01,10,11\),
\[
 \boxed{\qquad
 K_{\rm f}
 =\operatorname{diag}\left(0,0,\frac49,\frac49\right).
 \qquad}
 \tag{37}
\]
Indeed, the first two physical products have respectively zero and
one unequal local pair, so \(S\) annihilates them.  Each of the last
two has three unequal local pairs.  Its exact-two-antisymmetric
probability is \(3/8\), its fully antisymmetric probability is \(1/8\),
and hence its feature energy is
\[
 \frac49\frac38+\frac{20}{9}\frac18=\frac49.
 \tag{38}
\]
All cross terms vanish by the computational-basis swap contractions.
It follows that
\[
\begin{aligned}
 \lambda_{\max}(K_{\rm f})&=\frac49,\\
 \operatorname{Tr}_B K_{\rm f}
 &=\operatorname{diag}\left(0,\frac89\right).
\end{aligned}
\tag{39}
\]
Thus (35) fails by the exact amount \(2/9\).

This code is not a pair-sector counterexample.  The full compressed
witness is
\[
 \frac29I_4+K_{\rm f}
 =
 \operatorname{diag}\left(
 \frac29,\frac29,\frac23,\frac23\right),
 \tag{40}
\]
which is unchanged by logical partial transpose and is strictly
positive.  The failure shows that a proof cannot replace the full
two-qubit PPT geometry by the smallest eigenvalue of one logical
marginal.
