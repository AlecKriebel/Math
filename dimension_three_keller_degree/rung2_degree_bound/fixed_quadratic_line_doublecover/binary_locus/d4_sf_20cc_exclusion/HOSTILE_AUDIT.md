# Hostile independent audit of `D4-SF-20CC`

**Audit completed:** `2026-07-26T04:39:39Z`
**Verdict:** **PASS**
**Method:** independent PARI/GP reconstruction over
\(\mathbb Q(i)\); the primary SymPy implementation was neither read,
imported, executed, nor edited.

## Claim audited

For
\[
\begin{aligned}
X&=p-q,\\
Y&=5p-(3-4i)q,\\
P&=XYp^2,\qquad Q=XYq^2,\\
R&=X^2((4-3i)p+5q),
\end{aligned}
\]
no quartic Keller counterexample can have this normalized top data.

The audit confirms the claim.  The complete \(E_7,E_6\) contact locus is
one affine line.  Its nonzero chart is empty at \(E_5\); its origin loses
all nonlinear \(r\)-dependence at \(E_4\) and exits to an unconditional
low-degree plane automorphism.

This is a representative exclusion for frozen canonical family
`D4-SF-20CC`.  It does not by itself close the global quartic row.

## 1. Orbit normalization

The exact homogeneous common divisor is
\[
\gcd\bigl(J(Q,R),-J(P,R),J(P,Q)\bigr)\doteq pqX^2.
\]
This was recomputed in both projective charts.  The four relevant lines
\(X,Y,p,q\), together with the residual line of \(R\), are pairwise
distinct where required.  Thus the incidence is one doubled fixed root
plus both branch contacts.

Let
\[
z=\frac{3+4i}{5},\qquad z^{-1}=\frac{3-4i}{5}.
\]
Then
\[
5z^2-6z+5=0,\qquad
\frac{(1+z^{-1})^2}{z^{-1}}=\frac{16}{5}.
\]
Starting from the canonical form with \(s^2=z\) and rescaling the old
binary coordinate by \(p_{\rm old}=sp\), its two fixed roots become
\(1,z^{-1}\).  Direct calculation gives
\[
\begin{aligned}
(p-q)(zp-q)&\doteq XY,\\
(p-q)^2((3z-5)p-4q)&=-\frac45R.
\end{aligned}
\]
Hence the displayed \(\mathbb Q(i)\)-form is exactly the canonical
\(\kappa=16/5\) orbit, not merely another delta-four example.

## 2. Complete \(E_7\) syzygies

With
\[
\alpha=J(Q,R),\quad\beta=-J(P,R),\quad\gamma=J(P,Q),
\]
the three coefficient matrices of
\[
E_7=\alpha U_r+\beta V_r+\gamma T_r
\]
have:

| block | variables | rank | nullity |
|---|---:|---:|---:|
| \(r^2\) | 2 | 2 | 0 |
| \(r^1\) | 5 | 3 | 2 |
| \(r^0\) | 8 | 4 | 4 |

The PARI reconstruction computes these matrices from the forms themselves,
computes their kernels, and separately substitutes an explicit
six-parameter solution.  Thus no contact direction is omitted.

## 3. Full \(E_6\) contact locus

Write \(d,z\) for the two \(r^2\)-contact parameters.  Two extreme
coefficients of the \(r^3\)-part of \(E_6\) are nonzero constants times
\[
\bigl((-6-3i)d+(8-4i)z\bigr)^2,\qquad
(3id+z)^2.
\]
The two linear forms are independent, so \(d=z=0\).

For the four remaining contact parameters \((a,b,x,y)\), include the two
\(r^2\)-coefficients of the lower quadratic pair \(A,B\), form the six
\(r^1\)-coefficient equations, and eliminate those lower variables by
augmented minors.  Two minors are nonzero constants times
\[
\begin{aligned}
L_b^2,\qquad
L_b&=\left(-\frac45+\frac{16}{15}i\right)b+y,\\
L_s^2,\qquad
L_s&=-\frac i3a+\left(\frac7{39}-\frac4{39}i\right)b
      +x+\left(\frac4{13}+\frac7{13}i\right)y.
\end{aligned}
\]
Thus \(L_b=L_s=0\).  After making those substitutions, two further
augmented minors factor as
\[
c_1L_aL_{a,1},\qquad c_2L_aL_{a,2},
\]
where \(c_1c_2\ne0\),
\[
L_a=\left(\frac45-\frac{16}{15}i\right)a+y,
\]
and \(L_{a,1},L_{a,2}\) are independent linear forms in \(a,y\).
If \(L_a\ne0\), both latter forms vanish, forcing \(a=y=0\), which also
forces \(L_a=0\), a contradiction.  Therefore \(L_a=0\).

