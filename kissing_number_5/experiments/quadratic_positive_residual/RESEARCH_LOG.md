# Research log

## 2026-07-24

- Used the exact \(-1/50\) cap theorem to derive a positive-width
  top-eigenvector separator subregion.  Convexity reduces cap containment
  to two exact endpoint inequalities.
- Tested 132 distinct stored unrestricted 41-point near-minimizers for
  nonnegative weighted centering and isotropy.  Every LP was feasible.
  Among the 102 configurations with maximum inner product below 0.55, every
  configuration admitted full-support weights with common floor between
  0.0204426384 and 0.0243902439.
- Audited the logical dependency after QPL: weighted design weights need
  not be uniform or positive, so the unweighted centered/tight identity
  cannot finish the branch.
- Derived the exact identities \(Gp=0\), \(GPG=G/5\), the rank-five
  projection \(5P^{1/2}GP^{1/2}\), the rank-six lifted projection, the
  weighted stress, and
  \[
  BPB=PB+BP-P+(2/5)I+(7/5)J-(2/5)B.
  \]
- Proved \(p_i\leq1/6\), weighted \(-1/50\)-deep mass at least \(9/98\),
  and the local \(-1/5\)-deep bound
  \(\alpha_i\geq(1-6p_i)/12\).
- Constructed exact counterexamples to uniformity and full support inside
  the \(D_5\) kissing code: a positive nonuniform 40-weight design and a
  design supported on only 12 of the 40 roots.  The regular simplex shows
  the \(1/6\) weight bound is sharp.
- Applied Carathéodory in the 19-dimensional degree-one/traceless-degree-two
  feature space: every feasible weighted branch has a representation
  supported on at most 20 code points.  Thus the exact residual can be
  viewed as a small weighted design plus at least 21 zero-weight extension
  points; the 12-support \(D_5\) example shows this phenomenon already at
  cardinality 40.
- Constructed an exact 41-vertex degree-four weighted graph countermodel to
  the current code-axis cap-count and deep-mass relaxation.
- Derived the global harmonic/Metzler shadow
  \[
  K=(5G+8H_2)/13,
  \]
  which has rank at most 19, weighted centroid zero, and off-diagonal
  interval \([-21/104,3/13]\).  The best current 41-point near-minimizer
  satisfies all associated rank, inertia, and equilibrium identities
  numerically; only its pairs above \(1/2\) break Metzler nonnegativity.
- Conclusion: the weighted branch is the more persistent branch in current
  constructions.  Local cap/depth inequalities alone are certified
  insufficient; a successful continuation must use a labeled
  common-source consequence of \(GPG=G/5\), the weighted stress, or the
  special Veronese relation between \(G\) and \(H_2\).
- Replaced every proof-critical bare assertion in the three exact
  verifiers by an always-on exception check.  Added optimized-mode normal
  runs and tamper rejection for the certificate and exact-identity
  families.
