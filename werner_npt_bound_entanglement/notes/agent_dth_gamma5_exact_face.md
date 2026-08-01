# The exact final-slot PPT face (reduced rank 751)

## Result

Write the five-replica space as

\[
 \mathcal A\otimes\mathcal B\otimes\mathcal C
 = (\wedge^2\mathcal H)_{12}
   \otimes(\wedge^2\mathcal H)_{34}\otimes\mathcal H_5.
\]

Let \(\Gamma_A\) transpose the first bivector slot and let \(\Gamma_C\)
transpose the final \(z\) slot.  The corrected first lift imposes

\[
 \sigma_A:=\rho^{\Gamma_A}\succeq0,
 \qquad
 \operatorname{ran}\sigma_A\subseteq\ker\mathcal C_{\rm supp}.
\tag{1}
\]

Suppose in addition that

\[
 \sigma_C:=\rho^{\Gamma_C}\succeq0.
\tag{2}
\]

This note identifies the exact face forced on \(\sigma_C\).  Let \(K_5\)
be the range obtained by imposing, on replicas 1--4,

- antisymmetry in replicas 1,2;
- antisymmetry in replicas 3,4;
- symmetry under exchange \((12)\leftrightarrow(34)\);
- the quadratic Pluecker equation, equivalently the kernel of the
  four-replica antisymmetrizer.

Define the crossed-support contraction

\[
 \mathcal D_5=d_0^{\otimes3}+d_2^{\otimes3}.
\tag{3}
\]

At one physical qutrit site, \(d_0\) contracts the final contravariant index
with replica 2 and retains replicas \((1,3,4)\).  Similarly, \(d_2\)
contracts the final index with replica 4 and identifies the retained output
as \((3,1,2)\).  In local word notation,

\[
\begin{aligned}
 d_0|i_1i_2i_3i_4\bar j\rangle
  &=\delta_{i_2j}|i_1i_3i_4\rangle,\\
 d_2|i_1i_2i_3i_4\bar j\rangle
  &=\delta_{i_4j}|i_3i_1i_2\rangle.
\end{aligned}
\tag{4}
\]

The exact theorem is

\[
 \boxed{
 \operatorname{ran}\sigma_C
 \subseteq K_5\cap\ker\mathcal D_5.
 }
\tag{5}
\]

On the full vector space the dimensions and contraction rank are

\[
 \boxed{
 \dim K_5=1{,}194{,}102,
 \qquad
 \operatorname{rank}(\mathcal D_5|_{K_5})=6{,}552,
 \qquad
 \dim(K_5\cap\ker\mathcal D_5)=1{,}187{,}550.
 }
\tag{6}
\]

The locally invariant SDP stores only multiplicity matrices.  The sums of
the corresponding multiplicity-space support rank, removed rank, and face
rank are respectively

\[
 \boxed{772,\qquad21,\qquad751.}
\]

The exact reduced rank happens to equal the rank reported by the frozen
objective-free double-PPT projection.  A blockwise convention audit of that
archive is still unresolved, however, so this note does **not** identify the
archived numerical face with the exact face.  The exact theorem and both sets
of dimensions are independent of that comparison.

## 1. Why the crossed-support map is forced

Put

\[
 K_{\rm supp}
 =\mathcal C_{\rm supp}^{\dagger}\mathcal C_{\rm supp}\succeq0.
\]

Condition (1) is equivalent to

\[
 \operatorname{Tr}(K_{\rm supp}\sigma_A)=0.
\tag{7}
\]

Partial transpose is self-adjoint for the Hilbert--Schmidt pairing, so

\[
 \operatorname{Tr}(K_{\rm supp}\sigma_A)
 =
 \operatorname{Tr}
 \left(K_{\rm supp}^{\Gamma_A\Gamma_C}\sigma_C\right).
\tag{8}
\]

On the pair-symmetric space there is the exact operator identity

