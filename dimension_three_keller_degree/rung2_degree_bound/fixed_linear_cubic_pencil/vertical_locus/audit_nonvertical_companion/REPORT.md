# Hostile audit: the nonvertical cubic companion

**Verdict:** **PASS**, on the stated primitive triple-vertical leading
stratum over \(\mathbb C\).

**Completed:** 2026-07-25T20:53:41Z.

The two working lemmas
`../NONVERTICAL_NONTRIPLE_LEMMA.md` and
`../NONVERTICAL_TRIPLE_ROOT_LEMMA.md` correctly exclude every
nonvertical companion
\[
H_4=(z^4,zq,0)^T,\qquad (H_3)_3=q
\]
when \((z^3,q)\) is a coprime minimal cubic pencil.  I found no omitted
root stratum, minimal/nonminimal boundary, parameter divisor, or illegal
gauge.

This verdict does **not** close the frozen row
`Q2-E1-A3-B1-D1-N1`.  Its vertical companion
\((H_3)_3=z^3\) remains open.

## 1. Independent reconstruction of the \(E_7\) gauge

Put
\[
S=4z^4W-4z^3V+qU.
\]
The \(E_7\) equation is
\[
\{q,S\}_{x,y}=0.                                      \tag{1}
\]
Here \(q\) and \(z\) are algebraically independent, so (1) makes \(S\)
algebraic over \(\mathbb C(q,z)\).

Let \(u=q/z^3\).  Minimality of the pencil says that
\(\mathbb C(u)\) is relatively algebraically closed in the
degree-zero function field.  The same scaling-variable argument used in
the parent package therefore gives
\[
\frac{S}{z^6}=R(u),\qquad R\in\mathbb C(t).             \tag{2}
\]
No finite pole of \(R\) is possible: a pole at \(\lambda\) would give a
pole of \(S\) along a component of \(q-\lambda z^3\), and \(z\) is not a
component because \(q|_{z=0}\ne0\).  Thus \(R\) is a polynomial.
The \(z\)-valuation at infinity in (2) gives \(\deg R\le2\).  Consequently
\[
S\in\langle z^6,z^3q,q^2\rangle.                       \tag{3}
\]

Reducing (3) modulo \(z^3\), using \(\gcd(q,z)=1\), and then dividing the
remaining identity by \(z^3\) gives
\[
U=cq+dz^3,\qquad V=zW+eq+fz^3.                         \tag{4}
\]
This is the complete solution, not a sample solution.

The two target shears used to remove \(c,e\) are legal, but only if their
action on every jet is retained.  Explicitly,
\[
\begin{array}{c|ccc}
\text{shear}&H_3&H_2&L\\ \hline
F_1\mapsto F_1-cF_3&
U\mapsto U-cq&A\mapsto A-cW&L_1\mapsto L_1-cL_3\\
F_2\mapsto F_2-eF_3&
V\mapsto V-eq&B\mapsto B-eW&L_2\mapsto L_2-eL_3 .
\end{array}
\]
The third row of \(H_4\) is zero, so \(H_4\) is unchanged.  Since
\(A,B\) and all three rows of \(L\) remain arbitrary and are merely
renamed after the shear, the gauged family
\[
U=dz^3,\qquad V=zW+fz^3                               \tag{5}
\]
does not discard any lower jet or linear-part locus.

## 2. No omitted root or minimality stratum

Because \(z\nmid q\), the binary cubic
\[
q_0=q|_{z=0}
\]
is nonzero.  Over \(\mathbb C\), its divisor on \(\mathbb P^1\) has
exactly the three multiplicity partitions
\[
1+1+1,\qquad 2+1,\qquad 3,
\]
represented respectively by
\[
xy(x-y),\qquad x^2y,\qquad x^3.                        \tag{6}
\]
Thus there is no fourth root stratum.

On the first two strata, independent binary-bracket matrices have ranks
\[
\begin{array}{c|cc}
q_0&
\mathbb C[x,y]_2\longrightarrow\mathbb C[x,y]_3&
\mathbb C[x,y]_1\longrightarrow\mathbb C[x,y]_2\\ \hline
xy(x-y)&3&2\\
x^2y&3&2,
\end{array}
\]
so both kernels are zero.  A fresh determinant expansion then recovers
the three successive plane identities
\[
\begin{aligned}
E_6|_{z=0}&=-q_0\{A_0,q_0\},\\
E_5|_{z=0}&=-q_0\{\bar L_1,q_0\},\\
E_4|_{z=0}&=A_1\{B_0,q_0\},
\end{aligned}                                         \tag{7}
\]
where the second line is taken after \(A_0=0\), and the third after
\(\bar L_1=0\).  Since \(\mathbb C[x,y]\) is a domain, (7) gives exactly
\[
A=\alpha z^2\quad\text{or}\quad B_0=0.                 \tag{8}
\]
No division by a coefficient, root discriminant, or residual modulus is
used.

