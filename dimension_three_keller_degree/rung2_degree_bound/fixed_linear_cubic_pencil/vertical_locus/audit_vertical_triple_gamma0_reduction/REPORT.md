# Hostile audit: reduction of the triple-root \(\gamma=0\) branch

**Verdict:** **PASS**, precisely for the \(s\ne0\), triple-root,
\(\gamma=0\) vertical companion.

**Completed (UTC):** 2026-07-25T21:36:24Z.

The reduction in `../VERTICAL_TRIPLE_GAMMA0_REDUCTION.md` is correct:
the raw degree-six determinant identity forces the complete linear form
\(\ell=ux+vy\) in
\[
W=z(\ell+wz)
\]
to vanish on all three minimal charts.  The already hostile-audited
zero-\(\ell\) theorem then excludes the resulting locus.

This does **not** address \(\gamma\ne0\) or \(s=0\), and it does not close
frozen row `Q2-E1-A3-B1-D1-N1`.

## 1. Atlas, boundary, and gauges

With the triple root normalized to \(x\), the full marked cubic is
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.              \tag{1}
\]
Independent parabolic reduction gives:

\[
\begin{array}{c|c}
\text{source stratum}&\text{normal form before target removal}\\ \hline
C\ne0&
x^3+y^2z+\alpha xz^2+\beta z^3\\
C=0,\ B\ne0&
x^3+xyz+\beta z^3\\
C=B=0,\ E\ne0&
x^3+yz^2.
\end{array}                                            \tag{2}
\]
If \(C=B=E=0\), then \(q\) is binary in \(x,z\), which is exactly the
nonminimal boundary.  Conversely, nonminimality of \((z^3,q)\) forces
\(q\in\operatorname{Sym}^3\langle z,L\rangle\), and
\(q|_{z=0}=x^3\) then forces \(q\in\mathbb C[x,z]\).  Thus (2) is
complete on the minimal locus.

The source transformations preserve \(z\) up to scale.  Starting with
\(W|_{z=0}=0\), they therefore leave the exact general form
\[
W=z(ux+vy+wz),                                        \tag{3}
\]
with \(u,v,w\) all retained.  This is precisely \(\gamma=0\), because
the preceding plane restriction on the triple-root locus gives
\(W_0=\gamma x^2\).

On the vertical companion, the target shear
\(F_2\mapsto F_2-\beta F_1\) removes \(\beta z^3\) from \(q\) in the
first two charts.  It sends
\[
(V,B,L_2)\mapsto(V-\beta U,B-\beta A,L_2-\beta L_1),
\]
an invertible renaming of unrestricted lower jets.  Subsequent shears by
\(F_3\) kill the independent \(bz^3\) summand of \(U\) and the
\(z^3\)-coefficient of \(V\), changing \(A,B\) by multiples of \(W\)
and the corresponding linear rows by multiples of \(L_3\).  Hence the
complete gauged atlas is
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2,                                       \tag{4}
\end{aligned}
\]
with \(\alpha,u,v,w\), all twelve coefficients of \(A,B\), all nine
allowed coefficients of \(V\), and all nine entries of \(L\) retained.

## 2. Independent reconstruction of the raw \(E_6\) identity

Put
\[
P=z^4,\qquad Q=zq,\qquad R=z^3,\qquad
U=\frac43zW+s q.
\]
The hostile checker constructs the full raw determinant
\[
\det(L+JH_2+JH_3+JH_4)
\]
using dependency-free sparse polynomial arithmetic.  Separately, it
constructs the degree-six identity by exterior multilinearity:
\[
\begin{aligned}
E_6={}&
\operatorname{Jac}(P,Q,L_3)
+\operatorname{Jac}(U,Q,W)
+\operatorname{Jac}(P,V,W)\\
&+\operatorname{Jac}(A,Q,R)
+\operatorname{Jac}(U,V,R)
+\operatorname{Jac}(P,B,R).                           \tag{5}
\end{aligned}
\]
The two complete coefficient maps agree exactly on every chart.
The checker also confirms \(E_8=E_7=0\) before using \(E_6\).

Because every lower coefficient remains an independent symbolic
variable, equality of the expressions below certifies their cancellation;
it is not evidence from a sample specialization.

## 3. The common \(v\)-obstruction

On each chart in (4), exact extraction from either reconstruction gives
\[
[x^5z]E_6=-3sv.                                      \tag{6}
\]
For a Keller map, every positive-degree homogeneous part of its
determinant vanishes.  Since \(s\ne0\) and the field has characteristic
zero, (6) forces
\[
v=0.                                                  \tag{7}
\]
The coefficient contains no \(\alpha,w,A,B,V,L\), so there is no hidden
rank divisor or lower-jet compatibility condition.

## 4. The chartwise \(u\)-obstructions

After imposing (7), exact sparse addition gives:
\[
\begin{array}{c|l}
q_C&
\frac13[x^3yz^2]E_6+[y^3z^3]E_6=\frac83su\\[2mm]
q_B&
-\frac19[x^4z^2]E_6-\frac13[x^2yz^3]E_6
  +[y^2z^4]E_6=-\frac49su\\[2mm]
q_E&
\frac13[x^3z^3]E_6+[yz^5]E_6=\frac43su.
\end{array}                                           \tag{8}
\]
Again, these are identities in the full polynomial coefficient ring:
all entries of \(A,B,V,L\), together with \(\alpha,w\), cancel
literally.  Every coefficient on the left vanishes for a Keller map.
The nonzero rational constants and \(s\ne0\) therefore give
\[
u=0                                                   \tag{9}
\]
on every minimal chart.

Equations (7) and (9) prove
\[
W=wz^2.                                               \tag{10}
\]
No division by \(u,v,w,\alpha\), or a polynomial in any modulus occurs.

## 5. Inference to the audited theorem

The hostile-audited theorem in
`../VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md` has exactly the remaining
hypotheses:

- the same three minimal charts (4);
- the same \(s\ne0\) vertical-companion gauge;
- \(W=wz^2\), with \(w=0\) allowed;
- every lower jet unrestricted.

Thus applying it after (10) is direct and does not cross a chart or
genericity boundary.  The whole **\(s\ne0,\gamma=0\)** triple-root
vertical branch is excluded.

The candidate note's shorter phrase “the entire \(\gamma=0\) branch”
should always be read with its stated \(s\ne0\) hypothesis.  Its own
scope section correctly leaves the separate \(s=0\) family open.

## 6. Independent certificate and negative controls

`verify_vertical_triple_gamma0_reduction_sparse.py` imports no CAS and
does not import the supplied coefficient selections.  It reuses only the
dependency-free sparse arithmetic kernel from the earlier hostile audit.
For each chart it:

- compares the full raw-determinant \(E_6\) map with the independent
  exterior expansion (5);
- verifies (6) and (8) with all lower jets symbolic;
- changes only the normalized \(x^3\)-coefficient of \(q\) and confirms
  that both decisive identities fail;
- adds \(x^2\) to \(W_0\) and confirms the checker detects departure from
  the \(\gamma=0\) scope;
- rejects optimized Python and requires an exact success sentinel.

Run:

```text
./verify_strict.sh
../verify_vertical_triple_gamma0_reduction_strict.sh
```

Both the hostile sparse reconstruction and the supplied SymPy checker,
including its six mutation tests, pass.  Exact algebra checks are not
peer review.  This audit and its software were materially AI-assisted.