\[
 \boxed{
 P_{\rm sym}
 K_{\rm supp}^{\Gamma_A\Gamma_C}
 P_{\rm sym}
 =\frac14P_{\rm sym}\mathcal D_5^\dagger\mathcal D_5P_{\rm sym}.
 }
\tag{9}
\]

Here \(P_{\rm sym}\) projects onto
\(\operatorname{Sym}^2(\wedge^2\mathcal H)\otimes\bar{\mathcal H}\).
The convention behind (9) is the exact mixed-module localizer: on
\(\bar A\otimes A\otimes\mathcal H\), where
\(A=\wedge^2\mathcal H\),

\[
 \mathcal C_{\rm supp}(\bar w\otimes u\otimes z)
 =u\otimes(W^\dagger z).
\tag{10}
\]

This is equations (9)--(11) of `agent_dth_mixed_module.md`, with partial
transpose fixed coefficientwise by equation (7) there.  Thus (9) crosses an
already established exact density-operator localizer; it does not introduce
the phase-inconsistent holomorphic ket map ruled out earlier.

To prove (9), evaluate both sides on a diagonal Veronese--Segre ket

\[
 x=w\otimes w\otimes\bar z.
\]

Here \(w\) is *any* element of \(\wedge^2\mathcal H\), not only a
decomposable bivector.  Equation (10) and the coefficientwise definition of
\(\Gamma_A\Gamma_C\) give

\[
 \langle x,K_{\rm supp}^{\Gamma_A\Gamma_C}x\rangle
 =\|w\|^2\|W^\dagger z\|^2
 =\|w\|^2\|W\bar z\|^2.
\tag{11}
\]

The two terms in (3) agree on a diagonal pair-symmetric ket, and therefore

\[
 \|\mathcal D_5x\|^2
 =4\|w\|^2\|W\bar z\|^2.
\tag{12}
\]

Equations (11)--(12) give the diagonal equality.  Both sides of (9) are
Hermitian forms of bidegree \((2,2)\) in \((w,\bar w)\) and bidegree
\((1,1)\) in \((z,\bar z)\).  Complex polarization first in \(z\), then in
the two symmetric copies of arbitrary \(w\in\wedge^2\mathcal H\), recovers
every matrix coefficient on
\(\operatorname{Sym}^2(\wedge^2\mathcal H)\otimes\bar{\mathcal H}\).
Equivalently, diagonal Veronese tensors span the symmetric square and
polarization recovers the associated sesquilinear form.  Decomposability is
not used.

The factor \(1/4\) is audited without floating point in the verifier.  In
the normalized wedge convention take \(w=e_0\wedge e_1\).  For \(z=e_0\),
the two diagonal values before the factor are \(1/2\) and \(2\),
respectively; for \(z=e_2\), both vanish.  The verifier also compares every
matrix coefficient after \(P_{\rm sym}\) in the universal
\(\mathcal H=\mathbb C^3\) index model.

The constraints defining \(K_5\) involve replicas 1--4 only and commute with
\(\Gamma_C\), so \(\sigma_C=P_{K_5}\sigma_CP_{K_5}\).  Combining (2),
(8), and (9) gives

\[
 0=\frac14\operatorname{Tr}
   (\mathcal D_5^\dagger\mathcal D_5\sigma_C)
 =\frac14\|\mathcal D_5\sigma_C^{1/2}\|_2^2.
\]

There is no hidden converse or circular range assumption here.  Both
\(\mathcal D_5^\dagger\mathcal D_5\) and \(\sigma_C\) are positive
semidefinite.  Their zero Hilbert--Schmidt pairing is the displayed squared
norm, so \(\mathcal D_5\sigma_C^{1/2}=0\).  Hence
\(\operatorname{ran}\sigma_C\subseteq\ker\mathcal D_5\), proving (5).

## 2. Exact representation census

At one qutrit site,