On the triple-root stratum, normalize
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.               \tag{9}
\]
The complete parabolic preserving \(z=0\) and the marked triple root is
\[
x\mapsto ax+uz,\quad
y\mapsto by+cx+vz,\quad
z\mapsto dz,
\qquad abd\ne0.                                        \tag{10}
\]
Splitting before any division gives:

1. If \(C\ne0\), a \(y\)-shear kills \(B,E\), an \(x\)-translation
   kills the resulting \(x^2z\) term, and scaling gives
   \[
   x^3+y^2z+\alpha xz^2+\beta z^3.
   \]
2. If \(C=0,B\ne0\), an \(x\)-translation kills \(E\), and the two
   components of a \(y\)-shear kill \(A,D\), giving
   \[
   x^3+xyz+\beta z^3.
   \]
3. If \(C=B=0,E\ne0\), an \(x\)-translation and a \(y\)-shear kill
   \(A,D,F\), giving
   \[
   x^3+yz^2.
   \]
4. If \(C=B=E=0\), then \(q\in\mathbb C[x,z]_3\).

The last case is exactly the nonminimal boundary.  Conversely, if
\((z^3,q)\) is nonminimal, then
\(q\in\operatorname{Sym}^3\langle z,\ell\rangle\).
The equality \(q|_{z=0}=x^3\) forces
\(\ell\bmod z\) to be proportional to \(x\), so \(q\) is binary in
\(x,z\).  Hence the three displayed minimal families are exhaustive,
and the fourth family is correctly reclassified rather than silently
excluded.

## 3. Independent exact reconstruction of the constant minors

`verify_nonvertical_companion_independent.py` implements sparse
multivariate polynomial arithmetic over \(\mathbb Q\) from scratch.  It
does not import SymPy, PARI/GP, or either supplied verifier.  It builds
the weighted Jacobian determinant and the complete \(E_6,E_5\)
coefficient systems.

For each system, it selects independent pivot rows by rational
elimination at the zero-parameter specialization; the row lists are not
read from the supplied scripts.  It then computes the selected
determinant symbolically and verifies that every nonconstant coefficient
is zero.  The resulting literal pivots are
\[
\begin{array}{c|c|c}
\text{root stratum}&\text{\(E_4\) branch}&\text{pivot}\\ \hline
1+1+1&A=\alpha z^2&-2^{19}\\
1+1+1&B_0=0&-2^{11}\\
2+1&A=\alpha z^2&-2^{19}\\
2+1&B_0=0&-2^{11}\\ \hline
3&C\ne0&-2^{24}3^8\\
3&C=0,\ B\ne0&-2^{18}3^6\\
3&C=B=0,\ E\ne0&-2^{20}3^7.
\end{array}                                            \tag{11}
\]
All coefficients of \(W\), the lower \(z\)-jets of \(q\), \(d,f\), and
the displayed triple-root moduli remain symbolic.  Thus (11) has no
internal rank divisor.

The same independent expansion verifies every residual \(E_6,E_5\)
coefficient after the forced solution
\[
A=\alpha_0z^2,\qquad
B=z(\ell_{31}x+\ell_{32}y+\beta_0z),\qquad
\bar L_1=\bar L_2=0.                                  \tag{12}
\]
Hence the pivots do not merely give necessary fragments of a solution:
for each choice of the free variables, (12) is the unique solution in
the pivot variables.

The first two rows of \(L\) in (12) have the forms
\[
(0,0,\ell_{13}),\qquad(0,0,\ell_{23}),
\]
so \(\det L=0\).  But for a Keller map the constant value of the
Jacobian determinant is
\(\det JF(0)=\det L\ne0\).  This is the required contradiction.

## 4. Executed checks

The following all pass:

```text
../verify_nonvertical_nontriple_e4_strict.sh
../test_nonvertical_nontriple_mutations.sh
../verify_nonvertical_triple_root_strict.sh
./verify_strict.sh
```

The independent checker additionally verifies:

- the binary-kernel ranks and the successive identities (7);
- that the gauged family (5) satisfies \(E_7\) identically;
- all seven parameter-free pivots in (11);
- every nonpivot \(E_6,E_5\) equation after (12);
- singularity of the resulting linear matrix.

The proof still depends on the already audited relative-algebraic-closure
statement for a minimal cubic pencil.  The finite computations are exact
evidence about the encoded algebra, not peer review.  This audit and its
software were materially AI-assisted.
