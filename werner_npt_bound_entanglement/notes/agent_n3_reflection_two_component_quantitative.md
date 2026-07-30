# A quantitative two-component reflection theorem

## Status

This note proves a strict quantitative strengthening of every
two-component face of the three-copy qutrit pair-sector problem.
For two pair components with a common physical site, the ordinary
deficit remains positive after subtracting
\[
 \frac1{34}\tau\tau^\dagger .
\]
The reflection theorem would require the larger coefficient \(1/16\).
Thus the result does not prove the reflection conjecture, but it
replaces the previously known coefficient \(0\) by an exact positive
constant and isolates the remaining factor in one rank-one marginal
domination.

The proof uses only the established unrestricted two-copy qutrit
endpoint theorem and completely positive trace-complement maps.  The
dependency-free exact checker is
`verification/verify_n3_reflection_two_component_quantitative.py`.

## 1. The strengthened two-component deficit

Let
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
be an isometry.  It is enough to consider the two components
\[
 D_1=I_1\otimes B_{23},\qquad
 D_2=I_2\otimes B_{13},                                \tag{1}
\]
where \(B_{23}\) and \(B_{13}\) are doubly traceless.  Put
\[
 D=D_1+D_2,\qquad
 \tau=\operatorname{Tr}(V^\dagger DV).                 \tag{2}
\]

### Theorem 1

For every \(V,B_{23},B_{13}\) as above,
\[
\boxed{
 \|DV\|_2^2+\frac1{34}|\tau|^2
 \leq
 2\bigl(\|B_{23}\|_2^2+\|B_{13}\|_2^2\bigr).
}                                                       \tag{3}
\]
The assertion is polarized: arbitrary complex coefficients can be
absorbed into \(B_{23},B_{13}\).  Consequently, in the notation
\[
\begin{aligned}
 d_i&=2\|B_{\widehat i}\|_2^2-\|D_iV\|_2^2,\\
 c_{ij}&=\langle D_iV,D_jV\rangle,\\
 t_i&=\overline{\operatorname{Tr}(V^\dagger D_iV)},
\end{aligned}                                           \tag{4}
\]
every two-component principal block obeys
\[
\boxed{
 \begin{pmatrix}
 d_i&-c_{ij}\\
 -\overline{c_{ij}}&d_j
 \end{pmatrix}
 -
 \frac1{34}
 \begin{pmatrix}t_i\\ t_j\end{pmatrix}
 \begin{pmatrix}\overline{t_i}&\overline{t_j}\end{pmatrix}
 \succeq0.
}                                                       \tag{5}
\]

The desired reflection block is the same formula with \(1/16\) in
place of \(1/34\).

## 2. The common-site frame operator

On one qutrit define
\[
 e(X)=\operatorname{Tr}(X)I_3,\qquad
 {\cal E}=e-\frac13\operatorname{id},\qquad
 \Phi=e-\frac12\operatorname{id}.                       \tag{6}
\]
The map \({\cal E}\) is completely positive.  Indeed, in the
normalized maximally-entangled convention,
\[
 J({\cal E})=I-P_3\succeq0.                             \tag{7}
\]
Equivalently, if \((F_a)_{a=1}^8\) is any Hilbert--Schmidt
orthonormal basis of traceless qutrit matrices, then
\[
 {\cal E}(X)=\sum_{a=1}^8F_aXF_a^\dagger.               \tag{8}
\]

Introduce the normalized code purification
\[
 |\Psi\rangle
 =\frac1{\sqrt2}\sum_{r=0}^1V|r\rangle\otimes|r\rangle_K,
 \qquad R=|\Psi\rangle\langle\Psi|.                     \tag{9}
\]
Thus \(\rho_K=I_K/2\), and hence
\[
 2(e_1e_2e_3\otimes\operatorname{id}_K)(R)
 =I_{(\mathbb C^3)^{\otimes3}\otimes K}.                \tag{10}
\]

Use the bases \(I_1\otimes F_a^{(2)}\otimes F_b^{(3)}\)
and \(F_a^{(1)}\otimes I_2\otimes F_b^{(3)}\) for the two
pair-component spaces.  Their images of \(\Psi\) have frame operator
\[
\boxed{
 T=
 \bigl({\cal E}_2{\cal E}_3+
       {\cal E}_1{\cal E}_3\bigr)
 \otimes\operatorname{id}_K(R).
}                                                       \tag{11}
\]

The key exact lower bound is
\[
\boxed{\qquad
 I-T\succeq\frac1{18}R.
\qquad}                                                  \tag{12}
\]
To prove it, expand the left side using (10).  The following map
identity is exact:
\[
\boxed{
\begin{aligned}
&2e_1e_2e_3-{\cal E}_1{\cal E}_3
                 -{\cal E}_2{\cal E}_3
                 -\frac1{18}\operatorname{id}\\
&\qquad
=2e_3\Phi_1\Phi_2
 \frac13{\cal E}_1+\frac13{\cal E}_2+\frac16{\cal E}_3 .
\end{aligned}}                                         \tag{13}
\]
Every term on the second line is positive on \(R\):

