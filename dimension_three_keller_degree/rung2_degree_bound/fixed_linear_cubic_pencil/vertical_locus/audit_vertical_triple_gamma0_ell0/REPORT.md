# Hostile audit: all zero-\(\gamma\), zero-\(\ell\) triple-root charts

**Verdict:** **PASS**, precisely on the locus
\[
s\ne0,\qquad q|_{z=0}=x^3,\qquad W=wz^2
\]
and the three minimal charts listed below.

**Completed (UTC):** 2026-07-25T21:27:37Z.

The unified statement in `../VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md` is
correct.  The earlier independent audit of \(q=x^3+yz^2\) was rerun, and
the other two charts were reconstructed independently with their moduli
left symbolic.  I found no missing minimal chart, illegal gauge, hidden
specialization in \(\alpha\), omitted determinant equation, or internal
rank divisor.

This audit does **not** cover \(\gamma\ne0\), \(\ell\ne0\), or \(s=0\),
and it does not close frozen row `Q2-E1-A3-B1-D1-N1`.

## 1. Independent reconstruction of the atlas

Normalize the triple root to \(x\).  Before further source or target
operations,
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.              \tag{1}
\]
The parabolic preserving \(z=0\) and its marked triple root is
\[
x\mapsto ax+uz,\qquad
y\mapsto by+cx+vz,\qquad
z\mapsto dz,\qquad abd\ne0.                           \tag{2}
\]
Splitting before any division gives four exhaustive cases.

### \(C\ne0\)

The \(x\)- and \(z\)-parts of a \(y\)-shear complete the square in \(y\)
and kill \(B,E\).  An \(x\)-translation kills the remaining
\(x^2z\)-term.  Scaling \(y\) normalizes \(C\), leaving
\[
q=x^3+y^2z+\alpha xz^2+\beta z^3,                    \tag{3}
\]
with both \(\alpha,\beta\) retained.  No division by \(\alpha\) occurs,
so \(\alpha=0\) remains inside this chart.

### \(C=0,\ B\ne0\)

An \(x\)-translation kills \(E\).  The \(x\)- and \(z\)-parts of a
\(y\)-shear then kill \(A,D\), and scaling \(y\) normalizes \(B\):
\[
q=x^3+xyz+\beta z^3.                                  \tag{4}
\]

### \(C=B=0,\ E\ne0\)

An \(x\)-translation kills \(A\); the two parts of a \(y\)-shear kill
the resulting \(D,F\); and scaling \(y\) normalizes \(E\):
\[
q=x^3+yz^2.                                           \tag{5}
\]

### \(C=B=E=0\)

Here \(q\in\mathbb C[x,z]_3\), so \((z^3,q)\) is nonminimal.  Conversely,
if the pair is nonminimal, then
\[
q\in\operatorname{Sym}^3\langle z,L\rangle
\]
for a linear form \(L\).  Since \(q|_{z=0}=x^3\),
\(L\bmod z\) is proportional to \(x\), forcing \(q\) to be binary in
\(x,z\).  Thus this fourth case is exactly the reclassification boundary.
Each of (3)--(5) contains a \(y\)-term, so every displayed chart is
minimal for every retained modulus.

The source transformations above preserve \(z\) up to scale.  Therefore
they preserve
\[
W=wz^2
\]
and merely rescale the arbitrary \(w\).  They cannot turn
\(\gamma=\ell=0\) into an adjacent \(W\)-stratum.

## 2. Target gauges and removal of \(\beta\)

On the vertical companion, before the last gauges,
\[
\begin{aligned}
H_4&=(z^4,zq,0)^T,\\
H_3&=\left(\frac43zW+s q+bz^3,\ V,\ z^3\right)^T .
\end{aligned}                                         \tag{6}
\]
For (3) or (4), the shear
\[
F_2\mapsto F_2-\beta F_1
\]
replaces \(q\) by \(q-\beta z^3\).  It simultaneously sends
\[
(V,B,L_2)\mapsto(V-\beta U,\ B-\beta A,\ L_2-\beta L_1).
\]
All three affected objects were unrestricted, so this is an invertible
renaming, not a specialization.

Writing \(U\) in the new \(q\) changes its independent \(bz^3\) summand.
A shear by \(F_3\) kills that summand, changing \(A,L_1\) by multiples of
\(W,L_3\).  A final shear by \(F_3\) kills \([z^3]V\), changing
\(B,L_2\) by multiples of \(W,L_3\).  These operations preserve \(H_4\)
because its third row is zero.  Since \(W=wz^2\), the last two operations
only rename the free \(z^2\)-coefficients of \(A,B\).

The resulting complete atlas is therefore
\[
\begin{aligned}
q_C&=x^3+y^2z+\alpha xz^2,\\
q_B&=x^3+xyz,\\
q_E&=x^3+yz^2.                                       \tag{7}
\end{aligned}
\]

There is a minor wording ambiguity in the candidate note.  The shear of
the first row kills the independent \(bz^3\) summand, not the literal
total \(z^3\)-coefficient of \(U\): the constrained contribution
\(\frac43zW=\frac43wz^3\) remains when \(w\ne0\).  Also, the initial
\(\beta\)-removing shear changes \(B\) by a multiple of \(A\), whereas
the two subsequent third-row shears change \(A,B\) by multiples of
\(W\).  The note separately records the \(B\mapsto B-\beta A\) change,
and its displayed normal form and proof use the correct transformations;
these are exposition issues only.

## 3. Complete \(E_6\) audit

A fresh sparse expansion of
\[
\det(L+JH_2+JH_3+JH_4)
\]
first confirms \(E_8=E_7=0\) on every chart.  In the nine coefficients
of \(V\) other than \(z^3\), together with
\(\lambda=\ell_{31},\mu=\ell_{32}\), every \(E_6\) equation is jointly
linear.

