# Exact three-slice Fierz identity and the rank-four exterior remainder

## Status

A tempting block-matrix inequality is false for arbitrary blocks, and it
remains false when all three blocks are complex symmetric.  Numerical
counterexamples have positive normalized gaps as large as (0.16) in small
dimensions.  Thus a valid three-slice proof must use the common
double-Hodge origin

\[
 B_p=\mathscr D_{X_p}.
\]

For these blocks, the local cofactor polarization identity gives a complete
exact expansion of every Koszul column.  After summing over a rank-four
orthonormal frame, the conjectured block inequality reduces to one signed
exterior-square Gram inequality plus the global five-vector Gram
determinant.  This is the smallest exact lemma currently isolated on this
route.

No proof of the final exterior inequality is claimed here.

## 1. Three-slice block form

Slice a three-qutrit tensor at the first site:

\[
 x=\sum_{p=0}^2|p\rangle\otimes x_p,
 \qquad x_p=\operatorname{vec}X_p.
\]

Put

\[
 B_p=\mathscr D_{X_p}
 =\sum_{a,b}(X_p)_{ab}A_a\otimes A_b.
\]

Up to fixed block signs,

\[
 D_x={1\over\sqrt2}
 \begin{pmatrix}
 0&B_2&-B_1\\
 -B_2&0&B_0\\
 B_1&-B_0&0
 \end{pmatrix}.
\tag{1}
\]

For another tensor

\[
 y=\sum_p|p\rangle\otimes\operatorname{vec}Y_p,
\]

the cofactor polarization convention

\[
 \mathscr D_X\operatorname{vec}Y
 ={1\over2}\operatorname{vec}(X\times Y)
\]

gives

\[
 8\|D_xy\|^2
 =\sum_{p<q}\|X_p\times Y_q-X_q\times Y_p\|_2^2.
\tag{2}
\]

## 2. Exact matrix Fierz identity

Define the (3\times3) slice Gram matrices

\[
 A_{pq}=\langle X_p,X_q\rangle,
 \qquad
 B_{pq}=\langle Y_p,Y_q\rangle,
 \qquad
 C_{pq}=\langle X_p,Y_q\rangle,
\tag{3}
\]

and the left/right contractions

\[
\begin{aligned}
 L_X&=\sum_pX_pX_p^\dagger,&
 R_X&=\sum_pX_p^\dagger X_p,\\
 L_Y&=\sum_pY_pY_p^\dagger,&
 R_Y&=\sum_pY_p^\dagger Y_p.
\end{aligned}
\tag{4}
\]

### Proposition 1

For arbitrary complex (X_p,Y_p\in M_3\),

\[
\boxed{
\begin{aligned}
8\|D_xy\|^2={}&
(\operatorname{Tr}A)(\operatorname{Tr}B)-\operatorname{Tr}(AB)\\
&+\|C\|_2^2-|\operatorname{Tr}C|^2\\
&-\operatorname{Tr}(R_XR_Y)
 +\left\|\sum_pX_p^\dagger Y_p\right\|_2^2\\
&-\operatorname{Tr}(L_XL_Y)
 +\left\|\sum_pX_pY_p^\dagger\right\|_2^2.
\end{aligned}}
\tag{5}
\]

### Proof

Use the exact polarization identity

\[
\begin{aligned}
\langle X\times Z,Y\times W\rangle
={}&\langle X,Y\rangle\langle Z,W\rangle
+\langle X,W\rangle\langle Z,Y\rangle\\
&-\operatorname{Tr}(X^\dagger YZ^\dagger W)
-\operatorname{Tr}(YX^\dagger WZ^\dagger).
\end{aligned}
\tag{6}
\]

Expand every squared difference in (2) and sum over ordered (p,q).
The first scalar contraction gives

\[
 (\operatorname{Tr}A)(\operatorname{Tr}B)-\operatorname{Tr}(AB),
\]

and the second gives

\[
 \|C\|_2^2-|\operatorname{Tr}C|^2.
\]

The two negative trace contractions are the first terms on the last two
lines of (5).  Their crossed companions regroup as

\[
\begin{aligned}
\sum_{p,q}\operatorname{Tr}(X_p^\dagger X_qY_q^\dagger Y_p)
 &=\left\|\sum_pX_pY_p^\dagger\right\|_2^2,\\
\sum_{p,q}\operatorname{Tr}(X_qX_p^\dagger Y_pY_q^\dagger)
 &=\left\|\sum_pX_p^\dagger Y_p\right\|_2^2.
\end{aligned}
\]

This proves (5). \(\square\)

The two coherent positive sums in (5) must remain paired with
\(-\operatorname{Tr}(R_XR_Y)\) and
\(-\operatorname{Tr}(L_XL_Y)\).  Bounding them independently reproduces
the known factor-two loss at physical equality.

## 3. Basis-free one-column identity

For a physical site (i), write the one-site reduction and transition as

\[
 \rho_i^x=\operatorname{Tr}_{\widehat i}|x\rangle\langle x|,
 \qquad
 T_i(x,y)=\operatorname{Tr}_{\widehat i}|x\rangle\langle y|.
\]

Equation (5) is equivalently