* the last three terms are completely positive by (7);
* the established two-copy endpoint theorem says that
  \(\Phi_1\Phi_2\) is two-positive;
* \(e_3\) is trace replacement.  Applying \(e_3\) first leaves
  \(I_3\) tensored with a positive operator on
  \((\mathbb C^3)^{\otimes2}\otimes K\), and
  \(\dim K=2\), so two-positivity of \(\Phi_1\Phi_2\)
  applies directly.

Applying (13) to \(R\) therefore proves (12).

## 3. From the rank-one floor to the coefficient \(1/34\)

We use a small frame lemma.

### Lemma 2

Let \(Z:{\cal B}\to{\cal H}\) be linear, put \(T=ZZ^\dagger\),
and let \(\psi\in{\cal H}\) be a unit vector.  If
\[
 I-T\succeq\frac1H|\psi\rangle\langle\psi|,
 \qquad H>1,                                             \tag{14}
\]
then
\[
\boxed{
 \|Zb\|^2+\frac1{H-1}|\langle\psi,Zb\rangle|^2
 \leq\|b\|^2
 \quad\text{for every }b\in{\cal B}.
}                                                       \tag{15}
\]

#### Proof

The rank-one criterion applied to (14) gives
\[
 \langle\psi,(I-T)^+\psi\rangle\leq H.                  \tag{16}
\]
The squared dual norm of the functional
\(b\mapsto\langle\psi,Zb\rangle\), measured in the
residual form \(I-Z^\dagger Z\), is
\[
\begin{aligned}
&\langle\psi|
 Z(I-Z^\dagger Z)^+Z^\dagger
 |\psi\rangle\\
&\qquad
=\langle\psi|T(I-T)^+|\psi\rangle
=\langle\psi|(I-T)^+|\psi\rangle-1
\leq H-1.                                               \tag{17}
\end{aligned}
\]
Here the identities follow first on each nonzero singular subspace
of \(Z\), and then by continuity on the kernels.  Cauchy--Schwarz in
the residual form gives
\[
 |\langle\psi,Zb\rangle|^2
 \leq(H-1)
 \bigl(\|b\|^2-\|Zb\|^2\bigr),
\]
which is (15). \(\square\)

Apply Lemma 2 to the synthesis map of the frame (11), with
\(H=18\).  If \(b\) is the coefficient vector of
\((B_{23},B_{13})\), then
\[
 Zb=D\Psi,\qquad
 \|b\|^2=\|B_{23}\|_2^2+\|B_{13}\|_2^2.                 \tag{18}
\]
Moreover,
\[
 \|DV\|_2^2=2\|D\Psi\|^2,\qquad
 \tau=2\langle\Psi,D\Psi\rangle.                        \tag{19}
\]
Equations (15), (18), and (19) give
\[
\begin{aligned}
&\|DV\|_2^2+\frac1{34}|\tau|^2\\
&\qquad
=2\left(
 \|D\Psi\|^2+\frac1{17}
 |\langle\Psi,D\Psi\rangle|^2\right)
\leq2\|b\|^2,
\end{aligned}
\]
which proves Theorem 1.

## 4. The exact remaining factor

The coefficient \(1/16\) is equivalent, through the same frame
calculation, to the sharper rank-one floor
\[
\boxed{\qquad
 I-T\succeq\frac19R.
\qquad}                                                  \tag{20}
\]
Indeed, for a scalar coefficient \(\gamma\) in
\[
 \|DV\|^2+\gamma|\tau|^2\leq2\|b\|^2,                   \tag{21}
\]
the corresponding rank-one floor is
\[
 \lambda=\frac{2\gamma}{1+2\gamma}.                    \tag{22}
\]
Thus
\[
 \gamma=\frac1{34}\longleftrightarrow\lambda=\frac1{18},
 \qquad
 \gamma=\frac1{16}\longleftrightarrow\lambda=\frac19.   \tag{23}
\]

Identity (13) also exposes the missing amount exactly.  Put
\[
 {\cal P}
 =2e_3\Phi_1\Phi_2
 \frac13{\cal E}_1+\frac13{\cal E}_2+\frac16{\cal E}_3 .
                                                               \tag{24}
\]
Then
\[
 I-T-\frac19R
 =
 {\cal P}(R)-\frac1{18}R.                               \tag{25}
\]
Hence the desired \(1/16\) two-component theorem is now equivalent
to the single explicit rank-one domination
\[
\boxed{\qquad
 {\cal P}(R)\succeq\frac1{18}R
 \quad
 \text{for every code purification \(R\) in (9).}
\qquad}                                                  \tag{26}
\]
All terms in \({\cal P}(R)\) are already known positive.  What remains
is not positivity of a complicated alternating expression, but the
sharp amount by which this particular positive sum dominates its
generating code vector.

No claim is made here that \(1/34\) is sharp.  Unrestricted complex
discovery optimization reaches the conjectured \(1/16\) boundary
with \(\tau\) tending to zero and common one-dimensional support at
the shared site; this observation is discovery evidence only.