Exact elimination at \(s=1\), with every other parameter zero, selected
the following pivots without receiving a row or column list from either
supplied verifier:

| chart | selected \(V\)-columns | exact determinant |
|---|---|---:|
| \(q_C\) | \(v_0,v_1,v_2,v_3,v_4,v_5,v_7,v_8\) | \(-2^5 3^{15}s^8\) |
| \(q_B\) | \(v_0,v_1,v_2,v_3,v_4,v_6,v_7,v_8\) | \(2^3 3^{14}s^8\) |
| \(q_E\) | \(v_0,v_1,v_2,v_3,v_4,v_5,v_6,v_7\) | \(-2^3 3^{15}s^8\) |

The selected determinants contain neither \(\alpha\) nor \(w\).  They
therefore prove rank at least eight uniformly, including \(\alpha=0\)
and \(w=0\).

For each chart, direct construction with
\[
V=kq+\frac zs(A-a_5z^2)
       -\frac4{3s}z^2(\lambda x+\mu y)                 \tag{8}
\]
annihilates every \(E_6\) coefficient.  The directions
\((k,\lambda,\mu)\) are independent: the last two are coordinates of
the eleven-variable system, and the \(k\)-direction has nonzero
\(x^3\)-coefficient.  Thus the solution space has dimension at least
three.  The pivot and this family form a rank sandwich, proving rank
exactly eight and completeness of (8).

## 4. Complete \(E_5\) audit

After (8), the \(q_C,q_B,q_E\) systems have respectively \(12,10,7\)
nonzero coefficient equations, all jointly linear in
\[
b_0,b_1,b_2,b_3,b_4,\lambda,\mu.
\]
Independent elimination found rank seven in every case.  To check the
specific literal minors claimed in the note without importing their row
lists, the checker exhaustively searched all seven-row subsets after a
rational specialization, then recomputed each match symbolically over
the full coefficient ring.  It found:

| chart | independently discovered row monomials | determinant |
|---|---|---:|
| \(q_C\) | \(x^5,x^3yz,x^3z^2,x^2yz^2,x^2z^3,xyz^3,yz^4\) | \(2^5 3^9s^7\) |
| \(q_B\) | \(x^5,x^4z,x^3z^2,x^2yz^2,x^2z^3,xz^4,yz^4\) | \(2^2 3^8s^7\) |
| \(q_E\) | \(x^5,x^3z^2,x^2yz^2,x^2z^3,xz^4,yz^4,z^5\) | \(2^4 3^8s^7\) |

All are independent of \(\alpha,w,k,A,L\).  Substitution into every
pivot and nonpivot equation gives the common unique solution
\[
\begin{aligned}
\lambda&=\mu=0,\\
b_0&=a_0k/s,&b_1&=a_1k/s,&b_2&=a_2k/s,\\
b_3&=(a_3k+\ell_{11})/s,&
b_4&=(a_4k+\ell_{12})/s.                              \tag{9}
\end{aligned}
\]
The checker separately reproduces all three displayed eliminations of
\(\lambda,\mu\), including
\[
[x^3z^2]E_5+3[yz^4]E_5=4s\lambda
\]
on \(q_E\).  No division by \(w,k,\alpha\), or a polynomial in those
parameters occurs.

## 5. Complete \(E_4\) audit and contradiction

After (9), a direct equality of sparse polynomials gives exactly the
three \(E_4\) rows printed in the candidate note:
\[
\begin{array}{c|l}
q_C&
9\Delta_2x^2z^2-6\Delta_1yz^3+3\alpha\Delta_2z^4\\
q_B&
9\Delta_2x^2z^2-3\Delta_1xz^3+3\Delta_2yz^3\\
q_E&
9\Delta_2x^2z^2-3\Delta_1z^4,
\end{array}                                            \tag{10}
\]
where
\[
\Delta_1=-k\ell_{11}+s\ell_{21},\qquad
\Delta_2=-k\ell_{12}+s\ell_{22}.
\]
Independent pivot selection in \((\ell_{21},\ell_{22})\) gives,
respectively,
\[
54s^2,\qquad27s^2,\qquad27s^2.                        \tag{11}
\]
Consequently
\[
\ell_{21}=k\ell_{11}/s,\qquad
\ell_{22}=k\ell_{12}/s.
\]
Together with \(\ell_{31}=\ell_{32}=0\), this gives
\[
\det L
=\ell_{33}(\ell_{11}\ell_{22}-\ell_{12}\ell_{21})=0.
\]
Since \(\det L=\det JF(0)\ne0\) for a Keller map, every chart in (7) is
impossible on the stated \(W=wz^2,s\ne0\) locus.

## 6. Independent exact certificate

`verify_vertical_triple_gamma0_ell0_sparse.py` reuses only the
dependency-free sparse Laurent-polynomial arithmetic kernel from the
earlier \(q_E\) hostile audit.  It imports no CAS and no equations,
pivots, or row selections from the supplied SymPy/PARI scripts.  It:

- reconstructs each raw determinant;
- independently selects the \(E_6,E_5,E_4\) ranks;
- exhaustively rediscovers the claimed \(E_5\) literal minors;
- keeps \(\alpha,w,k\) and every unused coefficient symbolic;
- verifies every residual equation after (8), (9), and (10);
- includes negative controls for the \(V\)-solve, \(B\)-solve, and final
  singularity in every chart.

Run:

```text
./verify_strict.sh
../verify_vertical_triple_gamma0_ell0_strict.sh
```

The hostile sparse checker and both supplied exact implementations pass.
These computations are exact evidence about the encoded algebra, not
peer review.  The audit and its software were materially AI-assisted.