\[
\boxed{
8\|D_xy\|^2
=\|x\|^2\|y\|^2-|\langle x,y\rangle|^2
-\sum_{i=1}^3\operatorname{Tr}(\rho_i^x\rho_i^y)
+\sum_{i=1}^3\|T_i(x,y)\|_2^2.
}
\tag{7}
\]

This form makes all three pairings in (5) intrinsic.

## 4. Aggregation over a rank-four projector

Let (y_1,\ldots,y_4\) be orthonormal and

\[
 P=\sum_{\alpha=1}^4|y_\alpha\rangle\langle y_\alpha|.
\]

Write (P_i=\operatorname{Tr}_{\widehat i}P\).  Summing (7) gives

\[
\boxed{
\begin{aligned}
8\operatorname{Tr}(P D_x^\dagger D_x)
={}&4\|x\|^2-\langle x,Px\rangle\\
&-\sum_i\operatorname{Tr}(\rho_i^xP_i)
+\sum_{i,\alpha}\|T_i(x,y_\alpha)\|_2^2.
\end{aligned}}
\tag{8}
\]

In a fixed product basis, if

\[
 \rho_{\widehat i}^x
 =\operatorname{Tr}_i|x\rangle\langle x|,
\]

then

\[
 \sum_\alpha\|T_i(x,y_\alpha)\|_2^2
 =\operatorname{Tr}\left[
 P\left(I_i\otimes(\rho_{\widehat i}^x)^{\mathsf T}\right)
 \right].
\tag{9}
\]

Thus the desired Ky--Fan-four bound is exactly

\[
\boxed{
\langle x,Px\rangle
+\sum_i\operatorname{Tr}\left[
 P\left(\rho_i^x\otimes I_{\widehat i}
 -I_i\otimes(\rho_{\widehat i}^x)^{\mathsf T}\right)
 \right]\ge0.
}
\tag{10}

This is the aggregated rank-four remainder in projector/marginal form.

## 5. Exterior-square Gram form

At cut (i:\widehat i), flatten (x,y\) as (3\times9) matrices
\(X^{(i)},Y^{(i)}\).  Define the two nonnegative exterior Gram deficits

\[
\begin{aligned}
E_{\rm col}^{(i)}(x,y)
&=\|x\|^2\|y\|^2
  -\|(X^{(i)})^\dagger Y^{(i)}\|_2^2,\\
E_{\rm row}^{(i)}(x,y)
&=\|x\|^2\|y\|^2
  -\|X^{(i)}(Y^{(i)})^\dagger\|_2^2.
\end{aligned}
\tag{11}
\]

Each is explicitly a sum of squared two-vector wedges: the first over
columns, the second over rows.  Moreover,

\[
\boxed{
\operatorname{Tr}(\rho_i^x\rho_i^y)-\|T_i(x,y)\|_2^2
=E_{\rm row}^{(i)}(x,y)-E_{\rm col}^{(i)}(x,y).
}
\tag{12}

Consequently (10) is equivalent to the single exterior inequality

\[
\boxed{
\sum_{i=1}^3\sum_{\alpha=1}^4
\left(E_{\rm col}^{(i)}(x,y_\alpha)
     -E_{\rm row}^{(i)}(x,y_\alpha)\right)
\le\langle x,Px\rangle.
}
\tag{13}

Finally, (P^2=P\) and orthonormality give the exact five-vector Gram
identity

\[
 \|x\wedge y_1\wedge\cdots\wedge y_4\|^2
 =\|x\|^2-\langle x,Px\rangle.
\tag{14}

Hence the smallest remaining exterior lemma is

\[
\boxed{
\begin{aligned}
&\sum_{i,\alpha}
\left(E_{\rm col}^{(i)}(x,y_\alpha)
     -E_{\rm row}^{(i)}(x,y_\alpha)\right)\\
&\qquad
+\|x\wedge y_1\wedge\cdots\wedge y_4\|^2
\le\|x\|^2.
\end{aligned}}
\tag{15}

This uses the rank-four common origin through one orthonormal frame and its
global five-vector Gram determinant.  Treating the twelve exterior deficits
independently discards exactly that compatibility.

## 6. Relation to the proposed block inequality

The proposed decisive inequality is

\[
 F_4(D_x)
 \le\sum_{p=0}^2
 \left[s_1(\mathscr D_{X_p})^2+s_2(\mathscr D_{X_p})^2\right].
\tag{16}

It is numerically unviolated for unrestricted complex (X_p\), and Lemma 1
of `agent_dth_deficient_equality_classification.md` would then imply

\[
 F_4(D_x)\le{1\over2}\sum_p\|X_p\|_2^2={1\over2}\|x\|^2,
\]

settling Ky--Fan four and DTH.  Equations (5), (10), and (15) are exact
reformulations of the common-double-Hodge geometry needed for that attack.
The arbitrary-block and symmetric-block counterexamples show that a proof
cannot omit the cofactor/Fierz relations.

The dependency-free verifier

```text
python3 verification/verify_dth_three_slice_fierz.py
```

checks (5), (7), (8), and (12) on exact rational tensors and an exact
rank-four coordinate projection.
