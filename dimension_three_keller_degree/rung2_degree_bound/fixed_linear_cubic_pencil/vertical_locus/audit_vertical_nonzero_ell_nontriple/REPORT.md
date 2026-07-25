# Hostile audit: the nonzero-\(\ell\), nontriple vertical companion

**Verdict:** **PASS**, on exactly the \(s\ne0\), nontriple
vertical-companion locus.

**Completed (UTC):** 2026-07-25T21:50:05Z.

`../VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md` is mathematically correct.
The squarefree stratum, the double-root noncollision stratum, and both
double-root collision kernels are exhaustive and all are contradicted by
raw degree-six coefficients.  The decisive calculation retains every
lower jet and does not use the optional binary \(E_4\) relation.

Together with the already audited zero-\(\ell\) lemma, this excludes the
entire \(s\ne0\), nontriple vertical companion.  It says nothing about
the triple-root or \(s=0\) branches and does not close frozen row
`Q2-E1-A3-B1-D1-N1`.

## 1. Normal forms, gauges, and a missing expository step

After a binary source change,
\[
q_0=q|_{z=0}=xy(x-y)\quad\text{or}\quad q_0=x^2y.
\]
Killing \([z^3]q\) by the legal leading-row target shear leaves exactly
\[
q=q_0+z(r_{20}x^2+r_{11}xy+r_{02}y^2)
       +z^2(r_{10}x+r_{01}y),                         \tag{1}
\]
with all five coefficients arbitrary.  The accompanying changes to
\(V,B,L_2\) are invertible renamings of unrestricted coefficients.
Shears by the third target row kill the independent \(bz^3\) summand of
the first cubic row and \([z^3]V\); they change \(A,B\) by multiples of
\(W\) and lose no lower jet.

The candidate proof begins its displayed calculation with
\[
W=z(ux+vy+wz).                                        \tag{2}
\]
Its statement does not explicitly repeat why the binary part \(W_0\)
vanishes.  This is a local expository omission, not a mathematical gap:
the hostile checker starts instead with
\[
W=W_0+z(ux+vy+wz),\qquad
W_0=g_0x^2+g_1xy+g_2y^2,
\]
and reconstructs
\[
E_6|_{z=0}=-s\,q_0\{q_0,W_0\}.                        \tag{3}
\]
For both \(q_0\), the map
\[
\mathbb C[x,y]_2\longrightarrow\mathbb C[x,y]_3,
\qquad K\longmapsto\{q_0,K\},
\]
has the literal \(3\times3\) minor \(-8\).  Since
\(\mathbb C[x,y]\) is a domain and \(s\ne0\), (3) forces \(W_0=0\),
giving (2).

The note should either include this one-line reduction or state
\(W_0=0\) as an inherited hypothesis from `E8_E4_RANK_LEDGER.md`.
The theorem as stated remains correct.

No normalization of the nonzero linear form
\[
\ell=ux+vy
\]
is used.  This is important: its position relative to the roots of
\(q_0\) controls the binary-kernel rank.

## 2. Independent raw binary \(E_5\) identity

The hostile checker constructs both the full raw determinant and the
exterior-multilinear \(E_5\) expression over a dependency-free sparse
polynomial ring, retaining:

- all five \(r_{ij}\) in (1);
- all twelve coefficients of \(A,B\);
- all five lower-\(z\) coefficients of \(V\);
- \(u,v,w\);
- every unrestricted entry of \(L\).

The complete degree-five coefficient maps agree.  Restricting to \(z=0\)
gives exactly
\[
E_5|_{z=0}
=s\left(\ell\{q_0,V_0\}
        -q_0\{q_0,\bar L_3\}\right),                  \tag{4}
\]
where
\[
\bar L_3=\ell_{31}x+\ell_{32}y.
\]
Thus the six-variable binary system is
\[
\ell\{q_0,V_0\}=q_0\{q_0,\bar L_3\}.                  \tag{5}
\]

## 3. Complete binary-kernel reconstruction

Order the unknowns as
\[
([x^3]V_0,[x^2y]V_0,[xy^2]V_0,[y^3]V_0,
 \ell_{31},\ell_{32})
\]
and rows as \(x^5,x^4y,\ldots,y^5\).

### Squarefree

The vector representing \((q_0,0)\),
\[
(0,1,-1,0,0,0),
\]
is in the kernel.  Independent sparse determinants reproduce the three
claimed minors:
\[
\begin{aligned}
-27u(u^2-4uv-4v^2),\qquad
27u^2v,\qquad
27v(4u^2+4uv-v^2).                                   \tag{6}
\end{aligned}
\]
If \(uv\ne0\), the middle minor is nonzero.  If \(v=0,u\ne0\), the first
is \(-27u^3\); if \(u=0,v\ne0\), the last is \(-27v^3\).
Hence every nonzero \(\ell\), including all three squarefree root-line
collisions, has rank five and
\[
V_0=\kappa q_0,\qquad\bar L_3=0.                      \tag{7}
\]

