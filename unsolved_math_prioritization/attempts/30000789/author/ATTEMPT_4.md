# Approach 4: local optimization on the entire diagonal Weyl subspace

**Result:** an exact strict local maximum within a proper subspace. Local optimality cannot replace global control, and diagonalization of a curvature operator by an arbitrary orthogonal map of \(\Lambda^2\) is not an allowed change of frame in \(\mathbb R^n\).

For \(n=2m\), \(m\ge3\), let \(V=V_{m,m}\), and write \(\alpha=m/(m-1)\). A diagonal Weyl variation is encoded by symmetric edge values \(h_{ij}\), with zero diagonal and zero row sums. Its dimension is \(n(n-3)/2\): the vertex-edge incidence matrix of the complete graph has rank \(n\) for \(n\ge3\).

Let \(D=dQ_V\) on this space. For \(i\) in either block, let \(a_i\) denote the sum of the variation on edges from \(i\) within that block. Its cross-block row sum is then \(-a_i\). Differentiating the diagonal formula from Approach 3 gives

\[
(Dh)_{ij}=\begin{cases}
(1+\alpha)(a_i+a_j)&i,j\text{ in one block},\\
-(1+\alpha)(2h_{ij}+a_i+a_j)&i,j\text{ in different blocks}.
\end{cases}\tag{11}
\]

The sums of the \(a_i\) over the two blocks agree, by the cross-block row sums. Thus (11) preserves the row-zero subspace.

Here is a complete direct-sum decomposition into eigenspaces:

1. Internal edge variations in each block with zero row sums, and no cross edges. Eigenvalue 0, combined multiplicity \(m(m-3)\).
2. Cross-block variations with all row and column sums zero, and no internal edges. Eigenvalue \(-2(2m-1)/(m-1)\), multiplicity \((m-1)^2\).
3. For any first-block vector \((a_i)\) with zero sum, take internal entries \((a_i+a_j)/(m-2)\) in that block, zero internal entries in the other block, and cross entries \(-a_i/m\). There is an analogous second-block family. Equation (11) gives eigenvalue \((2m-1)(m-2)/(m-1)\), combined multiplicity \(2(m-1)\).
4. The radial direction \(V\), with eigenvalue \(2(2m-1)\), multiplicity 1.

The dimensions total \(m(2m-3)=n(n-3)/2\). The displayed directions are linearly independent across the four families: first separate block sums, then zero-sum within-block row vectors, then the remaining row-zero edges. This proves exhaustiveness. Symmetry of the curvature trilinear form makes \(D\) self-adjoint; alternatively, (11) directly verifies the orthogonal separation needed for the distinct eigenvalues.

For \(f(W)=\langle Q(W),W\rangle\), the gradient is \(3Q(W)\). Since \(Q(V)=(n-1)V\), the constrained Lagrangian on \(\|W\|^2=\|V\|^2\) is

\[
\mathcal L(W)=f(W)-\frac{3(n-1)}2\|W\|^2.
\]

Its Hessian is \(3(D-(n-1)\mathrm{Id})\). On the norm-sphere tangent space the radial family is removed. The remaining eigenvalues **after division by 3** are

\[
-(n-1),\quad-\frac{(n-1)(m+1)}{m-1},\quad
-\frac{n-1}{m-1},
\]

all negative. The usual second derivative test proves a strict local maximum in the diagonal norm sphere.

At \(n=12\), the one-third-Hessian spectrum is exactly

- \(-11\), multiplicity 18;
- \(-77/5\), multiplicity 25;
- \(-11/5\), multiplicity 10.

The checker independently constructs the 66-edge linearization, extracts its complete 54-dimensional row-zero subspace, and verifies its characteristic polynomial. This is a finite exact cross-check of (11), not the all-dimensional proof itself.

This approach cannot resolve the target: the full Weyl space in dimension 12 has dimension 1,638, and even local optimality in that whole space would not exclude distant maxima. Indeed, the same diagonal argument gives local maxima in dimensions 6, 8, and 10, although Approach 3 proves the proposed cones fail there because of a non-diagonal competitor. This is a concrete warning against promoting local or diagonal evidence to a solution.
