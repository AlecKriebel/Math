# Hostile audit: the zero-\(\ell\), nontriple vertical companion

**Verdict:** **PASS**, with the scope stated in
`../VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md`.

**Completed (UTC):** 2026-07-25T21:07:39Z.

The candidate lemma correctly excludes the \(a\ne0\), \(\ell=0\) part of
the vertical companion when \(q|_{z=0}\) has root partition \(1+1+1\) or
\(2+1\).  I found no illegal gauge, omitted lower-\(z\) modulus, hidden
division, internal rank divisor, or determinant-sign error.

This result does **not** close the frozen row
`Q2-E1-A3-B1-D1-N1`.  In particular it says nothing about the
nonzero-\(\ell\) families, either double-root collision, the triple-root
family, or the \(a=0\) family.

## 1. Scope and simultaneous legality of the gauges

Before the gauges, the already derived vertical-companion \(E_7\) family
has
\[
\begin{aligned}
H_4&=(z^4,zq,0)^T,\\
H_3&=\left(\frac43zW+a q+bz^3,\ V,\ z^3\right)^T .
\end{aligned}                                         \tag{1}
\]
The branch audited here has \(a\ne0\).  Renaming \(a=s\) therefore
introduces exactly the hypothesis \(s\ne0\), rather than an additional
genericity assumption.

All three coefficient removals in the candidate note can be made
simultaneously:

1. If \([z^3]q=c\), the target shear
   \(F_2\mapsto F_2-cF_1\) replaces \(q\) by \(q-cz^3\).
   It also replaces the complete lower jets
   \(V,B,L_2\) by \(V-cU,B-cA,L_2-cL_1\).
2. Rewriting (1) in the new \(q\) can change the coefficient \(b\).
   The shear \(F_1\mapsto F_1-bF_3\) kills that new coefficient and
   simultaneously replaces \(A,L_1\) by \(A-bW,L_1-bL_3\).
3. The shear \(F_2\mapsto F_2-dF_3\), for the resulting
   \(d=[z^3]V\), kills \([z^3]V\) and replaces \(B,L_2\) by
   \(B-dW,L_2-dL_3\).

The third row of \(H_4\) is zero, so the last two operations preserve
\(H_4\).  In every step, the affected quadratic and linear coefficients
were arbitrary before the shear and remain arbitrary after being
renamed.  Thus no lower-jet condition is smuggled into the normalization.

On the nontriple locus, a block-diagonal source change on \(x,y\)
normalizes
\[
q_0=q|_{z=0}
\]
to \(xy(x-y)\) or \(x^2y\).  This uses only the standard two
\(\operatorname{PGL}_2(\mathbb C)\)-orbits of nontriple binary cubics.
After the \(z^3\) term has been killed, an arbitrary cubic with either
leading form is exactly
\[
q=q_0+z(r_{20}x^2+r_{11}xy+r_{02}y^2)
       +z^2(r_{10}x+r_{01}y).                          \tag{2}
\]
All five displayed coefficients are retained without a nonvanishing
assumption.  The normalization may be redundant under the residual
stabilizer, but redundancy cannot omit a candidate.

Finally, \(W_0=0\) gives
\[
W=z(\alpha x+\beta y+wz).
\]
The exceptional leaf \(\ell=0\) is precisely \(\alpha=\beta=0\), hence
\(W=wz^2\), with \(w=0\) allowed.  The checker also reconstructs the raw
determinant and confirms that \(E_8=E_7=0\) identically on this normalized
family.

## 2. Independent degree-six reconstruction

Write the nine coefficients of \(V\), in order, on
\[
x^3,x^2y,xy^2,y^3,x^2z,xyz,y^2z,xz^2,yz^2
\]
and put \(\lambda=\ell_{31}\), \(\mu=\ell_{32}\).  A fresh sparse
determinant expansion confirms that every degree-six equation is jointly
linear in these eleven unknowns.

Without importing a pivot from the SymPy verifier, rational elimination
at the specialization \(s=1\) and all other parameters zero selects the
following common row monomials:
\[
\begin{gathered}
x^4z^2,\ x^3z^3,\ x^2y^2z^2,\ x^2yz^3,\ x^2z^4,\\
xy^3z^2,\ xy^2z^3,\ xyz^4.                             \tag{3}
\end{gathered}
\]
In the squarefree case the selected columns are
\[
v_0,v_1,v_3,v_4,v_5,v_6,v_7,v_8,
\]
and in the double-root case they are
\[
v_0,v_2,v_3,v_4,v_5,v_6,v_7,v_8.
\]
The exact symbolic determinant of either \(8\times8\) matrix is
\[
2^5 3^{11}s^8=5\,668\,704s^8.                          \tag{4}
\]
It is independent of every \(r_{ij}\), every coefficient of \(A,B\),
\(w\), and every entry of \(L\).  Hence the rank is at least eight
everywhere on \(s\ne0\).