### Double root away from collisions

The known \((q_0,0)\) direction again bounds the rank by five.  The exact
minor
\[
108uv^2                                                   \tag{8}
\]
has no further divisor on \(uv\ne0\), proving (7) is the complete
noncollision kernel.

### Double root on the two collision lines

The locus \(uv=0,\ell\ne0\) is the disjoint union
\(\ell=cx\) and \(\ell=cy\), with \(c\ne0\).

For \(\ell=cx\), a rank-four minor is
\[
-54c^3,
\]
and the two independent kernel directions give
\[
V_0=\kappa x^2y+\frac23txy^2,\qquad
\bar L_3=cty.                                         \tag{9}
\]
For \(\ell=cy\), the corresponding minor is
\[
108c^3,
\]
and the complete kernel is
\[
V_0=\kappa x^2y+\frac13tx^3,\qquad
\bar L_3=ctx.                                         \tag{10}
\]
The checker builds both collision matrices directly rather than
specializing a generic inverse, verifies both kernel vectors, and rejects
perturbations of \(2/3\) and \(1/3\).  Thus no rank-jump direction is
missing.

## 4. The \(E_4\) aside is correct but unused

On the one-dimensional kernel (7), exact extraction gives
\[
E_4|_{z=0}
=-\ell\{q_0,\kappa A_0-sB_0\}.                       \tag{11}
\]
The same \(-8\) bracket minor used in Section 1 proves
\[
\kappa A_0=sB_0
\]
when \(\ell\ne0\).

This relation is not substituted anywhere in the decisive calculation.
In the checker, the later \(E_6\) determinants are rebuilt with the
original fully general `A` and `B` forms.  Exact equality of the decisive
coefficients to expressions involving only \(s,u,v\) or \(s,c\)
independently proves that no \(E_4\) constraint was imported.

## 5. Independent raw and exterior \(E_6\)

For every generic or collision kernel, the checker compares the full
source-degree-six part of the raw determinant with
\[
\begin{aligned}
E_6={}&
\operatorname{Jac}(P,Q,L_3)
+\operatorname{Jac}(U,Q,W)
+\operatorname{Jac}(P,V,W)\\
&+\operatorname{Jac}(A,Q,R)
+\operatorname{Jac}(U,V,R)
+\operatorname{Jac}(P,B,R),
\end{aligned}                                         \tag{12}
\]
where
\[
P=z^4,\quad Q=zq,\quad R=z^3,\quad
U=\frac43zW+s q.
\]
The two complete coefficient maps agree.

With all five \(q\)-tail moduli, \(A,B,V_{\rm tail},w,L\) still
symbolic, the generic kernels give:
\[
\begin{array}{c|cc}
q_0&\text{first coefficient}&\text{second coefficient}\\ \hline
xy(x-y)&[x^4yz]E_6=su &[xy^4z]E_6=-sv\\
x^2y&[x^4yz]E_6=su &[x^3y^2z]E_6=-2sv.
\end{array}                                           \tag{13}
\]
Since \(s\ne0\), either row forces \(u=v=0\), contradicting the
nonzero-\(\ell\) hypothesis.  The squarefree row applies uniformly to
all its root-line positions; the double row is used only on \(uv\ne0\).

On the complete collision kernels (9)--(10), separate raw expansions
give
\[
\begin{array}{c|c}
\ell=cx &[x^4yz]E_6=sc\\
\ell=cy &[x^3y^2z]E_6=-2sc.
\end{array}                                           \tag{14}
\]
Both are independent of \(t\) and every lower jet.  Because \(s,c\ne0\),
both collision branches are impossible.

These four cases are exhaustive:
\[
\{\text{squarefree }\ell\ne0,\;
\text{double }uv\ne0,\;
\text{double }\ell=cx,\;
\text{double }\ell=cy\}.
\]

## 6. Independent exact certificate

`verify_vertical_nonzero_ell_nontriple_sparse.py` reuses only the custom
sparse arithmetic kernel from an earlier hostile audit.  It imports no
CAS and no equations or pivots from the supplied SymPy script.  It:

- supplies the omitted raw \(W_0=0\) reduction;
- compares complete raw and exterior \(E_5,E_6\) coefficient maps;
- verifies every minor and every full kernel above;
- checks (11) separately;
- retains every stated modulus and lower jet in (13)--(14);
- uses normal-form and kernel-coefficient negative controls;
- rejects optimized Python and requires an exact sentinel.

Run:

```text
./verify_strict.sh
../verify_vertical_nonzero_ell_nontriple_strict.sh
```

Both the hostile sparse reconstruction and the supplied SymPy
implementation pass.  Exact algebra checks are not peer review.  This
audit and its software were materially AI-assisted.
