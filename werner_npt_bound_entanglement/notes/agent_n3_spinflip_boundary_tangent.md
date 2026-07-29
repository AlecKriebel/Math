# The second 37-dimensional quartic-flat component is the spin-flip boundary

## Result

Let
\[
 C_0=|000\rangle\langle110|+|001\rangle\langle111|
\]
and use the 204-dimensional polar-Stiefel chart and the 55 exact Hessian
kernel coordinates from
`agent_n3_boundary_effective_quartic_sos.md`.

**Theorem.**  The second listed 37-dimensional component of the zero set
of the effective quartic is exactly the tangent space at \(C_0\) to the
embedded local-qubit spin-flip equality family.  In the zero-decomposition
certificate this is component number \(1\), with zero-based numbering.

Thus both 37-dimensional components now have intrinsic meanings:

1. component \(0\) is tangent to
   \( |a\rangle\langle b|_{12}\otimes P_W\);
2. component \(1\) is tangent to the local-qubit spin-flip family below.

This identifies the component; it does not yet prove that every formal
quartic-flat path belongs uniquely to that equality family, nor does it
settle the two 27-dimensional components.  It does prove that every
first-order direction in component \(1\) integrates to an exact-zero
curve: the differential of the family is onto the component.

## Exact equality family

Put
\[
 \epsilon=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
 J=\epsilon^{\otimes3}.
\]
Choose two-planes \(W_i\subset\mathbb C^{d_i}\), choose local isometries
\(T_i:\mathbb C^2\to W_i\), and put \(T=T_1\otimes T_2\otimes T_3\).
Let \(U:\mathbb C^2\to(\mathbb C^2)^{\otimes3}\) be an isometry.  In the
chosen local frames define
\[
 V=-J\overline U\,\epsilon,\qquad C_{\rm sf}=TUV^\dagger T^\dagger.
\tag{1}
\]
Both \(U\) and \(V\) are isometries, so \(C_{\rm sf}\) is a rank-two
partial isometry.

Every member of (1) is an exact endpoint zero:
\[
 Q_3(C_{\rm sf})=0.
\tag{2}
\]
Here is a short proof.  On a qubit,
\[
 L_2(A)=A-\frac12\operatorname{Tr}(A)I_2
\]
is the Hilbert--Schmidt orthogonal projection onto the traceless
matrices.  Hence
\[
 Q_3(C)=\langle C,L_2^{\otimes3}(C)\rangle
       =\|L_2^{\otimes3}(C)\|_2^2.
\tag{3}
\]
It is enough to work in the chosen qubit frames.  Since
\(\epsilon^\dagger=-\epsilon\) and \(J^\dagger=-J\), (1) gives
\[
 C_{\rm sf}=-U\epsilon U^{\mathsf T}J.
\tag{4}
\]
For every traceless \(2\times2\) matrix \(A\),
\[
 (\epsilon A)^{\mathsf T}=\epsilon A.
\tag{5}
\]
Therefore, for traceless \(A_1,A_2,A_3\), the matrix
\[
 J(A_1\otimes A_2\otimes A_3)^\dagger
 =(\epsilon A_1^\dagger)\otimes
  (\epsilon A_2^\dagger)\otimes
  (\epsilon A_3^\dagger)
\]
is symmetric.  Consequently
\[
\begin{aligned}
 \operatorname{Tr}\!\left[
 (A_1\otimes A_2\otimes A_3)^\dagger C_{\rm sf}
 \right]
 &=-\operatorname{Tr}\!\left[
 \epsilon U^{\mathsf T}
 J(A_1\otimes A_2\otimes A_3)^\dagger U
 \right]\\
 &=0,
\end{aligned}
\tag{6}
\]
because the trace pairing of a skew matrix with a symmetric matrix
vanishes.  Thus the fully traceless component of \(C_{\rm sf}\) is zero,
and (2) follows from (3).  Local isometries preserve the partial-trace
formula, so the same conclusion holds for arbitrary embedded two-planes.

At the canonical point take
\[
 U_0=(|000\rangle,|001\rangle).
\]
The convention for \(\epsilon\) gives
\[
 -J\overline{U_0}\epsilon
 =(|110\rangle,|111\rangle)=V_0,
\]
and therefore \(U_0V_0^\dagger=C_0\).

## Tangent parameterization

Near the standard planes
\(W_i^0=\operatorname{span}\{|0\rangle,|1\rangle\}\subset\mathbb C^3\),
write each moving plane as a graph over \(W_i^0\).  Its derivative is a
complex map \(\mathbb C^2\to\mathbb C|2\rangle\), giving four real
directions per site and twelve in total.

The real tangent dimension of
\(\operatorname{Stiefel}_2(\mathbb C^8)\) at \(U_0\) is
\[
 2(8)(2)-2^2=28.
\]
The transformation
\[
 U\longmapsto UR,\qquad R\in SU(2),
\]
does not change \(C_{\rm sf}\): the identity
\(\overline R\,\epsilon=\epsilon R\) gives \(V\mapsto VR\).
Its three infinitesimal directions are exactly the kernel of the
Stiefel part of the parameterization.  The scalar \(U(1)\) direction is
not gauge; it changes the phase of \(C_{\rm sf}\).  The expected image
dimension is therefore
\[
 12+28-3=37.
\tag{7}
\]

For an exact chart calculation, let \(X=\dot U\) and
\[
 Y=\dot V=-J\overline X\,\epsilon.
\tag{8}
\]
The ambient chart fixes the common right-\(U(2)\) gauge by requiring the
right-frame logical tangent to vanish.  If
\[
 K_V=V_0^\dagger Y,
\]
the represented pair is
\[
 (X-U_0K_V,\;Y-V_0K_V).
\tag{9}
\]
The twelve plane-graph directions instead apply the same local graph
derivative to both \(U_0\) and \(V_0\).

Exact rational row reduction of these \(28+12=40\) parameter
directions gives rank \(37\).  Every resulting direction lies in the
55-dimensional Hessian kernel.  In its exact kernel coordinates
\(x_0,\ldots,x_{54}\), its annihilator is
\[
\begin{gathered}
 x_5+x_6,\quad x_8-x_9,\quad x_{17}+x_{18},\quad
 x_{20}-x_{21},\quad x_{27}-x_{28},\quad x_{30}+x_{31},\\
 x_{36},x_{37},x_{40},x_{41},x_{42},x_{43},
 x_{44},x_{45},x_{48},x_{49},x_{52},x_{53}.
\tag{10}
\end{gathered}
\]
These are exactly, entry for entry, the RREF equations of component
\(1\) in the certified effective-quartic zero decomposition.  None of
the other three components has this annihilator.

Because the family (1) is made of exact zeros and its differential has
rank \(37\), every vector in this component has nonlinear Stiefel-chart
corrections along which \(Q_3\) vanishes to all orders.  In particular,
the zero Schur minimum observed in a generic order-six
Lyapunov--Schmidt calculation on this component is structural, not an
accidental cancellation at sixth order.

## Exact verification

Run

```text
/usr/bin/python3 -S verification/verify_n3_boundary_spinflip_tangent.py
```

The verifier uses only the Python standard library.  It:

1. checks the qubit epsilon/symmetry identity behind (2);
2. reconstructs all 40 rational tangent directions;
3. fixes the common logical gauge exactly;
4. independently rebuilds the 204-dimensional Hessian from \(Q_3\);
5. maps the tangent into its 55-dimensional kernel;
6. obtains tangent rank \(37\) and annihilator rank \(18\); and
7. compares that annihilator with all four certified zero components,
   finding a unique exact match with component \(1\).