The radical contact locus is exactly
\[
\begin{aligned}
y&=\kappa,\\
x&=-\left(\frac14+\frac34i\right)\kappa,\\
a&=-\left(\frac9{20}+\frac35i\right)\kappa,\\
b&=\left(\frac9{20}+\frac35i\right)\kappa.
\end{aligned}
\]
This argument checks all branches of the factored minors; it does not
discard the secondary factors by genericity.

## 4. All 18 lower variables and every pivot chart

The full \(E_6\) matrix retains

- all six nonbinary quadratic coefficients of \(A,B\);
- \(L_{33}\); and
- all 11 binary coefficients of \(U_0,V_0,T_0\).

There are exactly two charts:

| chart | rank \(M\) | rank \((M\mid b)\) | certified pivot |
|---|---:|---:|---|
| \(\kappa\ne0\) | 6 | 6 | \(3499200000000\,i(-6+17i)\kappa\) |
| \(\kappa=0\) | 5 | 5 | \(155520000000\,i(-8+i)\) |

The origin is recomputed from scratch; it is not obtained by specializing
a formula divided by \(\kappa\).

On \(\kappa\ne0\), solve the six-pivot \(E_6\) system with all 12 remaining
lower variables free.  Two coefficients of \(E_5\) are
\[
\begin{aligned}
[p^2qr^2]E_5&=\frac9{20}(-4+3i)\kappa^3,\\
[pq^2r^2]E_5&=\frac9{20}(4-3i)\kappa^3.
\end{aligned}
\]
They are nonzero, so the entire nonzero contact chart is empty.

At \(\kappa=0\), the complete rank-five \(E_6\) solve gives extreme
\(E_4\)-coefficients
\[
\begin{aligned}
[p^3r]E_4&=
\left(-\frac{200}{507}-\frac{160}{169}i\right)(3ib_{qr}+L_{33})^2,\\
[q^3r]E_4&=
\left(\frac{207872}{12675}-\frac{2432}{4225}i\right)
\left(\left(-\frac9{20}-\frac35i\right)b_{qr}+L_{33}\right)^2.
\end{aligned}
\]
The two linear forms are independent, hence
\(b_{qr}=L_{33}=0\).  The exact \(E_6\) solution then sets all other
nonbinary quadratic coefficients to zero as well.

All nonlinear terms are consequently binary.  First subtract \(F(0)\).
Since a Keller map has invertible linear part, a target-linear change
sends its constant \(r\)-column to \((0,0,1)^t\), putting the map in the
form
\[
(g_1(p,q),g_2(p,q),r+g_3(p,q)).
\]
The first two coordinates form a plane Keller map of degree at most four.
Moh's unconditional theorem for plane Keller maps of degree strictly less
than \(100\) makes it an automorphism, and the triangular extension is an
automorphism.  This uses no form of the open plane Jacobian Conjecture.

## 5. Adversarial checks

- **No zero-binary slice:** all 11 binary coefficients remain present in
  the full \(E_6\), \(E_5\), and origin \(E_4\) calculations.
- **No missed pivots:** \(\kappa\ne0\) and \(\kappa=0\) are separately
  certified; their pivots are displayed.
- **No denominator-clearing branches:** the proof uses direct determinant
  coefficients, ranks, augmented minors, and square identities.  No
  resultant is cleared.
- **No radical shortcut:** the secondary factors after \(L_b=L_s=0\) are
  explicitly checked for the only apparent extra branch.
- **Correct scope:** this is one frozen orbit, not all quartic maps.
- **Keller versus counterexample:** the origin exit is shown to be an
  automorphism, not merely another Keller map.
- **False-hypothesis audit:** the only plane input is Moh's proved theorem
  for degree strictly less than \(100\).

## Reproduction

Run:

```sh
./verify_strict.sh
```

Expected exact markers:

```text
D4_SF_20CC_PARI_HOSTILE_EXCLUSION_PASS
D4_SF_20CC_FULL_STRICT_PASS
```

The wrapper runs the primary SymPy implementation and the independent
PARI/GP reconstruction, rejects disabled Python assertions and interpreter
errors, and confirms that a deliberately mutated PARI obstruction is
rejected.

## Disclosure

This hostile audit and its verification code were produced with AI
assistance.  Exact checks are evidence about the encoded algebra and do
not constitute peer review.