Direct substitution into *every* degree-six coefficient gives
\[
V=kq+\frac zs(A-a_5z^2)
      -\frac4{3s}z^2(\lambda x+\mu y).                 \tag{5}
\]
The parameters \(k,\lambda,\mu\) give three independent solution
directions: \(\lambda,\mu\) are themselves two of the eleven coordinates,
and the \(k\)-direction has nonzero binary part \(q_0\).  Thus the
solution space has dimension at least three.  Together with (4), in an
eleven-variable linear system, this proves rank exactly eight and proves
that (5) is the complete family.  The only divisions are by \(s\) and
\(3\), both units under the stated hypotheses.

## 3. Degrees five and four

After (5), independent coefficient extraction gives
\[
\begin{array}{c|cc}
q_0&[x^4y]E_5&\text{second coefficient}\\ \hline
xy(x-y)&s\lambda&[xy^4]E_5=-s\mu\\
x^2y&s\lambda&[x^3y^2]E_5=-2s\mu .
\end{array}                                            \tag{6}
\]
Characteristic zero and \(s\ne0\) therefore force
\(\lambda=\mu=0\), with no division by a root modulus.

The remaining degree-five system is jointly linear in
\(b_0,\ldots,b_4\).  On the row monomials
\[
x^3z^2,\ x^2yz^2,\ x^2z^3,\ xy^2z^2,\ xyz^3           \tag{7}
\]
its literal determinant, in the displayed order, is
\[
-2^4 3^5s^5=-3888s^5.                                 \tag{8}
\]
Checking all remaining degree-five coefficients gives the unique solution
\[
\begin{aligned}
b_0&=a_0k/s,&b_1&=a_1k/s,&b_2&=a_2k/s,\\
b_3&=(a_3k+\ell_{11})/s,&
b_4&=(a_4k+\ell_{12})/s,
\end{aligned}                                         \tag{9}
\]
while \(b_5\) remains free at this stage.

After (9), the two stated degree-four coefficients are exactly
\[
\begin{array}{c|cc}
q_0&\text{first}&\text{second}\\ \hline
xy(x-y)&
3(k\ell_{11}-s\ell_{21})&
3(k\ell_{12}-s\ell_{22})\\
x^2y&
3(k\ell_{11}-s\ell_{21})&
-6(k\ell_{12}-s\ell_{22}).
\end{array}                                            \tag{10}
\]
Thus the first two entries of row two of \(L\) are \(k/s\) times the
first two entries of row one.  Equation (6) has already made the first
two entries of row three zero, so
\[
\det L=\ell_{33}
(\ell_{11}\ell_{22}-\ell_{12}\ell_{21})=0.             \tag{11}
\]
For a Keller map, however,
\(\det L=\det JF(0)\) is the nonzero constant Jacobian.  This is a valid
contradiction even when that constant has not been normalized to one.

## 4. Independent exact certificate

`verify_vertical_ell_zero_sparse.py` implements sparse multivariate
Laurent-polynomial arithmetic over \(\mathbb Q\) from scratch.  It does
not import SymPy, PARI/GP, or the supplied verifier.  It:

- reconstructs the determinant directly from \(L,JH_2,JH_3,JH_4\);
- checks \(E_8=E_7=0\);
- independently selects the pivots and proves (4) and (8) symbolically;
- asserts joint linearity before using either rank argument;
- verifies (5), (6), (9), (10), and (11) against every relevant
  determinant coefficient;
- retains all five \(q\)-moduli and all unused coefficients symbolically;
- includes negative controls for the \(V\)-solve, the \(B\)-solve, and
  the final singularity calculation.

Run:

```text
./verify_strict.sh
../verify_vertical_ell_zero_nontriple_strict.sh
```

Both the dependency-free reconstruction and the original SymPy
calculation pass.  These are methodologically independent implementations
of the encoded algebra.  They are not peer review, and the proof and
audit were produced with substantial AI assistance.
