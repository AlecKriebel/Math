# Exclusion of the isolated squarefree \(\kappa=16/5\) family

**Status:** certified family-level exclusion.  An exact SymPy derivation
and an independent clean-room PARI/GP reconstruction pass.

**First banked (UTC):** 2026-07-26T04:45:00Z.

This note is not peer reviewed.  The exact checks certify the encoded
algebra; they are not peer review.

## 1. Statement and scope

Put
\[
X=p-q,\qquad Y=5p-(3-4i)q,\qquad h=XY
\]
and
\[
P=hp^2,\qquad Q=hq^2,\qquad
R=X^2\bigl((4-3i)p+5q\bigr).                       \tag{1}
\]
These are the normalized top forms of frozen canonical family
`D4-SF-20CC`.

### Theorem

No degree-four Keller counterexample over \(\mathbb C\) has leading data
in the `D4-SF-20CC` orbit.  More precisely, every degree-four Keller map
with top data (1), up to the frozen source and target normalizations, is
a polynomial automorphism.

This closes one of the 26 canonical high-incidence families.  It does not
close the parent fixed-quadratic row and does not improve the universal
dimension-three total-degree floor.

## 2. Orbit and contact completeness

The exact common divisor
\[
\gcd\bigl(J(Q,R),-J(P,R),J(P,Q)\bigr)\doteq pqX^2             \tag{2}
\]
records one doubled fixed root and both branch contacts.  If
\[
z=\frac{3+4i}{5},
\]
then \(5z^2-6z+5=0\) and the frozen modulus is
\[
\kappa=\frac{(1+z^{-1})^2}{z^{-1}}=\frac{16}{5}.
\]
The coordinate and target rescalings checked in the hostile audit carry
the canonical \(z\)-presentation exactly to (1), so this is the frozen
orbit rather than merely an example with the same incidence count.

Write
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad\gamma=J(P,Q).
\]
The three coefficient blocks of
\[
E_7=\alpha U_r+\beta V_r+\gamma T_r=0
\]
have ranks and nullities
\[
(2,0),\qquad(3,2),\qquad(4,4).
\]
Thus the complete contact space has six parameters: two \(r^2\)-contact
coordinates and four \(r\)-contact coordinates.

At \(E_6\), two independent extreme squares force both \(r^2\)-contact
coordinates to vanish.  Eliminating the two lower \(r^2\)-coefficients
from the remaining six equations gives, set-theoretically, one affine
line in the four \(r\)-contact coordinates.  In the clean-room
coordinates of the independent reconstruction it is
\[
\begin{aligned}
y&=k,\\
x&=-\left(\frac14+\frac34i\right)k,\\
a&=-\left(\frac9{20}+\frac35i\right)k,\\
b&=\left(\frac9{20}+\frac35i\right)k.              \tag{3}
\end{aligned}
\]
The proof does not discard secondary factors of augmented minors: their
apparent common branch forces the defining linear factor of (3) after
all.

## 3. Full lower descent

Restore all 18 lower variables:

- the six nonbinary quadratic coefficients of the first two components;
- the \(L_{33}\) entry of the linear part; and
- all eleven binary coefficients of the integration constants
  \(U_0,V_0,T_0\).

There are exactly two pivot charts:

| chart | \(\operatorname{rank}M\) | \(\operatorname{rank}(M\mid b)\) | nonzero pivot |
|---|---:|---:|---|
| \(k\ne0\) | 6 | 6 | \(3499200000000\,i(-6+17i)k\) |
| \(k=0\) | 5 | 5 | \(155520000000\,i(-8+i)\) |

The origin is recomputed rather than obtained by specializing a solution
that divides by \(k\).

On \(k\ne0\), a complete six-pivot solution of \(E_6\), with all twelve
remaining lower variables free, gives
\[
\begin{aligned}
[p^2qr^2]E_5&=\frac9{20}(-4+3i)k^3,\\
[pq^2r^2]E_5&=\frac9{20}(4-3i)k^3.                 \tag{4}
\end{aligned}
\]
The first coefficient alone is nonzero, so this entire chart is empty.

At \(k=0\), a fresh rank-five solve gives
\[
\begin{aligned}
[p^3r]E_4&=
\left(-\frac{200}{507}-\frac{160}{169}i\right)
(3ib_{qr}+L_{33})^2,\\
[q^3r]E_4&=
\left(\frac{207872}{12675}-\frac{2432}{4225}i\right)
\left(\left(-\frac9{20}-\frac35i\right)b_{qr}
+L_{33}\right)^2.                                  \tag{5}
\end{aligned}
\]
The two scalar coefficients are nonzero and the two linear forms are
independent.  Hence
\[
b_{qr}=L_{33}=0.
\]
The complete \(E_6\) solution then sets all six nonlinear
\(r\)-dependent quadratic coefficients to zero.  Since the contact
coordinate \(k\) is zero, every nonlinear homogeneous term is binary.

## 4. Unconditional plane exit

First subtract \(F(0)\).  The Keller condition makes the linear part
invertible.  A target-linear normalization of its \(r\)-column puts the
map in the form
\[
(p,q,r)\longmapsto
\bigl(g_1(p,q),g_2(p,q),r+g_3(p,q)\bigr).           \tag{6}
\]
The first two coordinates form a plane Keller map of degree at most four.
Moh's unconditional theorem for degree strictly less than \(100\) makes
that plane map a polynomial automorphism.  Equation (6) is then a
triangular lift of an automorphism and is itself an automorphism.  No
assumption of the open plane Jacobian Conjecture is used.

This proves the theorem.

## 5. Exact verification

Run:

```sh
./verify_strict.sh
```

The terminal marker is:

```text
D4_SF_20CC_FULL_STRICT_PASS
```

`verify_exclusion_sympy.py` reconstructs the incidence, complete contact
radical, generic \(E_5\) obstruction, and origin \(E_4\) collapse from the
weighted determinant.  `verify_exclusion_pari.gp` independently
reconstructs the orbit normalization, syzygies, all 18 lower columns, both
pivot charts, and the lower obstructions over \(\mathbb Q(i)\).  The
wrapper rejects disabled Python assertions, interpreter diagnostics, and
a deliberately mutated PARI obstruction.

## Disclosure

The derivation, audit, and verification code were produced with
substantial AI assistance.  This work is not peer reviewed.  Exact
computer algebra checks are evidence about the algebra encoded in the
scripts, not a substitute for human proof review.

## Reference

R. Biggers, T.-T. Moh, and M. Fried, “On the Jacobian conjecture and the
configurations of roots,” *Journal für die reine und angewandte
Mathematik* **340** (1983), 140--213,
[doi:10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
