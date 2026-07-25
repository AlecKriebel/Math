# Hostile audit: triple-root nonzero-\(\gamma\) vertical branch

**Verdict:** **PASS**, exactly for the \(s\ne0\), \(\gamma\ne0\),
triple-root vertical companion stated in
`../VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md`.

**Completed (UTC):** 2026-07-25T21:41:16Z.

The three raw degree-six obstructions in the candidate note are correct.
The atlas is complete on the minimal triple-root locus, all target gauges
are legal with their lower-jet action retained, and neither \(s\) nor
\(\gamma\) is secretly normalized. No surviving chart or parameter divisor
was found.

This verdict says nothing about the separate \(s=0\) vertical companion and
does not by itself exclude the full frozen row
`Q2-E1-A3-B1-D1-N1`.

The audited inputs have hashes

```text
f7b972de0601e605e43c834a9558d8f5e5758d20fd8d7e13a1017f0d50482dfd  ../VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md
b35ee24e98ca67eb84d86c4fa0c293b11a9a2baf84cdb2a0873374ed81cb4750  ../verify_vertical_triple_gamma_nonzero_sympy.py
4b912aca939a8f63f5430e2fed36518a3c0de7d4718cff0404f5ea10bb622615  ../verify_vertical_triple_gamma_nonzero_strict.sh
33ceb29cb835361909f515510e76954a062bb05c06e84b89a9e7b8188b1667c7  verify_vertical_triple_gamma_nonzero_sparse.py
74071e1e8f4e0b2895ea9b881706e018d53b11620818588504d970a245f3c55c  verify_strict.sh
9ad87c003bc0ce00e86b8c863b53af356aeec900d487c93999981908e28528e9  ../audit_vertical_triple_yz2_gamma0_ell0/verify_vertical_triple_yz2_sparse.py
```

The shared sparse kernel was extended after the first audit run.  The exact
diff only appends the unused symbol names
`u,v,kappa,c,t,r20,r11,r02,r10,r01,g0,g1,g2` to `NAMES`; it changes no
arithmetic routine, form, determinant, or assertion.  This audit addresses
variables through the kernel's name-to-index map, so the larger exponent
tuples are semantically compatible.  The pin and hashes above record the
extended kernel.  The hostile runner, the supplied runner, the kernel's own
strict regression, and the three dependent prior hostile regressions were
all rerun successfully after the repin.

## 1. Atlas, minimality boundary, and gauges

Normalize the triple root of \(q|_{z=0}\) to \(x=0\) and its nonzero
coefficient to one. Before further reduction, the cubic is
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.
\tag{1}
\]
The coefficient of \(x^3\) was nonzero by the triple-root hypothesis, so
this initial scaling introduces no missing zero branch. It may rescale the
coefficient \(s\) in \(U=\frac43zW+sq\), but preserves \(s\ne0\).

The full parabolic preserving \(z=0\) and the marked triple root has the
form
\[
x\mapsto ax+uz,\qquad
y\mapsto by+cx+vz,\qquad
z\mapsto dz,\qquad abd\ne0.
\tag{2}
\]
Splitting before any division gives:

1. \(C\ne0\), which reduces to
   \[
   x^3+y^2z+\alpha xz^2+\beta z^3;
   \]
2. \(C=0,B\ne0\), which reduces to
   \[
   x^3+xyz+\beta z^3;
   \]
3. \(C=B=0,E\ne0\), which reduces to
   \[
   x^3+yz^2;
   \]
4. \(C=B=E=0\), when \(q\in\mathbb C[x,z]_3\).

The fourth case is exactly the nonminimal boundary. Conversely, if
\((z^3,q)\) is a nonminimal cubic pencil, then
\[
q\in\operatorname{Sym}^3\langle z,L\rangle.
\]
The equality \(q|_{z=0}=x^3\) forces \(L\bmod z\) to be proportional to
\(x\), hence \(q\in\mathbb C[x,z]\). Thus the three displayed charts are
disjoint by their ordered conditions and exhaustive on the minimal locus.

The source transformations (2) preserve \(z\) up to scale and send \(x\)
to a nonzero multiple of \(x\) modulo \(z\). Therefore
\[
W|_{z=0}=\gamma x^2,\qquad\gamma\ne0
\]
remains in the exact general form
\[
W=\gamma x^2+z(ux+vy+wz),
\tag{3}
\]
with a changed but still nonzero \(\gamma\). The audit retains
\(\gamma,u,v,w\); it never sets \(\gamma=1\).

On the first two charts, the target shear
\[
F_2\mapsto F_2-\beta F_1
\]
replaces \(q\) by \(q-\beta z^3\). Simultaneously it sends
\[
(V,B,L_2)\mapsto(V-\beta U,B-\beta A,L_2-\beta L_1),
\]
an invertible renaming because \(V,B,L_2\) remain unrestricted.

