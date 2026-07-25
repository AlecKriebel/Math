# Hostile audit: the zero-\(a\), zero-\(W_0\) vertical companion

**Verdict:** **PASS**, exactly for the \(a=0,\ W|_{z=0}=0\)
vertical-companion locus stated in
`../VERTICAL_A0_W0_ZERO_EXCLUSION.md`.

**Completed (UTC):** 2026-07-25T22:10:03Z.

I independently reconstructed the raw \(E_6,E_5,E_4\) calculation before
opening the candidate note or its checker.  I did not inspect any
`explore_*` or `derive_*` file.  After the reconstruction was complete, I
compared it with the candidate line by line and replayed both verification
paths.  No omitted chart, parameter divisor, lower jet, sign discrepancy,
or false implication was found.

This verdict excludes only the stated sublocus of frozen row
`Q2-E1-A3-B1-D1-N1`.  It says nothing about the separate
\(a=0,\ W|_{z=0}\ne0\) family and does not close the frozen row.

The audited inputs are pinned by

```text
d1f0889a54d9185a4f899d7ca6f5eb702a040a8cfdcb1733a4427896940eb09c  ../VERTICAL_A0_W0_ZERO_EXCLUSION.md
94961709c9bfbff7dd4fe0e4ce2d7283bcf958a9d52cc773dcd28c7edeec7566  ../verify_vertical_a0_w0zero_sympy.py
c57e44c44fb40cdd9557beec93e3594644360552115398bf4372684626391ed4  ../verify_vertical_a0_w0zero_strict.sh
8523035eb97b20ce28c20e96d8b9946888bfd013bf4ab46eca429add26f979fb  ../VERTICAL_SZERO_W0_EXCLUSION.md
e0ee3089f7e3155acc9497dbe4c0660637a3c2d84b863a0fd8f69f7a5cbd8c73  ../verify_vertical_szero_w0_sympy.py
b6eede6838de62051d07283d0fba3f52e2a27edc1c5ff597823dbd5b57c9a92e  ../verify_vertical_szero_w0_pari.gp
231d9e8284c94ac3bc12129cb4d9857244ecaa90fbf77061921f89496f7a06c3  ../verify_vertical_szero_w0_strict.sh
```

## 1. Independent setup and atlas

I started from
\[
H_4=(z^4,zq,0)^T,\qquad
H_3=\left(\frac43zW,V,z^3\right)^T,\qquad
H_2=(A,B,W)^T,
\]
with
\[
W=z(\mu x+\nu y+\omega z).
\]
For the squarefree and double-root strata I retained the more general
forms
\[
q=q_0+z(d_0x^2+d_1xy+d_2y^2)
      +z^2(e_0x+e_1y)+\beta z^3,
\]
where \(q_0=xy(x-y)\) or \(x^2y\).  On the triple-root stratum, a direct
reduction of
\[
x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3
\]
under the parabolic stabilizer of \(z=0\) and the marked triple root
gives precisely
\[
\begin{array}{ll}
C\ne0:&x^3+y^2z+\alpha xz^2+\beta z^3,\\
C=0,\ B\ne0:&x^3+xyz+\beta z^3,\\
C=B=0,\ E\ne0:&x^3+yz^2+\beta z^3.
\end{array}
\]
If \(C=B=E=0\), then \(q\) is binary in \(x,z\), which is exactly the
nonminimal boundary.  Thus the candidate's five charts are exhaustive
on its stated minimal locus.

My reconstruction also retained the \(z^3\)-coefficient of \(V\).
Neither that coefficient nor \(\beta\) occurs in the final
compatibilities.  The candidate removes them by target shears.  Those
shears only rename the otherwise arbitrary lower jets of \(A,B,V,L\), so
the shorter candidate atlas loses no locus.

## 2. Independent \(E_6\) solve

Write \(\ell=\mu x+\nu y\).  A fresh raw determinant expansion gives,
on all five charts,
\[
A=\frac29\ell^2+
z\left(\frac49\omega\ell+
       \frac43(\lambda_{31}x+\lambda_{32}y)\right)
+\eta z^2.                                           \tag{1}
\]
I solved for the five coefficients of \(A\), rather than for the five
variables selected by the candidate.  The resulting constant pivot
determinants, in squarefree, double-root, \(q_C,q_B,q_E\) order, are
\[
3888,\quad 3888,\quad -104976,\quad -8748,\quad -26244.
\]
Substitution into every coefficient of \(E_6\) gives zero.  Consequently
the solve has no hidden rank divisor in a chart modulus.

The candidate instead writes
\[
\begin{aligned}
A_{20}&=\frac29\mu^2,&
A_{11}&=\frac49\mu\nu,&
A_{02}&=\frac29\nu^2,\\
\lambda_{31}&=\frac{9A_{10}-4\mu\omega}{12},&
\lambda_{32}&=\frac{9A_{01}-4\nu\omega}{12}.
\end{aligned}                                        \tag{2}
\]
Equations (1) and (2) are identical:
\[
A_{10}=\frac49\mu\omega+\frac43\lambda_{31},\qquad
A_{01}=\frac49\nu\omega+\frac43\lambda_{32}.
\]
The differing pivot determinants therefore reflect only a different
choice of solved variables.