\[
 3^{\otimes4}\otimes\bar3
 \cong
 V_{41}^{\oplus1}\oplus
 V_{30}^{\oplus4}\oplus
 V_{22}^{\oplus3}\oplus
 V_{11}^{\oplus8}\oplus
 V_{03}^{\oplus2}\oplus
 V_{00}^{\oplus3}.
\tag{13}
\]

The exact sparse verifier constructs rational highest-weight bases in this
order, applies the pair/Pluecker projector, and performs rational column
elimination.  Summing the multiplicity-space support ranks over all 216
ordered local-type triples gives

\[
 \dim_{\rm red}K_5=772
\]

in 188 nonzero blocks.  It then applies (3).  The difference

\[
 d_0^{\otimes3}-d_2^{\otimes3}
\]

vanishes identically on every exact projected column.  The plus combination
has rank only in the following unordered type triples:

\[
\begin{array}{c|c|c}
\text{types}&\text{rank per ordered block}&\text{number of orders}\\ \hline
(30,30,11)&1&3\\
(30,11,11)&1&3\\
(30,11,00)&1&6\\
(11,11,11)&3&1\\
(11,11,00)&1&3\\
(11,00,00)&1&3
\end{array}
\tag{14}
\]

Thus the total removed reduced rank is

\[
3+3+6+3+3+3=21.
\]

Restoring the irrep carrier dimension in each ordered block gives full
support dimension (1{,}194{,}102), full removed rank (6{,}552), and full
face dimension (1{,}187{,}550), as stated in (6).  As a separate check,

\[
 \dim K_5
 =27\,\dim S_{(2,2)}(\mathbb C^{27})
 =27\frac{27^2(27^2-1)}{12}
 =1{,}194{,}102.
\]

The other 197 ordered blocks require no internal correction.  No claim is
made here that the archived numerical exposing operator uses the same
internal block coordinates; that comparison remains under audit.

## 3. Relation to the old \((30)^{\otimes3}\) obstruction

The local \((30)\) multiplicity space is the four-point permutation module

\[
 M_{30}\cong[4]\oplus[3,1].
\]

In \(M_{30}^{\otimes3}\), pair antisymmetry and pair exchange leave six
directions; the Pluecker equation removes one, leaving a five-dimensional
space.  Under permutations of the three physical qutrit sites it decomposes
as

\[
 \mathbf1\oplus2\,\mathbf2,
\tag{15}
\]

with no alternating component.  The exact old pseudomoment's positive
trivial component survives, while its two negative eigen-directions lie in
the standard isotypic component.  The new \(\Gamma_C\)-PPT constraint removes
that NPT direction directly.  Notice that (14) contains no
\((30,30,30)\) crossed-support correction: the old obstruction is excluded
by positivity on the existing five-dimensional block, not by shrinking that
block further.

## 4. Verification and scope

Run

```text
python3 verification/agent_dth_gamma5_face_exact.py
/usr/bin/python3 verification/verify_dth_gamma5_000_dense.py
```

The first program uses exact rational sparse tensors and exact elimination
on every block except \((00,00,00)\).  Expanding that block naively creates
three tensor factors of an eighteen-word local vector; the second program
instead verifies its fixed primitive \(27\times2\) chart by exact dense
rational arithmetic.  Together they are the complete 216-block census.
Exact integer face charts and pivots can additionally be exported by

```text
python3 verification/agent_dth_gamma5_face_sparse_export.py \
  --output /tmp/dth_gamma5_face_integer_charts.json.gz
```

The exact local crossing itself is independently checked by

```text
python3 verification/agent_dth_last_crossing_exact.py
python3 verification/verify_dth_last_crossing_blocks.py
```

The theorem proves the exact support face needed to reconstruct a
double-PPT pseudomoment.  It does not prove that the double-PPT relaxation is
positive, nor does it produce a physical DTH counterexample.  A negative
higher-rank point in this face remains a certificate-level obstruction.
