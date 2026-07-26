# Hostile release audit: `D3-BB-21`

**Certified audit timestamp:** 2026-07-26T09:37:13Z
**Verdict:** **PASS after two certificate repairs.**
**Scope:** the frozen fine family `D3-BB-21` only.  This is not a
quartic-row closure and does not improve the universal degree floor.

## Finding and repairs

The first candidate certificate omitted the degree-zero syzygy block of
\(E_7\), corresponding to the \(r^2\) coefficient of
\((U_r,V_r)\), and the full-BB routine asserted \(E_7=0\) but did not
explicitly replay \(E_9=E_8=0\).  These were completeness gaps in the
certificate, not counterexamples to the formulas.

Before this verdict was issued, the release was repaired:

1. the primary exact implementation now proves that the degree-zero
   \(E_7\) matrix has rank \(2\) on its two columns and explicitly checks
   \(E_9,E_8,E_7\);
2. the independent PARI/GP implementation checks the two degree-zero
   pivots separately and explicitly checks \(E_9,E_8,E_7\); and
3. its strict wrapper now rejects PARI interpreter-error text.  This matters
   because GP can continue after some parse errors.

The hostile dependency-free reconstruction independently checks all of
these repaired points.

The shared construction directory was being extended to `D3-BS-N2-Z`
while this audit was finalized.  This verdict deliberately runs the
BB-specific primary routines and the BB portion of the independent PARI
replay; it neither executes nor certifies the in-progress BS extension.

## 1. Frozen-family bridge

The audit reads the frozen denominator by exact SHA-256:

```text
440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a
```

It contains exactly \(19+6+1=26\) fine families and exactly one entry with
ID `D3-BB-21`.  That entry is a point stratum with
\[
h=pq,\qquad R=p^2q,\qquad \delta=3.
\]
There is no parameter modulus or retained pivot in this frozen entry.

## 2. Complete \(E_7\) coverage

For
\[
P=p^3q,\quad Q=pq^3,\quad R=p^2q
\]
the binary minors are
\[
\alpha=-5p^2q^3,\qquad \beta=-p^4q,\qquad
\gamma=8p^3q^3.
\]

Splitting \(E_7\) by powers of \(r\) gives three independent linear
blocks:

| block | unknown columns | rank | nullity |
|---|---:|---:|---:|
| \(r^2\): constant \(U_r,V_r\), no \(T_r\) term | 2 | 2 | 0 |
| \(r^1\): linear \(U_r,V_r\), constant \(T_r\) | 5 | 4 | 1 |
| \(r^0\): quadratic \(U_r,V_r\), linear \(T_r\) | 8 | 5 | 3 |

The hostile checker reconstructs these matrices over
\(\mathbf Q\), verifies the ranks, and verifies independence and
annihilation for the displayed bases.  Hence there is no missing \(r^3\)
term in \(U\) or \(V\), and the full contact space is exactly
\[
S=ap+bq+cr,\quad
U_r=\frac p5(8S-kp),\quad V_r=kq^2,\quad T_r=S.
\]

The sparse determinant engine also verifies \(E_9=E_8=E_7=0\) directly.

## 3. \(E_6\) coverage and pivots

With all eleven coefficients of \(U_0,V_0,T_0\), every quadratic
coefficient of \(A,B\), and all nine entries of \(L\) still symbolic, raw
coefficients give successively
\[
\frac{12}{5}c^2,\qquad \frac{24}{5}b^2,\qquad
\frac25(12a^2-8ak+3k^2).
\]
In characteristic zero these force
\[
c=b=0,\qquad C:=12a^2-8ak+3k^2=0.
\]

The remaining pivots divide only by \(5\) or \(25\), never by \(a\),
\(k\), \(3a-k\), or \(2k-a\).  Thus there is no omitted parameter
boundary.  Rebuilding the determinant after the pivots leaves exactly
\[
\frac25C\,p^3q^2r+
\frac35v_0(3a-k)p^6+
3u_3(2k-a)pq^5.
\]
This exact polynomial equality proves that every \(E_6\) coefficient has
been retained.

## 4. Decisive \(E_5\) coefficient

After the same unit pivots, the dependency-free reconstruction finds
\[
[p^2qr^2]E_5=\frac25ak(8a-k),
\]
with no occurrence of a lower coefficient.  Independently constructed
Sylvester determinants give
\[
\operatorname{Res}_k(C,ak(8a-k))=1680a^6,\qquad
\operatorname{Res}_a(C,ak(8a-k))=420k^6.
\]

There is also a simpler saturation-free audit.  The second equation splits
into \(a=0\), \(k=0\), or \(k=8a\).  On the conic these give respectively
\(3k^2=0\), \(12a^2=0\), and \(140a^2=0\).  Characteristic zero therefore
forces \(a=k=0\).  Together with \(b=c=0\), every nonzero \(E_7\) contact
is excluded.  No resultant denominator or extraneous branch occurs.

## 5. Origin charts

At \(a=b=c=k=0\), the hostile determinant identity is
\[
E_6=\alpha A_r+\beta B_r+\gamma\ell_{33}.
\]
Its six disjoint monomial coefficients give
\[
(A_{pr},A_{qr},A_{rr},B_{pr},B_{qr},B_{rr})
=\left(\frac85\ell_{33},0,0,0,0,0\right).
\]

The two charts are exhaustive:

- If \(\ell_{33}=0\), every nonlinear term is binary.  Since the Keller
  constant equals \(\det L\ne0\), the \(r\)-column of \(L\) is nonzero.
  A target linear normalization gives
  \((g_1(p,q),g_2(p,q),r+g_3(p,q))\).  The degree-four plane Keller map
  \((g_1,g_2)\) is an automorphism by Moh's unconditional bounded-degree
  theorem, so the extension is an automorphism.

- If \(\ell_{33}\ne0\), then
  \(F_3=\ell_{33}r+B_3(p,q)\), \(\deg B_3\le3\), is a coordinate with
  inverse degree at most three.  Straightening it raises the first two
  degrees to at most \(3\cdot4=12<100\).  Each plane fibre is therefore
  an automorphism by Moh; fibrewise injectivity and Ax--Grothendieck make
  the threefold map an automorphism.

Neither chart assumes the plane Jacobian Conjecture.

## Verdict and accounting

Every nonzero contact is inconsistent with \(E_5\), and every origin map
is an automorphism.  Therefore the canonical frozen family
`D3-BB-21` contains no Keller counterexample.

This closes one additional fine family only.  It does not close the
fixed-quadratic parent row or any global quartic row.

## Reproduction

Run:

```sh
./verify_hostile_strict.sh
```

The final marker is:

```text
D3_BB21_HOSTILE_RELEASE_AUDIT_PASS
```

The hostile algebra is a dependency-free sparse-polynomial implementation
over \(\mathbf Q\).  It is independent of both the SymPy primary and the
PARI/GP reconstruction.  Five hostile mutations, a release-contract
mutation, and optimized-Python assertion bypass are required to fail.

## Disclosure

This audit, its proof text, and its exact checker were produced with AI
assistance.  Exact checks are evidence about the encoded algebra, not peer
review.  This work has not been peer reviewed.
