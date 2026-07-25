# The triple-root, zero-\(\gamma\) vertical branch reduces to zero \(\ell\)

**Recorded (UTC):** 2026-07-25T21:34:00Z.

**Status:** exact reduction, passed an independent dependency-free hostile
audit.  Together with `VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md`, it excludes
the entire \(s\ne0,\gamma=0\) triple-root sublocus of the frozen row
`Q2-E1-A3-B1-D1-N1`.  It does not exclude that frozen row.

## Statement

Let a normalized quartic Keller candidate have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,                                        \tag{1}
\]
where \(s\ne0\), \(q|_{z=0}=x^3\), and \(W|_{z=0}=0\).
After the complete minimal triple-root normalization, write
\[
W=z(ux+vy+wz).                                        \tag{2}
\]
Then the degree-six Keller identity forces
\[
u=v=0.                                                \tag{3}
\]
Thus every candidate on this branch lies in the already excluded
\(\gamma=\ell=0\) locus \(W=wz^2\), and no Keller map occurs on the
entire \(\gamma=0\) triple-root branch.

## Proof

After killing the removable \(z^3\)-coefficient of \(q\), the complete
minimal atlas is
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2, &&\alpha\in\mathbb C,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2.
\end{aligned}                                         \tag{4}
\]
Keep all six coefficients of each of \(A,B\), all nine allowed
coefficients of \(V\), and all nine entries of the linear part arbitrary.
Let \(E_6\) be the source-degree-six homogeneous part of the raw Jacobian
determinant.

On every chart in (4), direct exterior expansion gives the same
coefficient
\[
[x^5z]E_6=-3sv.                                       \tag{5}
\]
The Keller identity and \(s\ne0\) therefore imply \(v=0\).

After substituting \(v=0\), the following chartwise linear combinations
of \(E_6\)-coefficients contain no lower-jet coefficient:
\[
\begin{array}{c|l}
q_C&
\frac13[x^3yz^2]E_6+[y^3z^3]E_6=\frac83su\\[2mm]
q_B&
-\frac19[x^4z^2]E_6-\frac13[x^2yz^3]E_6
  +[y^2z^4]E_6=-\frac49su\\[2mm]
q_E&
\frac13[x^3z^3]E_6+[yz^5]E_6=\frac43su .
\end{array}                                           \tag{6}
\]
Every coefficient on the left must vanish.  Since \(s\ne0\), each row
forces \(u=0\).  This proves (3), uniformly in \(\alpha,w\) and every
lower jet.

Now \(W=wz^2\).  The hostile-audited theorem in
`VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md` excludes all three charts in (4)
on precisely this locus.  Hence the whole \(\gamma=0\) triple-root branch
is impossible. \(\square\)

## Verification and scope

Run

```text
./verify_vertical_triple_gamma0_reduction_strict.sh
./audit_vertical_triple_gamma0_reduction/verify_strict.sh
```

The checker reconstructs the raw determinant independently on all three
charts, retains every lower coefficient, and verifies (5)--(6) exactly.
It also mutates each decisive coefficient to ensure the wrapper fails
closed.  The hostile audit independently compares a raw sparse determinant
with an exterior-multilinear reconstruction; its report is
`audit_vertical_triple_gamma0_reduction/REPORT.md`.

This result says nothing about the remaining \(\gamma\ne0\) triple-root
branch or the separate \(s=0\) family.  Exact computer algebra is evidence
about the encoded identities, not peer review.  This note and its
verification were materially AI-assisted.