The candidate extracts homogeneous source degrees from
\(\det(L+JH_2+JH_3+JH_4)\), rather than introducing an auxiliary
parameter.  This is valid here: \(JH_i\) has source degree \(i-1\), so
source degree \(k\) is exactly the coefficient of the corresponding
weight in the auxiliary-parameter expansion.

## 3. Independent \(E_5\) branch decomposition

After (1), the complete \(E_5\) identity gives:

- on the squarefree, double-root, and \(q_C\) charts,
  \(\mu=\nu=0\);
- on \(q_B\) and \(q_E\), first \(\nu=0\), followed by either
  \(\mu=0\) or the exceptional nonzero-\(\mu\) branch.

On the common \(\mu=\nu=0\) branch,
\[
\lambda_{11}=\frac49\omega\lambda_{31},\qquad
\lambda_{12}=\frac49\omega\lambda_{32}.               \tag{3}
\]
On the exceptional \(q_B\) branch,
\[
\begin{aligned}
\lambda_{32}&=-\frac19\mu^2,&
\lambda_{31}&=\frac13\mu\omega,\\
\lambda_{12}&=-\frac4{81}\mu^2\omega,&
\lambda_{11}&=\frac{\mu}{27}
  (-12\lambda_{33}+18\eta-4\omega^2).
\end{aligned}                                        \tag{4}
\]
On the exceptional \(q_E\) branch,
\[
\begin{aligned}
\lambda_{32}&=0,&
\lambda_{31}&=\frac13\mu\omega,\\
\lambda_{12}&=\frac4{81}\mu^3,&
\lambda_{11}&=\frac{\mu}{27}
  (-12\lambda_{33}+18\eta-4\omega^2).
\end{aligned}                                        \tag{5}
\]
Substitution verifies every \(E_5\) coefficient on each branch.  Under
(2), (3)--(5) are exactly the candidate's equations (17), (20), and
(22).

## 4. Independent \(E_4\) obstruction

On the common zero-\(\ell\) branch, literal squares force
\(\lambda_{31}=\lambda_{32}=0\):
\[
\begin{array}{c|cc}
q_{\rm sf}&[x^3z]=-\frac43\lambda_{31}^2&
[y^3z]=-\frac43\lambda_{32}^2\\
q_{\rm dbl}&[x^3z]=-\frac43\lambda_{31}^2&
[xy^2z]=\frac83\lambda_{32}^2\\
q_C&[x^2yz]=4\lambda_{32}^2&
[xyz^2]=-\frac83\lambda_{31}^2\\
q_B&[x^2yz]=4\lambda_{32}^2&
[x^2z^2]_{\lambda_{32}=0}=-\frac43\lambda_{31}^2\\
q_E&[x^2yz]=4\lambda_{32}^2&
[xz^3]=-\frac43\lambda_{31}^2.
\end{array}                                          \tag{6}
\]
Then (3) kills \(\lambda_{11},\lambda_{12}\).  Rows one and three of
\(L\) are both vertical, so \(\det L=0\).

For the exceptional \(q_B\) branch, let
\(v_1=[x^2y]V\) and \(v_6=[yz^2]V\).  Three coefficients are
\[
\begin{aligned}
c_{400}&=\frac4{81}\mu^3(\mu+9v_1),\\
c_{211}&=-\frac4{27}\mu^3(-\mu+v_1-6v_6),\\
c_{022}&=\frac4{243}\mu^3(\mu+18v_6),
\end{aligned}
\]
and the denominator-free combination
\[
81c_{400}+243c_{211}-729c_{022}=28\mu^4             \tag{7}
\]
contradicts \(E_4=0\) when \(\mu\ne0\).

For \(q_E\), with \(v_5=[xyz]V\),
\[
c_{301}=\frac4{81}\mu^3(-2\mu+9v_5),\qquad
c_{013}=-\frac4{27}\mu^3(-\mu+v_5),
\]
and
\[
81c_{301}+243c_{013}=28\mu^4.                        \tag{8}
\]
Equations (6)--(8) are exactly the candidate's \(E_4\) contradictions
after applying (2).

## 5. Independent verification

The independent artifacts are

- `../VERTICAL_SZERO_W0_EXCLUSION.md`, the reconstruction recorded
  before the candidate comparison;
- `../verify_vertical_szero_w0_sympy.py`, a full raw-determinant check
  with all five charts, all lower jets, full \(E_5\) converses, mutations,
  and an optimized-Python guard;
- `../verify_vertical_szero_w0_pari.gp`, a second implementation in
  PARI/GP using exterior row-polarization: it sums the \(4^3\) row
  selections directly instead of forming the weighted determinant;
- `../verify_vertical_szero_w0_strict.sh`, which fail-closes both paths.

Both the candidate strict runner and the independent strict runner pass:

```text
VERTICAL_A0_W0_ZERO_SYMPY_PASS_3C79E1
VERTICAL_A0_W0_ZERO_STRICT_PASS_91D42B
PASS: s=0, W0=0 vertical companion excluded on 2 nontriple + 3 minimal triple-root charts
VERTICAL_SZERO_W0_PARI_PASS_C5E4A2
PASS: optimized-Python false-pass guard
```

The independent checker is not dependency-free: it uses SymPy for one
path and PARI/GP for the other.  It is nevertheless methodologically
independent of the candidate checker in both derivation and the
PARI/GP exterior-expansion algorithm.  All calculations are exact
evidence about the encoded algebra, not peer review.  This audit and its
software were materially AI-assisted.