The complete vertical-companion \(E_7\) solution is
\[
U=\frac43zW+sq+bz^3.
\]
Adding a multiple of \(F_3\) to \(F_1\) kills \(b\), while adding a
multiple of \(F_3\) to \(F_2\) kills the \(z^3\)-coefficient of \(V\).
These shears change \(A,B\) by multiples of \(W\) and the corresponding
linear rows by multiples of \(L_3\). Since all those coefficients are
retained, the operations discard no lower-jet locus.

The exact gauged atlas is consequently
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2,
\end{aligned}
\tag{4}
\]
with \(\alpha,\gamma,s,u,v,w\), all six coefficients of each of \(A,B\),
all nine allowed coefficients of \(V\), and all nine entries of \(L\)
retained.

## 2. Independent sparse reconstruction of \(E_6\)

The hostile checker imports no computer algebra system and does not import
the supplied SymPy checker. It uses exact sparse multivariate arithmetic
over \(\mathbb Q\).

First it constructs
\[
\det(L+JH_2+JH_3+JH_4)
\tag{5}
\]
directly and extracts its complete source-degree-six coefficient map.
Independently, with
\[
P=z^4,\qquad Q=zq,\qquad R=z^3,\qquad
U=\frac43zW+sq,
\]
it constructs the exterior expansion
\[
\begin{aligned}
E_6={}&
\operatorname{Jac}(P,Q,L_3)
+\operatorname{Jac}(U,Q,W)
+\operatorname{Jac}(P,V,W)\\
&+\operatorname{Jac}(A,Q,R)
+\operatorname{Jac}(U,V,R)
+\operatorname{Jac}(P,B,R).
\end{aligned}
\tag{6}
\]
The two complete coefficient maps agree exactly on every chart. The checker
also verifies \(E_8=E_7=0\) before using \(E_6\).

Because all lower coefficients are independent sparse variables, the
cancellations below are polynomial identities, not sample
specializations.

## 3. Chartwise reconstruction

### Chart \(q_C\)

Both reconstructions give
\[
\boxed{[x^4yz]E_6=4\gamma s.}
\tag{7}
\]
The expression contains no \(\alpha,u,v,w,A,B,V,L\). Since
\(\gamma s\ne0\), this chart is empty.

### Chart \(q_B\)

The two claimed expressions are exactly
\[
\begin{aligned}
C_1&=[x^5z]E_6=s(2\gamma-3v),\\
C_2&=-\frac16[x^3yz^2]E_6+[xy^2z^3]E_6
    =-\frac{s}{3}(\gamma+v).
\end{aligned}
\tag{8}
\]
Rather than divide by \(s\) or solve for \(v\), the hostile checker verifies
the denominator-free elimination
\[
\boxed{C_1-9C_2=5\gamma s.}
\tag{9}
\]
If \(E_6=0\), both \(C_1,C_2\) vanish, contradicting
\(\gamma s\ne0\). Thus the two relations are incompatible on the entire
chart.

### Chart \(q_E\)

Exact sparse addition gives
\[
\boxed{
\frac23[x^4z^2]E_6+[xyz^4]E_6
=\frac{10}{3}\gamma s.}
\tag{10}
\]
This chart is empty for the same reason.

Equations (7)--(10) retain every lower jet and contain no denominator in a
modulus. The rational constants are nonzero in characteristic zero.

## 4. Negative controls and strict replay

For every chart, the hostile checker performs three raw-input mutations.

1. It doubles the normalized \(x^3\)-coefficient of \(q\) and confirms that
   at least one advertised identity changes.
2. It adds \(xy\) to \(W|_{z=0}\), leaving the classified
   \(\gamma x^2\) scope, and confirms that the complete \(E_6\) coefficient
   map changes before coefficient selection.
3. It shifts the \(x^2\)-coefficient of \(W|_{z=0}\) and confirms that an
   advertised obstruction changes.

The strict wrapper rejects optimized Python and requires an exact output
whitelist. The independent and supplied checks both pass:

```text
./audit_vertical_triple_gamma_nonzero/verify_strict.sh
./verify_vertical_triple_gamma_nonzero_strict.sh
```

with terminal sentinels

```text
PASS: HOSTILE_VERTICAL_TRIPLE_GAMMA_NONZERO_STRICT_119F2A
VERTICAL_TRIPLE_GAMMA_NONZERO_STRICT_PASS_0A6B35
```

## 5. Final disposition

No omitted minimal chart, illegal shear, lost lower coefficient, hidden
\(\gamma=1\) normalization, parameter divisor, or cancellation error was
found.

\[
\boxed{\text{HOSTILE AUDIT PASS at the candidate theorem's exact scope.}}
\]

This audit and its software were produced with substantial AI assistance.
They are not peer review. Exact checks are evidence about the encoded
algebra, not verification by the mathematical community.
