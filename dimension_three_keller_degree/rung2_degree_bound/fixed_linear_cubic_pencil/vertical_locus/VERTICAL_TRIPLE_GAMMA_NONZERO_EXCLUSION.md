# The triple-root, nonzero-\(\gamma\) vertical branch is impossible

**Recorded (UTC):** 2026-07-25T21:39:00Z.

**Status:** exact lemma, passed an independent dependency-free hostile
audit.  It excludes a sublocus of the frozen row
`Q2-E1-A3-B1-D1-N1`; it does not exclude that row.

## Statement

Let a normalized quartic Keller candidate have
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T,\qquad
H_2=(A,B,W)^T,                                        \tag{1}
\]
where \(s\ne0\), \(q|_{z=0}=x^3\), and
\[
W=\gamma x^2+z(ux+vy+wz),\qquad \gamma\ne0.            \tag{2}
\]
Then the degree-six Keller identity is impossible.  Consequently the
nonzero-\(\gamma\) triple-root vertical branch contains no Keller map.

## Proof

After the complete minimal triple-root normalization and removal of the
free \(z^3\)-coefficient of \(q\), the three charts are
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2, &&\alpha\in\mathbb C,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2.
\end{aligned}                                         \tag{3}
\]
Retain every coefficient of \(A,B,V\), every entry of the linear part,
and all parameters in (2).  Let \(E_6\) be the source-degree-six
homogeneous part of the raw Jacobian determinant.

### The \(q_C\) chart

One coefficient is already
\[
[x^4yz]E_6=4\gamma s.                                 \tag{4}
\]
It cannot vanish because \(\gamma s\ne0\).

### The \(q_B\) chart

Two exact identities are
\[
\begin{aligned}
[x^5z]E_6&=s(2\gamma-3v),\\
-\frac16[x^3yz^2]E_6+[xy^2z^3]E_6
  &=-\frac{s}{3}(\gamma+v).
\end{aligned}                                         \tag{5}
\]
Their simultaneous vanishing would give
\[
v=\frac23\gamma,\qquad v=-\gamma,
\]
and hence \(\gamma=0\), contrary to (2).

### The \(q_E\) chart

Here
\[
\frac23[x^4z^2]E_6+[xyz^4]E_6
=\frac{10}{3}\gamma s,                                \tag{6}
\]
again impossible.

Equations (4)--(6) cover the complete minimal atlas (3), retain
\(\alpha,u,v,w\) and every lower jet, and divide by no coefficient.
Thus no candidate with \(\gamma\ne0\) satisfies \(E_6=0\).
\(\square\)

## Verification and scope

Run

```text
./verify_vertical_triple_gamma_nonzero_strict.sh
./audit_vertical_triple_gamma_nonzero/verify_strict.sh
```

The exact checker reconstructs the raw determinant on all three charts,
verifies (4)--(6), and tests fail-closed mutations of every obstruction.
The hostile audit independently reconstructs the raw determinant and
exterior \(E_6\) with dependency-free sparse arithmetic; its report is
`audit_vertical_triple_gamma_nonzero/REPORT.md`.

Together with the separate zero-\(\gamma\) reduction and its terminal
zero-\(\ell\) theorem, this excludes the complete
triple-root part of the \(s\ne0\) vertical companion.  It says nothing
about the separate \(s=0\) family.  Exact computation is evidence about
the encoded identities, not peer review; this note and checker were
materially AI-assisted.
