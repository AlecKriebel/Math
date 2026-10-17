# Conditional C² obstruction to an E-6322 counterexample

Date: 2026-10-16. This is a conditional exclusion, not a regularity theorem for the benchmark minimizers. No originality claim is made.

## Claim

If an E-6322 full-class minimizer happens to belong to \(C^2(\overline\Omega;\mathbb R^3)\), then its determinant has a positive lower bound on \(\overline\Omega\). In particular, a compliant counterexample cannot have this degree of whole-domain regularity.

## Proof

Let \(F=Dy\), \(J=\det F\), and

\[
H(F)=a|F|^6+b|\operatorname{cof}F|^3+c(\det F)^2.
\]

The function \(H\) is \(C^2\) on all matrices: \(|\cdot|^3\) is \(C^2\), including at zero, and the cofactor map is polynomial. Since \(y\in C^2(\overline\Omega)\), both \(F\) and \(\operatorname{div}DH(F)\) are bounded.

Finite energy gives \(J>0\) almost everywhere. Continuity gives \(J\ge0\) everywhere. On the open set \(U_+=\{J>0\}\), compactly supported sufficiently small smooth additive variations are admissible, so local minimality gives the classical Euler equation

\[
\operatorname{div}DH(F)+6dJ^{-4}(\operatorname{cof}F)\nabla J=0.
\]

Here the Piola identity has been used to differentiate the determinant-barrier stress. Multiplying by \(F^T\) and using \(F^T\operatorname{cof}F=JI\) yields

\[
\nabla(J^{-2})=\frac{1}{3d}F^T\operatorname{div}DH(F)\quad\text{on }U_+.
\]

Thus \(|\nabla(J^{-2})|\le K\) on \(U_+\), with one finite constant valid throughout that set.

Choose one point where \(J>0\), which exists because \(\Omega\) is nonempty and \(J>0\) almost everywhere. Along any finite polygonal path in \(\Omega\) starting there, \(J^{-2}\) grows at most by \(K\) times the path length until the first hypothetical zero of \(J\). Such a zero would force \(J^{-2}\to+\infty\) along a path segment of finite length, a contradiction. Connectedness of the open domain therefore gives \(U_+=\Omega\).

A bounded connected smooth domain has a finite intrinsic diameter, equivalently a uniform finite bound on the lengths of suitable connecting paths in the domain. Applying the same estimate gives a uniform finite upper bound for \(J^{-2}\) on \(\Omega\), hence a strictly positive lower bound for \(J\). By continuity the bound extends to the closure. \(\square\)

## Scope

The proof obtains no \(C^2\) regularity from the energy or from minimality. It therefore does not establish E-6322. In particular, admissible \(C^{2,\beta}\) maps with degenerating determinants are not counterexamples unless they are minimizers; the stress identity shows why their admissibility alone is insufficient.

The boundedness of \(F^T\operatorname{div}DH(F)\), together with justified stationarity on \(\{J>0\}\), is the operative conditional hypothesis. Neither factor is known to be bounded for arbitrary benchmark minimizers.
