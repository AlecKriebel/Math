# Substantive turn 2: exact symmetrization, and why one representation fails

2026-10-01 05:58–06:02 UTC. Status: partial theorem and exact obstruction to a tempting classification route, unreviewed. Full-characterization estimate: 35%.

Work over C. Let M(x) be a 4-by-4 matrix of linear forms with det M nonzero. Write its j-th column as A_j x, where A_j is a constant 4-by-4 matrix. Define the linear space

    S(M) = { U in Mat_4(C) : U A_j is symmetric for j=0,1,2,3 }.

It is the kernel of an explicit 24-by-16 constant matrix. For each j and r<s, its equation is

    sum_i U[r,i] A_j[i,s] - sum_i U[s,i] A_j[i,r] = 0.

## Exact fixed-equivalence-class criterion

**Theorem.** The constant left-right equivalence class of M contains the column-gradient matrix of four independent quadrics if and only if S(M) contains an invertible matrix. If U is such a matrix, the quadrics can be taken as q_j=x^T U A_j x/2.

Proof. Symmetry is exactly the equality of mixed partial derivatives for the linear vector field U A_j x. The displayed quadratic has that gradient. The four quadrics are independent: a constant relation among them gives a relation among the columns of U M, impossible when its determinant is nonzero. Conversely, if R M B is a gradient matrix with R,B invertible, multiplying its columns by B^{-1} preserves integrability, so R lies in S(M). This proves both directions.

The criterion is effective linear algebra followed by one polynomial identity test. For a basis U_1,...,U_s of S(M), expand det(sum z_i U_i). There is an invertible symmetrizer over C exactly when this polynomial is not identically zero. A merely nonzero symmetrizer does not suffice. The identically-zero test is finite and exact, and a nonzero polynomial over the infinite field supplies an invertible specialization.

It is invariant under changes of projective coordinates as well. For M'(x)=R M(Cx) B, an invertible U for M gives U'=C^T U R^{-1}; each transformed column coefficient is a linear combination of C^T U A_j C and hence is symmetric. The converse follows by inverse changes. No additional coordinate search is required for a fixed equivalence class.

## Exact counterexample to checking only a supplied determinant matrix

The four explicit symmetric slices in `checks/SYMMETRIZER_CERTIFICATE.json` define M=[A_0 x ... A_3 x]. Its determinant takes value -12 at (1,0,0,0), so it is a genuine quartic Weddle equation. The exact test matrix for M has rank 15 and kernel C times the identity. However, the test matrix for M^T has rank 16. Thus S(M^T)=0 even though det(M^T)=det(M).

The certificate supplies all integer entries and nonzero maximal minors; `checks/check_symmetrizer.py` verifies them and reconstructs the four quadrics and determinant equality. No floating-point rank is involved. Smoothness is not asserted for this sample, and is unnecessary for the stated obstruction.

Therefore the criterion completely settles an individual determinant representation up to constant row, column and coordinate changes, but a failed test does **not** exclude the underlying quartic from being Weddle. One must control every inequivalent determinantal representation. Taking an arbitrary supplied representation or treating transpose as left-right equivalent would yield a false negative on this explicit example.

The full original characterization remains unresolved. The next route is the intrinsic geometry of the polar correspondence on a smooth Weddle quartic; singular and nonreduced quartics must still be treated separately, rather than silently excluded.
